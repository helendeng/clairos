# dataTaggers

Core classification logic for the ingestion pipeline. Classifies email text chunks into organizational knowledge domains using zero-shot NLI.

## Files

| File | Purpose |
|---|---|
| [`ZeroShot.py`](ZeroShot.py) | BART-MNLI model wrapper |
| [`ZeroShotController.py`](ZeroShotController.py) | Email → chunk → tag orchestrator |
| [`ZeroShotTestExamples.py`](ZeroShotTestExamples.py) | 320 labeled examples for evaluation |
| [`ZeroShotValidation.py`](ZeroShotValidation.py) | Full evaluation suite with metrics |

---

## ZeroShot.py

Wraps `facebook/bart-large-mnli` as a reusable zero-shot classifier.

### How It Works

Zero-shot classification via NLI (Natural Language Inference): for each candidate label, a hypothesis is constructed (e.g., `"This text is about employee performance reviews."`) and the model predicts entailment probability between the input text and hypothesis. High entailment = the text is about that label.

**Model**: `facebook/bart-large-mnli`
**Device**: CUDA if available, CPU otherwise

### `zero_shot_classify(text, candidate_labels, hypothesis_template, multi_label)`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | required | Input text to classify |
| `candidate_labels` | `list[str]` | required | Human-readable label descriptions |
| `hypothesis_template` | `str` | `"This text is about {}."` | Template for NLI hypothesis |
| `multi_label` | `bool` | `True` | If True, sigmoid per label (independent); if False, softmax across labels |

**Returns**:
```python
{
    "text":   str,              # The input text
    "labels": list[str],        # Labels sorted by confidence (descending)
    "scores": list[float],      # Confidence scores (0-1), matching label order
    "raw":    list[tuple],      # [(label, score), ...] all pairs
    "config_id2label":  dict,   # Model's label index map
    "entailment_id":    int,    # Index of "entailment" in model output
    "contradiction_id": int     # Index of "contradiction" in model output
}
```

**Multi-label vs single-label**:
- `multi_label=True` — Each label gets an independent sigmoid score. Use when a chunk may belong to multiple categories.
- `multi_label=False` — Softmax across all entailment logits. Use when exactly one label applies.

The pipeline uses `multi_label=True` throughout.

---

## ZeroShotController.py

Orchestrates the per-email classification pipeline: splits email body into chunks, runs classification, applies thresholds, and emits tagged `OutputSchema` objects.

### `process_email_with_zero_shot(email, zero_shot_classify_fn, label_groups, threshold, split_by)`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `email` | `EmailRecord` | required | Normalized email input |
| `zero_shot_classify_fn` | callable | required | The `zero_shot_classify` function |
| `label_groups` | `dict` | required | `ZERO_SHOT_LABEL_GROUPS` from taxonomy |
| `threshold` | `float` | `0.5` | Default confidence threshold |
| `split_by` | `str` | `"sentence"` | `"sentence"` or `"paragraph"` |

**Returns**: `list[OutputSchema]`

### Processing Steps

1. **Chunk the email body**
   - `"sentence"`: splits on `.`, `!`, `?`; keeps chunks > 50 characters
   - `"paragraph"`: splits on `\n\n`

2. **Classify each chunk** against all label groups
   - Runs `zero_shot_classify` once per group (4 passes total)
   - Collects all (score, category_key) pairs across all groups

3. **Apply thresholds**
   - Looks up per-category threshold from `CATEGORY_THRESHOLDS`
   - Falls back to the `threshold` parameter for unlisted categories
   - Only keeps categories where `score >= threshold`

4. **Select winner**
   - Picks the highest-scoring qualifying category for the chunk
   - Resolves category key → `(domain, subdomain)` via `TAXONOMY`

5. **Emit OutputSchema**
   - One per chunk that has a qualifying category

Chunks with no category exceeding any threshold are silently dropped.

---

## ZeroShotTestExamples.py

320 hand-curated test examples used by `ZeroShotValidation.py` for benchmarking and threshold tuning.

### Structure

```python
zero_shot_test_examples = [
    {
        "text": "We need to finalize the acquisition terms before the board meeting...",
        "true_labels": ["Strategic.M&A"]
    },
    {
        "text": "Sarah's Q4 performance review is scheduled for next Thursday...",
        "true_labels": ["HR.Performance_Reviews"]
    },
    # 318 more ...
]
```

Each example has one `text` field and a list of `true_labels` (multi-label, 1-4 labels per example). Examples span all 13+ domains in the taxonomy.

---

## ZeroShotValidation.py

Full evaluation suite for benchmarking classifier performance on the test set.

### `evaluate_zero_shot_classifier_parallel(test_examples, label_groups, zero_shot_classify_fn, category_thresholds, default_threshold, multi_label)`

Runs inference on all test examples and computes multi-label classification metrics.

**Returns** a dict with:

#### Overall Metrics
| Key | Description |
|---|---|
| `micro_precision` | Precision averaged over all label instances |
| `micro_recall` | Recall averaged over all label instances |
| `micro_f1` | Micro F1 score |
| `macro_f1` | Macro F1 (unweighted average over categories) |
| `exact_match_accuracy` | Fraction of examples with perfect label prediction |
| `hamming_loss` | Fraction of labels incorrectly predicted |

#### Per-Category Metrics
For each category in `TAXONOMY`:
```python
results["per_category"]["HR.Performance_Reviews"] = {
    "precision": 0.72,
    "recall":    0.68,
    "f1":        0.70,
    "support":   25,       # # of examples with this label
    "tp": 17, "fp": 7, "fn": 8,
    "threshold": 0.5
}
```

#### Confusion & Error Analysis
- `confusion_pairs`: most common (predicted, true) misclassification pairs
- `false_positives`: categories most often predicted when wrong
- `false_negatives`: categories most often missed
- `failed_examples`: examples with zero predictions, low confidence correct predictions, or high confidence wrong predictions

### `print_evaluation_report(results, top_n=10)`

Prints a human-readable table to stdout showing top/bottom N categories by F1, confusion pairs, threshold config, and summary stats. Used for manual review during threshold tuning.

### `export_results_to_csv(results, output_prefix)`

Exports per-category metrics and per-example predictions to CSV files for offline analysis.

### Running an Evaluation

```python
from dataTaggers.ZeroShot import zero_shot_classify
from dataTaggers.ZeroShotTestExamples import zero_shot_test_examples
from dataTaggers.ZeroShotValidation import evaluate_zero_shot_classifier_parallel, print_evaluation_report
from Schemas.taxonomy import ZERO_SHOT_LABEL_GROUPS, CATEGORY_THRESHOLDS

results = evaluate_zero_shot_classifier_parallel(
    test_examples=zero_shot_test_examples,
    label_groups=ZERO_SHOT_LABEL_GROUPS,
    zero_shot_classify_fn=zero_shot_classify,
    category_thresholds=CATEGORY_THRESHOLDS,
    default_threshold=0.5,
    multi_label=True
)

print_evaluation_report(results, top_n=10)
```

Previous evaluation outputs are saved in [`../ZS_Evaluation_Logs/`](../ZS_Evaluation_Logs/).

### Eval_1 Benchmark Summary (320 examples)

| Category | F1 |
|---|---|
| Financial.Accounting.Bonuses | 0.897 |
| Financial.Accounting.Salary_Negotiations | 0.818 |
| Strategic.Market_Expansion | 0.743 |
| Strategic.M&A | 0.733 |
| ... | ... |
| Strategic.Pricing_Models | 0.370 |
| R&D.Technical.Models | 0.385 |
| Legal.Litigation.Legal_Disputes | 0.361 |
