import type { OpenClawConfig } from "../config/config.js";
import type { SessionEntry } from "../config/sessions/types.js";
import { resolveAgentConfig } from "../agents/agent-scope.js";
import { normalizeAgentId, parseAgentSessionKey } from "../routing/session-key.js";

const DEFAULT_MAX_SPAWN_DEPTH = 1;
const ABSOLUTE_MAX_SPAWN_DEPTH = 10;

export type SpawnDepthResult = {
  allowed: boolean;
  reason?: string;
  currentDepth: number;
  maxDepth: number;
};

/**
 * Computes the spawn depth for a given session key by traversing the spawnedBy chain.
 * Returns 0 for non-subagent sessions, 1+ for subagent sessions based on nesting level.
 */
export function computeSpawnDepth(params: {
  sessionKey: string;
  sessionStore?: Record<string, SessionEntry>;
}): number {
  const { sessionKey, sessionStore } = params;
  const raw = (sessionKey ?? "").trim();
  if (!raw) {
    return 0;
  }

  // Check if this is a subagent session
  const parsed = parseAgentSessionKey(raw);
  const rest = parsed?.rest ?? raw;
  if (!rest.toLowerCase().startsWith("subagent:")) {
    return 0;
  }

  // If no store provided, assume depth 1 (direct spawn)
  if (!sessionStore) {
    return 1;
  }

  // Look up the session entry
  const entry = sessionStore[raw];
  if (!entry) {
    return 1;
  }

  // If spawnDepth is already stored, use it
  if (typeof entry.spawnDepth === "number" && entry.spawnDepth > 0) {
    return entry.spawnDepth;
  }

  // Traverse spawnedBy chain to compute depth
  const visited = new Set<string>();
  let depth = 1;
  let currentKey = entry.spawnedBy;

  while (currentKey && depth < ABSOLUTE_MAX_SPAWN_DEPTH) {
    // Cycle detection
    if (visited.has(currentKey)) {
      break;
    }
    visited.add(currentKey);

    const currentParsed = parseAgentSessionKey(currentKey);
    const currentRest = currentParsed?.rest ?? currentKey;

    // If parent is also a subagent, increment depth
    if (currentRest.toLowerCase().startsWith("subagent:")) {
      depth++;
      const parentEntry = sessionStore[currentKey];
      currentKey = parentEntry?.spawnedBy;
    } else {
      // Parent is not a subagent, we've reached the top
      break;
    }
  }

  return depth;
}

/**
 * Resolves the effective nested spawn configuration for an agent.
 */
function resolveNestedSpawnConfig(params: { cfg: OpenClawConfig; agentId: string }): {
  allowNestedSpawn: boolean;
  maxSpawnDepth: number;
} {
  const { cfg, agentId } = params;

  // Agent-level config takes priority
  const agentConfig = resolveAgentConfig(cfg, agentId);
  const agentSubagents = agentConfig?.subagents;

  // Global defaults
  const globalSubagents = cfg.agents?.defaults?.subagents;

  const allowNestedSpawn =
    agentSubagents?.allowNestedSpawn ?? globalSubagents?.allowNestedSpawn ?? false;

  const maxSpawnDepth = Math.min(
    ABSOLUTE_MAX_SPAWN_DEPTH,
    Math.max(
      1,
      agentSubagents?.maxSpawnDepth ?? globalSubagents?.maxSpawnDepth ?? DEFAULT_MAX_SPAWN_DEPTH,
    ),
  );

  return { allowNestedSpawn, maxSpawnDepth };
}

/**
 * Checks if a nested spawn is allowed from the given requester session.
 * Uses configuration to determine if nested spawning is enabled and depth limits.
 */
export function isNestedSpawnAllowed(params: {
  requesterSessionKey: string;
  requesterAgentId: string;
  cfg: OpenClawConfig;
  sessionStore?: Record<string, SessionEntry>;
}): SpawnDepthResult {
  const { requesterSessionKey, requesterAgentId, cfg, sessionStore } = params;

  // Compute current depth of the requester
  const currentDepth = computeSpawnDepth({
    sessionKey: requesterSessionKey,
    sessionStore,
  });

  // If requester is not a subagent (depth 0), this is a normal spawn
  if (currentDepth === 0) {
    return {
      allowed: true,
      currentDepth: 0,
      maxDepth: ABSOLUTE_MAX_SPAWN_DEPTH,
    };
  }

  // Requester is a subagent - check nested spawn config
  const normalizedAgentId = normalizeAgentId(requesterAgentId);
  const { allowNestedSpawn, maxSpawnDepth } = resolveNestedSpawnConfig({
    cfg,
    agentId: normalizedAgentId,
  });

  // Check if nested spawn is enabled
  if (!allowNestedSpawn) {
    return {
      allowed: false,
      reason: "sessions_spawn is not allowed from sub-agent sessions (allowNestedSpawn: false)",
      currentDepth,
      maxDepth: maxSpawnDepth,
    };
  }

  // Check depth limit (the spawned child would be at currentDepth + 1)
  const childDepth = currentDepth + 1;
  if (childDepth > maxSpawnDepth) {
    return {
      allowed: false,
      reason: `spawn depth limit exceeded (current: ${currentDepth}, max: ${maxSpawnDepth})`,
      currentDepth,
      maxDepth: maxSpawnDepth,
    };
  }

  return {
    allowed: true,
    currentDepth,
    maxDepth: maxSpawnDepth,
  };
}

/**
 * Resolves the nested tools policy for a subagent at a given depth.
 */
export function resolveNestedToolsPolicy(params: {
  cfg: OpenClawConfig;
  agentId: string;
  spawnDepth: number;
}): { allow?: string[]; deny?: string[] } | undefined {
  const { cfg, agentId, spawnDepth } = params;

  // Only apply nested tools for depth > 1
  if (spawnDepth <= 1) {
    return undefined;
  }

  const agentConfig = resolveAgentConfig(cfg, agentId);
  const agentNestedTools = agentConfig?.subagents?.nestedTools;
  const globalNestedTools = cfg.agents?.defaults?.subagents?.nestedTools;

  // Agent-level takes priority
  const nestedTools = agentNestedTools ?? globalNestedTools;
  if (!nestedTools) {
    return undefined;
  }

  return {
    allow: Array.isArray(nestedTools.allow) ? nestedTools.allow : undefined,
    deny: Array.isArray(nestedTools.deny) ? nestedTools.deny : undefined,
  };
}
