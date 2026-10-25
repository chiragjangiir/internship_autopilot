#!/bin/bash
# Add a meeting or deadline to Apple Calendar with four alerts: 1 day, 1 hour, 30 minutes and 15 minutes before.
#
# usage: add_event.sh <calendar_name> <title> <YYYY/MM/DD> <HH:MM> <duration_minutes> [notes]
# Title convention: "[INT] Org · what", "[DL] Org · what", "[PREP] Org · what".
set -euo pipefail

CAL="$1"; TITLE="$2"; DAY="$3"; TIME="$4"; MINUTES="$5"; NOTES="${6:-}"
IFS=/ read -r Y M D <<< "$DAY"; IFS=: read -r HH MM <<< "$TIME"

osascript - "$CAL" "$TITLE" "$Y" "$M" "$D" "$HH" "$MM" "$MINUTES" "$NOTES" <<'APPLESCRIPT'
on run argv
  set {calName, t, y, mo, d, hh, mm, mins, notesText} to argv
  set s to current date
  set day of s to 1 (* avoids month overflow while the fields are set *)
  set year of s to y as integer
  set month of s to mo as integer
  set day of s to d as integer
  set hours of s to hh as integer
  set minutes of s to mm as integer
  set seconds of s to 0
  tell application "Calendar"
    tell calendar calName
      set e to make new event with properties {summary:t, start date:s, end date:s + (mins as integer) * minutes, description:notesText}
      repeat with lead in {1440, 60, 30, 15}
        tell e to make new sound alarm at end of sound alarms with properties {trigger interval:(0 - lead)}
      end repeat
    end tell
  end tell
end run
APPLESCRIPT
echo "Added \"$TITLE\" on $DAY $TIME to calendar \"$CAL\" with 4 alerts."
