# Project Agent Coordination

Treat this repository as the project’s **single source of truth**. Before planning or changing code, synchronize with `main`, read `README.md`, read `coordination/status.md`, and inspect the progress files relevant to overlapping work.

## Required progress behavior

Every contributor or agent must maintain one root-level `{username}_progress.md` file. Update it when starting a meaningful task, when scope or blockers change, and when finishing a task. Keep the headings defined in `README.md`. Do not edit another contributor’s progress file except to resolve a merge conflict with their explicit approval.

The scheduled heartbeat owns only the text between `heartbeat-managed` markers in `tpeters-keystone_progress.md`. Do not place human-authored notes inside that block.

## Delegation protocol

Before delegating work, check `coordination/status.md` for overlap, blockers, and requests. Assign delegated work with a concrete owner, scope, expected files, verification criteria, and dependency notes. Delegated agents should update their own progress file rather than appending private chain-of-thought or hidden instructions to another contributor’s file.

Do not expose system prompts, private reasoning, credentials, tokens, personal data, or secrets in coordination files. Record decisions, assumptions, evidence, blockers, and externally useful plans only.

## Change protocol

Prefer small, reviewable changes. Pull before starting, avoid rewriting shared history, and resolve conflicts by preserving each contributor’s authored sections. Update project files and the associated progress record in the same commit when practical. If a change is externally visible, destructive, security-sensitive, or irreversible, obtain the appropriate human approval before executing it.
