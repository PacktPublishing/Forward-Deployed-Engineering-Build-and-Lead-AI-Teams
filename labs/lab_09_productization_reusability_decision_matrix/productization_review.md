# Enterprise AI Claims Assistant — Productization and Reusability Review

- **Decision:** PORTFOLIO_PLAN_APPROVED
- **Scope:** Claims deployment assets reviewed for cross-customer reuse

## Decision Matrix

| Item | Capability | Score | Decision | Owner |
| --- | --- | ---: | --- | --- |
| P-01 | Prompt-injection evaluation pack | 20 | PRODUCT | AI Quality Product Owner |
| P-03 | Protected-action audit schema | 20 | PRODUCT | Security Product Owner |
| P-02 | Effective-policy retrieval pattern | 16 | PRODUCT | Knowledge Platform Product Owner |
| P-04 | Enterprise identity adapter framework | 11 | PLATFORM | Identity Platform Owner |
| P-05 | Claims decision workspace shell | 8 | PLATFORM | Claims Solution Platform Owner |
| P-06 | Tenant claim-field mapping | 6 | CONFIGURATION | Implementation Configuration Owner |
| P-08 | Pilot spreadsheet export | -6 | RETIRE | Claims Solution Owner |
| P-07 | Northstar legacy mainframe action adapter | -7 | CUSTOM_EXTENSION | Northstar Integration Owner |

## Portfolio Mix

- PRODUCT: 3
- PLATFORM: 2
- CONFIGURATION: 1
- CUSTOM_EXTENSION: 1
- RETIRE: 1

## Decision Definitions

- **PRODUCT:** Versioned supported capability with a standard customer-facing contract and roadmap owner.
- **PLATFORM:** Shared internal service or framework used by multiple deployments with platform ownership.
- **CONFIGURATION:** Supported declarative variation that does not fork shared code.
- **CUSTOM_EXTENSION:** Isolated customer-specific component with funding owner review date and no shared-core fork.
- **RETIRE:** Remove or archive because value and reuse do not justify ongoing maintenance.

## Guardrails

- No permanent customer-specific fork of shared product or platform code.
- Product and platform decisions require repeated demand and a named owner.
- Configuration must use a supported contract rather than copied source.
- Custom extensions require customer funding an isolation boundary and a dated review.
- Retirement must identify the dependency check and removal action.
