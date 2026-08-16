import assert from "node:assert/strict";
import test from "node:test";
import { evaluateAuthority } from "../src/authority.js";
import { loadRegistries } from "../src/registries.js";
import { resolveIdentifier } from "../src/resolution.js";
import { loadSchemaCatalog } from "../src/schemas.js";

test("unknown identifiers do not resolve as terminal records", () => {
  assert.equal(resolveIdentifier({ known: false, terminal: true }).outcome, "not_found");
});

test("discovery never implies authority", () => {
  assert.equal(evaluateAuthority({
    profile: "A",
    request: { action: "purchase.submit", time: "2026-07-15T10:00:00Z" }
  }).outcome, "not_applicable");
});

test("missing status fails closed", () => {
  assert.equal(evaluateAuthority({
    profile: "C",
    request: { action: "purchase.submit", time: "2026-07-15T10:00:00Z" }
  }).outcome, "indeterminate");
});

test("registries are consumed from repository sources", () => {
  const registries = loadRegistries();
  assert.ok(registries.size >= 10);
  assert.ok(registries.has("registries/lifecycle-statuses.json"));
  assert.ok(registries.has("registries/reason-codes.json"));
});

test("normative schema catalog is consumed directly", () => {
  const schemas = loadSchemaCatalog();
  assert.ok(schemas.length >= 20);
  assert.ok(schemas.every((schema) => schema.draft.includes("2020-12")));
  assert.ok(schemas.some((schema) => schema.file === "schemas/decision-receipt.schema.json"));
});

import { assessHistoricalResolution, selectEffectiveRecords } from "../src/historical.js";
import { createDecisionReceipt } from "../src/receipts.js";
import { verifyEventContinuity } from "../src/events.js";
import { readJson } from "../src/repository.js";

test("historical selection uses effective time rather than current state", () => {
  const selected = selectEffectiveRecords([
    { record_id: "v1", effective_from: "2026-07-01T00:00:00Z", effective_until: "2026-07-20T00:00:00Z" },
    { record_id: "v2", effective_from: "2026-07-20T00:00:00Z", effective_until: null }
  ], "2026-07-15T10:00:00Z");
  assert.deepEqual(selected.map((record) => record.record_id), ["v1"]);
});

test("historical resolution fails closed outside retention", () => {
  const vector = readJson<any>("conformance/test-vectors/historical/HV-11-retention-boundary.json");
  const assessment = assessHistoricalResolution(vector);
  assert.equal(assessment.outcome, "indeterminate");
  assert.equal(assessment.usable, false);
});

test("verified authoritative historical state remains distinct from current state", () => {
  const vector = readJson<any>("conformance/test-vectors/historical/HV-01-active-at-T-now-revoked.json");
  const assessment = assessHistoricalResolution(vector);
  assert.equal(assessment.outcome, "usable");
  assert.equal(assessment.stateAtRequestedTime?.registration, "active");
  assert.equal(vector.current_state.registration, "revoked");
});

test("decision receipt captures deterministic request digest and evidence references", () => {
  const input = {
    profile: "C" as const,
    agent_status: { registration: "active", operation: "available", security: "normal", observed_at: "2026-07-15T09:59:00Z", valid_until: "2026-07-15T11:00:00Z" },
    authority_envelope: { effective_from: "2026-07-01T00:00:00Z", action_classes: ["purchase.submit"] },
    request: { action: "purchase.submit", time: "2026-07-15T10:00:00Z" }
  };
  const decision = evaluateAuthority(input);
  const receipt = createDecisionReceipt({ input, decision, subject: "agentreg:example.org:agent-123", evaluatorIdentity: "registry.example.org", authorityRecordIds: ["authority-1"], statusRecordIds: ["status-1"], evidence: ["evidence:bundle:1"] });
  assert.equal(receipt.decision, "allow");
  assert.match(receipt.request_digest, /^sha256:[0-9a-f]{64}$/);
  assert.deepEqual(receipt.evaluated_authority_records, ["authority-1"]);
});

test("event continuity detects sequence gaps", () => {
  const result = verifyEventContinuity([
    { event_id: "e1", event_type: "agent.registered", subject: "agentreg:example.org:a", sequence: 1, occurred_at: "2026-07-01T00:00:00Z", effective_at: "2026-07-01T00:00:00Z", issuer: "registry", reason_code: "registered" },
    { event_id: "e3", event_type: "agent.suspended", subject: "agentreg:example.org:a", sequence: 3, occurred_at: "2026-07-02T00:00:00Z", effective_at: "2026-07-02T00:00:00Z", issuer: "registry", reason_code: "suspended" }
  ]);
  assert.equal(result.contiguous, false);
  assert.ok(result.reasonCodes.includes("event_sequence_gap"));
});
