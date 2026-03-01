# Schemas

Data structures and classification taxonomy for the ingestion pipeline.

## Files

- [`schemas.py`](schemas.py) — Dataclasses for input/output types
- [`taxonomy.py`](taxonomy.py) — Category definitions, label groups, confidence thresholds

---

## schemas.py

Defines the three canonical data structures used throughout the pipeline.

### SourceInfo

Metadata about the originating email. Embedded in every `OutputSchema`.

```python
@dataclass
class SourceInfo:
    email_id:  str        # Unique identifier for the email
    sender:    str        # Sender email address
    subject:   str        # Email subject line
    cc:        List[str]  # CC recipients
    bcc:       List[str]  # BCC recipients
    timestamp: str        # Date/time string from email header
```

### EmailRecord

Normalized input format. `parseMbox` converts raw `mailbox.Message` objects into this before handing off to the classifier.

```python
@dataclass
class EmailRecord:
    email_id:  str        # Unique identifier
    sender:    str        # Sender address
    subject:   str        # Subject line
    cc:        List[str]  # CC list
    bcc:       List[str]  # BCC list
    body:      str        # Plain-text email body (cleaned)
    timestamp: str        # Parsed date string
```

### OutputSchema

One classified chunk produced by the pipeline. A single email produces one `OutputSchema` per qualifying text chunk.

```python
@dataclass
class OutputSchema:
    chunk_id:   int        # Sequential index within the source email
    domain:     str        # Primary category (e.g., "HR", "Legal", "R&D")
    sub_domain: str        # Subcategory (e.g., "Performance_Reviews")
    text:       str        # The classified text chunk
    source:     SourceInfo # Metadata linking back to the source email
```

---

## taxonomy.py

Central configuration file for the entire classification system. Three top-level objects:

### TAXONOMY

Maps category keys to `(domain, subdomain)` tuples. This is the single source of truth for what a classifier output means in human-readable terms.

```python
TAXONOMY = {
    "HR.Performance_Reviews":          ("HR",       "Performance_Reviews"),
    "Legal.Litigation.Legal_Disputes": ("Legal",    "Litigation"),
    "Strategic.M&A":                   ("Strategic","M&A"),
    "R&D.Technical.Experiments":       ("R&D",      "Experiments"),
    # 180+ total entries ...
}
```

**Covered domains**: PII, HR, Legal, Security, Strategic, R&D, Financial, Operational, Vendor, Scheduling, Personal.

Adding a new category requires:
1. Adding an entry to `TAXONOMY`
2. Adding it to the appropriate group in `ZERO_SHOT_LABEL_GROUPS`
3. Optionally adding a custom threshold to `CATEGORY_THRESHOLDS`

### ZERO_SHOT_LABEL_GROUPS

Groups categories into batches for the zero-shot classifier. The classifier is run once per group against each text chunk. Groups are sized to keep inference fast while maintaining label coherence.

```python
ZERO_SHOT_LABEL_GROUPS = {
    "Strategic_&_HR": {
        "HR.Performance_Reviews":    "Employee performance review, evaluation, or feedback",
        "Strategic.M&A":             "Merger, acquisition, or company buyout discussion",
        # 6 more ...
    },
    "R&D": {
        "R&D.Technical.Experiments": "Scientific or technical experiment, test, or trial results",
        # 5 more ...
    },
    "Financial": {
        "Financial.Accounting.Salary_Negotiations": "Salary discussion, pay negotiation, or compensation",
        # 5 more ...
    },
    "Operational_&_Personal": {
        "Operational.Project_Metadata.Deadlines": "Project deadline, timeline, or milestone",
        # 3 more ...
    }
}
```

The human-readable description (the dict value) is what gets passed to the model as the classification hypothesis.

### CATEGORY_THRESHOLDS

Per-category confidence thresholds for multi-label classification. Categories with low recall in evaluation get lower thresholds (cast wider net); categories prone to false positives get higher thresholds.

```python
CATEGORY_THRESHOLDS = {
    "Financial.Accounting.Firing_Hiring": 0.25,  # Aggressive — catch more
    "R&D.Technical.Experiments":          0.60,  # Conservative — reduce FP
    # 11 more entries ...
    # Default for any unlisted category: 0.5
}
```

Any category key not listed here uses a default threshold of **0.5**.
