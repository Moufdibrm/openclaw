# Credential Standardization Audit

Date: `2026-05-07`

Scope: read-only credential/source-of-truth audit for agent toolboxes used by Naya, Safir, Selena, Jack, and Tony during supervised validation.

No secret value is recorded here. No external send, support reply, PayPal dispute message, refund, payment mutation, campaign publication, deploy, restart, gateway edit, Mission Manager edit, or systemd action was performed.

## Verdict

The credentials Moufdi expected are present and usable.

The previous `missing credentials` / `permission_denied` diagnosis was too broad. The real blocker is credential standardization: some scripts read the canonical Hermes env, while others fall back to stale local skill configs or service env files.

Current canonical source observed:

1. AWS Secrets Manager secret metadata: `brm-api-keys`.
2. Local materialized agent env: `/Users/moufdi/.brm-hermes/.env`.

Current SSM status:

- no SSM Parameter Store parameters were found for `KLAVIYO`.
- no SSM Parameter Store parameters were found for `PAYPAL`.
- Zendesk SSM parameters exist, but they are org/OAuth/runtime-style parameters, not the `ZENDESK_*_MAYBE_PARIS` env-key shape consumed by the current Selena skill helpers.

So the standard today is not SSM for these agent-level keys. It is `brm-api-keys` materialized into `/Users/moufdi/.brm-hermes/.env`.

## Evidence

| Surface | Result | Proof |
| --- | --- | --- |
| AWS account context | `314146310107`, region `eu-west-3` | AWS caller identity check, no secrets printed |
| AWS Secrets Manager | `brm-api-keys` exists, last changed `2026-04-19`, last accessed `2026-05-07` | `describe-secret` metadata only |
| Secret sync dry-run | BigBlue, Klaviyo Maybe Paris, PayPal Maybe Paris, Zendesk Maybe Paris keys are present in the sync plan | `/Users/moufdi/.openclaw/credential-audit-20260507/sync-business-secrets-dry-run.json` |
| Local Hermes env | `/Users/moufdi/.brm-hermes/.env` contains the expected key names | presence checked only, values not printed |
| BigBlue canonical env | `ListProducts`, `ListInventories`, and `ListOrders` returned `200` | live read-only probe with `BIGBLUE_API_KEY` loaded from `/Users/moufdi/.brm-hermes/.env` |
| BigBlue stale local config | same endpoints returned `403 permission_denied` when canonical env was not loaded | identifies stale or under-scoped `/Users/moufdi/clawd/skills/bigblue/config.json` fallback |
| Klaviyo Maybe Paris | account API returned ok with one account | live read-only probe with `KLAVIYO_API_KEY_MAYBE_PARIS` loaded |
| PayPal Maybe Paris | auth check returned `environment=live`, `credential_source=env:MAYBE_PARIS`, token present | `python3 /Users/moufdi/clawd/skills/paypal/scripts/paypal.py auth-check --store maybe-paris` |
| Zendesk Maybe Paris | `whoami` returned authenticated admin user id `380832128798` | `python3 /Users/moufdi/clawd/skills/zendesk/scripts/zendesk.py whoami --store maybe-paris` |
| Naya stock check | live stock check passed for `MONOI LOVE 100mL` after canonical env load | `/Users/moufdi/.openclaw/credential-validation/cred-20260507T142320Z/naya-stock-check-monoi-love/manifest.json` |
| Selena PayPal live | live fetch + audit passed in read-only mode | `/Users/moufdi/.openclaw/credential-validation/cred-20260507T142320Z/selena-paypal-live/manifest.json` |
| Selena Zendesk live | live fetch + review passed in read-only mode | `/Users/moufdi/.openclaw/credential-validation/cred-20260507T142320Z/selena-zendesk-live/manifest.json` |
| Safir mail-pole audit | Klaviyo credential stage passed and HTML was rendered; PDF render failed | `/Users/moufdi/.openclaw/workspace-safir/reports/mail-pole-audit/2026-05-07T14-25-08Z-maybe_paris/mail-pole-audit.html` |

