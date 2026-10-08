# Wave engineering backlog

Drafted October 8, 2026 against current implementation. These are proposed contributor tasks, not Wave enrollment or earned points. Complexity requires maintainer review in the app.

## 1. Reproduce a named auth error with a valid envelope

## Context

Record valid invocation context, exact observed failure and source/WASM provenance; malformed transaction rejection cannot satisfy acceptance.

## Acceptance criteria

- Implement and document the specific behavior above.
- Cover positive, negative and unavailable-input cases appropriate to the change.
- Pass the repository documented build/test checks and required CI.
- Preserve exact identities/amounts and uncertain evidence outcomes.

## Relevant files

verification/, entries/host-errors/require-auth-missing.md

## Proposed complexity

high; planning only. Actual Wave complexity and enrollment are set by maintainers in the Drips app.

## Contribution

Open a focused feat/fix/test/docs branch. PRs explain behavior and actual validation and include Closes #<issue_id>. Follow CONTRIBUTING.md and SECURITY.md.

## 2. Reproduce a contract arithmetic panic with execution evidence

## Context

Deploy/use reviewed source and valid simulation, capture exact diagnostic type and compare documented error aliases to observed behavior.

## Acceptance criteria

- Implement and document the specific behavior above.
- Cover positive, negative and unavailable-input cases appropriate to the change.
- Pass the repository documented build/test checks and required CI.
- Preserve exact identities/amounts and uncertain evidence outcomes.

## Relevant files

verification/, entries/host-errors/arith-error.md

## Proposed complexity

high; planning only. Actual Wave complexity and enrollment are set by maintainers in the Drips app.

## Contribution

Open a focused feat/fix/test/docs branch. PRs explain behavior and actual validation and include Closes #<issue_id>. Follow CONTRIBUTING.md and SECURITY.md.

## 3. Define a reviewed verification evidence schema

## Context

Require reproduction source/revision, network, context and observed named-error diagnostics; reject connectivity-only and generic invalid-XDR records.

## Acceptance criteria

- Implement and document the specific behavior above.
- Cover positive, negative and unavailable-input cases appropriate to the change.
- Pass the repository documented build/test checks and required CI.
- Preserve exact identities/amounts and uncertain evidence outcomes.

## Relevant files

schema/, tools/validate_schema.py

## Proposed complexity

medium; planning only. Actual Wave complexity and enrollment are set by maintainers in the Drips app.

## Contribution

Open a focused feat/fix/test/docs branch. PRs explain behavior and actual validation and include Closes #<issue_id>. Follow CONTRIBUTING.md and SECURITY.md.

## 4. Check catalog error aliases against current Stellar sources

## Context

Review one error family against pinned official XDR/SDK definitions and distinguish canonical codes from human search aliases.

## Acceptance criteria

- Implement and document the specific behavior above.
- Cover positive, negative and unavailable-input cases appropriate to the change.
- Pass the repository documented build/test checks and required CI.
- Preserve exact identities/amounts and uncertain evidence outcomes.

## Relevant files

entries/, docs/

## Proposed complexity

medium; planning only. Actual Wave complexity and enrollment are set by maintainers in the Drips app.

## Contribution

Open a focused feat/fix/test/docs branch. PRs explain behavior and actual validation and include Closes #<issue_id>. Follow CONTRIBUTING.md and SECURITY.md.

## 5. Generate consumer bundles without touching sibling checkouts

## Context

Write deterministic versioned local artifacts by default and support explicit consumer destinations; verify byte identity and unsupported verification flags.

## Acceptance criteria

- Implement and document the specific behavior above.
- Cover positive, negative and unavailable-input cases appropriate to the change.
- Pass the repository documented build/test checks and required CI.
- Preserve exact identities/amounts and uncertain evidence outcomes.

## Relevant files

tools/sync_explorer.py

## Proposed complexity

medium; planning only. Actual Wave complexity and enrollment are set by maintainers in the Drips app.

## Contribution

Open a focused feat/fix/test/docs branch. PRs explain behavior and actual validation and include Closes #<issue_id>. Follow CONTRIBUTING.md and SECURITY.md.

## 6. Add an evidence legend and contributor reproducer guide

## Context

Explain unverified, captured and error-reproduced states with exact examples; require matching diagnostics before verified=true.

## Acceptance criteria

- Implement and document the specific behavior above.
- Cover positive, negative and unavailable-input cases appropriate to the change.
- Pass the repository documented build/test checks and required CI.
- Preserve exact identities/amounts and uncertain evidence outcomes.

## Relevant files

README.md, CONTRIBUTING.md

## Proposed complexity

trivial; planning only. Actual Wave complexity and enrollment are set by maintainers in the Drips app.

## Contribution

Open a focused feat/fix/test/docs branch. PRs explain behavior and actual validation and include Closes #<issue_id>. Follow CONTRIBUTING.md and SECURITY.md.

## Published contributor issues

- [Reproduce a named auth error with a valid envelope](https://github.com/TrapTrace/soroban-error-index/issues/17) — proposed high.
- [Reproduce a contract arithmetic panic with execution evidence](https://github.com/TrapTrace/soroban-error-index/issues/18) — proposed high.
- [Define a reviewed verification evidence schema](https://github.com/TrapTrace/soroban-error-index/issues/19) — proposed medium.
- [Check catalog error aliases against current Stellar sources](https://github.com/TrapTrace/soroban-error-index/issues/20) — proposed medium.
- [Generate consumer bundles without touching sibling checkouts](https://github.com/TrapTrace/soroban-error-index/issues/21) — proposed medium.
- [Add an evidence legend and contributor reproducer guide](https://github.com/TrapTrace/soroban-error-index/issues/22) — proposed trivial.
