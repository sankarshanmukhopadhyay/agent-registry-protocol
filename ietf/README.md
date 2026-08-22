# ARPA IETF Internet-Draft Track

This directory is the IETF authoring surface for the **Agent Registry Protocol**.
It is deliberately separate from `spec/agent-registry-protocol-v0.9.0.md`.

## Draft identity

Initial individual draft:

`draft-sankarshan-agent-registry-protocol-00`

The IETF draft revision is independent of ARPA project semantic versions. A future
working-group adoption would normally create a new `draft-ietf-<wg>-...-00`
series rather than continuing the individual-draft revision number.

## Authority and scope

The ARPA Candidate Specification remains the project-level specification and
source architecture. The Internet-Draft extracts the interoperable protocol core:

- identifiers and registry resources;
- typed relationships;
- bounded delegated authority;
- lifecycle and status;
- registration and resolution;
- point-in-time resolution;
- event semantics;
- HTTP processing and errors;
- versioning/extensibility;
- security and privacy considerations; and
- prospective IANA actions.

Project governance, conformance programmes, A2A/TRQP profiles, deployment
guidance, and assurance evidence remain supporting ARPA artifacts unless later
standardized separately.

## Legal status

Files under `ietf/` are prepared as prospective **IETF Contributions**. Submission
to the IETF is governed by the IETF Trust Legal Provisions and applicable BCP 78
terms. This does not change the artifact-specific licensing of the existing ARPA
project specification, code, schemas, test vectors, or documentation.

Do not add a separate CC BY 4.0 notice to the Internet-Draft body.

## Build

Install the IETF authoring dependencies:

```bash
make ietf-setup
```

Build RFCXML v3, plaintext, and HTML:

```bash
make ietf-build
```

Validate the source and generated RFCXML:

```bash
make ietf-check
```

Generated files are written to `ietf/generated/`.

## Generated artifact policy

`ietf/draft-sankarshan-agent-registry-protocol.md` is the checked-in authoring
source. The RFCXML v3, plaintext, HTML, and any derived PDF are deterministic
build products and remain excluded from Git by `ietf/.gitignore`.

GitHub Actions owns generation and publication of the submission renderings:

1. the dedicated IETF workflow runs `make ietf-check` and retains XML, TXT, and
   HTML as an Actions artifact for CI inspection;
2. the GitHub Pages workflow independently runs the same IETF validation gate;
3. a successful Pages build publishes XML, TXT, HTML, and SHA-256 checksums under
   `/ietf/generated/`;
4. the checksum file is also copied into the Pages assurance artifact so the
   published draft outputs can be tied to retained deployment evidence; and
5. a failed IETF build or failed complete-publication validation blocks the Pages
   deployment.

This keeps generated content reproducible and developer-accessible without
allowing generated files to drift as independently committed repository state.
The generated artifacts are publication products, not a separate authority
surface.

## Pre-submission gates

Before submitting `-00` through the IETF Datatracker:

1. populate durable author contact information in the draft metadata;
2. confirm the protocol title and individual-draft name;
3. resolve all `ietf/TODO` markers, if any;
4. make the IANA section concrete or explicitly no-action;
5. complete overlap review against active IETF work, particularly workload identity and OAuth/delegation work;
6. run `make ietf-check` and `make release-check-all`;
7. inspect generated TXT and HTML renderings manually;
8. verify the published SHA-256 checksums against the generated submission files;
9. submit the generated RFCXML v3 artifact; and
10. record the Datatracker URL and submitted revision in this README.

## Version provenance

The initial I-D is derived from the ARPA v0.9.x repository state and the v0.9.0
Candidate Specification baseline, including subsequent candidate-hardening
changes represented by machine-readable normative artifacts. The I-D MUST NOT
silently track a moving `Unreleased` state. Any normative change imported from
ARPA must be reviewed and recorded in the I-D change history before submission.
