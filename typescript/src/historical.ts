import type { Decision } from "./types.js";

export type ReconstructionStatus =
  | "authoritative_complete"
  | "authoritative_partial"
  | "reconstructed_complete"
  | "reconstructed_partial"
  | "indeterminate";

export type HistoricalEffect = "none" | "prospective" | "retroactive" | "governance_defined" | "indeterminate";

export interface EffectiveRecord {
  record_id: string;
  version?: string;
  effective_from: string;
  effective_until?: string | null;
  digest?: string;
  [key: string]: unknown;
}

export interface HistoricalEvidence {
  references: string[];
  integrity_status: "verified" | "partial" | "failed" | "not_available" | string;
  lineage_mechanism?: string | null;
}

export interface HistoricalResolutionDocument {
  subject: string;
  requested_time: string;
  evaluation_time: string;
  state_at_requested_time: Record<string, unknown>;
  current_state: Record<string, unknown>;
  reconstruction_status: ReconstructionStatus;
  selected_records: EffectiveRecord[];
  event_checkpoint?: string | null;
  later_material_events: Array<{ historical_effect?: HistoricalEffect; effective_at?: string; [key: string]: unknown }>;
  historical_effect: HistoricalEffect;
  retention: { evidence_available: boolean; status: string; boundary?: string | null };
  evidence: HistoricalEvidence;
  warnings: string[];
}

export interface HistoricalAssessment {
  usable: boolean;
  reconstructionStatus: ReconstructionStatus;
  historicalEffect: HistoricalEffect;
  stateAtRequestedTime?: Record<string, unknown>;
}

const parseTime = (value: string): number => {
  const parsed = Date.parse(value);
  if (Number.isNaN(parsed)) throw new Error(`Invalid RFC3339 timestamp: ${value}`);
  return parsed;
};

/** Select effective records at a requested time without substituting current state. */
export function selectEffectiveRecords(records: EffectiveRecord[], at: string): EffectiveRecord[] {
  const requested = parseTime(at);
  return records
    .filter((record) => {
      const from = parseTime(record.effective_from);
      const until = record.effective_until == null ? Number.POSITIVE_INFINITY : parseTime(record.effective_until);
      return from <= requested && requested < until;
    })
    .sort((a, b) => parseTime(a.effective_from) - parseTime(b.effective_from));
}

/**
 * Evaluate whether a historical-resolution response is safe to rely on.
 * This independently enforces ARPA v0.9.4 fail-closed historical invariants.
 */
export function assessHistoricalResolution(document: HistoricalResolutionDocument): Decision<"usable" | "indeterminate"> & HistoricalAssessment {
  const requested = parseTime(document.requested_time);
  const evaluated = parseTime(document.evaluation_time);
  if (requested > evaluated) {
    return {
      outcome: "indeterminate", usable: false,
      reconstructionStatus: "indeterminate", historicalEffect: "indeterminate",
      reasonCodes: ["requested_time_after_evaluation_time"]
    };
  }

  if (document.retention.status === "outside_retention" || !document.retention.evidence_available) {
    return {
      outcome: "indeterminate", usable: false,
      reconstructionStatus: "indeterminate", historicalEffect: "indeterminate",
      reasonCodes: ["historical_evidence_outside_retention"]
    };
  }

  if (document.evidence.integrity_status === "failed" || document.evidence.integrity_status === "not_available") {
    return {
      outcome: "indeterminate", usable: false,
      reconstructionStatus: "indeterminate", historicalEffect: "indeterminate",
      reasonCodes: ["historical_evidence_integrity_unusable"]
    };
  }

  if (document.reconstruction_status === "indeterminate" || document.historical_effect === "indeterminate") {
    return {
      outcome: "indeterminate", usable: false,
      reconstructionStatus: document.reconstruction_status,
      historicalEffect: document.historical_effect,
      reasonCodes: ["historical_reconstruction_indeterminate"]
    };
  }

  if (requested < evaluated && Object.is(document.state_at_requested_time, document.current_state)) {
    return {
      outcome: "indeterminate", usable: false,
      reconstructionStatus: "indeterminate", historicalEffect: "indeterminate",
      reasonCodes: ["current_state_substituted_for_historical_state"]
    };
  }

  return {
    outcome: "usable", usable: true,
    reconstructionStatus: document.reconstruction_status,
    historicalEffect: document.historical_effect,
    stateAtRequestedTime: document.state_at_requested_time,
    reasonCodes: ["historical_state_reconstructed_with_qualified_evidence"]
  };
}
