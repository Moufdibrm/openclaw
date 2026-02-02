import { describe, expect, it } from "vitest";
import type { OpenClawConfig } from "../config/config.js";
import type { SessionEntry } from "../config/sessions/types.js";
import {
  computeSpawnDepth,
  isNestedSpawnAllowed,
  resolveNestedToolsPolicy,
} from "./spawn-depth.js";

describe("computeSpawnDepth", () => {
  it("returns 0 for non-subagent session keys", () => {
    expect(computeSpawnDepth({ sessionKey: "main" })).toBe(0);
    expect(computeSpawnDepth({ sessionKey: "agent:main:main" })).toBe(0);
    expect(computeSpawnDepth({ sessionKey: "agent:jack-x:main" })).toBe(0);
    expect(computeSpawnDepth({ sessionKey: "" })).toBe(0);
  });

  it("returns 1 for direct subagent sessions without store", () => {
    expect(computeSpawnDepth({ sessionKey: "agent:main:subagent:abc-123" })).toBe(1);
    expect(computeSpawnDepth({ sessionKey: "subagent:abc-123" })).toBe(1);
  });

  it("returns stored spawnDepth when available", () => {
    const sessionStore: Record<string, SessionEntry> = {
      "agent:main:subagent:abc-123": {
        sessionId: "s1",
        updatedAt: Date.now(),
        spawnDepth: 2,
        spawnedBy: "agent:main:subagent:parent-123",
      },
    };
    expect(
      computeSpawnDepth({
        sessionKey: "agent:main:subagent:abc-123",
        sessionStore,
      }),
    ).toBe(2);
  });

  it("computes depth by traversing spawnedBy chain", () => {
    const sessionStore: Record<string, SessionEntry> = {
      "agent:main:subagent:level-3": {
        sessionId: "s3",
        updatedAt: Date.now(),
        spawnedBy: "agent:main:subagent:level-2",
      },
      "agent:main:subagent:level-2": {
        sessionId: "s2",
        updatedAt: Date.now(),
        spawnedBy: "agent:main:subagent:level-1",
      },
      "agent:main:subagent:level-1": {
        sessionId: "s1",
        updatedAt: Date.now(),
        spawnedBy: "agent:main:main",
      },
    };

    expect(
      computeSpawnDepth({
        sessionKey: "agent:main:subagent:level-1",
        sessionStore,
      }),
    ).toBe(1);

    expect(
      computeSpawnDepth({
        sessionKey: "agent:main:subagent:level-2",
        sessionStore,
      }),
    ).toBe(2);

    expect(
      computeSpawnDepth({
        sessionKey: "agent:main:subagent:level-3",
        sessionStore,
      }),
    ).toBe(3);
  });

  it("handles cycle detection", () => {
    const sessionStore: Record<string, SessionEntry> = {
      "agent:main:subagent:a": {
        sessionId: "s1",
        updatedAt: Date.now(),
        spawnedBy: "agent:main:subagent:b",
      },
      "agent:main:subagent:b": {
        sessionId: "s2",
        updatedAt: Date.now(),
        spawnedBy: "agent:main:subagent:a",
      },
    };

    // Should not hang, should return a reasonable depth
    const depth = computeSpawnDepth({
      sessionKey: "agent:main:subagent:a",
      sessionStore,
    });
    expect(depth).toBeGreaterThanOrEqual(1);
    expect(depth).toBeLessThanOrEqual(10);
  });
});

