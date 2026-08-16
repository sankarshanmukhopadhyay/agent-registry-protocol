export type Profile = "A" | "B" | "C" | "D";
export type ResolutionOutcome = "active_record" | "terminal_record" | "not_found" | "not_authorized";
export type AuthorityDecision = "allow" | "allow_with_conditions" | "deny" | "indeterminate" | "not_applicable";

export interface Decision<T extends string> {
  outcome: T;
  reasonCodes: string[];
}

export interface IdentifierResolutionInput {
  known?: boolean;
  terminal?: boolean;
  authorized_caller?: boolean;
}

export interface AgentStatus {
  registration: string;
  operation: string;
  security: string;
  observed_at: string;
  valid_until: string;
}

export interface RequiredApproval {
  condition: string;
  approval: string;
}

export interface AuthorityEnvelope {
  effective_from: string;
  effective_until?: string | null;
  action_classes?: string[];
  resource_scope?: string[];
  jurisdiction_scope?: string[];
  prohibitions?: string[];
  required_approvals?: RequiredApproval[];
  limits?: Record<string, number>;
}

export interface AuthorityRequest {
  action: string;
  resource?: string;
  jurisdiction?: string;
  amount?: number;
  time: string;
  policy_max_status_age_seconds?: number;
}

export interface AuthorityEvaluationInput {
  profile: Profile;
  agent_status?: AgentStatus | null;
  authority_envelope?: AuthorityEnvelope | null;
  request: AuthorityRequest;
}
