# CIANDLITHE — Demo Paths

> **Per the locked plan** — all 3 demo paths (self-rep claimant / WRC claimant / HSE-NHS complainant / PIAB applicant / coroner / inquest / legal-aid applicant) plus the law-clinic analyst path (cloud) and the developer path (local dev).

> **Companion docs:** [`USAGE-GUIDELINES.md`](USAGE-GUIDELINES.md) + [`DEPLOYMENT.md`](DEPLOYMENT.md) + [`HOW-BRITISH-ISLES-LITIGATION-ENTITIES-USE-CIANDLITHE.md`](HOW-BRITISH-ISLES-LITIGATION-ENTITIES-USE-CIANDLITHE.md) + [`case-study/composite-pilot.md`](case-study/composite-pilot.md) + [`source-catalogue/blip-v1-sources.md`](source-catalogue/blip-v1-sources.md) + [`configuration-surface.md`](configuration-surface.md).

> **Licence:** BUSL-1.1 v2 — CIANDLITHE edition (per `LICENSE.md`)

---

## Quick orientation

The ciandlithe platform serves **7 distinct user personas**es with **2 different deployment footprints**:

| Persona | Deployment footprint | Demo duration | Primary value |
|---|---|---|---|
| **Self-rep claimant** | Self-hosted Docker Compose bundle | 5 minutes | Conversational agent for non-emergency form preparation |
| **WRC / ET claimant** | Self-hosted Docker Compose bundle | 5 minutes | WRC complaint drafting + hearing-day checklists |
| **HSE / NHS complainant** | Self-hosted Docker Compose bundle | 5 minutes | HSE / NHS complaint drafting + clinical-incident navigation |
| **PIAB applicant** | Self-hosted Docker Compose bundle | 5 minutes | PIAB form + book of documents + medical report collation |
| **Coroner's court applicant** | Self-hosted Docker Compose bundle | 5 minutes | Notification of death + post-mortem request + inquest witness prep |
| **Inquest counsel** | Cloud deployment at `*.ciandlithe.ie` | 30 minutes | Article 2 ECHR framing + disclosure requests + interested-party status |
| **Legal-aid applicant** | Self-hosted Docker Compose bundle | 5 minutes | Legal Aid Board / Agency / SLAB / NILSC eligibility + form drafting |

Each demo path is **staged** so a fresh user can progress through them at their own pace.

---

## Demo path 1 — Self-rep claimant (5-minute quickstart)

### Who
A natural person of the British Isles who wants to represent themselves in a civil case (Circuit / District / High Court). NOT a foreign entity. NOT a private-sector commercial user.

### Prerequisites
- A Docker-compatible machine (MacBook / Linux / Windows-with-WSL2)
- At least 8 GB RAM (the self-hosted bundle runs Unsloth Studio + Crawl4AI + Stagehand + Locket + LiteLLM locally)
- An Internet connection (to pull the Docker images + to access the public OSINT sources)

### Steps

#### 0:00–0:30 — Clone the bundle
```bash
git clone https://github.com/cianfhoghlaim/ciandlithe
cd ciandlithe/web/apps/ciandlithe-self-rep
```

#### 0:30–2:00 — Boot the self-hosted bundle
```bash
docker compose up -d
# 5 containers spin up: unsloth-serve + litellm + locket + crawl4ai + stagehand
```

#### 2:00–3:00 — Open the per-persona web app
```bash
open http://localhost:7777
```

#### 3:00–5:00 — Ask the canonical self-rep question
> "I was misprescribed olanzapine in a Galway hospital and now I have brain damage. The HSE won't give me my medical records. What can I do?"

The platform will:
1. Classify the complaint into the `medical_malpractice` cohort (Ireland jurisdiction) via `dlt_sources/ciandlithe/cross/complaint_classifier.py`
2. Load the QUB/RVH + sodium valproate case-study leabharlann PDFs as read-only context
3. Generate a 3-step action plan: (i) Submit a data-access request under the GDPR / Data Protection Acts, (ii) File a Statement of Claim in the Circuit Court, (iii) Refer the matter to the Medical Council
4. Provide the relevant court forms (CC1, HC1), the relevant statutes (Civil Liability Act 1961 §s.9, Data Protection Acts 1988-2018), and the relevant precedents (case-law citations)
5. Generate a dossier (PDF + JSON) for manual review by the claimant or their solicitor

**The platform NEVER directly submits any form.** Per `LICENSE.md §3.8`.

---

## Demo path 2 — WRC / ET claimant (5-minute quickstart)

### Who
A natural person of the British Isles who has a workplace-relations complaint (Ireland: WRC; UK: Employment Tribunal). Wants to file a complaint + prepare for a hearing.

### Steps

