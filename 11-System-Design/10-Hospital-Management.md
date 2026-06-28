# Hospital Management System Design

## Requirements
### Functional Requirements

- Patient registration and profiles
- Appointment scheduling
- Doctor management
- Medical records (EHR)
- Prescription management
- Lab results management
- Billing and insurance
- Pharmacy management
- Multi-branch support
- Role-based access control
- Telemedicine support

### Non-Functional Requirements

- HIPAA compliance
- High availability (99.99%)
- Data encryption at rest and in transit
- Audit logging for all access
- Support 100K+ patients
- Handle 10K+ appointments per day
- Real-time availability updates
- Multi-tenant architecture

## Capacity Estimation

```text
Hospital Estimates:

- 100 hospitals
- 10K doctors
- 100K patients per hospital
- 10M total patients
- 10 appointments per patient per year

Appointment Estimates:

- 100K appointments per day
- Average appointment: 30 minutes
- Peak hours: 9 AM - 5 PM
- Concurrent appointments: 5K

Storage Estimates:

- Patient records: 10M × 10 KB = 100 GB
- Medical records: 10M × 100 KB = 1 TB
- Lab results: 10M × 50 KB = 500 GB
- Prescriptions: 10M × 5 KB = 50 GB
- Total: ~1.65 TB

Bandwidth Estimates:

- Patient queries: 10K × 10 KB = 100 MB/s
- Appointment requests: 1K × 1 KB = 1 MB/s
- Total: ~101 MB/s peak

```

## API Design

```yaml
# Patient Registration
POST /api/v1/patients
  Request:
    {
      "first_name": "John",
      "last_name": "Doe",
      "date_of_birth": "1990-01-15",
      "email": "john@example.com",
      "phone": "+1234567890",
      "insurance": {
        "provider": "BlueCross",
        "policy_number": "BC123456"
      }
    }
  Response:
    {
      "patient_id": "pat_123",
      "mrn": "MRN0000123"  # Medical Record Number
    }

# Appointment Scheduling
GET /api/v1/doctors/{id}/availability
  Query: ?date=2025-01-15&specialty=cardiology
  Response:
    {
      "doctor_id": "doc_456",
      "available_slots": [
        {"time": "09:00", "duration": 30},
        {"time": "09:30", "duration": 30}
      ]
    }

POST /api/v1/appointments
  Request:
    {
      "patient_id": "pat_123",
      "doctor_id": "doc_456",
      "date": "2025-01-15",
      "time": "09:00",
      "type": "consultation",
      "reason": "Chest pain"
    }
  Response:
    {
      "appointment_id": "apt_789",
      "status": "confirmed",
      "queue_number": 15
    }

# Medical Records
GET /api/v1/patients/{id}/records
  Response:
    {
      "patient_id": "pat_123",
      "records": [
        {
          "record_id": "rec_012",
          "type": "consultation",
          "doctor": "Dr. Smith",
          "date": "2025-01-15",
          "notes": "..."
        }
      ]
    }

# Prescription
POST /api/v1/prescriptions
  Request:
    {
      "patient_id": "pat_123",
      "doctor_id": "doc_456",
      "appointment_id": "apt_789",
      "medications": [
        {
          "name": "Aspirin",
          "dosage": "100mg",
          "frequency": "Once daily",
          "duration": "30 days"
        }
      ]
    }

# Lab Results
GET /api/v1/patients/{id}/lab-results
  Response:
    {
      "results": [
        {
          "test_name": "Blood Sugar",
          "value": 120,
          "unit": "mg/dL",
          "range": "70-140",
          "status": "normal"
        }
      ]
    }

# Billing
POST /api/v1/billing
  Request:
    {
      "patient_id": "pat_123",
      "appointment_id": "apt_789",
      "services": [...],
      "insurance_claim": {...}
    }

```

## Database Design
### Schema

