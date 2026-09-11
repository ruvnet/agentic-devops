# ADR 001: Separate artifact planning from deployment authority

Status: accepted for v2 alpha.

## Context

The prior interface sent user instructions into a general coding agent and executed model selected shell strings. This entangled configuration advice with authority to modify infrastructure. Reproducing output and validating rollback required a narrower contract.

## Decision

Use a deterministic generator over a closed numeric and identifier schema. Emit five fixed artifact names. Validate by regenerating the complete canonical bundle and comparing bytes. Preview may change configuration but never resource identity. Artifact rollback requires the caller's current digest and returns the previous validated bundle. No tool acquires deployment credentials or executes artifact content.

Use the official MCP TypeScript SDK 2.0.0 for local stdio. Keep the domain planner independent of MCP and external packages. RuFlo owns orchestration; MetaHarness owns repeatable evaluations; Autogenous gates supplied evidence. Hashes do not prove identity and do not grant promotion authority.

## Alternatives and consequences

Keeping shell execution would preserve broad compatibility but preserve its privilege boundary problem. A universal Terraform or Kubernetes interpreter would increase the policy and testing surface beyond this release. Restricting output sacrifices arbitrary cloud templates and application builds, but gives checkable invariants and reproducible byte restoration.

## Sources reviewed 2026-09-11

[Kubernetes security checklist](https://kubernetes.io/docs/concepts/security/security-checklist/) guides security context, resource and network controls. [MCP server guide](https://modelcontextprotocol.io/docs/develop/build-server) informs the official SDK integration. These practices establish baseline safeguards, not proof of production security or superiority over deployment platforms.
