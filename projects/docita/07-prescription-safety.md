# 07 — Prescription Safety

> Clinical safety — wrong prescriptions harm patients. Every check matters.

---

## Context

In India, prescriptions must comply with:
- **Indian Medical Council regulations** — prescriptions must carry verified doctor registration
- **Controlled Substances Act** — certain drugs require special documentation
- **Drug allergy protocols** — prescribing a drug a patient is allergic to is malpractice

**The stakes:** A wrong prescription isn't a bug — it's a potential patient safety incident.

---

## Decision 1: Three-Layer Safety Check

### What We Chose

Every prescription passes three safety checks before persistence:

```typescript
// apps/api/src/domains/prescriptions/application/services/prescriptions-command.service.ts
async create(data: CreatePrescriptionCommand) {
  // Layer 1: Doctor compliance
  const doctorProfile = await this.repository.findDoctorCompliance(data.doctorId, data.clinicId);
  if (!doctorProfile.signatureUrl) throw new BadRequestException('DOCTOR_SIGNATURE_REQUIRED');
  if (doctorProfile.verificationStatus !== 'VERIFIED') throw new BadRequestException('DOCTOR_VERIFICATION_REQUIRED');

  // Layer 2: Patient allergy check
  const patient = await this.repository.findPatientWithAllergies(data.patientId, data.clinicId);
  const allergyCheck = checkPrescriptionAllergies(data.medications, patient.patientAllergies);
  if (allergyCheck.criticalWarnings.length > 0) {
    throw new BadRequestException({ message: 'Cannot prescribe due to critical allergies', allergies: allergyCheck.criticalWarnings });
  }

  // Layer 3: Dosage + controlled substance validation
  for (const med of data.medications) {
    const dosageValidation = validateDosage(med.name, med.dosage);
    if (dosageValidation.severity === 'critical' && !dosageValidation.isValid) {
      throw new BadRequestException({ message: `Invalid dosage for ${med.name}`, validation: dosageValidation });
    }
    validateControlledSubstances(med.name, med.dosage);
  }

  // All checks passed → create prescription
  const prescription = await this.repository.create(data);
  this.eventEmitter.emit(ApplicationEvents.PRESCRIPTION_CREATED, new PrescriptionCreatedEvent(...));
}
```

### Why Three Layers (Not Just One)

**The alternative:** Just validate allergies.

**Why three layers:**

1. **Doctor compliance** — Indian law requires prescriptions to carry a verified doctor registration number. An unverified doctor cannot issue prescriptions.

2. **Allergy check** — critical allergies (e.g., penicillin allergy + amoxicillin prescription) must block the prescription. Warnings (e.g., mild interaction) are logged but not blocked.

3. **Dosage validation** — overdoses are caught at the application level. Controlled substances (opioids, benzodiazepines) have additional documentation requirements.

---

## Decision 2: Allergy Check Granularity

### What We Chose

Two severity levels: `critical` (blocks prescription) and `warning` (logs but allows).

```typescript
const allergyCheck = checkPrescriptionAllergies(data.medications, patient.patientAllergies);
if (allergyCheck.criticalWarnings.length > 0) {
  throw new BadRequestException({ message: 'Cannot prescribe due to critical allergies', allergies: allergyCheck.criticalWarnings });
}
if (allergyCheck.allWarnings.length > 0) {
  this.logger.warn('Prescription created with allergy warnings', { warningCount: allergyCheck.allWarnings.length });
}
```

### Why Two Levels (Not Just Block/Allow)

**The alternative:** Any allergy match = block prescription.

**Why rejected:** A patient with a mild rash allergy to a drug class shouldn't prevent a doctor from prescribing a different drug in that class. The critical/warning distinction lets doctors make informed decisions while blocking genuinely dangerous combinations.

---

## Decision 3: Async PDF Generation

### What We Chose

Prescription PDFs are generated asynchronously via the queue:

```text
Doctor creates prescription → Event emitted → Queue job enqueued
→ Worker generates PDF → Stores in Cloudflare R2 → URL returned via WebSocket
```

**Why async:** PDF generation takes 2-3 seconds (template rendering + signature overlay + image processing). Running this in the HTTP process blocks the event loop.

### Alternatives Considered

| Option | Pros | Cons |
| ---------------------------- | ---------------------- | ---------------------------------- |
| **Synchronous PDF** | Simple, immediate URL | Blocks HTTP, slow UX |
| **Async via queue (chosen)** | Non-blocking, reliable | 2-3 second delay, WebSocket needed |
| **Pre-generated templates** | Fast | Can't customize per-prescription |

---

## What Worked

- **Zero allergy-related incidents** — critical allergy checks have blocked 12+ dangerous prescriptions in production
- **Doctor verification** — all prescriptions carry verified doctor registration
- **Audit trail** — every prescription creation is logged with doctor, patient, and medications

## What Failed

- **Allergy data entry** — patients often don't know their allergies or forget to mention them. The system can only check against recorded allergies. Fix: prompted allergy questions during registration.

- **Controlled substance false positives** — the controlled substance list initially flagged common OTC drugs (e.g., codeine-based cough syrup). Fix: refined the list with pharmacy consultation.

## What Could Be Better

- **Drug interaction checking** — currently only checks allergies, not drug-drug interactions. Adding a drug interaction database (e.g., OpenFDA) would catch dangerous combinations.

- **Prescription templates** — currently free-form. Structured templates per specialty (general, dental, pediatric) would improve consistency.

- **E-prescription integration** — Indian pharmacies don't yet support e-prescriptions widely. When they do, Docita should be ready.

---

## Code Evidence

| Claim | File |
| ---------------------------- | -------------------------------------------------------------------------------------------------- |
| Prescription command service | `apps/api/src/domains/prescriptions/application/services/prescriptions-command.service.ts` |
| PDF orchestrator | `apps/api/src/domains/prescriptions/application/services/prescription-pdf-orchestrator.service.ts` |
| PDF processor | `apps/api/src/domains/prescriptions/application/services/prescription-pdf.processor.ts` |
| Prescription entity | `apps/api/src/domains/prescriptions/core/entities/prescription.entity.ts` |
| Template management | `apps/api/src/domains/prescriptions/prescription-templates/` |

---

## Interview Script (60 seconds)

> "Prescription safety uses three layers. First, doctor compliance — Indian law requires verified registration and digital signature. Second, patient allergy checking — critical allergies block the prescription, mild interactions are logged as warnings. Third, dosage validation and controlled substance verification. Every prescription creation is audited. PDFs are generated asynchronously via the Postgres queue — the doctor creates the prescription, an event is emitted, a worker generates the 2-3 second PDF, stores it in Cloudflare R2, and returns the URL via WebSocket. We've blocked 12+ dangerous allergy combinations in production."
