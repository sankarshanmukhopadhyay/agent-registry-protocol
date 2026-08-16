import { createHash } from "node:crypto";
import type { AuthorityDecision, AuthorityEvaluationInput, Decision } from "./types.js";

export interface DecisionReceipt {
  record_id: string;
  record_type: "decision_receipt";
  schema_version: string;
  issuer: string;
  subject: string;
  issued_at: string;
  effective_from: string;
  status: string;
  request_digest: string;
  decision: AuthorityDecision;
  evaluated_authority_records: string[];
  evaluated_status_records: string[];
  evaluated_policy_version?: string;
  conditions?: string[];
  evaluation_time: string;
  validity_duration_seconds?: number;
  evaluator_identity: string;
  reason_codes: string[];
  evidence: string[];
  governance: string[];
  supersedes: string[];
}

function canonicalJson(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.entries(value as Record<string, unknown>).sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => `${JSON.stringify(k)}:${canonicalJson(v)}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

export function requestDigest(input: AuthorityEvaluationInput): string {
  return `sha256:${createHash("sha256").update(canonicalJson(input.request)).digest("hex")}`;
}

export function createDecisionReceipt(args: {
  input: AuthorityEvaluationInput;
  decision: Decision<AuthorityDecision>;
  subject: string;
  evaluatorIdentity: string;
  authorityRecordIds: string[];
  statusRecordIds?: string[];
  policyVersion?: string;
  validityDurationSeconds?: number;
  evidence?: string[];
  governance?: string[];
}): DecisionReceipt {
  if (args.authorityRecordIds.length === 0) throw new Error("Decision receipts require at least one evaluated authority record");
  const evaluationTime = args.input.request.time;
  const digest = requestDigest(args.input);
  const conditions = args.decision.outcome === "allow_with_conditions" ? ["approval_required"] : undefined;
  const receipt: DecisionReceipt = {
    record_id: `decision:${digest.slice(7, 23)}:${Date.parse(evaluationTime)}`,
    record_type: "decision_receipt",
    schema_version: "1.0.0",
    issuer: args.evaluatorIdentity,
    subject: args.subject,
    issued_at: evaluationTime,
    effective_from: evaluationTime,
    status: "active",
    request_digest: digest,
    decision: args.decision.outcome,
    evaluated_authority_records: args.authorityRecordIds,
    evaluated_status_records: args.statusRecordIds ?? [],
    evaluation_time: evaluationTime,
    evaluator_identity: args.evaluatorIdentity,
    reason_codes: [...args.decision.reasonCodes],
    evidence: args.evidence ?? [],
    governance: args.governance ?? [],
    supersedes: []
  };
  if (args.policyVersion !== undefined) receipt.evaluated_policy_version = args.policyVersion;
  if (conditions !== undefined) receipt.conditions = conditions;
  if (args.validityDurationSeconds !== undefined) receipt.validity_duration_seconds = args.validityDurationSeconds;
  return receipt;
}
