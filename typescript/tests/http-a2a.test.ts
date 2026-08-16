import test from "node:test";
import assert from "node:assert/strict";
import { once } from "node:events";
import { createArpaServer } from "../src/server.js";
import { ArpaClient } from "../src/client.js";
import { classifyAgentCardCompatibility, createA2APublicationProjection } from "../src/a2a.js";

test("A2A projection never implies authority", () => {
  const projection = createA2APublicationProjection(
    { record_id: "core-1", agent_id: "agentreg:example:test", status: "active", issuer: "registry:test" },
    { record_id: "desc-1", subject: "agentreg:example:test", uri: "https://example.test/card", digest: "0".repeat(64), protocol_versions: ["1.0"] }
  );
  assert.equal(projection.authority_implication, false);
  assert.equal(projection.agent_card_uri, "https://example.test/card");
});

test("A2A compatibility is conservative", () => {
  assert.equal(classifyAgentCardCompatibility({ skills: [{ id: "a" }] }, { skills: [{ id: "a" }, { id: "b" }] }), "compatible");
  assert.equal(classifyAgentCardCompatibility({ skills: [{ id: "a" }, { id: "b" }] }, { skills: [{ id: "a" }] }), "breaking");
  assert.equal(classifyAgentCardCompatibility(null, { skills: [] }), "indeterminate");
});

test("HTTP client and server provide a consumable ARPA surface", async () => {
  const { server } = createArpaServer({ port: 0, host: "127.0.0.1" });
  server.listen(0, "127.0.0.1"); await once(server, "listening");
  const address = server.address();
  assert.ok(address && typeof address === "object");
  const client = new ArpaClient(`http://127.0.0.1:${address.port}`);
  try {
    assert.equal((await client.health()).status, "ok");
    await client.registerAgent({ record_id: "core-http", record_type: "agent_core", schema_version: "1.0.0", issuer: "registry:test", subject: "agentreg:example:http", agent_id: "agentreg:example:http", issued_at: "2026-08-01T00:00:00Z", effective_from: "2026-08-01T00:00:00Z", effective_until: null, status: "active" });
    await client.putRecord({ record_id: "desc-http", record_type: "agent-description-reference", subject: "agentreg:example:http", issuer: "registry:test", issued_at: "2026-08-01T00:00:00Z", effective_from: "2026-08-01T00:00:00Z", effective_until: null, uri: "https://example.test/card", digest: "0".repeat(64), disclosure_class: "public", protocol_versions: ["1.0"] });
    const list = await client.listAgents();
    assert.equal(list.items[0].authority_implication, false);
    assert.equal((await client.resolveAgent("agentreg:example:http")).agent.record_id, "core-http");
  } finally { server.close(); }
});