```sql
-- Hospitals table (multi-tenant)
CREATE TABLE hospitals (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table (doctors, nurses, staff)
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    hospital_id BIGINT REFERENCES hospitals(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL, -- 'admin', 'doctor', 'nurse', 'staff'
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    specialty VARCHAR(100),
    license_number VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Patients table
CREATE TABLE patients (
    id BIGSERIAL PRIMARY KEY,
    hospital_id BIGINT REFERENCES hospitals(id),
    mrn VARCHAR(20) UNIQUE NOT NULL, -- Medical Record Number
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10),
    email VARCHAR(255),
    phone VARCHAR(20),
    address TEXT,
    blood_type VARCHAR(5),
    allergies TEXT[],
    emergency_contact JSONB,
    insurance JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patients_hospital ON patients(hospital_id);
CREATE INDEX idx_patients_mrn ON patients(mrn);
CREATE INDEX idx_patients_name ON patients(last_name, first_name);

-- Appointments table
CREATE TABLE appointments (
    id BIGSERIAL PRIMARY KEY,
    hospital_id BIGINT REFERENCES hospitals(id),
    patient_id BIGINT REFERENCES patients(id),
    doctor_id BIGINT REFERENCES users(id),
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    duration_minutes INT DEFAULT 30,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled',
    reason TEXT,
    notes TEXT,
    queue_number INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_appointments_hospital ON appointments(hospital_id);
CREATE INDEX idx_appointments_doctor ON appointments(doctor_id, appointment_date);
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);

-- Medical records
CREATE TABLE medical_records (
    id BIGSERIAL PRIMARY KEY,
    hospital_id BIGINT REFERENCES hospitals(id),
    patient_id BIGINT REFERENCES patients(id),
    doctor_id BIGINT REFERENCES users(id),
    appointment_id BIGINT REFERENCES appointments(id),
    record_type VARCHAR(50) NOT NULL,
    chief_complaint TEXT,
    diagnosis TEXT,
    treatment_plan TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_medical_records_patient ON medical_records(patient_id);

-- Prescriptions
CREATE TABLE prescriptions (
    id BIGSERIAL PRIMARY KEY,
    hospital_id BIGINT REFERENCES hospitals(id),
    patient_id BIGINT REFERENCES patients(id),
    doctor_id BIGINT REFERENCES users(id),
    appointment_id BIGINT REFERENCES appointments(id),
    medications JSONB NOT NULL,
    instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Lab results
CREATE TABLE lab_results (
    id BIGSERIAL PRIMARY KEY,
    hospital_id BIGINT REFERENCES hospitals(id),
    patient_id BIGINT REFERENCES patients(id),
    test_name VARCHAR(255) NOT NULL,
    test_date DATE NOT NULL,
    results JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'completed',
    ordered_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Billing
CREATE TABLE billing (
    id BIGSERIAL PRIMARY KEY,
    hospital_id BIGINT REFERENCES hospitals(id),
    patient_id BIGINT REFERENCES patients(id),
    appointment_id BIGINT REFERENCES appointments(id),
    services JSONB NOT NULL,
    subtotal DECIMAL(10,2),
    insurance_covered DECIMAL(10,2),
    patient_responsibility DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit log (HIPAA requirement)
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    hospital_id BIGINT REFERENCES hospitals(id),
    user_id BIGINT REFERENCES users(id),
    action VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id BIGINT,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (created_at);

```

### ER Diagram (ASCII)

```text
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  hospitals  │     │     users       │     │    patients     │
├─────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)     │◄────│ hospital_id(FK) │     │ id (PK)         │
│ name        │     │ id (PK)         │     │ hospital_id(FK) │
│ code        │     │ email           │     │ mrn             │
│ address     │     │ role            │     │ first_name      │
│ phone       │     │ first_name      │     │ last_name       │
│ email       │     │ last_name       │     │ date_of_birth   │
└─────────────┘     │ specialty       │     │ gender          │
        │           │ license_number  │     │ email           │
        │           │ is_active       │     │ phone           │
        │           └─────────────────┘     │ address         │
        │                    │              │ blood_type      │
        │                    │              │ allergies       │
        │                    │              │ insurance       │
        │                    │              └─────────────────┘
        │                    │                       │
        │                    ▼                       │
        │           ┌─────────────────┐              │
        │           │  appointments   │◄─────────────┘
        │           ├─────────────────┤
        │           │ id (PK)         │
        │           │ hospital_id(FK) │
        │           │ patient_id (FK) │
        │           │ doctor_id (FK)  │
        │           │ appointment_date│
        │           │ appointment_time│
        │           │ type            │
        │           │ status          │
        │           │ reason          │
        │           └─────────────────┘
        │                    │
        │                    ▼
        │           ┌─────────────────┐
        │           │medical_records  │
        │           ├─────────────────┤
        │           │ id (PK)         │
        │           │ hospital_id(FK) │
        │           │ patient_id (FK) │
        │           │ doctor_id (FK)  │
        │           │ appointment_id  │
        │           │ record_type     │
        │           │ diagnosis       │
        │           │ notes           │
        │           └─────────────────┘
        │
        ▼
┌─────────────────┐     ┌─────────────────┐
│    billing      │     │   audit_log     │
├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │
│ hospital_id(FK) │     │ hospital_id(FK) │
│ patient_id (FK) │     │ user_id (FK)    │
│ appointment_id  │     │ action          │
│ services        │     │ entity_type     │
│ subtotal        │     │ entity_id       │
│ insurance       │     │ old_values      │
│ status          │     │ new_values      │
└─────────────────┘     │ ip_address      │
                        │ user_agent      │
                        │ created_at      │
                        └─────────────────┘

```

