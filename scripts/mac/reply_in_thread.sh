#!/bin/bash
# Reply to the newest message from a sender, in the same thread, after you approved the reply text.
#
# usage: reply_in_thread.sh <sender_address> <their_address> <subject_contains> <body_file>
set -euo pipefail

FROM="$1"; THEIRS="$2"; SUBJECT_PART="$3"; BODY_FILE="$4"
DIR="$(cd "$(dirname "$0")" && pwd)"
[ -e "${STOP_FILE:-$DIR/STOP}" ] && { echo "STOP file present, nothing sent."; exit 2; }
[ -f "$BODY_FILE" ] || { echo "Body file not found: $BODY_FILE"; exit 1; }

if [ "${DRY_RUN:-0}" = "1" ]; then
  echo "DRY RUN  would reply to the newest mail from $THEIRS containing \"$SUBJECT_PART\""; exit 0
fi

result=$(osascript - "$FROM" "$THEIRS" "$SUBJECT_PART" "$(cat "$BODY_FILE")" <<'APPLESCRIPT'
on run argv
  set {fromAddr, theirAddr, subjPart, bodyText} to argv
  tell application "Mail"
    set hits to (messages of inbox whose sender contains theirAddr and subject contains subjPart)
    if (count of hits) is 0 then return "NOT FOUND"
    set original to item 1 of hits (* newest first *)
    set r to reply original opening window no
    set sender of r to fromAddr
    set content of r to bodyText & return & return
    delay 2
    send r
    return "Re: " & (subject of original)
  end tell
end run
APPLESCRIPT
)
[ "$result" = "NOT FOUND" ] && { echo "No message from $THEIRS with \"$SUBJECT_PART\" in the inbox."; exit 1; }

for _ in $(seq 1 24); do
  sleep 5
  n=$(osascript -e "tell application \"Mail\" to count (messages of sent mailbox whose subject is \"$result\" and date sent > ((current date) - 900))")
  [ "$n" -gt 0 ] && { echo "SENT  reply \"$result\" (verified in Sent folder)"; exit 0; }
done
echo "NOT VERIFIED  reply did not appear in Sent within 120s. Check Mail before retrying."; exit 4
