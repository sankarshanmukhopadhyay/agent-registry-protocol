export class ArpaClient {
  constructor(readonly baseUrl: string) {}

  private async request(path: string, init?: RequestInit): Promise<any> {
    const response = await fetch(`${this.baseUrl.replace(/\/$/, "")}${path}`, {
      ...init,
      headers: { "content-type": "application/json", ...(init?.headers ?? {}) }
    });
    const body = await response.json();
    if (!response.ok) throw new Error(`ARPA ${response.status}: ${JSON.stringify(body)}`);
    return body;
  }

  health(): Promise<any> { return this.request("/health"); }
  registry(): Promise<any> { return this.request("/registry"); }
  listAgents(): Promise<any> { return this.request("/agents"); }
  resolveAgent(agentId: string, at?: string): Promise<any> {
    return this.request(`/agents/${encodeURIComponent(agentId)}${at ? `?at=${encodeURIComponent(at)}` : ""}`);
  }
  historicalResolution(agentId: string, at: string): Promise<any> {
    return this.request(`/agents/${encodeURIComponent(agentId)}/historical-resolution?at=${encodeURIComponent(at)}`);
  }
  registerAgent(record: Record<string, unknown>): Promise<any> {
    return this.request("/agents", { method: "POST", body: JSON.stringify(record) });
  }
  putRecord(record: Record<string, unknown>): Promise<any> {
    return this.request("/records", { method: "POST", body: JSON.stringify(record) });
  }
  evaluateAuthority(payload: Record<string, unknown>): Promise<any> {
    return this.request("/authority/evaluate", { method: "POST", body: JSON.stringify(payload) });
  }
}