## Architecture
### ASCII Architecture Diagram

```text
┌──────────────────────────────────────────────────────────────────┐
│                    Client Applications                           │
│         (Web Portal, Mobile App, Staff Dashboard)                │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │   API Gateway        │
                    │   (Authentication,   │
                    │    HIPAA Logging)    │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Patient        │  │  Appointment    │  │  Medical        │
│  Service        │  │  Service        │  │  Records        │
│  (Registration, │  │  (Scheduling,   │  │  Service        │
│   Profiles)     │  │   Queue)        │  │  (EHR, Labs)    │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │  PostgreSQL  │  │  Redis      │  │  Kafka      │
     │  (Patient,   │  │  (Session,  │  │  (Events,   │
     │   Medical)   │  │   Cache)    │  │   Audit)    │
     └─────────────┘  └─────────────┘  └─────────────┘
              │
              ▼
     ┌─────────────────┐
     │  File Storage   │
     │  (HIPAA         │
     │   Compliant)    │
     └─────────────────┘

```

## Key Components

### HIPAA Compliance Service

```python
class HIPAAComplianceService:
    def __init__(self, db, encryption_service):
        self.db = db
        self.encryption = encryption_service

    async def log_access(self, user_id: int, action: str,
                        entity_type: str, entity_id: int,
                        old_values: dict = None,
                        new_values: dict = None,
                        ip_address: str = None,
                        user_agent: str = None):
        # Log all access to PHI
        await self.db.execute("""
            INSERT INTO audit_log
            (user_id, action, entity_type, entity_id,
             old_values, new_values, ip_address, user_agent)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, action, entity_type, entity_id,
              old_values, new_values, ip_address, user_agent))

    async def check_access_permission(self, user_id: int,
                                     entity_type: str,
                                     entity_id: int) -> bool:
        # Check if user has permission to access entity
        user = await self.db.get_user(user_id)
        entity = await self.db.get_entity(entity_type, entity_id)

        # Check hospital match
        if user['hospital_id'] != entity['hospital_id']:
            return False

        # Check role-based access
        if user['role'] == 'doctor':
            # Doctors can only access their patients
            return await self.db.is_doctor_patient(
                user_id, entity['patient_id']
            )

        return True

    def encrypt_phi(self, data: dict) -> dict:
        # Encrypt Protected Health Information
        sensitive_fields = [
            'ssn', 'medical_record_number',
            'diagnosis', 'treatment'
        ]

        encrypted = {}
        for key, value in data.items():
            if key in sensitive_fields:
                encrypted[key] = self.encryption.encrypt(str(value))
            else:
                encrypted[key] = value

        return encrypted

    def decrypt_phi(self, data: dict) -> dict:
        # Decrypt Protected Health Information
        sensitive_fields = [
            'ssn', 'medical_record_number',
            'diagnosis', 'treatment'
        ]

        decrypted = {}
        for key, value in data.items():
            if key in sensitive_fields and value:
                decrypted[key] = self.encryption.decrypt(value)
            else:
                decrypted[key] = value

        return decrypted

```

### Appointment Scheduling Service