describe("isNestedSpawnAllowed", () => {
  const baseCfg: OpenClawConfig = {};

  it("allows spawn from non-subagent sessions", () => {
    const result = isNestedSpawnAllowed({
      requesterSessionKey: "agent:main:main",
      requesterAgentId: "main",
      cfg: baseCfg,
    });
    expect(result.allowed).toBe(true);
    expect(result.currentDepth).toBe(0);
  });

  it("denies nested spawn when allowNestedSpawn is false (default)", () => {
    const result = isNestedSpawnAllowed({
      requesterSessionKey: "agent:main:subagent:abc-123",
      requesterAgentId: "main",
      cfg: baseCfg,
    });
    expect(result.allowed).toBe(false);
    expect(result.reason).toContain("allowNestedSpawn: false");
    expect(result.currentDepth).toBe(1);
  });

  it("allows nested spawn when allowNestedSpawn is true globally", () => {
    const cfg: OpenClawConfig = {
      agents: {
        defaults: {
          subagents: {
            allowNestedSpawn: true,
            maxSpawnDepth: 3,
          },
        },
      },
    };

    const result = isNestedSpawnAllowed({
      requesterSessionKey: "agent:main:subagent:abc-123",
      requesterAgentId: "main",
      cfg,
    });
    expect(result.allowed).toBe(true);
    expect(result.currentDepth).toBe(1);
    expect(result.maxDepth).toBe(3);
  });

  it("allows nested spawn when allowNestedSpawn is true per-agent", () => {
    const cfg: OpenClawConfig = {
      agents: {
        list: [
          {
            id: "jack-x",
            subagents: {
              allowNestedSpawn: true,
              maxSpawnDepth: 4,
            },
          },
        ],
      },
    };

    const result = isNestedSpawnAllowed({
      requesterSessionKey: "agent:jack-x:subagent:abc-123",
      requesterAgentId: "jack-x",
      cfg,
    });
    expect(result.allowed).toBe(true);
    expect(result.maxDepth).toBe(4);
  });

  it("denies spawn when depth limit exceeded", () => {
    const cfg: OpenClawConfig = {
      agents: {
        defaults: {
          subagents: {
            allowNestedSpawn: true,
            maxSpawnDepth: 2,
          },
        },
      },
    };

    const sessionStore: Record<string, SessionEntry> = {
      "agent:main:subagent:level-2": {
        sessionId: "s2",
        updatedAt: Date.now(),
        spawnDepth: 2,
        spawnedBy: "agent:main:subagent:level-1",
      },
    };

    const result = isNestedSpawnAllowed({
      requesterSessionKey: "agent:main:subagent:level-2",
      requesterAgentId: "main",
      cfg,
      sessionStore,
    });
    expect(result.allowed).toBe(false);
    expect(result.reason).toContain("depth limit exceeded");
    expect(result.currentDepth).toBe(2);
    expect(result.maxDepth).toBe(2);
  });

  it("agent config overrides global config", () => {
    const cfg: OpenClawConfig = {
      agents: {
        defaults: {
          subagents: {
            allowNestedSpawn: false,
          },
        },
        list: [
          {
            id: "special-agent",
            subagents: {
              allowNestedSpawn: true,
              maxSpawnDepth: 5,
            },
          },
        ],
      },
    };

    const resultGlobal = isNestedSpawnAllowed({
      requesterSessionKey: "agent:main:subagent:abc",
      requesterAgentId: "main",
      cfg,
    });
    expect(resultGlobal.allowed).toBe(false);

    const resultSpecial = isNestedSpawnAllowed({
      requesterSessionKey: "agent:special-agent:subagent:abc",
      requesterAgentId: "special-agent",
      cfg,
    });
    expect(resultSpecial.allowed).toBe(true);
    expect(resultSpecial.maxDepth).toBe(5);
  });
});

describe("resolveNestedToolsPolicy", () => {
  it("returns undefined for depth <= 1", () => {
    const cfg: OpenClawConfig = {
      agents: {
        defaults: {
          subagents: {
            nestedTools: {
              deny: ["exec"],
            },
          },
        },
      },
    };

    expect(resolveNestedToolsPolicy({ cfg, agentId: "main", spawnDepth: 0 })).toBeUndefined();
    expect(resolveNestedToolsPolicy({ cfg, agentId: "main", spawnDepth: 1 })).toBeUndefined();
  });

  it("returns global nested tools for depth > 1", () => {
    const cfg: OpenClawConfig = {
      agents: {
        defaults: {
          subagents: {
            nestedTools: {
              allow: ["read", "write"],
              deny: ["exec", "gateway"],
            },
          },
        },
      },
    };

    const result = resolveNestedToolsPolicy({ cfg, agentId: "main", spawnDepth: 2 });
    expect(result).toEqual({
      allow: ["read", "write"],
      deny: ["exec", "gateway"],
    });
  });

  it("agent nested tools override global", () => {
    const cfg: OpenClawConfig = {
      agents: {
        defaults: {
          subagents: {
            nestedTools: {
              deny: ["exec"],
            },
          },
        },
        list: [
          {
            id: "jack-x",
            subagents: {
              nestedTools: {
                allow: ["read"],
                deny: ["memory_search"],
              },
            },
          },
        ],
      },
    };

    const result = resolveNestedToolsPolicy({ cfg, agentId: "jack-x", spawnDepth: 3 });
    expect(result).toEqual({
      allow: ["read"],
      deny: ["memory_search"],
    });
  });

  it("returns undefined when no nested tools configured", () => {
    const cfg: OpenClawConfig = {
      agents: {
        defaults: {
          subagents: {
            allowNestedSpawn: true,
          },
        },
      },
    };

    expect(resolveNestedToolsPolicy({ cfg, agentId: "main", spawnDepth: 2 })).toBeUndefined();
  });
});
