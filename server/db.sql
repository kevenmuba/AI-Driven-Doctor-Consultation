-- =====================================================
-- AI-Driven Doctor Consultation Platform (MVP)
-- Database Schema
-- PostgreSQL
-- =====================================================

-- =========================
-- 1. USERS
-- =========================
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,

    role VARCHAR(20) NOT NULL
        CHECK (role IN ('ADMIN', 'DOCTOR', 'PATIENT')),

    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 2. DOCTOR PROFILES
-- =========================
CREATE TABLE doctor_profiles (
    id BIGSERIAL PRIMARY KEY,

    user_id BIGINT UNIQUE NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    years_experience INTEGER NOT NULL CHECK (years_experience >= 0),
    bio TEXT,
    is_verified BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_doctor_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- =========================
-- 3. PATIENT PROFILES
-- =========================
CREATE TABLE patient_profiles (
    id BIGSERIAL PRIMARY KEY,

    user_id BIGINT UNIQUE NOT NULL,
    age INTEGER CHECK (age >= 0),
    gender VARCHAR(20),
    medical_history TEXT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_patient_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- =========================
-- 4. DOCTOR AVAILABILITY
-- =========================
CREATE TABLE doctor_availability (
    id BIGSERIAL PRIMARY KEY,

    doctor_id BIGINT NOT NULL,

    day_of_week VARCHAR(10) NOT NULL
        CHECK (day_of_week IN (
            'MONDAY', 'TUESDAY', 'WEDNESDAY',
            'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'
        )),

    start_time TIME NOT NULL,
    end_time TIME NOT NULL,

    CONSTRAINT fk_availability_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctor_profiles(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_time_range
        CHECK (start_time < end_time)
);

-- =========================
-- 5. AI SYMPTOM ANALYSIS
-- =========================
CREATE TABLE symptom_analyses (
    id BIGSERIAL PRIMARY KEY,

    patient_id BIGINT NOT NULL,
    symptoms_text TEXT NOT NULL,

    predicted_specialty VARCHAR(100) NOT NULL,
    confidence_score NUMERIC(4,2)
        CHECK (confidence_score >= 0 AND confidence_score <= 1),

    ai_model_version VARCHAR(50),

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_symptom_patient
        FOREIGN KEY (patient_id)
        REFERENCES patient_profiles(id)
        ON DELETE CASCADE
);

-- =========================
-- 6. APPOINTMENTS
-- =========================
CREATE TABLE appointments (
    id BIGSERIAL PRIMARY KEY,

    patient_id BIGINT NOT NULL,
    doctor_id BIGINT NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'PENDING'
        CHECK (status IN ('PENDING', 'ACCEPTED', 'REJECTED', 'COMPLETED')),

    scheduled_time TIMESTAMP WITH TIME ZONE NOT NULL,
    ai_reason TEXT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_appointment_patient
        FOREIGN KEY (patient_id)
        REFERENCES patient_profiles(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_appointment_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctor_profiles(id)
        ON DELETE CASCADE
);

-- =========================
-- 7. CHAT ROOMS
-- =========================
CREATE TABLE chat_rooms (
    id BIGSERIAL PRIMARY KEY,

    appointment_id BIGINT UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_chat_appointment
        FOREIGN KEY (appointment_id)
        REFERENCES appointments(id)
        ON DELETE CASCADE
);

-- =========================
-- 8. MESSAGES
-- =========================
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,

    chat_room_id BIGINT NOT NULL,
    sender_id BIGINT NOT NULL,

    message_text TEXT NOT NULL,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_message_chat
        FOREIGN KEY (chat_room_id)
        REFERENCES chat_rooms(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_message_sender
        FOREIGN KEY (sender_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- =====================================================
-- END OF SCHEMA
-- =====================================================