```python
class AppointmentSchedulingService:
    def __init__(self, db, redis_client, notification_service):
        self.db = db
        self.redis = redis_client
        self.notifications = notification_service

    async def get_available_slots(self, doctor_id: int,
                                 date: str) -> list:
        # Check cache first
        cache_key = f"availability:{doctor_id}:{date}"
        cached = await self.redis.get(cache_key)

        if cached:
            return json.loads(cached)

        # Get doctor's schedule
        doctor = await self.db.get_user(doctor_id)

        # Get existing appointments
        existing = await self.db.get_appointments(
            doctor_id=doctor_id,
            date=date
        )

        # Calculate available slots
        available = self.calculate_available_slots(
            doctor['work_hours'],
            existing,
            date
        )

        # Cache for 5 minutes
        await self.redis.setex(
            cache_key, 300, json.dumps(available)
        )

        return available

    async def book_appointment(self, patient_id: int,
                              doctor_id: int,
                              date: str,
                              time: str,
                              appointment_type: str,
                              reason: str) -> dict:
        # Check slot availability
        available = await self.get_available_slots(
            doctor_id, date
        )

        if not any(slot['time'] == time for slot in available):
            raise SlotUnavailableError("Slot not available")

        # Create appointment
        appointment = await self.db.create_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=date,
            time=time,
            type=appointment_type,
            reason=reason
        )

        # Invalidate cache
        await self.redis.delete(f"availability:{doctor_id}:{date}")

        # Send confirmation
        await self.notifications.send_appointment_confirmation(
            patient_id, appointment
        )

        return appointment

    async def cancel_appointment(self, appointment_id: int,
                                user_id: int) -> bool:
        appointment = await self.db.get_appointment(appointment_id)

        # Check permission
        if appointment['patient_id'] != user_id:
            # Check if user is staff
            user = await self.db.get_user(user_id)
            if user['role'] not in ['admin', 'nurse']:
                raise PermissionError("No permission to cancel")

        # Cancel appointment
        await self.db.update_appointment_status(
            appointment_id, 'cancelled'
        )

        # Invalidate cache
        await self.redis.delete(
            f"availability:{appointment['doctor_id']}:{appointment['date']}"
        )

        # Notify doctor
        await self.notifications.send_cancellation_notice(
            appointment['doctor_id'], appointment
        )

        return True

```

### Medical Records Service

```python
class MedicalRecordsService:
    def __init__(self, db, encryption_service, audit_service):
        self.db = db
        self.encryption = encryption_service
        self.audit = audit_service

    async def get_patient_records(self, patient_id: int,
                                 user_id: int) -> dict:
        # Check access permission
        has_access = await self.audit.check_access_permission(
            user_id, 'patient', patient_id
        )

        if not has_access:
            raise PermissionError("Access denied")

        # Log access
        await self.audit.log_access(
            user_id, 'read', 'patient', patient_id
        )

        # Get records
        records = await self.db.get_patient_records(patient_id)

        # Decrypt PHI
        decrypted_records = []
        for record in records:
            decrypted = self.encryption.decrypt_phi(record)
            decrypted_records.append(decrypted)

        return {
            'patient_id': patient_id,
            'records': decrypted_records
        }

    async def create_medical_record(self, patient_id: int,
                                   doctor_id: int,
                                   appointment_id: int,
                                   record_data: dict,
                                   user_id: int) -> dict:
        # Check permission
        has_access = await self.audit.check_access_permission(
            user_id, 'patient', patient_id
        )

        if not has_access:
            raise PermissionError("Access denied")

        # Encrypt PHI
        encrypted_data = self.encryption.encrypt_phi(record_data)

        # Create record
        record = await self.db.create_medical_record(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_id=appointment_id,
            **encrypted_data
        )

        # Log access
        await self.audit.log_access(
            user_id, 'create', 'medical_record', record['id'],
            new_values=record_data
        )

        return record

```

### Multi-Tenant Service

```python
class MultiTenantService:
    def __init__(self, db):
        self.db = db

    async def get_hospital_context(self, hospital_code: str) -> dict:
        # Get hospital details
        hospital = await self.db.get_hospital_by_code(hospital_code)

        return {
            'hospital_id': hospital['id'],
            'name': hospital['name'],
            'settings': hospital.get('settings', {}),
            'features': hospital.get('features', [])
        }

    async def filter_by_hospital(self, query: str,
                                hospital_id: int) -> str:
        # Add hospital filter to query
        return f"{query} AND hospital_id = {hospital_id}"

    async def get_hospital_stats(self, hospital_id: int) -> dict:
        # Get hospital statistics
        stats = await self.db.execute("""
            SELECT
                (SELECT COUNT(*) FROM patients WHERE hospital_id = %s) as total_patients,
                (SELECT COUNT(*) FROM users WHERE hospital_id = %s AND role = 'doctor') as total_doctors,
                (SELECT COUNT(*) FROM appointments
                 WHERE hospital_id = %s AND appointment_date = CURRENT_DATE) as today_appointments
        """, (hospital_id, hospital_id, hospital_id))

        return stats[0] if stats else {}

```

