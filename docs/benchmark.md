# Benchmark evidence

2026-09-11, managed Linux workspace, Node 24.19.0, 1,000 iterations of generation plus canonical validation: median 0.0455 ms, p95 0.0898 ms. These are warm local CPU measurements, not deployment or network latency. Hardware and shared workspace load affect results. Run `npm run benchmark` to reproduce the method.

The supported suite has 16 tests covering real SDK stdio, CLI roundtrip, security contexts, malformed identifiers, resource ceilings, digest requirements, artifact tampering, identity changes and stale rollback rejection. npm audit reported zero known advisories in the supported lockfile on the same date. No live registry, cluster, image build, cloud provider or production rollback benchmark was run.
