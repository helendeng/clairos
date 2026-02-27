"""
Input controller: ingests a .mbox file and feeds each email through the pipeline.

Entry point: controller(mbox_fp, zero_shot_classify_fn)
"""
import mailbox

from Ingestion.Schemas.schemas import EmailRecord, OutputSchema
from Ingestion.dataTaggers.ZeroShotController import process_email_with_zero_shot
from Ingestion.Schemas.taxonomy import ZERO_SHOT_LABEL_GROUPS
from database.core.ingest_chunks import ChunkIngestion


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_email_body(message) -> str | None:
    """Extracts the plain-text body from a mailbox.Message."""
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode(
                    part.get_content_charset() or "utf-8", "ignore"
                )
    else:
        if message.get_content_type() == "text/plain":
            return message.get_payload(decode=True).decode(
                message.get_content_charset() or "utf-8", "ignore"
            )
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
        subject=message.get("Subject", ""),
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
    print(all_outputs_list)
    return all_outputs_list

    ## Add this when we want to fully connect the data ingestion to the database
    # ingestion = ChunkIngestion()
    # ingestion.upload_batch(all_outputs_list)