## Caching Strategy (Redis)

### Appointment Cache

```python
class AppointmentCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 300  # 5 minutes

    async def get_availability(self, doctor_id: int,
                              date: str) -> list:
        key = f"availability:{doctor_id}:{date}"
        cached = await self.redis.get(key)

        if cached:
            return json.loads(cached)

        return None

    async def set_availability(self, doctor_id: int,
                              date: str, slots: list):
        key = f"availability:{doctor_id}:{date}"
        await self.redis.setex(key, self.ttl, json.dumps(slots))

    async def invalidate_availability(self, doctor_id: int,
                                     date: str):
        await self.redis.delete(f"availability:{doctor_id}:{date}")

```

### Patient Cache

```python
class PatientCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 600  # 10 minutes

    async def get_patient(self, patient_id: int) -> dict:
        key = f"patient:{patient_id}"
        cached = await self.redis.get(key)

        if cached:
            return json.loads(cached)

        return None

    async def set_patient(self, patient_id: int, patient: dict):
        key = f"patient:{patient_id}"
        await self.redis.setex(key, self.ttl, json.dumps(patient))

    async def invalidate_patient(self, patient_id: int):
        await self.redis.delete(f"patient:{patient_id}")

```

## Message Queue (Kafka)

### Topics and Events

```text
Topics:
├── appointment.created     (new appointment)
├── appointment.cancelled   (appointment cancelled)
├── medical_record.created  (new medical record)
├── lab_result.created      (new lab result)
├── prescription.created    (new prescription)
├── billing.created         (new billing entry)
└── audit.event             (HIPAA audit events)

Event Schema:
{
  "event_id": "evt_123",
  "event_type": "appointment.created",
  "timestamp": "2025-01-15T10:30:00Z",
  "hospital_id": "hosp_456",
  "data": {
    "appointment_id": "apt_789",
    "patient_id": "pat_012",
    "doctor_id": "doc_345",
    "date": "2025-01-15",
    "time": "09:00"
  }
}

```

### Event Processing

```python
class HospitalEventProcessor:
    def __init__(self, kafka_consumer, notification_service):
        self.consumer = kafka_consumer
        self.notifications = notification_service

    async def process_events(self):
        async for message in self.consumer:
            event = message.value

            if event['event_type'] == 'appointment.created':
                await self.handle_appointment_created(event)
            elif event['event_type'] == 'lab_result.created':
                await self.handle_lab_result_created(event)

    async def handle_appointment_created(self, event: dict):
        # Send confirmation to patient
        await self.notifications.send_appointment_confirmation(
            event['data']['patient_id'],
            event['data']
        )

        # Notify doctor
        await self.notifications.send_doctor_notification(
            event['data']['doctor_id'],
            event['data']
        )

```

## Scaling Strategy

### Horizontal Scaling

```text
Architecture:
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                         │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Patient     │   │  Appointment │   │  Medical     │
│  Service     │   │  Service     │   │  Records     │
│  (10+ nodes) │   │  (10+ nodes) │   │  (10+ nodes) │
└──────────────┘   └──────────────┘   └──────────────┘

```

### Database Sharding

```python
class HospitalDatabaseScaler:
    def __init__(self):
        self.shards = 16

    def get_shard(self, hospital_id: int) -> int:
        return hospital_id % self.shards

    async def get_patient(self, patient_id: int) -> dict:
        # Get hospital_id from patient
        hospital_id = await self.db.get_patient_hospital(patient_id)
        shard = self.get_shard(hospital_id)

        return await self.shards[shard].execute(
            "SELECT * FROM patients WHERE id = %s",
            (patient_id,)
        )

```

## Failure Handling

### Appointment Conflict Resolution

```python
class AppointmentConflictResolver:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client

    async def resolve_conflict(self, doctor_id: int,
                              date: str, time: str) -> dict:
        # Check for conflicts
        conflicts = await self.db.get_conflicting_appointments(
            doctor_id, date, time
        )

        if not conflicts:
            return {'status': 'no_conflict'}

        # Try to reschedule
        alternative_slots = await self.get_alternative_slots(
            doctor_id, date
        )

        return {
            'status': 'conflict',
            'conflicts': conflicts,
            'alternatives': alternative_slots
        }

```

### Failure Scenarios

| Failure | Mitigation |
|---------|------------|
| Database failover | Read from replica |
| Redis down | Fall back to database |
| Notification service down | Queue notifications |
| Encryption service down | Use cached keys |
| Audit log failure | Buffer locally |

