# Toolbox Change Procedure

Last updated: `2026-05-06`

This procedure lets Jack maintain governed toolbox changes without turning installed skills into blanket permissions.

## Product Rule

Skills and toolboxes are centralized.
Agents receive access through the governance matrix and route allowlists.

An installed skill is not permission.
Permission comes from:

1. the agent role
2. the agent toolbox matrix
3. the route package tool policy
4. the global approval gates

## Who Can Change What

Jack may propose and maintain governance changes when the request is explicit.
Tony may make mechanical doc/code edits only when explicitly delegated.
Other agents may propose changes through a handoff, but they do not decide governance policy.

Allowed Jack governance edits:

- add a skill family to an agent in `agent-toolbox-matrix.yaml`
- mark a skill family as forbidden/gated
- add or update a planned protocol in `agent-protocol-matrix.yaml`
- add external surfaces in `agent-environment-matrix.yaml`
- add notes to `AGENT_GOVERNANCE_MATRIX.md`

Jack must not silently:

- install runtime skills
- edit gateway/runtime/deploy/Mission Manager code
- mutate credentials
- print or move API keys
- grant broad access to all agents
- bypass approval gates because a skill is installed

Jack may install or update an agent profile skill only when the operator request is explicit or a governed route asks for a bounded install.
The install is still not a permission grant until this matrix is updated.

## Change Types

### 1. Add A New Skill Family

Use when a new skill or platform capability exists, but no protocol is proven yet.

Required fields:

- target agent
- skill/toolbox name
- external platform
- read surfaces
- mutable surfaces
- approval gates
- exploratory test plan
- expected proof
- owner agent

Default status:

- agent toolbox: `allowed_skill_families` only for the owning agent
- protocol: `draft`
- autonomy: `audit_read` or `discussion_approval`

### 2. Promote A Skill Into A Protocol

Use when direct tool use repeats or has clear workflow shape.

Required fields:

- route/protocol id
- owner agent
- inputs
- allowed tools/scripts
- forbidden tools
- output artifacts
- validation method
- approval gates
- rollback or blocked path

Default status:

- `draft` until the first bounded test succeeds
- `beta` after supervised test with reviewable artifacts
- `prod` only after validated route evidence and stable proof contract

### 3. Widen An Agent Toolbox

Use only when the agent's product role naturally owns the surface.

Before widening:

- confirm no existing agent is the better owner
- confirm the skill is not only convenient but actually role-aligned
- keep write access approval-gated by default

Example:

- Selena may read Zendesk tickets because support-risk is her role.
- Selena should not modify Klaviyo emails because that belongs to Safir/Rosa.

### 4. Emergency Block

Use when a skill/tool is too broad or unsafe.

Actions:

- remove it from the agent's `allowed_skill_families`
- add it to `forbidden_or_gated`
- document the reason in `AGENT_GOVERNANCE_MATRIX.md`
- keep a replacement path or explicit blocker

### 5. Install Or Update A Profile Skill

Use when a skill package must exist in one or more agent profiles.

Required fields to document:

- target profile paths
- source package or repo
- installed skill ids
- owning agent
- Jack scope if Jack also receives the skill
- current status: `installed_auth_pending`, `installed_test_pending`, `beta`, or `blocked`
- auth rule, without printing secrets
- proof required before route promotion

Default procedure:

1. List the remote package contents before installing when the installer supports it.
2. Stage the install in a temporary directory first.
3. Copy only the intended skill folders into `~/.brm-hermes/profiles/<agent>/skills`.
4. Do not copy generated dot-agent config folders unless the route explicitly requires them.
5. Update `agent-toolbox-matrix.yaml`, `agent-environment-matrix.yaml`, and, if repeated execution is expected, `agent-protocol-matrix.yaml`.
6. Validate installed `SKILL.md` files and parse YAML.
7. Keep live tests blocked until CLI/auth presence is confirmed without exposing secrets.

Higgsfield current precedent:

- source: `higgsfield-ai/skills`
- installed profiles: `jack`, `kanye`
- installed skills: `higgsfield-generate`, `higgsfield-marketplace-cards`, `higgsfield-product-photoshoot`, `higgsfield-soul-id`
- current status: `installed_hf_api_and_cli_live_test_passed`
- owner: `kanye`
- Jack scope: governed supervision or direct creative execution when explicitly requested
- beta evidence: `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-validation/20260505T214148Z/manifest.json`
- product photoshoot beta evidence: `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-validation/20260505T222952Z/manifest.json`
- attachment policy: `/Users/moufdi/openclaw/docs/ops/agent-governance/SKILL_ATTACHMENT_POLICY.md`
- prod blocker: polling `502` recovery must be standardized before route promotion

## Implementation Steps

1. Read the current files:
   - `agent-toolbox-matrix.yaml`
   - `agent-environment-matrix.yaml`
   - `agent-protocol-matrix.yaml`
   - `AGENT_GOVERNANCE_MATRIX.md`
2. Decide whether the change is:
   - skill family only
   - direct tool permission
   - draft protocol
   - beta/prod route promotion
3. Edit the smallest matrix section.
4. Keep access scoped to the owning agent.
5. Add or update approval gates.
6. Validate:
   - YAML parse OK
   - local referenced paths exist when paths are introduced
   - no reserved runtime/gateway/deploy/MM paths are touched
7. Summarize:
   - what changed
   - which agent got access
   - which actions remain approval-gated
   - what proof is required before promotion

## Reserved Zones

Do not edit these from toolbox governance work:

- Hermes gateway/runtime service files
- deployment scripts
- systemd services
- Mission Manager implementation files
- Jack reserved startup/action files

## Direct Tool Use To Protocol Candidate

Direct tool use is allowed when:

- the agent owns the surface
- the action stays within the approved autonomy level
- global approval gates are respected
- the result is logged or summarized clearly

Repeated direct tool use should become a protocol candidate.

Curator target signal:

- same agent
- same platform/toolbox
- same input shape
- same output/proof shape
- same recurring operator request

When that pattern appears, create or update a `draft` protocol entry instead of widening permissions again.

## Validation Command

From local Mac:

```bash
ruby -ryaml -e 'ARGV.each { |f| YAML.load_file(f); puts "OK #{f}" }' \
  /Users/moufdi/openclaw/docs/ops/agent-governance/*.yaml
```
