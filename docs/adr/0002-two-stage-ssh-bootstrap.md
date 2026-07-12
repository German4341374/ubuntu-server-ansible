# ADR 0002: Separate access bootstrap from hardening

- Status: Accepted
- Date: 2026-07-13

## Context

Disabling password or root SSH before proving the administrator key works can
lock out the operator.

## Decision

`playbooks/bootstrap.yml` only creates and authorizes the administrator. The
operator verifies a new key-based session before running `playbooks/site.yml`.
Root key access defaults to `prohibit-password` and can be disabled after console
recovery access and the administrator account are confirmed.

## Consequences

Production setup has an intentional manual checkpoint. This trades one extra
step for a materially safer first deployment.