### Data Recovery

```python
class DataRecoveryService:
    def __init__(self, db, backup_service):
        self.db = db
        self.backup = backup_service

    async def recover_deleted_record(self, record_type: str,
                                    record_id: int) -> dict:
        # Get from backup
        backup = await self.backup.get_backup(
            record_type, record_id
        )

        if backup:
            # Restore record
            await self.db.restore_record(backup)
            return {'status': 'recovered', 'record': backup}

        return {'status': 'not_found'}

```

## Monitoring

### Key Metrics

```yaml
Business Metrics:

  - appointments_per_day
  - patient_satisfaction_score
  - average_wait_time
  - no_show_rate

System Metrics:

  - appointment_booking_latency_p95
  - medical_record_access_latency
  - api_response_time
  - error_rate

Infrastructure Metrics:

  - server_cpu_usage
  - memory_usage
  - database_query_latency
  - redis_memory_usage

Compliance Metrics:

  - hipaa_audit_events
  - access_denied_count
  - encryption_operations

```

### Alerting Rules

```yaml
alerts:

  - name: High No-Show Rate
    condition: no_show_rate > 20%
    severity: warning

  - name: HIPAA Violation Attempt
    condition: access_denied_count > 100
    severity: critical

  - name: Appointment Booking Slow
    condition: p95_booking_latency > 5s
    severity: warning

  - name: Database Connection Pool Exhausted
    condition: active_connections > 90%
    severity: critical

```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Storage | PostgreSQL | MongoDB | PostgreSQL (ACID) |
| Encryption | Application-level | Database-level | Application-level |
| Multi-tenant | Shared database | Separate databases | Shared with row-level security |
| Audit | Synchronous | Asynchronous | Synchronous (HIPAA) |
| Scheduling | Optimistic | Pessimistic | Pessimistic |

## Interview Questions

### Design Questions

1. **How would you design a HIPAA-compliant system?**

   - Encrypt PHI at rest and in transit
   - Audit logging for all access
   - Role-based access control
   - Data backup and recovery

2. **How do you handle appointment scheduling?**

   - Real-time availability checking
   - Pessimistic locking for slots
   - Cache invalidation on booking
   - Conflict detection and resolution

3. **How would you implement multi-tenancy?**

   - Shared database with row-level security
   - Hospital-specific encryption keys
   - Separate audit logs per hospital
   - Feature flags per hospital

### Scaling Questions

4. **How do you scale to 100K+ patients?**

   - Database sharding by hospital
   - Redis for caching
   - Read replicas for queries
   - Async processing for records

5. **How do you handle peak appointment times?**

   - Pre-warm availability cache
   - Queue booking requests
   - Auto-scale during peaks
   - Monitor and alert

### Trade-off Questions

6. **How do you balance security vs usability?**

   - Strong authentication
   - Role-based access
   - Session management
   - Audit without friction

7. **How do you handle data migration between hospitals?**

   - Patient consent required
   - Secure data transfer
   - Audit trail
   - Backup before migration

### Senior-level Questions

8. **How would you implement telemedicine?**

   - Video conferencing integration
   - E-prescriptions
   - Virtual waiting room
   - Insurance verification

9. **How do you handle lab result integration?**

   - HL7/FHIR standards
   - Real-time result delivery
   - Abnormal result alerts
   - Result interpretation

10. **How would you implement predictive analytics?**

    - Patient risk scoring
    - Appointment no-show prediction
    - Resource allocation
    - Disease outbreak detection

## Summary

The Hospital Management system design covers:

- **HIPAA Compliance**: Encryption, audit logging, access control
- **Multi-tenancy**: Shared database with row-level security
- **Appointment Scheduling**: Real-time availability with caching
- **Medical Records**: Encrypted storage with access control
- **Scalability**: Database sharding, caching, async processing

Key takeaways:

1. Implement HIPAA compliance from the start

2. Use pessimistic locking for appointment slots

3. Encrypt PHI at application level

4. Audit all access to sensitive data

5. Design for multi-tenancy with hospital isolation

This design supports 100K+ patients with 10K+ appointments per day while maintaining HIPAA compliance.

---

## References & Learn More

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [GitHub - system-design-primer](https://github.com/donnemartin/system-design-primer)
- [High Scalability](http://highscalability.com/)
- [System Design Interview (ByteByteGo)](https://bytebytego.com/)
