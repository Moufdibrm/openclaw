# Agent Profile Pack

Last updated: `2026-05-07`

This folder contains the Git-versioned, no-secret profile materialization pack for V1 BRM/Hermes agents.

It is generated from the local materialized profiles and governance matrices. It is not a runtime engine and does not deploy, restart, edit gateway files, or edit Mission Manager.

Apply policy:

- dry-run first
- copy only listed files
- never copy `.env`, auth files, sessions, memory stores, caches, or secrets
- never overwrite Jack reserved files
- do not apply `SOUL.md` for source-owned profiles `jack` and `mnemos`; update their canonical OpenClaw SOUL sources intentionally instead
- profile config changes are stored as `config.governance-overlay.yaml`, not full runtime config replacement

Machine-readable manifest: `../agent-profile-materialization-manifest.yaml`.
