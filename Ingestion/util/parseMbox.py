"""
Input controller: ingests a .mbox file and feeds each email through the pipeline.

Entry point: controller(mbox_fp, zero_shot_classify_fn)
"""
import mailbox
import re

from Ingestion.Schemas.schemas import EmailRecord, OutputSchema
from Ingestion.dataTaggers.ZeroShotController import process_email_with_zero_shot
from Ingestion.Schemas.taxonomy import ZERO_SHOT_LABEL_GROUPS
from database.core.ingest_chunks import ChunkIngestion


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _decode_qp_artifacts(text: str) -> str:
    """
    Decode residual quoted-printable sequences left in email bodies.

    Emails that contain forwarded messages often have an inner QP-encoded
    body that Python's mailbox decoder never touches (it only decodes the
    outer Content-Transfer-Encoding). This does a safe second pass:
      - '=\\r\\n' / '=\\n'  →  ''   (soft line-break join)
      - '=XX'               →  chr  (hex-encoded character)
    """
    text = re.sub(r'=\r?\n', '', text)
    text = re.sub(r'=([0-9A-Fa-f]{2})', lambda m: chr(int(m.group(1), 16)), text)
    return text


def _strip_forwarding_headers(text: str) -> str:
    """
    Remove forwarding boilerplate and inline email header lines from body text.

    Strips:
      - Separator lines like '--- Forwarded by ... ---' or '--- Original Message ---'
      - Inline header lines: To:, From:, Cc:, Bcc:, Subject:, Date:, Sent:
    Collapses any resulting runs of blank lines down to a single blank line.
    """
    # Remove separator lines (5+ dashes or equals, optional text)
    text = re.sub(r'^[-=]{5,}.*$', '', text, flags=re.MULTILINE)
    # Remove inline email header lines
    text = re.sub(r'^(To|From|Cc|Bcc|Subject|Date|Sent|cc):\s.*$', '', text, flags=re.MULTILINE)
    # Collapse excess blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def _get_email_body(message) -> str | None:
    """Extracts, decodes, and cleans the plain-text body from a mailbox.Message."""
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    text = payload.decode(part.get_content_charset() or "utf-8", "ignore")
                    text = _decode_qp_artifacts(text)
                    text = _strip_forwarding_headers(text)
                    return text

    else:
        if message.get_content_type() == "text/plain":
            payload = message.get_payload(decode=True)
            if payload:
                text = payload.decode(message.get_content_charset() or "utf-8", "ignore")
                text = _decode_qp_artifacts(text)
                text = _strip_forwarding_headers(text)
                return text

    return None


def _parse_addresses(header_val: str | None) -> list[str]:
    """Splits a comma-separated address header into a list."""
    if not header_val:
        return []
    return [addr.strip() for addr in header_val.split(",")]


def parse_message_to_record(message, email_id: int) -> EmailRecord | None:
    """
    Converts a mailbox.Message into an EmailRecord.
    Returns None if the message has no plain-text body.
    """
    body = _get_email_body(message)
    if not body:
        return None

    return EmailRecord(
        email_id=str(email_id),
        sender=message.get("From", ""),
        subject=" ".join(message.get("Subject", "").split()),
        cc=_parse_addresses(message.get("Cc")),
        bcc=_parse_addresses(message.get("Bcc")),
        body=body,
        timestamp=message.get("Date", ""),
    )


def output_schemas_to_dicts(outputs: list[OutputSchema]) -> list[dict]:
    """
    Converts a list of OutputSchema objects into a list of plain dicts
    matching the canonical chunk format used for storage/export.
    """
    result = []
    for output in outputs:
        src = output.source
        result.append({
            "chunk_id": str(output.chunk_id),
            "domain": output.domain,
            "subdomain": output.sub_domain,
            "text": output.text,
            "source": {
                "email_id": src.email_id,
                "from": src.sender,
                "cc": ", ".join(src.cc),
                "bcc": ", ".join(src.bcc),
                "subject": src.subject,
                "timestamp": src.timestamp,
            },
        })
    return result


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def controller(
            mbox_fp: str,
            zero_shot_classify_fn,
            label_groups: dict = ZERO_SHOT_LABEL_GROUPS,
            threshold: float = 0.5,
        ) -> list[OutputSchema]:
    """
    Reads a .mbox file, parses each email into an EmailRecord,
    passes it to the ZeroShotController, and returns all OutputSchema results.

    Parameters
    ----------
    mbox_fp               : path to the .mbox file
    zero_shot_classify_fn : zero-shot pipeline callable
    label_groups          : group_name -> {category_key: description} mapping
                            (defaults to ZERO_SHOT_LABEL_GROUPS)
    threshold             : default confidence threshold (overridden per-category
                            by CATEGORY_THRESHOLDS where defined)

    Returns
    -------
    list[OutputSchema]  — all tagged chunks across all emails
    """
    mbox = mailbox.mbox(mbox_fp)
    all_outputs: list[OutputSchema] = []

    for email_id, message in enumerate(mbox):
        record = parse_message_to_record(message, email_id)
        if record is None:
            continue

        outputs = process_email_with_zero_shot(
            email=record,
            zero_shot_classify_fn=zero_shot_classify_fn,
            label_groups=label_groups,
            threshold=threshold,
        )

        all_outputs.extend(outputs)


    all_outputs_list = output_schemas_to_dicts(all_outputs)

    ## Add this when we want to fully connect the data ingestion to the database
    # upload to qdrant
    ingestion = ChunkIngestion()
    ingestion.upload_batch(all_outputs_list)

    return all_outputs_list    # Return list of dicts for easier downstream handling (e.g. JSON export)