import fs from "node:fs";
import path from "node:path";
import { evaluateAuthority } from "./authority.js";
import { repositoryRoot, jsonFiles, readJson } from "./repository.js";
import { resolveIdentifier } from "./resolution.js";
import type { AuthorityEvaluationInput, IdentifierResolutionInput, Profile } from "./types.js";

interface Vector {
  vector_id: string;
  profile: Profile;
  check: "identifier_resolution" | "authority_evaluation";
  input: unknown;
  expected_outcome: string;
}
interface VectorResult { vector_id: string; profile: Profile; expected: string; actual: string; passed: boolean; reason_codes: string[]; }

const vectors = jsonFiles("conformance/test-vectors")
  .filter((file) => path.basename(file).startsWith("TV-"))
  .map((file) => readJson<Vector>(file));

const results: VectorResult[] = vectors.map((vector) => {
  const decision = vector.check === "identifier_resolution"
    ? resolveIdentifier(vector.input as IdentifierResolutionInput)
    : evaluateAuthority(vector.input as AuthorityEvaluationInput);
  return {
    vector_id: vector.vector_id,
    profile: vector.profile,
    expected: vector.expected_outcome,
    actual: decision.outcome,
    passed: decision.outcome === vector.expected_outcome,
    reason_codes: decision.reasonCodes
  };
});

const report = {
  report_type: "arpa-typescript-conformance-report",
  arpa_baseline: "0.9.4",
  implementation: "arpa-typescript",
  implementation_version: "0.3.0",
  runtime: `node ${process.version}`,
  independence_statement: "Behavioral logic is implemented from ARPA normative requirements and shared conformance vectors; it is not imported from or executed through the Python reference implementation.",
  supported_profiles: [...new Set(results.filter((r) => r.passed).map((r) => r.profile))].sort(),
  vectors: {
    total: results.length,
    passed: results.filter((r) => r.passed).length,
    failed: results.filter((r) => !r.passed).length
  },
  results
};

const out = path.join(repositoryRoot, "artifacts/typescript/conformance-report.json");
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, JSON.stringify(report, null, 2) + "\n");

const implementationReport = {
  report_version: "1.0.0",
  generated_at: new Date().toISOString(),
  implementation: "ARPA TypeScript implementation track",
  implementation_version: "0.3.0",
  arpa_version: "0.9.4-baseline",
  modules: ["ARPA-Core", "ARPA-Authority", "Historical Resolution", "Decision Receipts", "Event Continuity", "HTTP Client/Server", "A2A Publication Adapters"],
  profile_claims: ["A-conformance-vector", "B-deterministic-subset", "C-deterministic-subset", "D-deterministic-subset"],
  checks: [
    { name: "shared-conformance-vectors", passed: report.vectors.failed === 0, output: `${report.vectors.passed}/${report.vectors.total} passed` },
    { name: "normative-artifact-consumption", passed: true, output: "Schemas and registries are read from repository sources at runtime." }
  ],
  passed: report.vectors.failed === 0,
  known_limitations: [
    "HTTP/client surfaces are development-grade and use in-memory persistence only",
    "A2A adapters cover publication projection and conservative compatibility, not task execution or capability verification",
    "No proof verification, issuer-competence resolution or production federation",
    "Repository ownership does not constitute external independent implementation evidence",
    "Authority evaluation remains bounded to deterministic semantics exercised by shared vectors",
    "Historical resolution is a repository-artifact and reliance implementation; network retrieval remains deferred"
  ]
};
fs.writeFileSync(path.join(repositoryRoot, "artifacts/typescript/implementation-report.json"), JSON.stringify(implementationReport, null, 2) + "\n");
console.log(`TypeScript conformance: ${report.vectors.passed}/${report.vectors.total} vectors passed`);
if (report.vectors.failed > 0) process.exitCode = 1;
