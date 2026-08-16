export interface AgentDescriptionReference {
  record_id: string;
  subject: string;
  uri: string;
  digest: string;
  disclosure_class?: string;
  representation_version?: string | null;
  protocol_versions?: string[];
  retrieved_at?: string;
  valid_until?: string | null;
}

export interface AgentCoreRecord {
  record_id: string;
  agent_id?: string;
  subject?: string;
  status?: string;
  issuer?: string;
}

export interface A2APublicationProjection {
  publication_id: string;
  agent_id: string;
  agent_card_uri: string;
  card_digest: string;
  representation_version?: string | null;
  observed_at?: string;
  valid_until?: string | null;
  disclosure_class: string;
  lifecycle_status: string;
  publisher?: string;
  protocol_versions: string[];
  skills: string[];
  capabilities: string[];
  authority_implication: false;
  source_record_ids: string[];
}

/** Build the registry publication layer without embedding caller-specific authority. */
export function createA2APublicationProjection(core: AgentCoreRecord, ref: AgentDescriptionReference): A2APublicationProjection {
  const agentId = core.agent_id ?? core.subject;
  if (!agentId) throw new Error("Agent core record does not identify an agent");
  return {
    publication_id: ref.record_id,
    agent_id: agentId,
    agent_card_uri: ref.uri,
    card_digest: ref.digest,
    ...(ref.representation_version !== undefined ? { representation_version: ref.representation_version } : {}),
    ...(ref.retrieved_at !== undefined ? { observed_at: ref.retrieved_at } : {}),
    ...(ref.valid_until !== undefined ? { valid_until: ref.valid_until } : {}),
    disclosure_class: ref.disclosure_class ?? "public",
    lifecycle_status: core.status ?? "active",
    ...(core.issuer !== undefined ? { publisher: core.issuer } : {}),
    protocol_versions: ref.protocol_versions ?? [],
    skills: [],
    capabilities: [],
    authority_implication: false,
    source_record_ids: [core.record_id, ref.record_id]
  };
}

export interface AgentCardSummary {
  skills?: Array<{ id?: string; name?: string }>;
  capabilities?: Record<string, boolean>;
  supportedInterfaces?: string[];
}

export type Compatibility = "compatible" | "breaking" | "indeterminate";

/** Conservative compatibility classification for publication change management. */
export function classifyAgentCardCompatibility(previous: AgentCardSummary | null, next: AgentCardSummary | null): Compatibility {
  if (!previous || !next) return "indeterminate";
  const oldSkills = new Set((previous.skills ?? []).map((s) => s.id ?? s.name).filter(Boolean));
  const newSkills = new Set((next.skills ?? []).map((s) => s.id ?? s.name).filter(Boolean));
  for (const skill of oldSkills) if (!newSkills.has(skill)) return "breaking";

  const oldInterfaces = new Set(previous.supportedInterfaces ?? []);
  const newInterfaces = new Set(next.supportedInterfaces ?? []);
  for (const iface of oldInterfaces) if (!newInterfaces.has(iface)) return "breaking";

  for (const [name, enabled] of Object.entries(previous.capabilities ?? {})) {
    if (enabled && next.capabilities?.[name] === false) return "breaking";
  }
  return "compatible";
}
