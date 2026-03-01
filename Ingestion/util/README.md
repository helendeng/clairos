# util

Pipeline utilities: `.mbox` file parsing and RAG domain routing.

## Files

| File | Purpose |
|---|---|
| [`parseMbox.py`](parseMbox.py) | Entry point — parses `.mbox` files and runs the full ingestion pipeline |
| [`get_domains_RAG.py`](get_domains_RAG.py) | Routes user queries to relevant RAG domain indexes |

---

## parseMbox.py

Parses `.mbox` email archives and feeds each email through the zero-shot classification pipeline. This is the **main entry point** for ingesting raw email data.

### `controller(mbox_fp, zero_shot_classify_fn, label_groups, threshold)`

| Parameter | Type | Description |
|---|---|---|
| `mbox_fp` | `str` | Path to the `.mbox` file |
| `zero_shot_classify_fn` | callable | The `zero_shot_classify` function from `dataTaggers/ZeroShot.py` |
| `label_groups` | `dict` | `ZERO_SHOT_LABEL_GROUPS` from `Schemas/taxonomy.py` |
| `threshold` | `float` | Default confidence threshold (0.5 recommended) |

**Returns**: `list[dict]` — Flat list of tagged chunk dicts, ready for JSON export or database ingestion.

Each dict has the shape:
```python
{
    "chunk_id":   int,
    "domain":     str,
    "sub_domain": str,
    "text":       str,
    "source": {
        "email_id":  str,
        "sender":    str,
        "subject":   str,
        "cc":        list[str],
        "bcc":       list[str],
        "timestamp": str
    }
}
```

**Example**:
```python
from dataTaggers.ZeroShot import zero_shot_classify
from Schemas.taxonomy import ZERO_SHOT_LABEL_GROUPS
from util.parseMbox import controller

outputs = controller(
    mbox_fp="data/company_emails.mbox",
    zero_shot_classify_fn=zero_shot_classify,
    label_groups=ZERO_SHOT_LABEL_GROUPS,
    threshold=0.5
)

print(f"Tagged {len(outputs)} chunks from the email archive")
```

### Helper Functions

#### `_decode_qp_artifacts(text) -> str`
Decodes residual quoted-printable encoding sequences in email body text.
- Removes soft line breaks: `=\r\n` or `=\n`
- Decodes hex sequences: `=XX` → `chr(0xXX)`

#### `_strip_forwarding_headers(text) -> str`
Removes forwarded email boilerplate that would confuse the classifier.
- Strips separator lines: `--- Forwarded by ... ---`, `--- Original Message ---`
- Removes inline re-headers: `To:`, `From:`, `Cc:`, `Bcc:`, `Subject:`, `Date:`, `Sent:`
- Collapses excess blank lines

#### `_get_email_body(message) -> str | None`
Extracts the plain-text body from a `mailbox.Message` object.
- Handles multipart MIME messages (walks parts looking for `text/plain`)
- Handles non-multipart messages
- Decodes charset, falls back to UTF-8 with error ignoring
- Returns `None` if no plain text part is found

#### `_parse_addresses(header_val) -> list[str]`
Splits a comma-separated email address header into a list of addresses.

#### `parse_message_to_record(message, email_id) -> EmailRecord | None`
Converts a `mailbox.Message` object into a normalized `EmailRecord`.
- Extracts From, Subject, Cc, Bcc, timestamp
- Calls `_get_email_body` and `_strip_forwarding_headers`
- Returns `None` if no usable plain-text body is found

#### `output_schemas_to_dicts(outputs) -> list[dict]`
Converts a list of `OutputSchema` dataclass instances to plain dicts for JSON export or database ingestion. Flattens the nested `SourceInfo` into a `"source"` key.

### Database Integration (Disconnected)

The end of `controller()` contains commented-out database ingestion code:

```python
## Add this when we want to fully connect the data ingestion to the database
# ingestion = ChunkIngestion()
# ingestion.upload_batch(all_outputs_list)
```

Uncomment and import `ChunkIngestion` from the `database/` module to enable persistent storage of tagged chunks.

---

## get_domains_RAG.py

Uses the same zero-shot classifier to route user queries to the appropriate RAG domain indexes before retrieval. Ensures query routing is consistent with how documents were tagged during ingestion.

### `get_domains_for_rag(query) -> list[str]`

| Parameter | Type | Description |
|---|---|---|
| `query` | `str` | A user question or search query |

**Returns**: Deduplicated, sorted list of RAG index filenames to search.

**Example**:
```python
from util.get_domains_RAG import get_domains_for_rag

domains = get_domains_for_rag("What are the Q3 revenue projections?")
# Returns: ["Financial_Accounting", "Financial_Strategy"]

domains = get_domains_for_rag("Tell me about the merger with Acme Corp")
# Returns: ["Business_Strategy"]
```

### LABEL_TO_RAG_DOMAIN

Maps taxonomy category keys to RAG index names. Some categories map to multiple indexes; PII and Personal categories map to empty lists (no dedicated RAG index).

```python
LABEL_TO_RAG_DOMAIN = {
    "Strategic.M&A":                         ["Business_Strategy"],
    "Strategic.Pricing_Models":              ["Business_Strategy", "Financial_Strategy"],
    "Financial.Accounting.Salary_Negotiations": ["Financial_Accounting"],
    "R&D.Technical.Experiments":             ["R&D"],
    "PII.Direct_Identifiers":               [],   # No RAG index
    # 17 more entries ...
}
```

### How Query Routing Works

1. The query is classified using `zero_shot_classify` against `ZERO_SHOT_LABEL_GROUPS`
2. Categories exceeding their threshold in `CATEGORY_THRESHOLDS` are selected
3. Each selected category is looked up in `LABEL_TO_RAG_DOMAIN`
4. All resulting index names are deduplicated and sorted

### Integration Status

`get_domains_for_rag` is implemented but **not currently called from the backend**. It would be called in `backend/server.py` before the RAG query to pre-filter which domain indexes to search, reducing retrieval noise.
