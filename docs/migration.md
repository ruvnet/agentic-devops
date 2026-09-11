# Migration from 0.0.8

The historical Python distribution embedded an old Aider snapshot and interactive provider integrations. It could execute model selected shell commands, invoke installation scripts as root and request broad cloud permissions. These paths do not satisfy a bounded deployment planner's trust model.

V2 uses a new Node runtime. Root pip installation and legacy main, coder, agentic command, credential utility and Aider dispatch entrypoints now fail closed with a migration message before importing dependencies or accessing credentials. Old source remains for review and license provenance; it must not be imported as a supported library. No claim is made that its obsolete dependency closure has been patched.

Replace `pip install -e .` with `npm ci`. Replace interactive generation with `node src/cli.mjs plan` and a structured specification. Replace shell execution with a separately authorized deployment system consuming reviewed artifacts. Existing cloud credentials are neither needed nor read by v2. The previous UI, arbitrary Bash generation, seven cloud provider automation paths and embedded Aider are retired rather than silently exposed through MCP.

The supported dependency closure is package-lock.json. Historical requirements and setup files in docs are evidence only. Do not install them. This is a breaking alpha migration, not a drop in upgrade.
