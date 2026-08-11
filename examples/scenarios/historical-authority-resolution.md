---
layout: default
title: "Historical authority resolution"
parent: Scenarios
---

# Scenario: historical authority after later revocation

An agent held active procurement authority at 10:00 on 15 July. The authority was revoked on 18 July. On 11 August an auditor asks whether the agent was authorized at the earlier time.

The registry resolves the records and event checkpoint applicable to 15 July, returns the historical state separately from the current revoked state, and discloses the later revocation as a material event. The revocation is marked `prospective` unless the applicable governance framework explicitly gives it retroactive effect.

```text
15 Jul 10:00   authority active     <-- requested time
18 Jul 09:30   authority revoked
11 Aug 08:30   historical query     <-- evaluation time
```

A valid result can therefore state that the authority was active at the requested time while also stating that it is revoked today. The result does **not** decide whether the auditor, court, relying party, or governance process must accept the historical action. That determination applies its own policy to the registry evidence.

This scenario is exercised by the historical conformance vector `HV-01-active-at-T-now-revoked.json`.
