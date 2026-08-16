export interface StoredEvent {
  event_id: string;
  event_type: string;
  subject: string;
  sequence: number;
  effective_at: string;
  issued_at: string;
  payload: Record<string, unknown>;
}

export class MemoryStore {
  private records = new Map<string, Record<string, unknown>>();
  private eventsList: StoredEvent[] = [];

  putRecord(record: Record<string, unknown>): void {
    const id = record.record_id;
    if (typeof id !== "string") throw new Error("record_id is required");
    this.records.set(id, structuredClone(record));
  }

  getRecord(id: string): Record<string, unknown> | undefined {
    const record = this.records.get(id);
    return record ? structuredClone(record) : undefined;
  }

  allRecords(): Record<string, unknown>[] {
    return [...this.records.values()].map((r) => structuredClone(r));
  }

  recordsForSubject(subject: string, at?: string): Record<string, unknown>[] {
    const instant = at ? Date.parse(at) : null;
    return this.allRecords().filter((record) => {
      const candidate = record.agent_id ?? record.subject;
      const matches = typeof candidate === "object" && candidate !== null
        ? (candidate as Record<string, unknown>).agent === subject
        : candidate === subject;
      if (!matches) return false;
      if (instant === null) return true;
      const fromValue = record.effective_from ?? record.issued_at;
      if (typeof fromValue !== "string" || Date.parse(fromValue) > instant) return false;
      return typeof record.effective_until !== "string" || instant <= Date.parse(record.effective_until);
    });
  }

  addEvent(event: Omit<StoredEvent, "sequence">): StoredEvent {
    const stored = { ...event, sequence: this.eventsList.length + 1 };
    this.eventsList.push(stored);
    return structuredClone(stored);
  }

  events(subject?: string, after = 0): StoredEvent[] {
    return this.eventsList.filter((e) => e.sequence > after && (!subject || e.subject === subject)).map((e) => structuredClone(e));
  }
}
