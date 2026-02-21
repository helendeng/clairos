# The core model that will be run using the wrapper of ZeroShotController during inference, 
# or tested in the ZeroShotValidation code for validation and accuracy verification


# Load model directly using libraries
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Import local variables and files
from Schemas.taxonomy import ZERO_SHOT_LABELS
# Load the model and the tokenizer locally
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")
model = AutoModelForSequenceClassification.from_pretrained("facebook/bart-large-mnli")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device).eval()


## The generic classification model
def zero_shot_classify(
                        text: str,
                        candidate_labels: list[str],
                        hypothesis_template: str = "This text is about {}.",
                        multi_label: bool = False,  # False = single best label via softmax; True = independent scores per label
                      ):
    """
    Zero-shot classification using an NLI model (MNLI).
    For each label, we form a hypothesis and score 'entailment' (and optionally vs contradiction).
    """

    # label2id: maps label string -> class index
    label2id = {str(k).lower(): int(v) for k, v in model.config.label2id.items()}

    # id2label: maps class index -> label string
    id2label = {int(i): str(lbl).lower() for i, lbl in model.config.id2label.items()}

    entailment_id = label2id.get("entailment")
    contradiction_id = label2id.get("contradiction")

    if entailment_id is None:
        raise ValueError(f"Couldn't find entailment in label2id: {model.config.label2id}")

    # Build hypothesis strings
    hypotheses = [hypothesis_template.format(lbl) for lbl in candidate_labels]

    # Tokenize as premise/hypothesis pairs (premise=text, hypothesis=label statement)
    enc = tokenizer(
        [text] * len(candidate_labels),
        hypotheses,
        return_tensors="pt",
        padding=True,
        truncation=True,
    ).to(device)

    with torch.no_grad():
        logits = model(**enc).logits  # shape: (num_labels, 3) for MNLI models

    if multi_label:
        # Independent probability per label: P(entailment) vs P(contradiction)
        if contradiction_id is None:
            # fallback: just use sigmoid(entailment_logit) if contradiction isn't defined
            scores = torch.sigmoid(logits[:, entailment_id])
        else:
            # Use only entailment and contradiction logits, softmax them
            pair_logits = torch.stack([logits[:, contradiction_id], logits[:, entailment_id]], dim=1)
            scores = F.softmax(pair_logits, dim=1)[:, 1]  # prob(entailment)
    else:
        # Single-label (mutually exclusive): softmax over entailment logits across labels
        scores = F.softmax(logits[:, entailment_id], dim=0)

    # Package results
    scored = list(zip(candidate_labels, scores.detach().cpu().tolist()))
    scored.sort(key=lambda x: x[1], reverse=True)

    return {
        "text": text,
        "labels": [l for l, _ in scored],
        "scores": [s for _, s in scored],
        "raw": scored,
        "config_id2label": id2label,
        "entailment_id": entailment_id,
        "contradiction_id": contradiction_id,
    }