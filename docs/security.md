# Security review

Review date: 2026-09-11. Supported scope: src/, tests/, package lock, README and workflows. Historical Python tree inspected at execution and credential entrypoints, not certified as safe.

| Finding | Evidence | Resolution |
| --- | --- | --- |
| Critical: model selected shell execution | legacy cli/agentic.py and main.py used subprocess.run(selected_action, shell=True) | Legacy launchers now stop before imports; no v2 shell interpreter |
| High: command injection through repository path | legacy ls -lR interpolation used shell=True | Legacy command entrypoint retired; MCP has no paths |
| High: elevated downloaded installer | legacy utilities pip installed dependencies and curl piped into sudo bash | Utility/main entrypoints fail closed; locked explicit npm installation |
| High: overly broad cloud privilege advice | legacy utilities recommended Owner and could modify/delete Azure resources | No supported v2 cloud client or credential access |
| Misleading CI deployment | legacy workflows printed a production deployment message without deploying | Replaced with measured verification and artifact delivery |

Assets: infrastructure authority, local files, secrets and integrity of reviewed artifacts. Threat actors: untrusted MCP inputs and model generated specifications. Trust boundary: untrusted data enters a pure validator; only local operator configured validation may spawn one fixed test command. No request selects executable, argument list, path, credential or network endpoint.

Inputs are bounded, closed schema and digest pinned. Every artifact alteration fails canonical validation. Test subprocess environment is stripped, output bounded and deadline enforced. Root stdio host remains trusted and can alter installed source; this is not an OS sandbox. Hashes are unsigned consistency receipts. Fictional test images are never represented as reviewed production images.

Residual risks: a valid digest can still identify malicious code; namespace peers can reach the service; NetworkPolicy depends on CNI enforcement; no cluster admission, image attestation, registry vulnerability or live restoration test has been performed. A deployment owner must qualify those boundaries before rollout. Autogenous supplied evidence cannot replace independent measurements.

Validation commands: npm ci; npm test; npm audit --audit-level=moderate; npm run benchmark. Dependency audit uses npm's configured advisory feed at execution time and is limited to the supported locked Node dependency closure. See benchmark evidence for actual timings.
