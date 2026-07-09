# Security and Clinical Safety

This repository is a portfolio and research demonstration. It is not a medical device and must not be used for real patient care without formal validation and clinical governance.

## Data Handling

- Do not commit patient data, PHI, secrets, API keys, or private clinical documents.
- `.env`, local vector stores, generated reports, and local data files are ignored by Git.
- The hosted Vercel demo uses built-in synthetic seed documents only.

## Safety Controls

- Responses include citations and a verification object.
- The critic agent flags adverse events, contraindications, and conflicting evidence.
- The adjudicator reports confidence and decision factors.
- Reports include an explicit clinical safety note.

## Production Requirements Before Healthcare Use

- HIPAA/GDPR compliant storage and access control
- PHI redaction and audit logging
- Clinician review workflow
- Model and retrieval evaluation on validated datasets
- Monitoring for drift, latency, failures, and hallucination risk
- Legal, regulatory, and institutional approval
