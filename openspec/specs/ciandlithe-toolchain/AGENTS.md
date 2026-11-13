# ciandlithe-toolchain — Agent Routing

| Spec | Path |
|:--|:--|
| spec.md | [./spec.md](./spec.md) |

## Quick orientation

`ciandlithe-toolchain` is the load-bearing repair for the 3 defects
that blocked every later work order: the missing `scripts/` directory,
the unpinned Python toolchain, and the missing jurisdiction pipeline
runners. Once this lands, every subsequent WO has a trustworthy
verification harness.

## Routing table

| I want to... | Look at... |
|:--|:--|
| Run the OSINT allowlist lint | `mise run lint:license` |
| Run the doc-number drift lint | `mise run lint:drift-docs` |
| Run the skills frontmatter lint | `mise run lint:skills` |
| Run the BLIP m1 (ROI) milestone | `mise run ciandlithe:blip:v1:m1` |
| Run the BLIP m2 (UK) milestone | `mise run ciandlithe:blip:v1:m2` |
| Run the BLIP m3 (Crown Deps) milestone | `mise run ciandlithe:blip:v1:m3` |
| Run the BLIP GA (all) milestone | `mise run ciandlithe:blip:v1:ga` |