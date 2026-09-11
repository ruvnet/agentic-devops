# Operations

The local artifact planner has no deployment identity. Its operating system principal can only invoke the installed source; MCP provides no remote execution or file export operation. Run the host under a dedicated local account if other local files are sensitive.

Create a specification with name, namespace, image and baseImage. Optional numeric fields are port (1024..65535), replicas (1..20), cpuMillis (10..4000), memoryMiB (16..8192). Image references must be digest pinned. Names use lowercase DNS label characters with a maximum of 40 characters and minimum of two.

Preview input: `{ "before": <validated old bundle>, "after": <validated new bundle> }`.

Rollback input: `{ "current": <validated new bundle>, "previous": <validated old bundle>, "expectedCurrent": "<new bundle sha256>" }`.

Rollback returns the previous bundle without writing a file or changing a cluster. The compare and swap guard rejects stale local expectations. An actual deployer must additionally compare the live cluster revision and perform its own admission checks. Database migrations and persistent data restoration are outside this artifact rollback boundary.

Every generated container must expose the configured TCP port, run as UID/GID 10001 without writing its root filesystem and function without outbound network access. Add application specific network permissions only through a separately reviewed policy extension; manual changes cause bundle validation to reject the artifact. JSON Kubernetes files can be applied by kubectl after operator review, image qualification and server side dry run in a staging cluster. No namespace or cluster wide role is generated.

Generated CI only builds the supplied app/server image; it does not authenticate to a registry or deploy. Repository CI delivers evaluation evidence. Production CD requires a deployment owned environment, scoped short lived identity, admission policy, registry attestation verification, rollout health checks and a tested restoration procedure.