#### 0:00–0:30 — Clone + boot
```bash
git clone https://github.com/cianfhoghlaim/ciandlithe
cd ciandlithe/web/apps/ciandlithe-wrc
docker compose up -d
open http://localhost:7778
```

#### 0:30–5:00 — Ask the canonical WRC question
> "I was unfairly dismissed from my job at a Monroes restaurant in Galway after I complained about a breach of contract by the CEO. I have WhatsApp evidence. What can I do?"

The platform will:
1. Classify into `EmployerBreach` cohort (ROI jurisdiction)
2. Load the Eric-case + cross-border legal-action leabharlann PDFs as read-only context
3. Generate a 3-step action plan: (i) Submit a WRC complaint within the 6-month time limit, (ii) Compile the WhatsApp evidence into a book of documents, (iii) Prepare a witness statement
4. Provide the relevant WRC complaint form, the relevant statutes (Workplace Relations Act 2015, Unfair Dismissals Acts 1977-2007), and the relevant precedents
5. Generate a dossier (PDF + JSON) for manual review

---

## Demo path 3 — HSE / NHS complainant (5-minute quickstart)

### Who
A natural person of the British Isles who has an HSE / NHS complaint (medical care quality, clinical incident, complaint handling).

### Steps

#### 0:00–0:30 — Clone + boot
```bash
git clone https://github.com/cianfhoghlaim/ciandlithe
cd ciandlithe/web/apps/ciandlithe-health-complain
docker compose up -d
open http://localhost:7779
```

#### 0:30–5:00 — Ask the canonical HSE/NHS question
> "I was misprescribed sodium valproate during pregnancy and my child has neurological damage. What can I do?"

The platform will:
1. Classify into `medical_malpractice` cohort (Ireland jurisdiction)
2. Load the sodium valproate + medical_malpractice_brain_damage_legal_action leabharlann PDFs as read-only context
3. Generate a 3-step action plan: (i) Submit an HSE complaint under §s.49 Health Act 2004, (ii) File a Statement of Claim in the High Court, (iii) Refer to the Medical Council
4. Provide the relevant HSE complaint form, the relevant statutes (Civil Liability Act 1961, Product Liability Act 1991), and the relevant precedents
5. Generate a dossier (PDF + JSON) for manual review

---

## Demo path 4 — PIAB applicant (5-minute quickstart)

### Who
A natural person of the British Isles who has suffered a personal injury and wants to apply to PIAB (Personal Injuries Assessment Board).

### Steps
Similar to demo path 1. The platform classifies into the `personal_injury_piab_nhs` cohort and generates the PIAB application form + book of documents + medical report collation.

---

## Demo path 5 — Coroner's court applicant (5-minute quickstart)

### Who
A family member of a deceased person in Ireland who wants to apply to the Coroner's Court for an inquest.

### Steps
Similar to demo path 1. The platform classifies into the `court_judgments_tribunal_decisions` cohort and generates the notification of death + post-mortem request + inquest witness preparation.

---

## Demo path 6 — Inquest counsel (30-minute)

### Who
A solicitor or barrister preparing for an inquest (article 2 ECHR framing, disclosure requests, interested-party status).

### Steps

#### 0:00–2:00 — Clone + boot
```bash
git clone https://github.com/cianfhoghlaim/ciandlithe
cd ciandlithe
mise run core  # full bootstrap
```

#### 2:00–5:00 — Open the per-persona web app
```bash
open http://localhost:3000/inquest
```

#### 5:00–30:00 — Use the full pipeline
- Cross-reference all 7 BLIP v1 cohorts via the AG-UI chat window
- Generate the article 2 ECHR framing memo
- Prepare the disclosure requests list
- Submit the interested-party status application

---

## Demo path 7 — Legal-aid applicant (5-minute quickstart)

### Who
A natural person of the British Isles who wants to apply for legal aid (Ireland: Legal Aid Board; England & Wales: Legal Aid Agency; Scotland: SLAB; NI: NILSC).

### Steps
Similar to demo path 1. The platform classifies into the `civil_litigation_forms` cohort and generates the legal-aid application form + the supporting financial documentation.

---

## Cross-references

- [`USAGE-GUIDELINES.md`](USAGE-GUIDELINES.md) — operational guidelines
- [`HOW-BRITISH-ISLES-LITIGATION-ENTITIES-USE-CIANDLITHE.md`](HOW-BRITISH-ISLES-LITIGATION-ENTITIES-USE-CIANDLITHE.md) — audience-targeted use guide
- [`DEPLOYMENT.md`](DEPLOYMENT.md) — deployment procedure
- [`case-study/composite-pilot.md`](case-study/composite-pilot.md) — canonical pilot narrative
- [`source-catalogue/blip-v1-sources.md`](source-catalogue/blip-v1-sources.md) — DLT source URL catalogue