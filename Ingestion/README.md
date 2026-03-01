# Ingestion Pipeline

Zero-shot NLI-based document classification system for tagging email content into organizational knowledge domains. Uses Facebook's `bart-large-mnli` model to classify email chunks without task-specific training.

## What It Does

Takes raw `.mbox` email files and produces structured, tagged chunks where each chunk is labeled with a domain (e.g., `HR`, `Legal`, `R&D`) and subdomain (e.g., `Performance_Reviews`, `Litigation`). These tags enable downstream RAG retrieval to route queries to the correct knowledge indexes.

## Module Overview

```
Ingestion/
├── Schemas/                   # Data structures & classification taxonomy
│   ├── schemas.py             # EmailRecord, OutputSchema, SourceInfo dataclasses
│   └── taxonomy.py            # Category definitions, label groups, thresholds
├── dataTaggers/               # Core classification logic
│   ├── ZeroShot.py            # BART-MNLI classifier wrapper
│   ├── ZeroShotController.py  # Email → chunk → tag orchestrator
│   ├── ZeroShotTestExamples.py# 320 labeled test examples
│   └── ZeroShotValidation.py  # Evaluation suite with full metrics
└── util/                      # Pipeline utilities
    ├── parseMbox.py            # .mbox parser and ingestion entry point
    └── get_domains_RAG.py      # Query → RAG domain routing
```

See each subfolder's `README.md` for detailed documentation.

## Data Flow

```
.mbox file
    │
    ▼
parseMbox.controller()
    ├── Parse each email message
    ├── Decode quoted-printable artifacts
    └── Strip forwarding boilerplate
    │
    ▼
EmailRecord
    (normalized: sender, subject, body, cc, bcc, timestamp)
    │
    ▼
ZeroShotController.process_email_with_zero_shot()
    ├── Split body into sentence or paragraph chunks
    ├── Run zero-shot classification against 4 label groups
    ├── Apply per-category confidence thresholds
    └── Resolve category key → (domain, subdomain) via TAXONOMY
    │
    ▼
List[OutputSchema]
    (chunk_id, domain, sub_domain, text, source metadata)
    │
    ▼
[Database ingestion — currently disconnected]
    ChunkIngestion().upload_batch(outputs)
```

## Classification Taxonomy

Emails are classified into 13+ organizational domains:

| Domain | Example Subdomains |
|---|---|
| PII | Direct_Identifiers, Contact_Info, Financial_IDs |
| HR | Performance_Reviews, Internal_Disputes, Credit_Bank_Info |
| Legal | Litigation, Compliance, Contractual, Privileged_Communications |
| Security | Operational_Security, Behavioral_Data |
| Strategic | M&A, Market_Expansion, Pricing_Models, Competitive_Analysis |
| R&D | Experiments, Algorithms, Models, Prototypes, IP |
| Financial | Salary_Negotiations, Budgets, Revenue, Investments |
| Operational | Project_Metadata, Org_Structure |
| Vendor | Vendor_Docs, Support_Escalation |
| Scheduling | Travel, Time_Zones, Coordination |
| Personal | Health_Disclosures, Crisis_Content |

Full taxonomy: [`Schemas/taxonomy.py`](Schemas/taxonomy.py)

## Quick Start

```python
from dataTaggers.ZeroShot import zero_shot_classify
from Schemas.taxonomy import ZERO_SHOT_LABEL_GROUPS, CATEGORY_THRESHOLDS
from util.parseMbox import controller

# Run the full ingestion pipeline on an .mbox file
outputs = controller(
    mbox_fp="path/to/emails.mbox",
    zero_shot_classify_fn=zero_shot_classify,
    label_groups=ZERO_SHOT_LABEL_GROUPS,
    threshold=0.5
)

# outputs is a list of dicts, each with:
# { chunk_id, domain, sub_domain, text, source: { email_id, sender, subject, ... } }
```

## RAG Query Routing

`util/get_domains_RAG.py` uses the same zero-shot classifier to route user queries to relevant RAG indexes before retrieval:

```python
from util.get_domains_RAG import get_domains_for_rag

domains = get_domains_for_rag("What were the Q3 revenue projections?")
# Returns: ["Financial_Strategy", "Financial_Accounting"]
```

## Evaluation

The pipeline has been evaluated on 320 hand-labeled test examples. Key metrics (Eval_1):

| Metric | Score |
|---|---|
| Macro F1 | 0.554 |
| Micro F1 | 0.536 |
| Exact Match Accuracy | 15.3% |
| Avg processing time | 0.087s/example |

Best-performing categories: Financial.Accounting.Bonuses (F1=0.897), Financial.Accounting.Salary_Negotiations (F1=0.818).

Full evaluation logs: [`ZS_Evaluation_Logs/`](ZS_Evaluation_Logs/)

## Integration Status

| Component | Status |
|---|---|
| Zero-shot classification | Working |
| .mbox parsing | Working |
| Evaluation suite | Working |
| RAG domain routing | Implemented, not called from backend |
| Database ingestion | Implemented, commented out in `parseMbox.py:176` |
| Backend `/upload` integration | Not connected |
