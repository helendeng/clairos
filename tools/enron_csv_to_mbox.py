#!/usr/bin/env python3
"""
tools/enron_csv_to_mbox.py

Convert the rcmonteiro structured Enron CSV dataset (pre-parsed columns)
into a .mbox file for pipeline testing.

Expected CSV columns (others are ignored):
  Message-ID  - email message identifier
  Date        - date string (RFC-2822 or similar)
  From        - sender address / display name
  To          - recipient(s)
  Subject     - email subject line
  content     - plain-text email body
  user        - employee/mailbox owner (used by --sender filter)

Usage:
  python tools/enron_csv_to_mbox.py \
      --input  data/enron_structured.csv \
      --output data/test.mbox           \
      --limit  500                      \
      --sender phillip.allen
"""

import argparse
import email.utils
import mailbox
import time

import pandas as pd


_DEFAULT_CTIME = "Thu Jan  1 00:00:00 1970"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_ctime(date_str: str) -> str:
    """
    Convert an RFC-2822 date string to ctime format required by the mbox
    From_ separator line.  Returns a fixed epoch string on any parse failure.
    """
    if not date_str:
        return _DEFAULT_CTIME
    try:
        parsed = email.utils.parsedate(date_str)
        if parsed:
            ts = time.mktime(parsed)
            return time.asctime(time.localtime(ts))
    except (OverflowError, OSError, TypeError, ValueError):
        pass
    return _DEFAULT_CTIME


def _extract_addr(from_hdr: str) -> str:
    """Return the bare email address from a From header value."""
    _, addr = email.utils.parseaddr(from_hdr)
    return (addr or from_hdr).strip() or "unknown@unknown"


def _str(val) -> str:
    """Return an empty string for NaN/None, otherwise str(val).strip()."""
    if val is None:
        return ""
    try:
        if pd.isna(val):
            return ""
    except (TypeError, ValueError):
        pass
    return str(val).strip()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Convert structured Enron CSV to .mbox for pipeline testing.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--input", required=True,
                   help="Path to the structured Enron CSV file")
    p.add_argument("--output", required=True,
                   help="Path for the output .mbox file")
    p.add_argument("--limit", type=int, default=500,
                   help="Maximum number of emails to write")
    p.add_argument("--sender", default=None,
                   help="Substring filter on the From column (e.g. 'phillip.allen')")
    return p.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = _parse_args()

    df = pd.read_csv(args.input, dtype=str)

    total_read = 0
    written = 0
    skipped_empty = 0   # null/empty content or len(content) < 50
    skipped_sender = 0  # failed --sender filter

    # Truncate the output file so re-runs always start clean.
    open(args.output, "w").close()
    mbox_out = mailbox.mbox(args.output, create=True)
    mbox_out.lock()

    try:
        for _, row in df.iterrows():
            if written >= args.limit:
                break

            total_read += 1

            # --- Gate 1: content must be non-null and >= 75 chars ---
            body = _str(row.get("content"))

            if not body or len(body) < 75:
                skipped_empty += 1
                continue

            # --- Gate 2: optional sender substring filter ---
            # Checks both From header and the 'user' column (mailbox owner).
            from_hdr = _str(row.get("From"))
            user_col = _str(row.get("user"))
            if args.sender:
                needle = args.sender.lower()
                if needle not in from_hdr.lower() and needle not in user_col.lower():
                    skipped_sender += 1
                    continue

            # --- Build mbox message from pre-parsed columns ---
            to_hdr = _str(row.get("To"))
            subject_hdr = _str(row.get("Subject"))
            date_hdr = _str(row.get("Date"))

            msg = mailbox.mboxMessage()
            msg["From"] = from_hdr
            msg["To"] = to_hdr
            msg["Subject"] = subject_hdr
            msg["Date"] = date_hdr
            msg.set_payload(body, charset="utf-8")

            # mbox From_ separator: "From <addr> <ctime-date>"
            addr = _extract_addr(from_hdr)
            msg.set_from(f"{addr} {_safe_ctime(date_hdr)}")

            mbox_out.add(msg)
            written += 1

    finally:
        mbox_out.flush()
        mbox_out.unlock()
        mbox_out.close()

    # --- Verify the output is readable by mailbox.mbox() ---
    verify_mbox = mailbox.mbox(args.output)
    verified = sum(1 for _ in verify_mbox)
    verify_mbox.close()

    skipped_total = skipped_empty + skipped_sender
    print()
    print("Summary")
    print(f"  Total rows read            : {total_read}")
    print(f"  Emails written             : {written}")
    print(f"  Emails skipped (total)     : {skipped_total}")
    print(f"    - empty/short content    : {skipped_empty}")
    print(f"    - sender filter mismatch : {skipped_sender}")
    print(f"  Verified readable messages : {verified}")


if __name__ == "__main__":
    main()
