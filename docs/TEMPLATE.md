# Postmortem: [Short title describing what broke]

**Date:** YYYY-MM-DD
**Duration:** X hours Y minutes
**Severity:** P0 / P1 / P2
**Author:** Ahmed Ghanima
**Status:** Draft / In review / Final

---

## Summary

One paragraph. What broke, when it was detected, and what the impact was. Write this after you fill in the rest of the document.

---

## Timeline

All times in EET (UTC+2) or EEST (UTC+3) depending on season.

| Time | Event |
|---|---|
| HH:MM | First sign of the problem (alert, user report, or noticed manually) |
| HH:MM | Started investigating |
| HH:MM | Root cause identified |
| HH:MM | Fix applied |
| HH:MM | Service confirmed healthy |

---

## Root cause

What actually caused the incident. Be specific — not "disk was full" but "Loki's data volume hit 100% because log retention was set to 7 days but ingest rate increased after adding Promtail to a high-traffic container."

If the root cause has sub-causes (e.g. a monitoring gap that prevented early detection), list them here.

---

## Impact

- Which services were affected
- For how long
- Whether data was lost (and how much)
- Whether any external users were affected

---

## What we did to fix it

Step-by-step account of the response. Include commands run, configs changed, and anything that didn't work before finding the fix. This is for the next person who hits the same issue.

---

## What went well

Things that helped during the incident. Examples: alert fired before users noticed, runbook existed and was accurate, rollback was clean.

---

## What went wrong

Things that slowed down detection or recovery. Examples: no alert for that metric, runbook was outdated, had to look up the restore command during the incident.

---

## Action items

| Item | Owner | Due date |
|---|---|---|
| Add alert for X metric | Ahmed | YYYY-MM-DD |
| Update runbook Y | Ahmed | YYYY-MM-DD |
| Automate backup of Z | Ahmed | YYYY-MM-DD |

---

## Lessons learned

One or two sentences on what this incident changed about how you operate the platform. Skip this if there's nothing meaningful beyond the action items above.
