import type { Decision, IdentifierResolutionInput, ResolutionOutcome } from "./types.js";

/** Independent implementation of the observable identifier-resolution outcomes in ARPA §12.6. */
export function resolveIdentifier(input: IdentifierResolutionInput): Decision<ResolutionOutcome> {
  const known = input.known ?? false;
  const terminal = input.terminal ?? false;
  const authorized = input.authorized_caller ?? true;

  if (!known) return { outcome: "not_found", reasonCodes: ["identifier_never_issued"] };
  if (!authorized) return { outcome: "not_authorized", reasonCodes: ["caller_not_authorized_for_record"] };
  if (terminal) return { outcome: "terminal_record", reasonCodes: ["identifier_known_but_terminal"] };
  return { outcome: "active_record", reasonCodes: ["identifier_known_and_active"] };
}
