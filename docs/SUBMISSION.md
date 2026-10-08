# Searchable Soroban diagnostic catalog with conservative evidence status

Prepared October 8, 2026 for same-day Stellar Wave application.

## Implemented utility

Thirty-five structured host/CLI/RPC/SDK diagnostic entries, local validation and ranked search. The evidence review retains historical RPC responses while clearing unsupported verification claims. Connectivity and malformed XDR responses cannot produce a verification PASS.

## Reproduce and evidence

python3 -m pytest -q: five tests passed October 8. python3 tools/validate_schema.py validated all 35 entries. No custom contract is required for a searchable reference catalog.

## Supported scope

Entry-specific live reproductions remain contributor work. The catalog does not establish every named failure or correctness of suggested fixes.

## Maintainers and application

Maintainers xteesamz and EthTobi were owner-confirmed across these project families; contact through GitHub, available anytime. Follow CONTRIBUTING.md and SECURITY.md (or organization defaults). Review the preparation PR and its CI before using its final revision in the application. Engineering issues and draft complexity do not establish Wave enrollment. No application has been submitted by this work.
