#!/bin/bash
# Send one approved email with the CV attached from Apple Mail, then confirm it reached the Sent folder.
#
# usage: send_att.sh <sender_address> <to_address> <subject> <body_file> <attachment> [organisation]
#
# Guard rails: refuses if a STOP file exists, if the address is already in sent_log.csv,
# or if the attachment is missing. DRY_RUN=1 prints what would happen and sends nothing.
set -euo pipefail

FROM="$1"; TO="$2"; SUBJECT="$3"; BODY_FILE="$4"; ATTACHMENT="$5"; ORG="${6:-}"
DIR="$(cd "$(dirname "$0")" && pwd)"
SENT_LOG="${SENT_LOG:-$DIR/sent_log.csv}"
STOP_FILE="${STOP_FILE:-$DIR/STOP}"
WAIT_SECONDS="${WAIT_SECONDS:-120}"

[ -e "$STOP_FILE" ] && { echo "STOP file present, nothing sent."; exit 2; }
[ -f "$BODY_FILE" ] || { echo "Body file not found: $BODY_FILE"; exit 1; }
[ -f "$ATTACHMENT" ] || { echo "Attachment not found: $ATTACHMENT"; exit 1; }
if [ -f "$SENT_LOG" ] && grep -qiF ",$TO," "$SENT_LOG"; then
  echo "SKIP  $TO already in sent_log.csv"; exit 3
fi

if [ "${DRY_RUN:-0}" = "1" ]; then
  echo "DRY RUN  would send \"$SUBJECT\" from $FROM to $TO with $(basename "$ATTACHMENT")"; exit 0
fi

osascript - "$FROM" "$TO" "$SUBJECT" "$(cat "$BODY_FILE")" "$ATTACHMENT" <<'APPLESCRIPT'
on run argv
  set {fromAddr, toAddr, subj, bodyText, attPath} to argv
  tell application "Mail"
    set msg to make new outgoing message with properties {subject:subj, content:bodyText & return & return, visible:false}
    tell msg
      set sender to fromAddr
      make new to recipient at end of to recipients with properties {address:toAddr}
      tell content to make new attachment with properties {file name:(POSIX file attPath) as alias} at after the last paragraph
    end tell
    delay 3 (* gives Mail time to load the attachment *)
    send msg
  end tell
end run
APPLESCRIPT

# Delivery check: the message must show up in the Sent folder within WAIT_SECONDS.
for _ in $(seq 1 $((WAIT_SECONDS / 5))); do
  sleep 5
  found=$(osascript - "$SUBJECT" "$TO" <<'APPLESCRIPT'
on run argv
  set {subj, toAddr} to argv
  tell application "Mail"
    set hits to (messages of sent mailbox whose subject is subj and date sent > ((current date) - 900))
    repeat with m in hits
      repeat with r in to recipients of m
        if address of r is toAddr then return "yes"
      end repeat
    end repeat
  end tell
  return "no"
end run
APPLESCRIPT
)
  if [ "$found" = "yes" ]; then
    [ -f "$SENT_LOG" ] || echo "timestamp,email,organisation,status,client" > "$SENT_LOG"
    echo "$(date '+%Y/%m/%d %H:%M:%S'),$TO,$ORG,sent,Apple Mail" >> "$SENT_LOG"
    echo "SENT  $TO  (verified in Sent folder)"; exit 0
  fi
done
echo "NOT VERIFIED  $TO did not appear in Sent within ${WAIT_SECONDS}s. Check Mail before retrying."; exit 4
