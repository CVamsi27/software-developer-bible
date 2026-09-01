# 06 — WhatsApp Integration

> WhatsApp-first means it must work perfectly — because for many clinics, WhatsApp IS the product.

---

## Context

Docita's core value proposition: a clinic owner in India should be able to run their clinic without opening a browser. WhatsApp is the primary interface for:

- **Appointment reminders** — sent 24h and 1h before
- **Prescription delivery** — PDF sent after consultation
- **Payment confirmations** — receipt sent after payment
- **Follow-up reminders** — scheduled follow-up notifications
- **Patient responses** — patients reply "yes", "no", "delay 30 min"

**The scale:** ~500 WhatsApp messages/day across 25+ clinics.

---

## Decision 1: Three Sender Modes

### What We Chose

| Mode | Description | Cost | Branding |
|------|-------------|------|----------|
| **SHARED** | Meta's shared business number | Free | "via Docita" |
| **BYO** | Clinic's own WhatsApp Business number | Clinic pays Meta | Clinic's name |
| **MANAGED** | Docita-managed number | Docita pays Meta | Docita branding |

**Why three modes:** Indian clinics have different budgets and branding needs. A small clinic might start with SHARED (free) and upgrade to BYO as they grow.

### Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| **Shared only** | Simple, free | No clinic branding, Meta rate limits |
| **BYO only** | Full branding | Setup complexity, clinic must have Meta Business account |
| **Three modes (chosen)** | Flexible, caters to all clinic sizes | More code paths, more testing |

---

## Decision 2: Patient Response Handling

### What We Chose

A response parser that maps free-text WhatsApp replies to appointment actions.

```typescript
// apps/api/src/domains/whatsapp/application/services/response-handler.service.ts
async handlePatientResponseForAppointment(context, responseText, phoneNumber, messageSid) {
  // 1. Parse response type
  const responseType = parsePatientResponse(responseText);  // YES, NO, DELAY, UNKNOWN
  const delayMinutes = extractDelayMinutes(responseText);    // 30, 60, etc.

  // 2. Handle two-step delay flow
  if (pendingDelayResponse && delayMinutes !== null) {
    await this.handleDelayMinutesFollowUp(context, pendingDelayResponse.id, responseText, delayMinutes);
    return;
  }

  // 3. Persist response
  await this.persistence.appointmentResponse.create({
    data: { appointmentId, responseType, patientMessage: responseText, delayMinutes },
  });

  // 4. Update appointment status
  await this.updateAppointmentStatus(context, responseType);

  // 5. Detect delay conflicts
  if (responseType === 'DELAY' && delayMinutes !== null) {
    const conflict = await this.evaluateDelayConflict(...);
    // If conflict → notify staff
  }

  // 6. Send confirmation + staff notification
  await this.patientConfirmation.sendPatientConfirmation(context, responseType, delayContext, ...);
  await this.patientStaffNotification.notifyStaff(context, responseType, delayContext, ...);
}
```

### The Two-Step Delay Flow

**The problem:** Patient replies "delay" → system asks "how many minutes?" → patient says "30" → system must associate the "30" with the pending delay request.

**The solution:** A `pendingDelayResponse` lookup with a 6-hour follow-up window:

```typescript
const pendingDelayResponse = await this.findPendingDelayResponse(appointmentId);
if (pendingDelayResponse && delayMinutes !== null && (responseType === 'UNKNOWN' || responseType === 'DELAY')) {
  await this.handleDelayMinutesFollowUp(context, pendingDelayResponse.id, responseText, delayMinutes);
  return;
}
```

### Why Not NLP/AI for Response Parsing

**The alternative:** Use OpenAI or a custom NLP model to parse patient responses.

**Why rejected:** Patient responses in Indian clinics are simple: "yes", "no", "10 min late", "come tomorrow". A regex-based parser handles 95% of cases. NLP adds latency, cost, and complexity for marginal improvement.

---

## Decision 3: WhatsApp Reconciliation

### What We Chose

A daily cron job that syncs message delivery status from Meta's API.

```typescript
// apps/api/src/domains/whatsapp/whatsapp-reconciliation.cron.ts
@Cron(CRON_SCHEDULES.WHATSAPP_RECONCILIATION)
async reconcile() {
  // Fetch messages with status 'SENT' but no delivery confirmation
  // Query Meta Graph API for actual status
  // Update local records
}
```

**Why reconciliation:** Meta's webhook delivery is at-least-once but not guaranteed. Some delivery confirmations are lost. The daily reconciliation catches any discrepancies.

---

## What Worked

- **Response parsing** — regex-based parser handles 95% of patient responses accurately
- **Two-step delay flow** — patients can delay appointments naturally via WhatsApp
- **Reconciliation** — daily sync catches any missed webhook deliveries

## What Failed

- **Rate limit burst** — a clinic sent 100+ reminders simultaneously. Meta's API rate-limited the batch, causing 30+ messages to fail silently. Fixed with per-clinic rate limiting (configurable, default 30/min) and exponential backoff on 429 responses.

- **Template approval delays** — Meta requires template approval before sending. A clinic's template was rejected for "marketing content" (it was a prescription delivery). Fixed by adding template pre-check and fallback to session messages.

- **Message delivery lag** — Meta's API sometimes delays delivery by 5-10 minutes. Patients called the clinic asking "did you get my reply?" Fixed by adding delivery status tracking and staff notifications.

## What Could Be Better

- **Rich media support** — currently text-only responses. Supporting image replies (e.g., patient sends a photo of a lab report) would improve clinical workflows.

- **Multi-language responses** — patients reply in Hindi, Telugu, etc. The parser currently only handles English. Adding multi-language support would improve adoption.

- **Chatbot flows** — currently linear (yes/no/delay). A decision tree chatbot could handle more complex interactions (e.g., "I need to reschedule to next week").

---

## Code Evidence

| Claim | File |
|-------|------|
| WhatsApp webhook ingress | `apps/api/src/domains/whatsapp/application/services/whatsapp-webhook-ingress.service.ts` |
| Response handler | `apps/api/src/domains/whatsapp/application/services/response-handler.service.ts` |
| Response parser | `apps/api/src/domains/whatsapp/application/services/patient-response-parser.helper.ts` |
| Send message use case | `apps/api/src/domains/whatsapp/application/use-cases/send-message.use-case.ts` |
| Reconciliation cron | `apps/api/src/domains/whatsapp/whatsapp-reconciliation.cron.ts` |
| Staff notification | `apps/api/src/domains/whatsapp/application/services/staff-notification.service.ts` |
| Template resolver | `apps/api/src/domains/whatsapp/core/services/template-resolver.service.ts` |

---

## Interview Script (60 seconds)

> "WhatsApp is Docita's primary patient communication channel. We support three sender modes: shared Meta number (free), bring-your-own (clinic's number), and Docita-managed. The challenge was handling patient responses — they reply with free text like 'yes', 'no', 'delay 30 min'. We built a regex-based parser that maps these to appointment actions, with a two-step flow for delays. We hit Meta's rate limits when a clinic sent 100+ reminders simultaneously — fixed with per-clinic rate limiting and exponential backoff. A daily reconciliation job syncs delivery status from Meta's API to catch any missed webhooks. The key design decision: keep it simple. NLP for response parsing was considered but rejected — Indian clinic patients use simple responses that regex handles accurately."
