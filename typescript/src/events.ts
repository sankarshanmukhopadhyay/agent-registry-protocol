export interface ArpaEvent {
  event_id: string;
  event_type: string;
  subject: string;
  sequence: number;
  occurred_at: string;
  effective_at: string;
  issuer: string;
  reason_code: string;
  record_refs?: string[];
  proof?: Record<string, unknown>;
}

export interface EventContinuityResult {
  contiguous: boolean;
  reasonCodes: string[];
  checkpoint: number | null;
}

/** Verify ordered event continuity without treating presence of an event as proof of authority. */
export function verifyEventContinuity(events: ArpaEvent[]): EventContinuityResult {
  if (events.length === 0) return { contiguous: true, reasonCodes: ["empty_event_stream"], checkpoint: null };
  const ordered = [...events].sort((a, b) => a.sequence - b.sequence);
  const reasons: string[] = [];
  const first = ordered[0]!;
  for (let index = 1; index < ordered.length; index += 1) {
    const current = ordered[index]!;
    const previous = ordered[index - 1]!;
    if (current.subject !== first.subject) reasons.push("mixed_subject_event_stream");
    if (current.sequence !== previous.sequence + 1) reasons.push("event_sequence_gap");
    if (Date.parse(current.occurred_at) < Date.parse(previous.occurred_at)) reasons.push("event_occurrence_time_regression");
  }
  return {
    contiguous: reasons.length === 0,
    reasonCodes: reasons.length ? [...new Set(reasons)] : ["event_stream_contiguous"],
    checkpoint: ordered[ordered.length - 1]!.sequence
  };
}
