-- PostgreSQL schema dump for the Hospital Management System.
-- Real server-based DB (PostgreSQL), normalized into patient / doctor / appointment.

SET client_encoding = 'UTF8';

CREATE TABLE patient (
    id          BIGSERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    dob         DATE,
    gender      VARCHAR(10)  NOT NULL DEFAULT '',
    phone       VARCHAR(20)  NOT NULL DEFAULT '',
    email       VARCHAR(254) NOT NULL DEFAULT '',
    is_deleted  BOOLEAN      NOT NULL DEFAULT FALSE
);
CREATE INDEX patient_name_idx  ON patient (name);
CREATE INDEX patient_phone_idx ON patient (phone);

CREATE TABLE doctor (
    id             BIGSERIAL PRIMARY KEY,
    name           VARCHAR(200) NOT NULL,
    specialization VARCHAR(120) NOT NULL,
    phone          VARCHAR(20)  NOT NULL DEFAULT '',
    email          VARCHAR(254) NOT NULL DEFAULT '',
    fee            NUMERIC(8,2) NOT NULL DEFAULT 0
);
CREATE INDEX doctor_spec_idx ON doctor (specialization);

CREATE TABLE appointment (
    id          BIGSERIAL PRIMARY KEY,
    patient_id  BIGINT NOT NULL REFERENCES patient (id) ON DELETE CASCADE,
    doctor_id   BIGINT NOT NULL REFERENCES doctor (id)  ON DELETE CASCADE,
    start_time  TIMESTAMPTZ NOT NULL,
    end_time    TIMESTAMPTZ NOT NULL,
    status      VARCHAR(20) NOT NULL DEFAULT 'booked'
);
-- Supports the overlap check (doctor_id, start_time) and day listings.
CREATE INDEX appointment_doctor_start_idx ON appointment (doctor_id, start_time);

-- Sample data
INSERT INTO doctor (name, specialization, fee) VALUES
    ('Gregory House', 'Diagnostics', 300.00),
    ('Meredith Grey', 'Surgery', 250.00);
INSERT INTO patient (name, phone, email) VALUES
    ('Alice Walker', '555-1000', 'alice@example.com'),
    ('Bob Smith',    '555-2000', 'bob@example.com');
INSERT INTO appointment (patient_id, doctor_id, start_time, end_time, status) VALUES
    (1, 1, '2030-01-01T10:00:00Z', '2030-01-01T10:30:00Z', 'completed');
