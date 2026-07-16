# Migration from v0.5.0 to v0.9.0

v0.9.0 preserves the v0.5.0 record-schema track and adds Candidate Specification requirements, durable event expectations, implementation capability declarations, evidence reports and an optional ARPA–TRQP projection profile.

Implementers should update release metadata to `0.9.0`, publish a capability declaration, validate event replay and idempotency, retain enforcement acknowledgements for suspension and revocation, and declare TRQP projection support separately. Mixed-version federation must treat unsupported candidate capabilities as unavailable, never affirmative.