## Reclassified Blockers

| Previous blocker | Current classification | Meaning |
| --- | --- | --- |
| `bigblue_inventory_permission_denied` | `credential_loader_not_standardized` plus stale BigBlue local config fallback | BigBlue works from canonical env; Naya can read stock when the env is loaded. |
| `missing_KLAVIYO_API_KEY_MAYBE_PARIS` | `credential_loader_not_standardized` plus Safir PDF rendering failure | Klaviyo Maybe Paris works; Safir still needs render/PDF stabilization and an email workflow brief. |
| `missing_paypal_credentials_for_maybe_paris` | resolved for read-only live routes | PayPal live read works; writes remain approval-gated. |
| `missing_zendesk_credentials_for_maybe_paris` | resolved for read-only live routes | Zendesk live read works; customer-visible replies remain approval-gated. |

## Required Standard

Use one source of truth for agent credentials:

1. AWS Secrets Manager `brm-api-keys` is the upstream secret bundle for current business-platform keys.
2. `/Users/moufdi/.brm-hermes/.env` is the local materialized env used by agents and scripts.
3. Git docs and profile packs must contain key names and source references only, never values.
4. Local skill `config.json` files may keep non-secret metadata and placeholders, but must not shadow canonical env values with stale secrets.
5. Every local runner invocation must load `/Users/moufdi/.brm-hermes/.env` before platform credential resolution.
6. Brand-specific env keys should stay explicit: `KLAVIYO_API_KEY_MAYBE_PARIS`, `PAYPAL_CLIENT_ID_MAYBE_PARIS`, `ZENDESK_API_TOKEN_MAYBE_PARIS`, etc.
7. Aliases may exist only as compatibility aliases and must map back to the canonical key name in the platform registry.
8. SSM Parameter Store should not be assumed as the source for agent-level business keys unless a migration is explicitly designed.

## Runner Gaps

| Area | Current gap | Owner lane |
| --- | --- | --- |
| BigBlue | skill falls back to `/Users/moufdi/clawd/skills/bigblue/config.json`, which can be stale if canonical env is not loaded | Tony/integrator for helper implementation; governance owns the standard |
| Safir | mail audit scripts read process env and `/etc/jack/jack.env`, not the canonical Hermes env in all local contexts | Tony/integrator for helper implementation; governance owns the standard |
| PayPal/Zendesk helpers | helpers work when process env is loaded, but do not load Hermes env themselves | Tony/integrator for helper implementation; governance owns the standard |
| Platform registry | now records the global credential source chain; per-platform brand/account fields should stay explicit as platforms are added | governance |
| Credential doctor | no single read-only command reports key presence, live-read permission, and runner source without printing values | Tony can implement; governance defines expected output |

## Agent Impact

| Agent | Impact |
| --- | --- |
| Naya | `naya.stock-check` can move from blocked to read-only beta when canonical env is loaded. Product query normalization remains needed because `Monoi Love` did not fuzzy-match `MONOI LOVE 100mL`. |
| Safir | Klaviyo Maybe Paris is not missing. Safir remains blocked on render/PDF reliability and the business brief for full email workflow validation. |
| Selena | PayPal and Zendesk live-read routes can be treated as read-only beta. Any customer reply, dispute message, refund, payment, or billing action still requires explicit approval. |
| Jack | Jack can see these platforms as available through governed toolboxes, but must respect route and approval gates. |
| Tony | Tony should standardize env loading and add a credential doctor without touching production deploy/restart/gateway/MM lanes unless explicitly delegated. |

## Product Decision Recommended

Keep the simple standard now:

`AWS Secrets Manager brm-api-keys -> /Users/moufdi/.brm-hermes/.env -> agent runner process env -> platform skill helper`

Do not migrate these keys to SSM just to satisfy naming expectations. SSM can remain for runtime/MM/OAuth parameters unless a separate migration is planned.
