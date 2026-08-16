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
