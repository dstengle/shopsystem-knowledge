---
id: capability/review-who-changed-what
title: Review who changed what
narrator: the user, seeing how the shop's knowledge came to be as it is
rests_on:
  - decision/history-filters-and-snapshot
  - decision/actor-from-kb-actor
formulated_as: features/review-who-changed-what.feature
---

# Review who changed what

## Purpose

Reading back the history: who changed what, when and why. It can be filtered by artifact, by role, by piece of work or by date. Making the changes the history records is not part of this capability.

## Behaviour

- When the user reviews the changes to one artifact, the user is shown every change to it, each with who made it, when, what it did and why.
- When the user reviews the changes made by one role, the user is shown only the changes that role made.
- When the user reviews the changes made for one piece of work, the user is shown only the changes made for it.
- When the user reviews the changes since a date, the user is shown only the changes made since then.

## Implementation, may change

| command | maps to |
|---|---|
| `shop-knol journal [--artifact <id>] [--actor <role>] [--execution <id>] [--since <when>]` | Journal |

- The filters are passed to kb as given; `--actor` is kb's `role`. A time kb cannot read is refused by kb.
- A history entry that records what was read is shown with `read`, listing each artifact with the revision read.

## Not yet

Nothing deferred.
