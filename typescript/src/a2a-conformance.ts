import fs from "node:fs";
import path from "node:path";
import { createA2APublicationProjection, classifyAgentCardCompatibility } from "./a2a.js";
import { repositoryRoot, readJson } from "./repository.js";

const core = readJson<any>("examples/valid/agent-core.json");
const ref = readJson<any>("examples/valid/agent-description-reference.json");
const projection = createA2APublicationProjection(core, ref);
const checks = [
  { name: "exact-agent-card-uri-preserved", passed: projection.agent_card_uri === ref.uri },
  { name: "publication-does-not-imply-authority", passed: projection.authority_implication === false },
  { name: "source-record-provenance-retained", passed: projection.source_record_ids.includes(core.record_id) && projection.source_record_ids.includes(ref.record_id) },
  { name: "additive-card-change-compatible", passed: classifyAgentCardCompatibility({ skills: [{ id: "a" }] }, { skills: [{ id: "a" }, { id: "b" }] }) === "compatible" },
  { name: "removed-card-skill-breaking", passed: classifyAgentCardCompatibility({ skills: [{ id: "a" }, { id: "b" }] }, { skills: [{ id: "a" }] }) === "breaking" }
];
const report = {
  report_type: "arpa-typescript-a2a-adapter-report",
  arpa_baseline: "0.9.4",
  implementation_version: "0.3.0",
  checks,
  summary: { total: checks.length, passed: checks.filter((c) => c.passed).length, failed: checks.filter((c) => !c.passed).length },
  assurance_boundary: "A2A publication and compatibility helpers preserve ARPA non-implication rules; they do not establish authority, capability verification or governance recognition."
};
const out = path.join(repositoryRoot, "artifacts/typescript/a2a-adapter-report.json");
fs.mkdirSync(path.dirname(out), { recursive: true }); fs.writeFileSync(out, JSON.stringify(report, null, 2) + "\n");
console.log(`TypeScript A2A adapter checks: ${report.summary.passed}/${report.summary.total} passed`);
if (report.summary.failed) process.exitCode = 1;
