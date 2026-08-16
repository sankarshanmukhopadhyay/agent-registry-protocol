import type { AuthorityDecision, AuthorityEvaluationInput, Decision } from "./types.js";

const ACTIVE_REGISTRATION = new Set(["active", "restricted"]);
const BLOCKING_OPERATION = new Set(["maintenance", "offline", "draining", "quarantined", "unknown"]);
const BLOCKING_SECURITY = new Set([
  "suspected_compromise", "confirmed_compromise", "containment_in_progress",
  "recovery_in_progress", "under_investigation", "unknown"
]);

const parseTime = (value: string): number => {
  const parsed = Date.parse(value);
  if (Number.isNaN(parsed)) throw new Error(`Invalid RFC3339 timestamp: ${value}`);
  return parsed;
};

/**
 * Independent TypeScript interpretation of the pure decision semantics exercised by
 * ARPA §28.2 conformance vectors. It intentionally does not copy Python control flow.
 */
export function evaluateAuthority(input: AuthorityEvaluationInput): Decision<AuthorityDecision> {
  if (input.profile === "A") {
    return { outcome: "not_applicable", reasonCodes: ["profile_a_discovery_only_no_authority_evaluation"] };
  }

  const status = input.agent_status;
  if (!status) return { outcome: "indeterminate", reasonCodes: ["missing_status_record"] };

  const request = input.request;
  const requestAt = parseTime(request.time);

  if (!ACTIVE_REGISTRATION.has(status.registration)) {
    return { outcome: "deny", reasonCodes: [`registration_status_${status.registration}_does_not_permit_action`] };
  }
  if (BLOCKING_OPERATION.has(status.operation)) {
    return { outcome: "deny", reasonCodes: [`operational_status_${status.operation}_blocks_execution`] };
  }
  if (BLOCKING_SECURITY.has(status.security)) {
    return { outcome: "deny", reasonCodes: [`security_status_${status.security}_blocks_execution`] };
  }

  const observedAt = parseTime(status.observed_at);
  const validUntil = parseTime(status.valid_until);
  if (requestAt > validUntil) {
    return { outcome: "indeterminate", reasonCodes: ["status_stale_past_valid_until"] };
  }
  const maxAge = request.policy_max_status_age_seconds;
  if (maxAge !== undefined && requestAt - observedAt > maxAge * 1000) {
    return { outcome: "indeterminate", reasonCodes: ["status_older_than_policy_max_age"] };
  }

  const envelope = input.authority_envelope;
  if (!envelope) return { outcome: "deny", reasonCodes: ["no_applicable_authority_envelope"] };

  if (requestAt < parseTime(envelope.effective_from)) {
    return { outcome: "deny", reasonCodes: ["authority_not_yet_effective"] };
  }
  if (envelope.effective_until && requestAt > parseTime(envelope.effective_until)) {
    return { outcome: "deny", reasonCodes: ["authority_expired"] };
  }

  if (!(envelope.action_classes ?? []).includes(request.action)) {
    return { outcome: "deny", reasonCodes: ["action_not_within_authority_scope"] };
  }
  if (envelope.resource_scope?.length && !envelope.resource_scope.includes(request.resource ?? "")) {
    return { outcome: "deny", reasonCodes: ["resource_not_within_authority_scope"] };
  }
  if (envelope.jurisdiction_scope?.length && !envelope.jurisdiction_scope.includes(request.jurisdiction ?? "")) {
    return { outcome: "deny", reasonCodes: ["jurisdiction_not_within_authority_scope"] };
  }
  if ((envelope.prohibitions ?? []).includes(request.action)) {
    return { outcome: "deny", reasonCodes: ["action_matches_mandatory_prohibition"] };
  }

  if (request.amount !== undefined) {
    const perTransaction = envelope.limits?.per_transaction;
    const aggregate = envelope.limits?.aggregate;
    if (perTransaction !== undefined && request.amount > perTransaction) {
      return { outcome: "deny", reasonCodes: ["amount_exceeds_per_transaction_limit"] };
    }
    if (aggregate !== undefined && request.amount > aggregate) {
      return { outcome: "deny", reasonCodes: ["amount_exceeds_aggregate_limit"] };
    }
  }

  const approvals = (envelope.required_approvals ?? []).filter((approval) => {
    const match = /^amount\s*>\s*(\d+(?:\.\d+)?)$/.exec(approval.condition);
    return match && request.amount !== undefined && request.amount > Number(match[1]);
  });
  if (approvals.length > 0) {
    return { outcome: "allow_with_conditions", reasonCodes: ["within_scope", "approval_required"] };
  }

  return { outcome: "allow", reasonCodes: ["within_scope"] };
}
