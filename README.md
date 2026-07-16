# Hackathon



This repository is the project’s **single source of truth** for plans, implementation, decisions, and contributor coordination.



## Coordination model



Each contributor or agent maintains one root-level progress file named:



```text

{username}_progress.md

```



The repository heartbeat runs every five minutes. It updates the configured owner’s heartbeat block, reads every other `*_progress.md` file, and regenerates [`coordination/status.md`](coordination/status.md) as a shared coordination view.



## Progress-file contract



Progress files should keep these headings so the coordination script can summarize them consistently:



```markdown

# {username} Progress



## Current Focus

What is being worked on now.



## Status

What has been completed and what remains.



## Blockers

Anything preventing progress, or `None`.



## Needs From Others

Specific requests for teammates or agents, or `None`.



## Next Steps

The next concrete actions.

```



The automation owns only the text between the `heartbeat-managed` markers. Contributors may edit every other section normally.



## Operating rules



Before starting work, pull `main` and read [`coordination/status.md`](coordination/status.md) plus the relevant contributor progress files. Before a meaningful implementation change, update your progress file with the intended scope. After completing or changing direction, update it again, commit the project changes and progress update together, then push to `main` or open a pull request according to the team’s chosen workflow.



Do not put secrets, credentials, tokens, private keys, personal data, or sensitive internal instructions in progress files. Progress files are coordination records, not authentication stores or private scratchpads.



## Running the heartbeat manually



The scheduled workflow can also be started from the repository’s **Actions** tab. For local verification:



```bash

python3 scripts/progress_heartbeat.py --username tpeters-keystone

```

