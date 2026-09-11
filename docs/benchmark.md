# Benchmark evidence

2026-09-11, managed Linux workspace, Node 24.19.0, 1,000 iterations of generation plus canonical validation: median 0.0455 ms, p95 0.0898 ms. These are warm local CPU measurements, not deployment or network latency. Hardware and shared workspace load affect results. Run `npm run benchmark` to reproduce the method.

The supported suite has 17 tests covering real SDK stdio, CLI roundtrip, security contexts, malformed identifiers, resource ceilings, digest requirements, artifact tampering, identity changes and stale rollback rejection. npm audit reported zero known advisories in the supported lockfile on the same date. No live registry, cluster, image build, cloud provider or production rollback benchmark was run.

## Rollback planning optimization

The baseline is merged commit `6d27e365da0f72746c18aa8f28e0baafa457b9d4`. Its source snapshot is preserved in `bench/baseline-planner.mjs`, SHA256 `9097be5880de766c6fe49cb9c42f599fe95104716d6bde18f0aed79b324e5429`. Run `node bench/rollback.mjs` for the same 100 varied specifications, 1000 warmup calls, five alternating baseline/candidate rounds and 3000 calls per implementation per round. Every valid output is checked for exact structural equality before timing. Measurements use Node's [performance API](https://nodejs.org/api/perf_hooks.html); no external benchmark leaderboard comparison is implied.

The baseline validated each bundle twice because rollback called preview after validating both bundles. The optimized path validates each bundle once, then applies the same resource identity guard. There is no validation cache and no trust granted to a previous invocation.

Recorded Node24 shared workspace results in [rollback-benchmark.json](rollback-benchmark.json): median round latency 0.1182–0.1208 ms baseline versus 0.0586–0.0604 ms optimized, approximately 50% lower local CPU time. Savings are approximately 60 microseconds per rollback planning request. This is a small implementation efficiency improvement, not a material reduction in actual deployment duration or a state of the art claim. Network and cluster latency are not measured. Regression tests reject mutation after a previously successful validation, either changed bundle, stale digests and mismatched resource identity.
