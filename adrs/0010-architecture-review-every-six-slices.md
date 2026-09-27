# 0010 An architecture review after every six slices

2026-09-26. Each repository carries a CLAUDE.md stating its module map, rules and size limits. After every six implemented slices an enabling slice reviews the code against it on Opus, logs findings, and cuts each refactor as its own enabling slice with a measurable check. Behaviour changes found by a review are logged as questions for the spec, not coded.
