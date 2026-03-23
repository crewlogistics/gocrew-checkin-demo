#!/usr/bin/env python3
"""Generate GoCrew Full System Specification PDF using fpdf2."""

from fpdf import FPDF
import os

# Colors
NAVY = (27, 42, 74)
TEAL = (13, 115, 119)
GOLD = (196, 151, 42)
EMERALD = (5, 150, 105)
RED = (220, 38, 38)
DARK_GRAY = (74, 85, 104)
PURPLE = (109, 40, 217)
WHITE = (255, 255, 255)
LIGHT_GRAY = (240, 240, 245)
MED_GRAY = (200, 200, 210)

OUTPUT_PATH = (
    "/Users/bretthogan/Library/CloudStorage/OneDrive-CrewFacilities.comLLC/"
    "GOCREW Roster Management/GC001 Review Current Roster Management Process/"
    "GoCrew_Full_System_Specification.pdf"
)


class SpecPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.is_cover = False
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        if self.is_cover:
            return
        if self.page_no() <= 1:
            return
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*NAVY)
        self.set_fill_color(*NAVY)
        self.rect(10, 5, 190, 8, "F")
        self.set_text_color(*WHITE)
        self.set_xy(12, 5.5)
        self.cell(0, 7, "GOCREW  |  FULL SYSTEM SPECIFICATION  |  CUI", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*NAVY)
        self.ln(4)

    def footer(self):
        if self.is_cover:
            return
        if self.page_no() <= 1:
            return
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*DARK_GRAY)
        self.cell(0, 10, f"Page {self.page_no()}", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_y(-10)
        self.cell(0, 5, "Crew Logistics  |  Confidential", align="C", new_x="LMARGIN", new_y="NEXT")


def add_cover(pdf):
    pdf.is_cover = True
    pdf.add_page()
    # Navy background
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, 210, 297, "F")

    # Gold accent bar
    pdf.set_fill_color(*GOLD)
    pdf.rect(20, 60, 170, 3, "F")

    # Title
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 36)
    pdf.set_xy(20, 75)
    pdf.cell(170, 18, "GOCREW", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_x(20)
    pdf.cell(170, 12, "ROSTER MANAGEMENT SYSTEM", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Gold bar
    pdf.set_fill_color(*GOLD)
    pdf.rect(60, pdf.get_y(), 90, 2, "F")
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*TEAL)
    pdf.set_x(20)
    pdf.cell(170, 12, "FULL SYSTEM SPECIFICATION", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(*GOLD)
    pdf.set_x(20)
    pdf.cell(170, 10, "Engineering Bible - v1.0", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    # Meta info box
    pdf.set_fill_color(40, 55, 90)
    pdf.rect(30, pdf.get_y(), 150, 50, "F")
    y = pdf.get_y() + 5
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*WHITE)
    meta = [
        "Document: GC-SYS-001",
        "Date: March 2026",
        "Classification: CUI // Controlled Unclassified Information",
        "",
        "10 Process Domains  |  15 Epics  |  80+ User Stories  |  20+ API Endpoints",
        "",
        "Incorporates: BPMN Process Diagrams + IOTA Blockchain + BLE Swarm Intelligence",
    ]
    for line in meta:
        pdf.set_xy(35, y)
        pdf.cell(140, 6, line, align="C", new_x="LMARGIN", new_y="NEXT")
        y += 6

    # Bottom bar
    pdf.set_fill_color(*GOLD)
    pdf.rect(20, 250, 170, 2, "F")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(20, 255)
    pdf.cell(170, 8, "Crew Logistics  |  Confidential  |  Not for Distribution", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.is_cover = False


def section_title(pdf, text, color=NAVY):
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*color)
    pdf.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")
    pdf.set_fill_color(*color)
    pdf.rect(10, pdf.get_y(), 190, 1, "F")
    pdf.ln(4)


def sub_title(pdf, text, color=TEAL):
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*color)
    pdf.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)


def sub_sub_title(pdf, text, color=DARK_GRAY):
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*color)
    pdf.cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)


def body_text(pdf, text):
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK_GRAY)
    pdf.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)


def bullet(pdf, text, indent=15):
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK_GRAY)
    pdf.set_x(pdf.l_margin + indent)
    pdf.cell(4, 5, "-", new_x="RIGHT", new_y="TOP")
    w = pdf.w - pdf.l_margin - pdf.r_margin - indent - 4
    pdf.multi_cell(w, 5, text, new_x="LMARGIN", new_y="NEXT")


def numbered_item(pdf, num, text, indent=15):
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK_GRAY)
    pdf.set_x(pdf.l_margin + indent)
    pdf.cell(8, 5, f"{num}.", new_x="RIGHT", new_y="TOP")
    w = pdf.w - pdf.l_margin - pdf.r_margin - indent - 8
    pdf.multi_cell(w, 5, text, new_x="LMARGIN", new_y="NEXT")


def table_header(pdf, cols, widths, color=TEAL):
    pdf.set_fill_color(*color)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 8)
    for i, col in enumerate(cols):
        pdf.cell(widths[i], 7, col, border=1, fill=True, new_x="RIGHT", new_y="TOP")
    pdf.ln(7)


def table_row(pdf, cols, widths, fill=False):
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*DARK_GRAY)
    if fill:
        pdf.set_fill_color(*LIGHT_GRAY)
    max_h = 5
    x_start = pdf.get_x()
    y_start = pdf.get_y()
    # Calculate row height
    heights = []
    for i, col in enumerate(cols):
        n_lines = pdf.get_string_width(str(col)) / (widths[i] - 2)
        h = max(5, int(n_lines + 1) * 5)
        heights.append(h)
    max_h = max(heights)
    if max_h > 5:
        max_h = min(max_h, 20)

    # Check page break
    if pdf.get_y() + max_h > 272:
        pdf.add_page()
        y_start = pdf.get_y()

    for i, col in enumerate(cols):
        pdf.set_xy(x_start + sum(widths[:i]), y_start)
        if fill:
            pdf.cell(widths[i], max_h, str(col)[:int(widths[i]/1.8)], border=1, fill=True, new_x="RIGHT", new_y="TOP")
        else:
            pdf.cell(widths[i], max_h, str(col)[:int(widths[i]/1.8)], border=1, new_x="RIGHT", new_y="TOP")
    pdf.set_xy(x_start, y_start + max_h)


def user_story(pdf, story_id, role, want, so_that, given, when, then, priority, sprint):
    check_page_space(pdf, 40)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 5, f"US-{story_id}  [{priority}]  Sprint: {sprint}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*DARK_GRAY)
    pdf.multi_cell(0, 4, f"As a {role}, I want {want}, so that {so_that}.", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(*TEAL)
    pdf.multi_cell(0, 4, f"Given {given}; When {when}; Then {then}.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def check_page_space(pdf, needed_mm):
    if pdf.get_y() + needed_mm > 272:
        pdf.add_page()


def add_domain_header(pdf, num, title, color=NAVY):
    pdf.add_page()
    pdf.set_fill_color(*color)
    pdf.rect(10, 18, 190, 14, "F")
    pdf.set_xy(12, 18)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*WHITE)
    pdf.cell(186, 14, f"DOMAIN {num}: {title}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)


def api_endpoint(pdf, method, path, req_body, resp_body, side_effects):
    check_page_space(pdf, 20)
    pdf.set_font("Helvetica", "B", 8)
    color = EMERALD if method == "GET" else TEAL if method == "POST" else GOLD if method == "PUT" else RED
    pdf.set_text_color(*color)
    pdf.cell(15, 5, method, new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 5, path, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*DARK_GRAY)
    if req_body:
        pdf.set_x(25)
        pdf.cell(0, 4, f"Body: {req_body}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(25)
    pdf.cell(0, 4, f"Response: {resp_body}", new_x="LMARGIN", new_y="NEXT")
    if side_effects:
        pdf.set_x(25)
        pdf.cell(0, 4, f"Side Effects: {side_effects}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


# ============================================================
# BUILD THE DOCUMENT
# ============================================================

pdf = SpecPDF()

# -- COVER --
add_cover(pdf)

# -- TABLE OF CONTENTS --
pdf.add_page()
section_title(pdf, "TABLE OF CONTENTS")
toc = [
    ("PART 1", "System Overview", 3),
    ("PART 2", "Process Domain Specifications", 5),
    ("  Domain 1", "BLE Swarm Roster", 5),
    ("  Domain 2", "AI Fraud Detection System", 8),
    ("  Domain 3", "Geofence Event State Machine", 11),
    ("  Domain 4", "Roster Check-In Process", 14),
    ("  Domain 5", "Lodging Authorization", 17),
    ("  Domain 6", "Crew Supervisor Mobile App", 20),
    ("  Domain 7", "Onsite/Offsite Supervisor Workflows", 23),
    ("  Domain 8", "Roster System Core Functions", 26),
    ("  Domain 9", "Compliance & Data Protection", 29),
    ("  Domain 10", "Roster Check-Off & Verification", 32),
    ("PART 3", "Integration Map", 35),
    ("PART 4", "Sprint Plan", 37),
    ("PART 5", "Appendix", 40),
]
pdf.set_font("Helvetica", "", 10)
for part, title, pg in toc:
    pdf.set_text_color(*NAVY)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(25, 7, part, new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*DARK_GRAY)
    pdf.cell(140, 7, title, new_x="RIGHT", new_y="TOP")
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 7, str(pg), align="R", new_x="LMARGIN", new_y="NEXT")

# ============================================================
# PART 1: SYSTEM OVERVIEW
# ============================================================
pdf.add_page()
section_title(pdf, "PART 1: SYSTEM OVERVIEW")

sub_title(pdf, "1.1 System Architecture")
body_text(pdf, "The GoCrew Roster Management System is a distributed, privacy-first workforce management platform built on three pillars: BLE Swarm Intelligence for decentralized presence detection, IOTA Distributed Ledger for tamper-proof audit trails, and AI-driven fraud detection for continuous compliance monitoring. The system comprises 10 interconnected process domains organized into three deployment phases.")

body_text(pdf, "ARCHITECTURE DIAGRAM:")
body_text(pdf, """
+------------------------------------------------------------------+
|                    GOCREW SYSTEM ARCHITECTURE                     |
+------------------------------------------------------------------+
|  PRESENTATION LAYER                                               |
|  [Crew Mobile App] [Supervisor App] [Ops Dashboard] [Admin Portal]|
+------------------------------------------------------------------+
|  API GATEWAY (Kong / AWS API Gateway)                             |
|  - Rate Limiting  - JWT Auth  - Request Routing                   |
+------------------------------------------------------------------+
|  SERVICE LAYER                                                    |
|  +----------------+ +----------------+ +------------------+       |
|  | Check-In Svc   | | Authorization  | | Geofence Engine  |       |
|  | (Domain 4)     | | Svc (Domain 5) | | (Domain 3)       |       |
|  +----------------+ +----------------+ +------------------+       |
|  +----------------+ +----------------+ +------------------+       |
|  | BLE Swarm Svc  | | Fraud Detection| | Compliance Svc   |       |
|  | (Domain 1)     | | (Domain 2)     | | (Domain 9)       |       |
|  +----------------+ +----------------+ +------------------+       |
|  +----------------+ +----------------+ +------------------+       |
|  | Supervisor Svc | | Roster Core    | | Check-Off Svc    |       |
|  | (Domains 6,7)  | | (Domain 8)     | | (Domain 10)      |       |
|  +----------------+ +----------------+ +------------------+       |
+------------------------------------------------------------------+
|  DATA LAYER                                                       |
|  [PostgreSQL] [Redis Cache] [IOTA Tangle] [S3/Blob Storage]      |
+------------------------------------------------------------------+
|  INFRASTRUCTURE                                                   |
|  [AWS EKS / Azure AKS] [BLE Beacon Network] [Geofence Providers] |
+------------------------------------------------------------------+
""")

sub_title(pdf, "1.2 Technology Stack")
headers = ["Layer", "Technology", "Purpose"]
widths = [40, 60, 90]
table_header(pdf, headers, widths)
stack_rows = [
    ("Frontend - Crew", "React Native + Expo", "Cross-platform mobile app for crew members"),
    ("Frontend - Supervisor", "React Native + Expo", "Supervisor mobile app with extended features"),
    ("Frontend - Dashboard", "Next.js 14 + TailwindCSS", "Operations and admin web dashboard"),
    ("API Layer", "Node.js + Express / Fastify", "RESTful API services with JWT authentication"),
    ("Database", "PostgreSQL 16 + PostGIS", "Primary data store with geospatial extensions"),
    ("Cache", "Redis 7", "Session management, real-time state, pub/sub"),
    ("Blockchain", "IOTA Chrysalis / Shimmer", "Feeless DLT for tamper-proof audit logging"),
    ("BLE", "Bluetooth 5.0 LE", "Proximity detection, swarm roster, beacon network"),
    ("AI/ML", "Python + scikit-learn + TF", "Fraud detection models, anomaly scoring"),
    ("Geofencing", "Google Geofence API + GPS", "Property boundary detection and monitoring"),
    ("Auth", "Auth0 / Keycloak", "Identity management, MFA, RBAC"),
    ("Infra", "AWS EKS + Terraform", "Container orchestration, IaC deployment"),
    ("CI/CD", "GitHub Actions", "Automated testing, deployment pipelines"),
    ("Monitoring", "Datadog + PagerDuty", "Observability, alerting, incident response"),
]
for i, row in enumerate(stack_rows):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

pdf.ln(4)
sub_title(pdf, "1.3 System Boundaries")
sub_sub_title(pdf, "In Scope:")
in_scope = [
    "Crew check-in/check-out at lodging properties via BLE + geofence + QR",
    "BLE swarm roster for decentralized presence verification and contact tracing",
    "IOTA blockchain for immutable audit trail of all roster events",
    "AI-powered fraud detection across geographic, temporal, and behavioral dimensions",
    "Lodging authorization workflow with rate verification and compliance checks",
    "Supervisor mobile applications (onsite and offsite workflows)",
    "Geofence event state machine for automatic roster updates",
    "Compliance framework (GDPR, CCPA, CMMC Level 2, CUI handling)",
    "Roster verification and check-off processes",
    "Real-time notifications and alerting across all channels",
]
for item in in_scope:
    bullet(pdf, item)

sub_sub_title(pdf, "Out of Scope:")
out_scope = [
    "Payroll processing (integration point only - data sent to external payroll system)",
    "Hotel property management systems (PMS) - integration via API only",
    "Travel booking and itinerary management (handled by travel operations team)",
    "Background check processing (handled by third-party KYC providers)",
    "Physical access control systems (badge readers, door locks - future phase)",
    "Crew recruitment and onboarding workflows (separate HR system)",
]
for item in out_scope:
    bullet(pdf, item)

pdf.ln(3)
sub_title(pdf, "1.4 Phase Roadmap")
headers = ["Phase", "Timeline", "Domains", "Key Deliverables"]
widths = [30, 30, 35, 95]
table_header(pdf, headers, widths, NAVY)
phases = [
    ("Phase 1", "Weeks 1-3", "4, 5, 3", "Check-In MVP: Core check-in, lodging auth, geofence events"),
    ("Phase 2", "Weeks 4-8", "1, 2, 9", "BLE Swarm + IOTA blockchain + AI fraud + compliance"),
    ("Phase 3", "Weeks 9-14", "6, 7, 8, 10", "Supervisor apps, workforce mgmt, check-off verification"),
]
for i, row in enumerate(phases):
    table_row(pdf, row, widths, fill=(i % 2 == 0))


# ============================================================
# PART 2: DOMAIN SPECIFICATIONS
# ============================================================

# ---- DOMAIN 1: BLE SWARM ROSTER ----
add_domain_header(pdf, 1, "BLE SWARM ROSTER", NAVY)

sub_title(pdf, "Domain Overview")
body_text(pdf, "The BLE Swarm Roster is the foundational privacy-preserving presence detection layer of GoCrew. It replaces centralized check-in with a decentralized swarm intelligence model where crew devices broadcast rotating UUIDs via Bluetooth Low Energy. When 3 or more crew devices corroborate each other's presence within a geofenced property, the system triggers an automated check-in -- no manual action required. All proximity data is encrypted on-device, submitted to the IOTA Tangle (feeless, quantum-resistant), and protected by five consent tiers. The Alibi Engine provides crew members with a continuous, tamper-proof location trail for legal defense against false accusations.")

sub_title(pdf, "Process Flow")
steps = [
    "BLE UUID Registration: Each crew device generates a cryptographically unique UUID during onboarding. UUID is linked to KYC-verified identity via one-way hash stored in secure enclave.",
    "Daily UUID Rotation: At 00:00 UTC, each device generates a new temporary UUID derived from the master key. Previous UUID mappings are retained in encrypted local storage for 14 days, then purged.",
    "KYC Verification: Identity documents are verified against government databases. Verified identity is linked to device UUID via encrypted binding. KYC status is stored on-chain as a zero-knowledge proof.",
    "UUID Broadcasting: Device broadcasts temporary UUID via BLE advertising packets at 1-second intervals. Broadcast power is calibrated for 10-meter detection range. Advertising payload includes: temp UUID, timestamp, signal strength, device class.",
    "BLE Scanning and Logging: Device simultaneously scans for other crew BLE advertisements. Detected UUIDs are logged with RSSI, timestamp, and duration. Minimum contact duration threshold: 30 seconds.",
    "Data Encryption: All contact logs are encrypted on-device using AES-256-GCM before any transmission. Encryption key is derived from device secure enclave + user passphrase.",
    "Log Aggregation: At configurable intervals (default: 15 min), device compiles proximity contact summary. Summary includes: unique contacts count, duration per contact, average RSSI, location hash.",
    "IOTA Blockchain Submission: Encrypted aggregated logs are submitted to IOTA Tangle as zero-value transactions. Tangle provides: feeless submission, DAG structure, quantum-resistant signatures.",
    "Smart Contracts for Roster Status: IOTA smart contracts evaluate swarm data to determine check-in/check-out status. Contract logic: IF crew_contacts >= 3 AND geofence == true AND time_window == shift THEN status = CHECKED_IN.",
    "Blockchain Query for Proximity Assessment: Authorized systems can query the Tangle for roster status. Queries return only status (CHECKED_IN/OUT) -- never raw contact data -- unless consent tier permits.",
    "Anonymization Layers: Layer 1 - Rotating UUIDs (daily). Layer 2 - Hashed identifiers in logs. Layer 3 - Zero-knowledge proofs for KYC. Layer 4 - Encrypted payload (AES-256). Layer 5 - Consent-gated access.",
    "End-to-End Encryption: All BLE communication uses ECDH key exchange. Data encrypted at rest (AES-256), in transit (TLS 1.3), and on-chain (encrypted payloads).",
    "Revocable Consent: Users can revoke data sharing at any time through the app. Revocation propagates within 60 seconds. Historical data access follows the consent state at time of collection.",
    "Automated Swarm Check-In: When 3+ crew devices mutually detect each other within geofence boundaries during shift window, system triggers automatic check-in for all corroborated crew. No manual scan, tap, or QR code required.",
    "Alibi Engine: Continuous tamper-proof location trail stored on IOTA Tangle. Creates cryptographic proof of crew location at any point in time. Designed for crew defense against false accusations (theft, damage, unauthorized entry).",
    "Consent-Gated Access: Tier 1 (System) - automated swarm operations, no human access. Tier 2 (Company Roster) - basic check-in/out status only. Tier 3 (Company+Consent) - detailed location with crew opt-in. Tier 4 (Crew Incident Consent) - full data for crew-initiated incident defense. Tier 5 (Legal/Court Order) - complete data release under valid court order.",
]
for i, step in enumerate(steps, 1):
    numbered_item(pdf, i, step)

check_page_space(pdf, 50)
sub_title(pdf, "Inputs")
headers = ["Field", "Type", "Source", "Required"]
widths = [45, 30, 60, 55]
table_header(pdf, headers, widths)
inputs = [
    ("device_uuid", "UUID v4", "Device Secure Enclave", "Required"),
    ("temp_uuid", "UUID v4", "Daily rotation algorithm", "Required"),
    ("kyc_document_hash", "SHA-256", "KYC Provider API", "Required"),
    ("ble_rssi", "Integer (dBm)", "BLE Radio", "Required"),
    ("contact_duration", "Integer (seconds)", "Device Timer", "Required"),
    ("gps_coordinates", "Float lat/lng", "Device GPS", "Required"),
    ("geofence_id", "UUID", "Geofence Service", "Required"),
    ("consent_tier", "Enum (1-5)", "User Settings", "Required"),
    ("encryption_key", "AES-256 Key", "Secure Enclave", "Required"),
]
for i, row in enumerate(inputs):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 50)
pdf.ln(3)
sub_title(pdf, "Outputs")
headers = ["Field", "Type", "Destination"]
widths = [50, 35, 105]
table_header(pdf, headers, widths)
outputs = [
    ("roster_status", "Enum (CHECKED_IN/OUT)", "Roster Core Service + IOTA Tangle"),
    ("proximity_log_hash", "SHA-256", "IOTA Tangle (encrypted)"),
    ("swarm_check_in_event", "JSON Event", "Event Bus -> Check-In Service"),
    ("alibi_proof", "Cryptographic Proof", "IOTA Tangle (crew-accessible)"),
    ("contact_summary", "JSON", "Encrypted local storage + Tangle"),
    ("consent_audit_log", "JSON", "Compliance Service"),
]
for i, row in enumerate(outputs):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 50)
pdf.ln(3)
sub_title(pdf, "API Endpoints")
api_endpoint(pdf, "POST", "/api/v1/ble/register",
    "{device_id, kyc_hash, public_key}", "201: {uuid, temp_uuid, rotation_schedule}",
    "Creates KYC binding, schedules first rotation")
api_endpoint(pdf, "POST", "/api/v1/ble/rotate",
    "{device_id, current_temp_uuid}", "200: {new_temp_uuid, valid_until}",
    "Archives old UUID mapping, generates new temp UUID")
api_endpoint(pdf, "POST", "/api/v1/ble/submit-log",
    "{encrypted_payload, tangle_address, timestamp}", "202: {tangle_tx_hash, status}",
    "Submits encrypted log to IOTA Tangle")
api_endpoint(pdf, "GET", "/api/v1/ble/swarm-status/{geofence_id}",
    None, "200: {crew_count, checked_in[], pending[], timestamp}",
    None)
api_endpoint(pdf, "POST", "/api/v1/ble/consent",
    "{crew_id, consent_tier, effective_from}", "200: {consent_id, status}",
    "Updates consent tier, propagates to all services within 60s")
api_endpoint(pdf, "GET", "/api/v1/ble/alibi/{crew_id}",
    None, "200: {alibi_chain[], proof_hashes[], time_range}",
    "Requires consent tier 4+ or court order")

check_page_space(pdf, 50)
sub_title(pdf, "Data Model")
headers = ["Column", "Type", "Constraints"]
widths = [50, 40, 100]
table_header(pdf, headers, widths, PURPLE)
cols = [
    ("id", "UUID PRIMARY KEY", "Auto-generated"),
    ("device_id", "UUID NOT NULL", "FK -> devices.id, UNIQUE"),
    ("master_uuid", "UUID NOT NULL", "Generated from secure enclave"),
    ("current_temp_uuid", "UUID NOT NULL", "Rotated daily at 00:00 UTC"),
    ("kyc_hash", "VARCHAR(64)", "SHA-256 of KYC verification"),
    ("consent_tier", "SMALLINT DEFAULT 1", "CHECK (1-5)"),
    ("last_rotation", "TIMESTAMPTZ", "NOT NULL"),
    ("swarm_status", "VARCHAR(20)", "CHECK IN (CHECKED_IN, CHECKED_OUT, PENDING)"),
    ("geofence_id", "UUID", "FK -> geofences.id, NULLABLE"),
    ("created_at", "TIMESTAMPTZ", "DEFAULT NOW()"),
    ("updated_at", "TIMESTAMPTZ", "DEFAULT NOW(), trigger on update"),
]
for i, row in enumerate(cols):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 40)
pdf.ln(3)
sub_title(pdf, "Business Rules")
rules = [
    "BR-1.01: UUID rotation MUST occur every 24 hours at 00:00 UTC. Devices that fail rotation are flagged STALE after 25 hours.",
    "BR-1.02: Swarm check-in requires exactly 3 or more mutual detections within geofence. Two-device corroboration is insufficient.",
    "BR-1.03: BLE contact logging requires minimum 30-second continuous detection (RSSI > -80 dBm) to count as a valid contact.",
    "BR-1.04: Alibi Engine data is immutable once written to Tangle. No administrative override can alter historical alibi records.",
    "BR-1.05: Consent revocation MUST propagate to all consuming services within 60 seconds. Failure triggers compliance alert.",
    "BR-1.06: Geofenced BLE activation means scanning ONLY operates within property geofence. BLE advertising stops within 30s of departing geofence.",
    "BR-1.07: Encrypted contact logs are retained for 14 days on-device, 90 days on Tangle. Retention is configurable per program.",
    "BR-1.08: Legal/Court Order access (Tier 5) requires verified court order document + compliance officer approval + crew notification.",
]
for rule in rules:
    bullet(pdf, rule)

check_page_space(pdf, 30)
sub_title(pdf, "Integration Points")
integrations = [
    "Domain 3 (Geofence): BLE activation/deactivation triggered by geofence entry/exit events.",
    "Domain 4 (Check-In): Swarm check-in events feed directly into check-in service for roster update.",
    "Domain 2 (Fraud Detection): BLE proximity data provides behavioral baseline for anomaly detection.",
    "Domain 9 (Compliance): Consent management, audit logs, and anonymization policies enforced.",
    "Domain 10 (Check-Off): Swarm roster data used by supervisors during daily verification.",
]
for item in integrations:
    bullet(pdf, item)

check_page_space(pdf, 50)
sub_title(pdf, "User Stories")
# 10 user stories for Domain 1
user_story(pdf, "1.01", "crew member",
    "to have my device automatically register with the BLE swarm when I arrive at a property",
    "I do not need to manually check in and my presence is verified by peer devices",
    "a crew member has a registered device with valid KYC", "they enter a geofenced property with 3+ other crew",
    "system auto-checks them in within 60 seconds and confirms via push notification",
    "Must", "Phase 2 - Week 5")
user_story(pdf, "1.02", "system administrator",
    "BLE UUIDs to rotate every 24 hours automatically",
    "crew member privacy is protected and tracking across days is prevented",
    "a device has an active UUID", "midnight UTC occurs",
    "new temp UUID is generated, old mapping archived, and device begins broadcasting new UUID within 5 seconds",
    "Must", "Phase 2 - Week 4")
user_story(pdf, "1.03", "crew member",
    "to control my consent tier at any time through the app",
    "I maintain full control over who can access my location and proximity data",
    "a crew member is logged into the mobile app", "they change consent tier from 2 to 1",
    "consent change propagates to all services within 60 seconds and confirmation is displayed",
    "Must", "Phase 2 - Week 5")
user_story(pdf, "1.04", "crew member",
    "an Alibi Engine that creates tamper-proof location proofs",
    "I can defend myself against false accusations with cryptographic evidence",
    "crew member is on-property with active BLE", "an incident is reported",
    "crew member can retrieve alibi proof showing location chain from IOTA Tangle",
    "Should", "Phase 2 - Week 6")
user_story(pdf, "1.05", "compliance officer",
    "all BLE contact logs to be encrypted end-to-end with AES-256",
    "sensitive proximity data cannot be intercepted or read by unauthorized parties",
    "contact logs are being generated", "logs are transmitted or stored",
    "all payloads are encrypted with AES-256-GCM and decryption requires authorized key access",
    "Must", "Phase 2 - Week 4")
user_story(pdf, "1.06", "operations manager",
    "to query swarm roster status for a geofenced property",
    "I can see real-time crew presence without accessing individual location data",
    "multiple crew are within a geofenced property", "ops manager queries swarm status",
    "API returns crew count, check-in status list, and timestamp -- no raw contact data",
    "Must", "Phase 2 - Week 5")
user_story(pdf, "1.07", "system",
    "to submit encrypted proximity logs to IOTA Tangle as zero-value transactions",
    "audit trail is immutable, feeless, and quantum-resistant",
    "device has aggregated 15-minute proximity summary", "submission interval is reached",
    "encrypted payload is submitted to Tangle and transaction hash is returned within 10 seconds",
    "Must", "Phase 2 - Week 5")
user_story(pdf, "1.08", "crew supervisor",
    "to see which crew members have been auto-checked-in via swarm detection",
    "I can verify that the swarm system is working and identify any crew who need manual check-in",
    "supervisor opens the daily roster view", "swarm check-ins have occurred",
    "check-in entries show source=SWARM with corroboration count and timestamp",
    "Should", "Phase 2 - Week 6")
user_story(pdf, "1.09", "legal counsel",
    "to access complete BLE proximity data under a valid court order",
    "lawful data requests can be fulfilled while maintaining the consent framework",
    "valid court order has been submitted and verified", "compliance officer approves Tier 5 access",
    "full decrypted proximity data is provided for specified crew and date range, crew is notified",
    "Could", "Phase 2 - Week 7")
user_story(pdf, "1.10", "crew member",
    "BLE tracking to automatically stop when I leave the property geofence",
    "my location is never tracked outside of work premises",
    "crew member is within geofence with active BLE", "they depart and exit geofence boundary",
    "BLE scanning ceases within 30 seconds, final contact log is submitted, and device confirms tracking stopped",
    "Must", "Phase 2 - Week 5")


# ---- DOMAIN 2: AI FRAUD DETECTION ----
add_domain_header(pdf, 2, "AI FRAUD DETECTION SYSTEM", TEAL)

sub_title(pdf, "Domain Overview")
body_text(pdf, "The AI Fraud Detection System provides continuous, real-time monitoring of all roster events across four threat dimensions: geographic, temporal, financial, and behavioral. Machine learning models trained on historical data establish baselines for each crew member and property, scoring every event against those baselines. Events are classified into four threat tiers (Standard, Enhanced, Suspicious, Critical) with configurable thresholds per property and program. Fraud alerts are automatically routed to the appropriate response team based on severity and type.")

sub_title(pdf, "Process Flow")
steps = [
    "Real-Time Data Collection: All check-in events, geofence transitions, BLE contacts, authorization requests, and time tracking data are streamed to the fraud detection pipeline via event bus.",
    "Geographic Anomaly Detection: Each event is evaluated against: (a) expected property geofence, (b) historical location patterns, (c) known impossible locations (crew at two properties simultaneously).",
    "Identity Verification Checks: Multi-factor verification score computed from: device fingerprint match, BLE swarm corroboration, QR code validation, face recognition confidence score.",
    "Velocity Checks: System calculates travel time between consecutive events. If time between events at different locations is less than minimum possible travel time, flag as IMPOSSIBLE_TRAVEL.",
    "Behavioral Anomaly Detection: ML model compares current behavior against 30-day rolling baseline. Features: check-in time variance, duration patterns, room assignment consistency, contact graph stability.",
    "Threat Classification: Standard (score 0-25) - normal operations, log only. Enhanced (score 26-50) - minor deviation, flag for review. Suspicious (score 51-75) - significant anomaly, alert supervisor. Critical (score 76-100) - probable fraud, alert compliance + security + operations.",
    "Configurable Alert Thresholds: Each property/program can adjust scoring weights and tier boundaries. Default thresholds can be overridden by program administrators.",
    "Machine Learning Model Training: Models retrained weekly on labeled data. Feedback loop: analyst-confirmed true/false positives improve model accuracy. Target: <5% false positive rate.",
    "Fraud Alert Generation and Routing: Alerts generated with full context (event data, score breakdown, recommended action). Routing: ops team for Standard/Enhanced, supervisor + ops for Suspicious, compliance + security + command for Critical.",
    "Compliance Reporting: Automated weekly fraud summary reports. Monthly trend analysis. Quarterly regulatory compliance reports with detection statistics.",
    "Continuous Monitoring: 24/7 automated scanning with no downtime windows. System health dashboard monitors model performance, alert volumes, and response times.",
    "Real-Time Alerting: Multi-channel delivery: push notification, SMS, email, dashboard widget, Microsoft Teams webhook. Alert priority determines channel selection and escalation timing.",
]
for i, step in enumerate(steps, 1):
    numbered_item(pdf, i, step)

check_page_space(pdf, 50)
sub_title(pdf, "Inputs")
headers = ["Field", "Type", "Source", "Required"]
widths = [45, 30, 60, 55]
table_header(pdf, headers, widths)
inputs = [
    ("event_type", "Enum", "Event Bus", "Required"),
    ("crew_id", "UUID", "Auth Service", "Required"),
    ("property_id", "UUID", "Roster Core", "Required"),
    ("gps_lat_lng", "Float pair", "Device GPS", "Required"),
    ("timestamp", "TIMESTAMPTZ", "Event source", "Required"),
    ("device_fingerprint", "VARCHAR(128)", "Device", "Required"),
    ("ble_corroboration", "Integer", "BLE Swarm", "Optional"),
    ("face_confidence", "Float 0-1", "FRS", "Optional"),
    ("historical_baseline", "JSON", "ML Model Store", "Required"),
]
for i, row in enumerate(inputs):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 50)
pdf.ln(3)
sub_title(pdf, "API Endpoints")
api_endpoint(pdf, "POST", "/api/v1/fraud/evaluate",
    "{event_type, crew_id, property_id, event_data}", "200: {score, tier, factors[], recommended_action}",
    "Logs evaluation, triggers alert if tier >= Suspicious")
api_endpoint(pdf, "GET", "/api/v1/fraud/alerts?property_id=X&tier=Y&from=Z&to=W",
    None, "200: {alerts[], total_count, page, per_page}",
    None)
api_endpoint(pdf, "PUT", "/api/v1/fraud/alerts/{alert_id}/resolve",
    "{resolution, analyst_id, is_true_positive}", "200: {alert_id, status: RESOLVED}",
    "Feeds back to ML model training pipeline")
api_endpoint(pdf, "GET", "/api/v1/fraud/model/performance",
    None, "200: {accuracy, precision, recall, f1, false_positive_rate, last_trained}",
    None)
api_endpoint(pdf, "POST", "/api/v1/fraud/thresholds",
    "{property_id, tier_boundaries, weight_overrides}", "200: {threshold_id, effective_from}",
    "Updates property-specific scoring configuration")

check_page_space(pdf, 50)
sub_title(pdf, "Data Model: fraud_events")
headers = ["Column", "Type", "Constraints"]
widths = [50, 40, 100]
table_header(pdf, headers, widths, PURPLE)
cols = [
    ("id", "UUID PRIMARY KEY", "Auto-generated"),
    ("crew_id", "UUID NOT NULL", "FK -> crew_profiles.id"),
    ("property_id", "UUID NOT NULL", "FK -> properties.id"),
    ("event_type", "VARCHAR(50)", "NOT NULL"),
    ("fraud_score", "DECIMAL(5,2)", "CHECK (0-100)"),
    ("threat_tier", "VARCHAR(20)", "CHECK IN (STANDARD,ENHANCED,SUSPICIOUS,CRITICAL)"),
    ("factors", "JSONB", "Score breakdown by dimension"),
    ("gps_coordinates", "POINT", "PostGIS geometry"),
    ("resolved", "BOOLEAN", "DEFAULT FALSE"),
    ("resolution_notes", "TEXT", "NULLABLE"),
    ("created_at", "TIMESTAMPTZ", "DEFAULT NOW()"),
]
for i, row in enumerate(cols):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 40)
pdf.ln(3)
sub_title(pdf, "Business Rules")
rules = [
    "BR-2.01: Every roster event MUST be scored within 500ms of receipt. Events exceeding SLA are logged as SCORING_TIMEOUT.",
    "BR-2.02: Impossible travel is defined as distance / time > 200 km/h for ground, 900 km/h for air (with 2-hour airport buffer).",
    "BR-2.03: Critical alerts MUST be delivered to compliance within 30 seconds. Delivery failure triggers escalation to on-call security.",
    "BR-2.04: ML models MUST maintain false positive rate below 5%. If rate exceeds 5% for 7 consecutive days, model is rolled back.",
    "BR-2.05: Property-specific threshold overrides require program administrator approval and are audited.",
    "BR-2.06: All fraud evaluations are retained for 7 years for regulatory compliance.",
]
for rule in rules:
    bullet(pdf, rule)

sub_title(pdf, "Integration Points")
integrations = [
    "Domain 1 (BLE Swarm): Receives swarm corroboration data as fraud scoring input.",
    "Domain 3 (Geofence): Geofence events are primary input for geographic anomaly detection.",
    "Domain 4 (Check-In): Every check-in event is scored by fraud detection before finalization.",
    "Domain 7 (Supervisors): Suspicious/Critical alerts are routed to supervisor dashboards.",
    "Domain 9 (Compliance): Fraud reports feed into compliance reporting pipeline.",
]
for item in integrations:
    bullet(pdf, item)

check_page_space(pdf, 50)
sub_title(pdf, "User Stories")
user_story(pdf, "2.01", "operations manager",
    "to receive real-time fraud alerts when crew check-ins show geographic anomalies",
    "I can investigate potential fraud immediately and protect program integrity",
    "a crew member checks in", "their GPS location is outside the property geofence by >100 meters",
    "fraud alert is generated with score >= 51 (Suspicious) and pushed to ops dashboard within 30 seconds",
    "Must", "Phase 2 - Week 6")
user_story(pdf, "2.02", "compliance officer",
    "automated weekly fraud summary reports",
    "I can monitor program integrity and provide evidence to auditors",
    "one or more fraud events occurred during the week", "Monday 06:00 UTC arrives",
    "report is generated with all events grouped by tier, property, and type, delivered via email",
    "Must", "Phase 2 - Week 7")
user_story(pdf, "2.03", "system",
    "to detect impossible travel scenarios in real-time",
    "crew who attempt to check in at two distant properties in rapid succession are flagged",
    "crew checked in at Property A at time T1", "crew attempts check-in at Property B at time T2 where travel time is impossible",
    "check-in is flagged as CRITICAL, alert sent to security, check-in held pending review",
    "Must", "Phase 2 - Week 6")
user_story(pdf, "2.04", "fraud analyst",
    "to resolve fraud alerts and provide feedback that improves the ML model",
    "the system continuously improves its detection accuracy",
    "a fraud alert is open", "analyst marks it as true positive or false positive with notes",
    "resolution is recorded, label is added to training data, and model retraining includes this feedback",
    "Should", "Phase 2 - Week 7")
user_story(pdf, "2.05", "program administrator",
    "to configure fraud detection thresholds per property",
    "properties with unique characteristics can have tuned detection without false positives",
    "admin has program administrator role", "they adjust tier boundaries for a property",
    "new thresholds take effect immediately, change is audit-logged, and existing open alerts are rescored",
    "Should", "Phase 2 - Week 8")
user_story(pdf, "2.06", "security team",
    "Critical-tier fraud alerts delivered via SMS and Teams within 30 seconds",
    "the highest-severity threats get immediate human attention",
    "a fraud event scores 76+", "alert is generated",
    "SMS sent to on-call security, Teams message posted to security channel, dashboard shows red alert -- all within 30s",
    "Must", "Phase 2 - Week 6")
user_story(pdf, "2.07", "data scientist",
    "to monitor ML model performance metrics in real-time",
    "I can detect model degradation before it impacts detection quality",
    "ML model is in production", "data scientist opens model performance dashboard",
    "current accuracy, precision, recall, F1, and false positive rate are displayed with 7-day trend",
    "Should", "Phase 2 - Week 8")
user_story(pdf, "2.08", "system",
    "to automatically roll back ML models when false positive rate exceeds 5%",
    "degraded models do not flood operators with false alerts",
    "current model FPR has exceeded 5% for 7 days", "daily model health check runs",
    "model is rolled back to previous version, ops team notified, and incident is logged",
    "Must", "Phase 2 - Week 7")


# ---- DOMAIN 3: GEOFENCE EVENT STATE MACHINE ----
add_domain_header(pdf, 3, "GEOFENCE EVENT STATE MACHINE", EMERALD)

sub_title(pdf, "Domain Overview")
body_text(pdf, "The Geofence Event State Machine manages the lifecycle of crew presence at properties through GPS and BLE boundary detection. It serves as the primary trigger for roster status changes -- when a crew device crosses a geofence boundary, the state machine initiates authentication, verification, and roster update processes. The geofence also controls BLE activation scope: swarm tracking is ONLY active within property boundaries and ceases when crew depart. This ensures no off-premises surveillance occurs.")

sub_title(pdf, "Process Flow")
steps = [
    "Crew Member Device Enters Geofence: GPS and/or BLE beacon detects device crossing property boundary. Dual-mode detection (GPS + BLE) reduces false positives from GPS drift.",
    "Authentication Processing: Device identity is verified against registered devices database. Multi-factor: device certificate + crew session token + BLE device fingerprint.",
    "Database/Card Verification: System checks crew assignment for this property on this date. Verifies: active assignment exists, assignment dates include today, property matches.",
    "Roster Update on Geofence Entry: If verified, crew status for this property transitions to ON_PREMISES. Timestamp, GPS coordinates, and entry method (GPS/BLE/both) are recorded.",
    "Crew Supervisor Override: Supervisors can manually override geofence status when: GPS is unreliable, device malfunction, or legitimate exceptions. Override requires supervisor PIN + reason code.",
    "Validation and NFI Check: No Further Information check ensures all required data is present. If any required field is missing, event is held in PENDING state until resolved.",
    "Roster System Update: Verified geofence event is pushed to Roster Core (Domain 8) for master roster sync. Event also published to event bus for downstream consumers.",
    "Logging and Compliance: All geofence events (entry, exit, override, failure) are logged with full metadata. Logs include: crew_id, property_id, timestamp, GPS, event_type, auth_result.",
    "Departure Detection: When device GPS leaves geofence boundary for >60 seconds, exit event is triggered. BLE beacon loss (no beacon detected for 120 seconds) also triggers exit. Status transitions to OFF_PREMISES.",
    "Geofenced BLE Activation: On geofence entry, BLE swarm scanning is activated. On geofence exit, BLE scanning is deactivated within 30 seconds. This ensures proximity tracking never extends beyond property bounds.",
]
for i, step in enumerate(steps, 1):
    numbered_item(pdf, i, step)

check_page_space(pdf, 50)
sub_title(pdf, "Inputs")
headers = ["Field", "Type", "Source", "Required"]
widths = [45, 30, 60, 55]
table_header(pdf, headers, widths)
inputs = [
    ("device_id", "UUID", "Device", "Required"),
    ("gps_lat", "DECIMAL(10,7)", "Device GPS", "Required"),
    ("gps_lng", "DECIMAL(10,7)", "Device GPS", "Required"),
    ("gps_accuracy", "Float (meters)", "Device GPS", "Required"),
    ("geofence_id", "UUID", "Geofence Config", "Required"),
    ("ble_beacon_ids", "UUID[]", "BLE Scanner", "Optional"),
    ("crew_session_token", "JWT", "Auth Service", "Required"),
    ("override_pin", "VARCHAR(6)", "Supervisor Input", "Optional"),
    ("override_reason", "Enum", "Supervisor Input", "Conditional"),
]
for i, row in enumerate(inputs):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 40)
pdf.ln(3)
sub_title(pdf, "API Endpoints")
api_endpoint(pdf, "POST", "/api/v1/geofence/event",
    "{device_id, gps_lat, gps_lng, geofence_id, event_type}", "201: {event_id, status, ble_activated}",
    "Triggers auth pipeline, activates/deactivates BLE")
api_endpoint(pdf, "POST", "/api/v1/geofence/override",
    "{supervisor_id, crew_id, property_id, override_type, reason, pin}", "200: {override_id, new_status}",
    "Logs override with full audit trail")
api_endpoint(pdf, "GET", "/api/v1/geofence/status/{property_id}",
    None, "200: {on_premises[], off_premises[], pending[], last_updated}",
    None)
api_endpoint(pdf, "GET", "/api/v1/geofence/events?crew_id=X&date=Y",
    None, "200: {events[], entry_time, exit_time, duration_minutes}",
    None)

check_page_space(pdf, 50)
sub_title(pdf, "Data Model: geofence_events")
headers = ["Column", "Type", "Constraints"]
widths = [50, 40, 100]
table_header(pdf, headers, widths, PURPLE)
cols = [
    ("id", "UUID PRIMARY KEY", "Auto-generated"),
    ("crew_id", "UUID NOT NULL", "FK -> crew_profiles.id"),
    ("property_id", "UUID NOT NULL", "FK -> properties.id"),
    ("geofence_id", "UUID NOT NULL", "FK -> geofences.id"),
    ("event_type", "VARCHAR(20)", "CHECK IN (ENTRY, EXIT, OVERRIDE)"),
    ("gps_point", "POINT NOT NULL", "PostGIS geometry"),
    ("gps_accuracy_m", "DECIMAL(6,2)", "Meters"),
    ("ble_confirmed", "BOOLEAN", "DEFAULT FALSE"),
    ("auth_result", "VARCHAR(20)", "PASS, FAIL, OVERRIDE"),
    ("status_after", "VARCHAR(20)", "ON_PREMISES, OFF_PREMISES, PENDING"),
    ("override_by", "UUID", "FK -> supervisors.id, NULLABLE"),
    ("override_reason", "VARCHAR(100)", "NULLABLE"),
    ("created_at", "TIMESTAMPTZ", "DEFAULT NOW()"),
]
for i, row in enumerate(cols):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 40)
pdf.ln(3)
sub_title(pdf, "Business Rules")
rules = [
    "BR-3.01: Geofence entry requires GPS accuracy < 50 meters. Events with accuracy > 50m are held in PENDING until better fix obtained or supervisor override.",
    "BR-3.02: Departure detection requires GPS outside boundary for >= 60 continuous seconds to prevent false exits from GPS drift.",
    "BR-3.03: BLE beacon loss triggers exit only after 120 seconds of no beacon detection (accounts for temporary signal obstruction).",
    "BR-3.04: Supervisor overrides are limited to 3 per crew per day. Fourth override requires operations manager approval.",
    "BR-3.05: BLE activation on geofence entry MUST complete within 5 seconds. BLE deactivation on exit MUST complete within 30 seconds.",
    "BR-3.06: All geofence events are logged regardless of auth result. Failed auth events trigger fraud scoring.",
]
for rule in rules:
    bullet(pdf, rule)

sub_title(pdf, "User Stories")
user_story(pdf, "3.01", "crew member",
    "my device to automatically detect when I arrive at my assigned property",
    "I do not need to remember to manually check in and my presence is immediately recorded",
    "crew member has an active assignment for Property X today", "their device GPS enters Property X geofence",
    "entry event is created, authentication runs, and status transitions to ON_PREMISES within 10 seconds",
    "Must", "Phase 1 - Week 2")
user_story(pdf, "3.02", "crew supervisor",
    "to override geofence status when crew GPS is unreliable",
    "legitimate crew are not blocked from working due to technical issues",
    "crew member is physically present but GPS shows them outside geofence", "supervisor enters PIN and selects reason code DEVICE_GPS_UNRELIABLE",
    "geofence status is overridden to ON_PREMISES, override is logged with supervisor ID and reason",
    "Must", "Phase 1 - Week 3")
user_story(pdf, "3.03", "operations manager",
    "to see real-time property occupancy based on geofence data",
    "I can monitor crew deployment across all properties at a glance",
    "multiple crew are assigned to multiple properties", "ops manager opens property status dashboard",
    "each property shows on_premises count, off_premises count, and pending count in real-time",
    "Must", "Phase 1 - Week 3")
user_story(pdf, "3.04", "system",
    "to activate BLE scanning only within geofence boundaries",
    "crew privacy is protected by ensuring no off-premises surveillance",
    "crew device enters geofence", "entry event is confirmed",
    "BLE scanning starts within 5 seconds; on geofence exit, BLE stops within 30 seconds",
    "Must", "Phase 1 - Week 3")
user_story(pdf, "3.05", "compliance officer",
    "a complete audit log of all geofence events including overrides",
    "we can demonstrate regulatory compliance and investigate incidents",
    "geofence events have occurred during the day", "compliance officer queries audit log for a property/date",
    "all events returned with full metadata: crew, time, GPS, auth result, override details if applicable",
    "Must", "Phase 1 - Week 3")
user_story(pdf, "3.06", "crew member",
    "my departure from a property to be automatically detected",
    "my work hours are accurately tracked and I do not need to remember to check out",
    "crew member is ON_PREMISES at Property X", "their device GPS exits geofence for >= 60 seconds",
    "exit event is created, status transitions to OFF_PREMISES, work duration is calculated",
    "Must", "Phase 1 - Week 2")


# ---- DOMAIN 4: ROSTER CHECK-IN PROCESS ----
add_domain_header(pdf, 4, "ROSTER CHECK-IN PROCESS", GOLD)

sub_title(pdf, "Domain Overview")
body_text(pdf, "The Roster Check-In Process is the core operational workflow of GoCrew. It defines the 12-step verification chain that every crew member passes through when checking into a lodging property. The process layers multiple verification methods (BLE beacon, GPS geofence, QR code, database assignment, identity match) to create a high-confidence check-in that is resistant to fraud and provides a complete audit trail. This is the Phase 1 MVP -- the minimum viable product that delivers immediate operational value.")

sub_title(pdf, "12-Step Process Flow")
steps = [
    "Crew Arrival at Property: Crew member physically arrives at assigned lodging property. Mobile app is open or running in background with location services enabled.",
    "BLE Beacon Detection: Lobby BLE beacon detects crew device within range (< 10 meters). Beacon UUID is matched against property beacon registry. Confirms physical presence in property lobby.",
    "Device Authentication: Crew device presents its device certificate and session JWT to the check-in service. Certificate is validated against device registry. Session JWT is verified for expiry and crew identity.",
    "Geofence GPS Confirmation: Secondary location verification via GPS. Device GPS coordinates must fall within property geofence polygon. GPS accuracy must be < 50 meters for valid confirmation.",
    "Database Assignment Check: System queries roster_assignments table for: crew_id + property_id + current_date. Assignment must exist, be in ACTIVE status, and have date range including today.",
    "QR Code Verification: Crew member scans property QR code displayed at front desk or lobby. QR contains signed JWT with property_id, date, and nonce. JWT signature verified against property's public key. Nonce prevents replay attacks.",
    "Identity Match: Crew ID (from device auth) is matched against roster assignment. If face recognition is enabled (Domain 6), camera captures crew face and compares against enrolled photo. Minimum confidence threshold: 95%.",
    "Room Number Confirmation: Crew member enters their assigned room number via numeric keypad in app. Double-entry required (enter twice, must match). Digits only validation. Room number checked against assignment record.",
    "Roster Status Update: If all prior steps pass, crew status is updated to CHECKED_IN. Metadata recorded: timestamp, property_id, room_number, check-in method, verification scores.",
    "Supervisor Notification: Push notification sent to assigned supervisor (onsite or offsite). Notification includes: crew name, property, room, check-in time, verification score. If supervisor has multiple crew checking in, notifications are batched (5-minute window).",
    "Compliance Validation: Final validation pass ensures all required fields are populated. Check: no active fraud alerts, no expired certifications, no missing KYC. If any flag exists, check-in is marked FLAGGED (not rejected) and compliance is notified.",
    "Final Event Logging: Complete check-in event written to PostgreSQL (operational data). Event hash written to IOTA Tangle (immutable audit trail). Event published to event bus for downstream consumers (fraud, analytics, billing).",
]
for i, step in enumerate(steps, 1):
    numbered_item(pdf, i, step)

check_page_space(pdf, 50)
sub_title(pdf, "Inputs")
headers = ["Field", "Type", "Source", "Required"]
widths = [45, 30, 60, 55]
table_header(pdf, headers, widths)
inputs = [
    ("crew_id", "UUID", "Device Auth", "Required"),
    ("device_certificate", "X.509", "Device Secure Enclave", "Required"),
    ("session_jwt", "JWT", "Auth Service", "Required"),
    ("property_id", "UUID", "BLE Beacon / QR", "Required"),
    ("gps_coordinates", "POINT", "Device GPS", "Required"),
    ("qr_jwt", "JWT", "Property QR Code", "Required"),
    ("room_number", "VARCHAR(10)", "Crew Input", "Required"),
    ("room_number_confirm", "VARCHAR(10)", "Crew Input (2nd entry)", "Required"),
    ("ble_beacon_uuid", "UUID", "BLE Scanner", "Required"),
    ("face_image", "BLOB", "Device Camera", "Optional"),
]
for i, row in enumerate(inputs):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 40)
pdf.ln(3)
sub_title(pdf, "Outputs")
headers = ["Field", "Type", "Destination"]
widths = [50, 35, 105]
table_header(pdf, headers, widths)
outputs = [
    ("check_in_event", "JSON", "PostgreSQL + Event Bus"),
    ("check_in_hash", "SHA-256", "IOTA Tangle"),
    ("roster_status", "CHECKED_IN", "Roster Core (Domain 8)"),
    ("supervisor_notification", "Push/SMS", "Supervisor App (Domain 7)"),
    ("fraud_score", "DECIMAL", "Fraud Detection (Domain 2)"),
    ("compliance_flag", "BOOLEAN", "Compliance Service (Domain 9)"),
]
for i, row in enumerate(outputs):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 50)
pdf.ln(3)
sub_title(pdf, "API Endpoints")
api_endpoint(pdf, "POST", "/api/v1/checkin/initiate",
    "{crew_id, property_id, device_cert, gps, ble_beacon_uuid}", "200: {session_id, steps_required[], status: IN_PROGRESS}",
    "Creates check-in session, begins verification pipeline")
api_endpoint(pdf, "POST", "/api/v1/checkin/{session_id}/qr",
    "{qr_jwt}", "200: {qr_valid, property_match, nonce_valid}",
    "Validates QR code JWT against property key")
api_endpoint(pdf, "POST", "/api/v1/checkin/{session_id}/room",
    "{room_number, room_number_confirm}", "200: {room_valid, assignment_match}",
    "Validates room number against assignment")
api_endpoint(pdf, "POST", "/api/v1/checkin/{session_id}/complete",
    "{face_image (optional)}", "201: {check_in_id, status, tangle_hash, fraud_score}",
    "Finalizes check-in, writes to DB + Tangle, notifies supervisor")
api_endpoint(pdf, "GET", "/api/v1/checkin/status/{crew_id}?date=YYYY-MM-DD",
    None, "200: {status, check_in_time, property_id, room, verification_scores}",
    None)

check_page_space(pdf, 50)
sub_title(pdf, "Data Model: check_in_events")
headers = ["Column", "Type", "Constraints"]
widths = [50, 40, 100]
table_header(pdf, headers, widths, PURPLE)
cols = [
    ("id", "UUID PRIMARY KEY", "Auto-generated"),
    ("crew_id", "UUID NOT NULL", "FK -> crew_profiles.id"),
    ("property_id", "UUID NOT NULL", "FK -> properties.id"),
    ("assignment_id", "UUID NOT NULL", "FK -> roster_assignments.id"),
    ("room_number", "VARCHAR(10)", "NOT NULL, digits only"),
    ("check_in_time", "TIMESTAMPTZ", "NOT NULL"),
    ("check_out_time", "TIMESTAMPTZ", "NULLABLE"),
    ("status", "VARCHAR(20)", "CHECK IN (CHECKED_IN, CHECKED_OUT, FLAGGED, FAILED)"),
    ("ble_confirmed", "BOOLEAN", "NOT NULL"),
    ("gps_confirmed", "BOOLEAN", "NOT NULL"),
    ("qr_confirmed", "BOOLEAN", "NOT NULL"),
    ("face_confidence", "DECIMAL(4,3)", "NULLABLE, CHECK (0-1)"),
    ("fraud_score", "DECIMAL(5,2)", "CHECK (0-100)"),
    ("tangle_hash", "VARCHAR(64)", "IOTA transaction hash"),
    ("created_at", "TIMESTAMPTZ", "DEFAULT NOW()"),
]
for i, row in enumerate(cols):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 40)
pdf.ln(3)
sub_title(pdf, "Business Rules")
rules = [
    "BR-4.01: All 12 steps must complete for a CHECKED_IN status. Partial completion results in PENDING or FAILED.",
    "BR-4.02: Room number double-entry must match exactly. Mismatch resets both fields and requires re-entry.",
    "BR-4.03: QR code nonce is single-use and expires after 5 minutes. Reuse attempt triggers fraud alert.",
    "BR-4.04: GPS accuracy > 50 meters does not block check-in but is flagged for review. BLE confirmation can compensate.",
    "BR-4.05: Face recognition confidence < 95% does not block check-in but triggers Enhanced fraud tier.",
    "BR-4.06: Check-in session timeout is 10 minutes from initiation. Expired sessions must restart from step 1.",
    "BR-4.07: Supervisor notifications are batched in 5-minute windows to prevent notification overload.",
    "BR-4.08: A crew member can only have one active check-in per property per day. Duplicate attempts are rejected.",
]
for rule in rules:
    bullet(pdf, rule)

sub_title(pdf, "User Stories")
user_story(pdf, "4.01", "crew member",
    "to check in at my assigned property using my mobile device",
    "my presence is officially recorded and I am confirmed as on-site",
    "crew member has active assignment for this property today", "they complete the 12-step check-in process",
    "status is CHECKED_IN, supervisor is notified, and event is logged to database and IOTA Tangle",
    "Must", "Phase 1 - Week 1")
user_story(pdf, "4.02", "crew member",
    "to scan a QR code at the property front desk as part of check-in",
    "there is a physical verification step that confirms I am at the specific property",
    "crew is at step 6 of check-in", "they scan the property QR code",
    "QR JWT is validated, property_id matches, nonce is consumed, and step 6 is marked complete",
    "Must", "Phase 1 - Week 1")
user_story(pdf, "4.03", "crew member",
    "to confirm my room number with double-entry validation",
    "room assignment errors are prevented by requiring me to enter the number twice",
    "crew is at step 8 of check-in", "they enter room 412 twice",
    "both entries match, room 412 matches assignment record, step 8 is marked complete",
    "Must", "Phase 1 - Week 1")
user_story(pdf, "4.04", "crew supervisor",
    "to receive a notification when my crew members check in",
    "I know when my team is on-site and can monitor arrival patterns",
    "supervisor has crew assigned to a property", "one or more crew complete check-in",
    "push notification is delivered within 5 minutes with crew name, property, room, and time",
    "Must", "Phase 1 - Week 2")
user_story(pdf, "4.05", "operations manager",
    "check-in events to be written to IOTA Tangle for tamper-proof auditing",
    "we have an immutable record that cannot be altered after the fact",
    "crew completes check-in successfully", "final event logging step executes",
    "event hash is submitted to IOTA Tangle and transaction hash is stored in check_in_events table",
    "Must", "Phase 1 - Week 2")
user_story(pdf, "4.06", "compliance officer",
    "check-ins to be validated against compliance requirements before finalization",
    "crew with expired certifications or active flags are identified at check-in time",
    "crew completes steps 1-11", "compliance validation runs at step 11",
    "if any compliance flag exists, check-in is marked FLAGGED (not rejected) and compliance team is notified",
    "Must", "Phase 1 - Week 2")
user_story(pdf, "4.07", "system",
    "to reject check-in attempts from crew not assigned to the property on this date",
    "unauthorized property access is prevented at the check-in level",
    "a crew member attempts check-in at Property X", "database assignment check (step 5) finds no active assignment",
    "check-in session is terminated with ASSIGNMENT_NOT_FOUND, crew sees error message, event is logged",
    "Must", "Phase 1 - Week 1")
user_story(pdf, "4.08", "system",
    "to score every check-in event through the fraud detection pipeline",
    "anomalous check-ins are identified in real-time",
    "check-in is being finalized", "all verification data is sent to fraud scoring",
    "fraud score is calculated, stored with check-in record, and alert generated if score >= 51",
    "Must", "Phase 1 - Week 3")


# ---- DOMAIN 5: LODGING AUTHORIZATION ----
add_domain_header(pdf, 5, "LODGING AUTHORIZATION", PURPLE)

sub_title(pdf, "Domain Overview")
body_text(pdf, "The Lodging Authorization domain manages the upstream process of approving crew lodging before they arrive at a property. It handles the full lifecycle from request submission through rate verification, availability checks, compliance pre-screening, supervisor approval, and finally generating the authorization number and purchase order that the hotel needs to accept the crew member. This domain is the gatekeeper that ensures every crew lodging assignment is financially authorized, compliant, and properly documented.")

sub_title(pdf, "Process Flow")
steps = [
    "Lodging Request Submission: Client or program manager initiates a lodging request specifying crew member(s), property, dates, room type, and program code. Request enters SUBMITTED status.",
    "Contract Rate Verification: System looks up the contracted rate for this property and room type. Requested rate is compared against contract ceiling. If requested rate > ceiling, request is flagged for manual rate negotiation.",
    "Property Availability Check: System queries property availability API (or cached inventory) for requested room type and dates. If unavailable, system suggests alternative properties within program parameters.",
    "Room Type Assignment: Based on crew count, accessibility needs, and program rules, room type is assigned: Single, Double, ADA-Accessible, Suite. Room type determines rate and per diem calculations.",
    "Tax Rate Lookup: System retrieves expected tax rate for the property's jurisdiction from a maintained reference table. Tax rates are broken down by: state tax, county tax, city tax, special district tax. Total expected tax is calculated for rate validation.",
    "Compliance Pre-Check: Property is screened against compliance databases: CrimeShield score (safety rating), certification status (required hotel certifications), risk level (based on incident history). Properties below compliance thresholds are flagged.",
    "Supervisor Authorization Sign-Off: Request is routed to the appropriate supervisor in the approval chain. Supervisor reviews all details and approves or rejects. Rejection requires reason code and notes.",
    "Authorization Number Generation: Upon approval, system generates a unique authorization number (format: AUTH-YYYYMMDD-XXXX). Auth number is the hotel's reference for accepting the crew member.",
    "PO Number Assignment: Purchase order number is generated and linked to the authorization. PO ties the lodging cost to the correct program budget and cost center.",
    "Hotel Notification: Authorization details are sent to the property via email/fax/API. Package includes: auth number, crew name, dates, room type, rate, PO number. Hotel confirms receipt and room hold.",
]
for i, step in enumerate(steps, 1):
    numbered_item(pdf, i, step)

check_page_space(pdf, 50)
sub_title(pdf, "Inputs")
headers = ["Field", "Type", "Source", "Required"]
widths = [45, 30, 60, 55]
table_header(pdf, headers, widths)
inputs = [
    ("crew_ids", "UUID[]", "Roster Core", "Required"),
    ("property_id", "UUID", "Property Registry", "Required"),
    ("check_in_date", "DATE", "Request Form", "Required"),
    ("check_out_date", "DATE", "Request Form", "Required"),
    ("room_type", "Enum", "Request Form", "Required"),
    ("program_code", "VARCHAR(20)", "Program Registry", "Required"),
    ("requested_rate", "DECIMAL(8,2)", "Request Form", "Optional"),
    ("contract_id", "UUID", "Contract Registry", "Required"),
    ("requestor_id", "UUID", "Auth Service", "Required"),
]
for i, row in enumerate(inputs):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 40)
pdf.ln(3)
sub_title(pdf, "API Endpoints")
api_endpoint(pdf, "POST", "/api/v1/authorization/request",
    "{crew_ids, property_id, dates, room_type, program_code}", "201: {request_id, status: SUBMITTED}",
    "Initiates rate verification and availability check pipeline")
api_endpoint(pdf, "GET", "/api/v1/authorization/{request_id}",
    None, "200: {request details, status, auth_number (if approved), rate, tax_estimate}",
    None)
api_endpoint(pdf, "POST", "/api/v1/authorization/{request_id}/approve",
    "{supervisor_id, notes}", "200: {auth_number, po_number, status: APPROVED}",
    "Generates auth number, PO, sends hotel notification")
api_endpoint(pdf, "POST", "/api/v1/authorization/{request_id}/reject",
    "{supervisor_id, reason_code, notes}", "200: {status: REJECTED}",
    "Notifies requestor with rejection reason")
api_endpoint(pdf, "GET", "/api/v1/authorization/tax-rates/{property_id}",
    None, "200: {state_tax, county_tax, city_tax, special_tax, total_rate}",
    None)

check_page_space(pdf, 50)
sub_title(pdf, "Data Model: lodging_authorizations")
headers = ["Column", "Type", "Constraints"]
widths = [50, 40, 100]
table_header(pdf, headers, widths, PURPLE)
cols = [
    ("id", "UUID PRIMARY KEY", "Auto-generated"),
    ("request_id", "UUID UNIQUE", "Business reference"),
    ("auth_number", "VARCHAR(20)", "UNIQUE, format AUTH-YYYYMMDD-XXXX"),
    ("po_number", "VARCHAR(20)", "UNIQUE, FK -> purchase_orders.id"),
    ("crew_id", "UUID NOT NULL", "FK -> crew_profiles.id"),
    ("property_id", "UUID NOT NULL", "FK -> properties.id"),
    ("contract_id", "UUID NOT NULL", "FK -> contracts.id"),
    ("program_code", "VARCHAR(20)", "NOT NULL"),
    ("check_in_date", "DATE NOT NULL", ""),
    ("check_out_date", "DATE NOT NULL", "CHECK > check_in_date"),
    ("room_type", "VARCHAR(20)", "CHECK IN (SINGLE,DOUBLE,ADA,SUITE)"),
    ("contracted_rate", "DECIMAL(8,2)", "From contract terms"),
    ("approved_rate", "DECIMAL(8,2)", "May differ if negotiated"),
    ("estimated_tax", "DECIMAL(8,2)", "Calculated from tax reference"),
    ("status", "VARCHAR(20)", "SUBMITTED/APPROVED/REJECTED/CANCELLED"),
    ("approved_by", "UUID", "FK -> users.id, NULLABLE"),
    ("approved_at", "TIMESTAMPTZ", "NULLABLE"),
    ("created_at", "TIMESTAMPTZ", "DEFAULT NOW()"),
]
for i, row in enumerate(cols):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 40)
pdf.ln(3)
sub_title(pdf, "Business Rules")
rules = [
    "BR-5.01: Requested rate exceeding contract ceiling by >10% requires VP-level approval, not just supervisor.",
    "BR-5.02: Authorization numbers are immutable once generated. Cancellation creates a new CANCELLED record referencing the original.",
    "BR-5.03: Tax rate lookup uses a maintained reference table updated quarterly. Actual tax at invoice is reconciled against estimate.",
    "BR-5.04: Properties with CrimeShield score < 60 are automatically rejected. Score 60-75 requires supervisor acknowledgment of risk.",
    "BR-5.05: Authorizations must be approved minimum 24 hours before check-in date. Rush requests require operations manager override.",
    "BR-5.06: PO numbers follow format PO-[program_code]-YYYYMMDD-XXXX for financial tracking.",
]
for rule in rules:
    bullet(pdf, rule)

sub_title(pdf, "User Stories")
user_story(pdf, "5.01", "program manager",
    "to submit a lodging authorization request for my crew",
    "crew have approved lodging before they travel to the property",
    "program manager selects crew, property, dates, and room type", "they submit the request",
    "request is created in SUBMITTED status, rate is verified against contract, and availability is checked",
    "Must", "Phase 1 - Week 1")
user_story(pdf, "5.02", "system",
    "to verify requested rates against contract ceilings automatically",
    "rate overcharges are caught before authorization",
    "lodging request is submitted with a nightly rate", "rate verification runs",
    "if rate <= contract ceiling, check passes; if rate > ceiling, request is flagged for manual review",
    "Must", "Phase 1 - Week 1")
user_story(pdf, "5.03", "crew supervisor",
    "to approve or reject lodging authorization requests",
    "crew lodging has proper supervisory sign-off before hotel is notified",
    "request has passed rate and availability checks", "supervisor reviews and clicks Approve",
    "auth number and PO number are generated, hotel is notified, and requestor is informed of approval",
    "Must", "Phase 1 - Week 2")
user_story(pdf, "5.04", "finance team",
    "each authorization to have a unique PO number linked to the program budget",
    "lodging costs are properly tracked against program budgets",
    "authorization is approved", "PO number is generated",
    "PO follows format PO-[program]-YYYYMMDD-XXXX and is linked to correct cost center",
    "Must", "Phase 1 - Week 2")
user_story(pdf, "5.05", "compliance officer",
    "properties to be screened against CrimeShield scores before authorization",
    "crew are not placed in properties that fail safety standards",
    "lodging request specifies a property", "compliance pre-check runs",
    "properties with score < 60 are rejected; score 60-75 requires supervisor risk acknowledgment",
    "Must", "Phase 1 - Week 2")
user_story(pdf, "5.06", "system",
    "to look up expected tax rates by property jurisdiction",
    "lodging cost estimates include accurate tax projections for budget planning",
    "property jurisdiction is identified", "tax rate lookup executes",
    "state, county, city, and special district tax rates are returned and total estimated tax is calculated",
    "Should", "Phase 1 - Week 3")


# ---- DOMAIN 6: CREW SUPERVISOR MOBILE APP ----
add_domain_header(pdf, 6, "CREW SUPERVISOR MOBILE APP", TEAL)

sub_title(pdf, "Domain Overview")
body_text(pdf, "The Crew Supervisor Mobile App is a comprehensive mobile application that serves as the primary operational tool for crew supervisors in the field. Built on React Native for cross-platform deployment, it provides 15 integrated module groups covering every aspect of supervisor responsibilities -- from lodging and travel management to compliance monitoring, incident reporting, and real-time crew location tracking. The app operates in both online and offline modes, syncing data when connectivity is restored.")

sub_title(pdf, "Module Groups")
modules = [
    "Lodging & Travel Management: Trip planner with route optimization, crew travel manifests, hotel assignment management, travel expense tracking, itinerary sharing with crew.",
    "Meal Planning & Per Diem: Daily meal allowance tracking per program rules, per diem calculations (GSA rates by location), receipt capture and submission, meal vendor directory.",
    "KYC & Identity: Crew identity verification dashboard, document expiry tracking (IDs, certifications, clearances), re-verification workflow for expired documents, bulk verification for new crew onboarding.",
    "Balance & Payroll: Hours worked summary by crew member, pay rate display (regular, overtime, per diem), overtime calculation and alerting, payroll data export to external system.",
    "Compliance Dashboard: Certification status for all crew (valid, expiring, expired), required training completion tracking, safety compliance scores, audit readiness indicator.",
    "Geofencing & GPS: Real-time crew location on property map (within geofence only), geofence boundary visualization, entry/exit event history, GPS accuracy indicators.",
    "Face Recognition: Identity verification at check-in via camera, enrolled photo comparison, confidence score display, manual override for FRS failures with reason logging.",
    "Time Tracking: Clock in/out for each crew member, hours worked calculation (daily, weekly, period), break tracking, overtime threshold alerts.",
    "Contact Tracing: BLE swarm roster data visualization, proximity history for selected crew, contact duration and frequency, consent-tier-aware data display.",
    "Safety Check: Daily safety briefing checklist, hazard report filing with photo capture, safety equipment verification, incident prevention tracking.",
    "Maintenance Requests: Facility issue reporting with photos, priority classification (urgent, high, normal, low), status tracking through resolution, hotel maintenance team coordination.",
    "Incident Reporting: Incident report creation with structured fields, evidence attachment (photos, videos, documents), witness information capture, automatic routing to operations and compliance.",
    "Messaging: Crew-to-supervisor messaging, supervisor-to-operations messaging, broadcast messages to all crew at a property, message read receipts and delivery confirmation.",
    "Document Management: Upload and view crew documents, certification storage and retrieval, document expiry alerts, bulk document requests.",
    "Training: Required training status per crew, training module assignment, completion tracking and certification issuance, overdue training escalation.",
]
for mod in modules:
    bullet(pdf, mod)

check_page_space(pdf, 50)
sub_title(pdf, "API Endpoints")
api_endpoint(pdf, "GET", "/api/v1/supervisor/dashboard/{supervisor_id}",
    None, "200: {properties[], crew_summary, alerts[], tasks[], compliance_score}",
    None)
api_endpoint(pdf, "GET", "/api/v1/supervisor/crew/{property_id}?date=YYYY-MM-DD",
    None, "200: {crew[], check_in_status[], assignments[], hours_worked[]}",
    None)
api_endpoint(pdf, "POST", "/api/v1/supervisor/incident",
    "{property_id, type, description, severity, evidence[], witnesses[]}", "201: {incident_id, status: OPEN}",
    "Routes to ops + compliance, notifies chain of command")
api_endpoint(pdf, "POST", "/api/v1/supervisor/maintenance",
    "{property_id, room, issue_type, description, photos[], priority}", "201: {request_id, status: SUBMITTED}",
    "Notifies property maintenance team")
api_endpoint(pdf, "POST", "/api/v1/supervisor/safety-check",
    "{property_id, checklist_items[], hazards[], equipment_status}", "201: {check_id, compliance_score}",
    "Updates compliance dashboard")
api_endpoint(pdf, "GET", "/api/v1/supervisor/time-tracking/{property_id}",
    None, "200: {crew_hours[], overtime_alerts[], period_summary}",
    None)

check_page_space(pdf, 50)
sub_title(pdf, "Data Model: supervisor_activities")
headers = ["Column", "Type", "Constraints"]
widths = [50, 40, 100]
table_header(pdf, headers, widths, PURPLE)
cols = [
    ("id", "UUID PRIMARY KEY", "Auto-generated"),
    ("supervisor_id", "UUID NOT NULL", "FK -> users.id"),
    ("property_id", "UUID NOT NULL", "FK -> properties.id"),
    ("activity_type", "VARCHAR(30)", "Module identifier"),
    ("activity_data", "JSONB", "Module-specific payload"),
    ("offline_created", "BOOLEAN", "DEFAULT FALSE"),
    ("synced_at", "TIMESTAMPTZ", "NULLABLE, set on sync"),
    ("created_at", "TIMESTAMPTZ", "DEFAULT NOW()"),
]
for i, row in enumerate(cols):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 40)
pdf.ln(3)
sub_title(pdf, "Business Rules")
rules = [
    "BR-6.01: Offline mode caches up to 72 hours of data. Sync priority: incidents > time tracking > check-ins > everything else.",
    "BR-6.02: Face recognition module requires explicit supervisor activation per check-in. No passive facial scanning.",
    "BR-6.03: GPS crew location display is restricted to within geofence boundaries. Off-premises location is never shown.",
    "BR-6.04: Incident reports with severity CRITICAL auto-escalate to operations director within 15 minutes.",
    "BR-6.05: Contact tracing data display respects crew consent tier. Supervisor sees only data their access level permits.",
    "BR-6.06: Time tracking overtime alerts trigger at 8 hours (daily) and 40 hours (weekly) with configurable thresholds per program.",
]
for rule in rules:
    bullet(pdf, rule)

sub_title(pdf, "User Stories")
user_story(pdf, "6.01", "crew supervisor",
    "a unified mobile dashboard showing all my properties and crew at a glance",
    "I can quickly assess operational status across my assignments",
    "supervisor has crew assigned to multiple properties", "they open the supervisor app",
    "dashboard shows property cards with crew count, check-in status, alerts, and compliance score for each",
    "Must", "Phase 3 - Week 10")
user_story(pdf, "6.02", "crew supervisor",
    "to file an incident report with photos and witness information from my phone",
    "incidents are documented immediately with evidence while details are fresh",
    "an incident occurs at a property", "supervisor opens incident module and fills in details with photos",
    "incident report is created, routed to ops and compliance, and confirmation is shown",
    "Must", "Phase 3 - Week 11")
user_story(pdf, "6.03", "crew supervisor",
    "to track crew hours worked with overtime alerts",
    "I can prevent unauthorized overtime and ensure accurate time records",
    "crew are clocked in at a property", "supervisor opens time tracking module",
    "each crew shows hours today, hours this week, and amber/red alerts for approaching/exceeded overtime thresholds",
    "Must", "Phase 3 - Week 10")
user_story(pdf, "6.04", "crew supervisor",
    "to verify crew identity using face recognition during check-in",
    "I have an additional identity verification layer beyond device authentication",
    "crew is checking in at a property with FRS enabled", "supervisor activates face recognition",
    "camera captures crew face, compares to enrolled photo, displays confidence score >= 95% for pass",
    "Should", "Phase 3 - Week 12")
user_story(pdf, "6.05", "crew supervisor",
    "the app to work offline and sync when connectivity is restored",
    "I can continue operations even in areas with poor connectivity",
    "supervisor loses network connectivity", "they continue using the app",
    "all actions are cached locally, sync occurs automatically when connectivity returns, no data is lost",
    "Must", "Phase 3 - Week 11")
user_story(pdf, "6.06", "crew supervisor",
    "to view crew location on a property map within geofence boundaries",
    "I can see where my crew are deployed on the property",
    "crew are checked in and within geofence", "supervisor opens geofencing module",
    "property map shows crew positions (within geofence only), last updated timestamps, and accuracy circles",
    "Should", "Phase 3 - Week 12")
user_story(pdf, "6.07", "crew supervisor",
    "to send broadcast messages to all crew at a specific property",
    "I can communicate important information to the entire crew quickly",
    "supervisor has crew assigned to a property", "they compose and send a broadcast message",
    "message is delivered to all crew at that property via push notification with delivery confirmation",
    "Should", "Phase 3 - Week 11")
user_story(pdf, "6.08", "crew supervisor",
    "to view compliance dashboard showing certification and training status",
    "I can identify crew with expiring certifications before they become non-compliant",
    "crew have various certifications with different expiry dates", "supervisor opens compliance dashboard",
    "crew listed with certification status: green (valid), amber (expiring in 30 days), red (expired)",
    "Must", "Phase 3 - Week 10")
user_story(pdf, "6.09", "crew supervisor",
    "to submit maintenance requests with photos and priority levels",
    "facility issues are reported promptly and tracked to resolution",
    "supervisor identifies a maintenance issue", "they file a request with photos and priority",
    "request is created, property maintenance is notified, and supervisor can track status updates",
    "Should", "Phase 3 - Week 12")
user_story(pdf, "6.10", "crew supervisor",
    "to conduct daily safety checks using a structured checklist",
    "safety compliance is documented consistently and hazards are reported",
    "supervisor begins daily safety walk-through", "they complete the safety checklist in the app",
    "checklist results are saved, compliance score is updated, and any hazards trigger the appropriate workflow",
    "Must", "Phase 3 - Week 11")


# ---- DOMAIN 7: ONSITE/OFFSITE SUPERVISOR WORKFLOWS ----
add_domain_header(pdf, 7, "ONSITE/OFFSITE SUPERVISOR WORKFLOWS", NAVY)

sub_title(pdf, "Domain Overview")
body_text(pdf, "This domain defines two parallel workflow tracks for crew supervisors: onsite (physically present at the property) and offsite (managing remotely). Both tracks share the same data and tools (Domain 6 app) but have distinct process flows optimized for their operational context. Onsite supervisors perform hands-on verification and physical walk-throughs, while offsite supervisors rely on BLE/GPS data, video calls, and dashboard monitoring. The system supports seamless transition between modes when a supervisor moves between properties.")

sub_title(pdf, "ONSITE SUPERVISOR WORKFLOW", EMERALD)
steps = [
    "Receive Daily Schedule: At 05:00 local time, supervisor receives push notification with day's schedule: properties, crew lists, special instructions, outstanding tasks.",
    "Travel to Property: Trip planner module provides route with estimated arrival. Supervisor confirms departure via app, notifying crew of ETA.",
    "Arrive On-Site: BLE beacon at property entrance confirms supervisor's physical presence. Status changes to ON_SITE. Crew and ops are notified.",
    "Task Management & Crew Assignment Review: Supervisor reviews crew assignments, room allocations, and any changes since last visit. Outstanding tasks from previous day are displayed.",
    "Daily Activity Log: Supervisor begins logging activities as they occur. Each activity entry includes: time, type, crew involved, notes, photos.",
    "Crew Check-In Verification: In-person verification of crew presence. BLE proximity confirms crew device is near supervisor device. Optional face recognition for identity confirmation.",
    "Time Tracking Monitoring: Review clock-in times for all crew. Identify late arrivals, missed clock-ins, overtime approaching. Take corrective action as needed.",
    "Safety Check & Walk-Through: Conduct property safety inspection using structured checklist. Document hazards with photos. Verify safety equipment availability.",
    "Incident Report Filing: If incidents occur, file detailed report with evidence, witnesses, and immediate actions taken. Critical incidents auto-escalate.",
    "Maintenance Request Submission: Report facility issues discovered during walk-through. Attach photos, set priority, track through resolution.",
    "Daily Wrap-Up & Summary: Review day's activities, confirm all crew have checked out, verify hours are accurate. Generate summary of notable events.",
    "Submit Daily Report to Operations: Compile and submit daily report including: crew attendance, hours, incidents, maintenance requests, compliance status, next-day needs.",
]
for i, step in enumerate(steps, 1):
    numbered_item(pdf, i, step)

pdf.ln(2)
sub_title(pdf, "OFFSITE SUPERVISOR WORKFLOW", TEAL)
steps = [
    "Receive Daily Schedule (Remote): Same schedule notification as onsite, plus remote access credentials and priority monitoring list.",
    "Remote Dashboard Login: Supervisor logs into web dashboard with MFA. Dashboard shows all assigned properties with real-time status.",
    "Monitor Crew Locations: View BLE/GPS data for crew within geofenced properties. Identify crew who have not yet checked in. Monitor for anomalies.",
    "Virtual Crew Check-In: Conduct check-in verification via video call. BLE data confirms crew is at property during call. Supervisor notes call completion in system.",
    "Review Time Tracking Data: Examine clock-in/out data across all properties. Flag discrepancies, investigate overtime, approve time adjustments.",
    "Remote Safety Compliance Verification: Review safety checklist submissions from onsite personnel. Verify compliance scores. Escalate unresolved safety issues.",
    "Incident Report Review & Escalation: Review incident reports filed by onsite staff or crew. Add context, escalate as needed, coordinate response from remote.",
    "Coordinate with Onsite Personnel: Message or call onsite staff for situations requiring physical presence. Delegate tasks, request photos/evidence, confirm actions taken.",
    "End-of-Day Report Generation: System auto-generates report draft from day's data. Supervisor reviews, adds notes, confirms accuracy.",
    "Submit Remote Supervisor Report: Submit daily report with remote monitoring summary, escalations, follow-up items, and next-day priorities.",
]
for i, step in enumerate(steps, 1):
    numbered_item(pdf, i, step)

check_page_space(pdf, 40)
sub_title(pdf, "API Endpoints")
api_endpoint(pdf, "POST", "/api/v1/supervisor/daily-report",
    "{supervisor_id, property_id, date, type (ONSITE/OFFSITE), report_data}", "201: {report_id, status}",
    "Stores report, notifies operations, updates compliance records")
api_endpoint(pdf, "GET", "/api/v1/supervisor/schedule/{supervisor_id}?date=YYYY-MM-DD",
    None, "200: {properties[], crew_lists[], tasks[], special_instructions[]}",
    None)
api_endpoint(pdf, "POST", "/api/v1/supervisor/activity-log",
    "{supervisor_id, property_id, activity_type, crew_ids[], notes, photos[]}", "201: {activity_id}",
    "Appends to daily activity log")
api_endpoint(pdf, "POST", "/api/v1/supervisor/virtual-checkin",
    "{supervisor_id, crew_id, video_call_id, ble_confirmed}", "200: {checkin_verified, notes}",
    "Records virtual check-in verification")

check_page_space(pdf, 40)
sub_title(pdf, "Business Rules")
rules = [
    "BR-7.01: Onsite supervisor arrival MUST be confirmed by property BLE beacon. GPS alone is insufficient.",
    "BR-7.02: Daily reports are due by 20:00 local time. Late reports trigger operations manager notification.",
    "BR-7.03: Offsite supervisors must conduct virtual check-in for each property minimum once per shift.",
    "BR-7.04: Supervisor mode (ONSITE/OFFSITE) is determined by geofence presence, not manual selection.",
    "BR-7.05: Critical incident reports bypass normal workflow and immediately notify operations director and compliance.",
]
for rule in rules:
    bullet(pdf, rule)

sub_title(pdf, "User Stories")
user_story(pdf, "7.01", "onsite supervisor",
    "to receive my daily schedule with all assigned properties and crew lists by 5 AM",
    "I can plan my day and travel routes before heading to the first property",
    "supervisor has property assignments for today", "05:00 local time arrives",
    "push notification with schedule summary is delivered; full details available in app",
    "Must", "Phase 3 - Week 10")
user_story(pdf, "7.02", "onsite supervisor",
    "my arrival at a property to be automatically confirmed via BLE beacon",
    "my presence is verified without manual check-in and crew/ops are notified",
    "supervisor arrives at assigned property", "their device detects property BLE beacon",
    "status changes to ON_SITE, timestamp recorded, crew and ops notified",
    "Must", "Phase 3 - Week 10")
user_story(pdf, "7.03", "offsite supervisor",
    "to monitor crew locations across all my assigned properties from a remote dashboard",
    "I can verify crew presence and identify issues without being physically present",
    "crew are assigned to properties supervised remotely", "offsite supervisor opens dashboard",
    "map view shows crew positions within geofences, check-in status, and time on-site for each crew",
    "Must", "Phase 3 - Week 11")
user_story(pdf, "7.04", "offsite supervisor",
    "to conduct virtual check-in via video call with BLE confirmation",
    "I can verify crew identity remotely while confirming they are physically at the property",
    "crew is at property but supervisor is remote", "supervisor initiates video check-in call",
    "video call connects, BLE confirms crew is at property during call, verification is recorded",
    "Should", "Phase 3 - Week 12")
user_story(pdf, "7.05", "onsite supervisor",
    "to submit a daily report covering attendance, incidents, and compliance status",
    "operations has a complete record of the day's activities at the property",
    "supervisor has completed daily activities", "they compile and submit daily report",
    "report is stored, ops is notified, and compliance records are updated",
    "Must", "Phase 3 - Week 11")
user_story(pdf, "7.06", "offsite supervisor",
    "to coordinate with onsite personnel when physical presence is needed",
    "situations requiring hands-on response are handled even when I am remote",
    "an issue requires physical investigation at a property", "offsite supervisor messages onsite staff",
    "message is delivered, onsite staff responds, actions are logged in the activity trail",
    "Should", "Phase 3 - Week 12")
user_story(pdf, "7.07", "system",
    "to automatically determine supervisor mode (ONSITE/OFFSITE) based on geofence",
    "mode is always accurate and workflows adapt accordingly",
    "supervisor approaches a property", "their device enters/exits the geofence",
    "mode switches automatically, UI adapts to show relevant tools, and mode change is logged",
    "Must", "Phase 3 - Week 10")
user_story(pdf, "7.08", "operations manager",
    "to receive notifications when supervisors submit late daily reports",
    "I can follow up on missing reports and ensure operational data is complete",
    "daily report deadline (20:00) passes without submission", "system checks for missing reports",
    "notification sent to ops manager listing supervisors with outstanding reports",
    "Should", "Phase 3 - Week 13")


# ---- DOMAIN 8: ROSTER SYSTEM CORE FUNCTIONS ----
add_domain_header(pdf, 8, "ROSTER SYSTEM CORE FUNCTIONS", GOLD)

sub_title(pdf, "Domain Overview")
body_text(pdf, "The Roster System Core is the central data backbone of GoCrew. It manages employee profiles, assignment scheduling, shift management, and the master roster that all other domains read from and write to. This domain owns the source of truth for who is assigned where, when, and for how long. It provides the APIs that check-in, geofence, supervisor, and compliance domains depend on for crew and assignment data.")

sub_title(pdf, "Process Flow")
steps = [
    "Employee Profile Management: Create and maintain crew profiles with personal information, KYC linkage, certifications, qualifications, and employment history. Profiles are the identity anchor for all system operations.",
    "Assignment Scheduling: Assign crew members to specific properties for defined date ranges. Assignments include: property, dates, room type, shift, program code, supervisor, pay rate. Conflict detection prevents double-booking.",
    "Contract Hours Definition: Define expected hours per role per program based on contract terms. Hours define: regular hours per day, overtime threshold, break requirements, maximum daily/weekly hours.",
    "Shift Management: Create and manage shift patterns (day, swing, night, rotating). Handle shift swaps between crew members with supervisor approval. Maintain minimum coverage requirements per property.",
    "Employee Schedule Publishing: Push finalized schedules to crew mobile app. Schedule includes: property, dates, shift times, room assignment, supervisor contact, special instructions. Published 7 days in advance minimum.",
    "Summary Shift Reports: Generate aggregated reports: daily attendance summary, weekly hours by crew/property, monthly utilization rates, overtime analysis. Reports available via dashboard and scheduled email delivery.",
    "Real-Time Alerts & Notifications: System generates operational alerts for: late arrivals (no check-in 30 min after shift start), no-shows, overtime approaching, assignment conflicts, certification expiry.",
    "Reporting & Analytics: Comprehensive reporting module with: trend analysis dashboards, property utilization heat maps, crew performance metrics, cost analysis by program, exportable data (CSV, PDF).",
    "Feedback Collection: Collect and manage feedback: crew feedback on properties, property ratings by crew, supervisor assessments of crew performance, crew satisfaction surveys.",
]
for i, step in enumerate(steps, 1):
    numbered_item(pdf, i, step)

check_page_space(pdf, 50)
sub_title(pdf, "API Endpoints")
api_endpoint(pdf, "POST", "/api/v1/roster/crew",
    "{name, employee_id, kyc_id, qualifications[], certifications[]}", "201: {crew_id, profile}",
    "Creates crew profile with KYC linkage")
api_endpoint(pdf, "PUT", "/api/v1/roster/crew/{crew_id}",
    "{updated fields}", "200: {crew_id, updated_profile}",
    "Updates profile, triggers certification check if certs changed")
api_endpoint(pdf, "POST", "/api/v1/roster/assignments",
    "{crew_id, property_id, dates, shift, room_type, program_code}", "201: {assignment_id}",
    "Creates assignment after conflict check")
api_endpoint(pdf, "GET", "/api/v1/roster/schedule/{property_id}?date=YYYY-MM-DD",
    None, "200: {assignments[], shifts[], coverage_status}",
    None)
api_endpoint(pdf, "POST", "/api/v1/roster/shifts/swap",
    "{crew_id_1, crew_id_2, shift_date, supervisor_approval}", "200: {swap_id, status}",
    "Swaps shifts after qualification check")
api_endpoint(pdf, "GET", "/api/v1/roster/reports/{type}?from=X&to=Y&property_id=Z",
    None, "200: {report_data, summary_stats, export_url}",
    None)

check_page_space(pdf, 50)
sub_title(pdf, "Data Model: crew_profiles")
headers = ["Column", "Type", "Constraints"]
widths = [50, 40, 100]
table_header(pdf, headers, widths, PURPLE)
cols = [
    ("id", "UUID PRIMARY KEY", "Auto-generated"),
    ("employee_id", "VARCHAR(20) UNIQUE", "Business identifier"),
    ("first_name", "VARCHAR(100)", "NOT NULL"),
    ("last_name", "VARCHAR(100)", "NOT NULL"),
    ("email", "VARCHAR(255) UNIQUE", "NOT NULL"),
    ("phone", "VARCHAR(20)", "NOT NULL"),
    ("kyc_id", "UUID", "FK -> kyc_verifications.id"),
    ("qualifications", "JSONB", "Array of qualification objects"),
    ("certifications", "JSONB", "Array with cert type, number, expiry"),
    ("employment_status", "VARCHAR(20)", "ACTIVE, INACTIVE, SUSPENDED"),
    ("hire_date", "DATE", "NOT NULL"),
    ("created_at", "TIMESTAMPTZ", "DEFAULT NOW()"),
    ("updated_at", "TIMESTAMPTZ", "DEFAULT NOW()"),
]
for i, row in enumerate(cols):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 30)
pdf.ln(3)
sub_title(pdf, "Data Model: roster_assignments")
headers = ["Column", "Type", "Constraints"]
widths = [50, 40, 100]
table_header(pdf, headers, widths, PURPLE)
cols = [
    ("id", "UUID PRIMARY KEY", "Auto-generated"),
    ("crew_id", "UUID NOT NULL", "FK -> crew_profiles.id"),
    ("property_id", "UUID NOT NULL", "FK -> properties.id"),
    ("program_code", "VARCHAR(20)", "NOT NULL"),
    ("start_date", "DATE NOT NULL", ""),
    ("end_date", "DATE NOT NULL", "CHECK >= start_date"),
    ("shift_pattern", "VARCHAR(20)", "DAY, SWING, NIGHT, ROTATING"),
    ("room_type", "VARCHAR(20)", "SINGLE, DOUBLE, ADA, SUITE"),
    ("room_number", "VARCHAR(10)", "Assigned room"),
    ("supervisor_id", "UUID", "FK -> users.id"),
    ("pay_rate", "DECIMAL(8,2)", "Hourly rate"),
    ("status", "VARCHAR(20)", "ACTIVE, COMPLETED, CANCELLED"),
    ("created_at", "TIMESTAMPTZ", "DEFAULT NOW()"),
]
for i, row in enumerate(cols):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 30)
pdf.ln(3)
sub_title(pdf, "Business Rules")
rules = [
    "BR-8.01: Crew cannot be assigned to overlapping properties on the same dates. Conflict detection blocks creation.",
    "BR-8.02: Schedules must be published minimum 7 days in advance. Changes within 7 days require supervisor approval and crew notification.",
    "BR-8.03: Shift swaps require both crew members to have matching qualifications for the role. Unqualified swaps are rejected.",
    "BR-8.04: Late arrival alerts trigger 30 minutes after scheduled shift start with no check-in event.",
    "BR-8.05: Certification expiry alerts begin 30 days before expiry. Expired certifications flag the crew as NON_COMPLIANT.",
    "BR-8.06: Feedback is anonymous by default. Identifiable feedback requires explicit opt-in from the submitter.",
]
for rule in rules:
    bullet(pdf, rule)

sub_title(pdf, "User Stories")
user_story(pdf, "8.01", "operations coordinator",
    "to create and manage crew assignments to properties with date ranges and shifts",
    "crew deployment is organized and no scheduling conflicts occur",
    "operations coordinator has crew and property data", "they create a new assignment",
    "assignment is created after conflict check passes, crew is notified, and schedule is updated",
    "Must", "Phase 3 - Week 9")
user_story(pdf, "8.02", "crew member",
    "to receive my schedule 7 days in advance via the mobile app",
    "I can plan my personal life around my work schedule with adequate notice",
    "assignments are finalized for next week", "schedule publishing job runs",
    "crew receives push notification with schedule details; full schedule visible in app",
    "Must", "Phase 3 - Week 10")
user_story(pdf, "8.03", "crew member",
    "to request a shift swap with another qualified crew member",
    "I have flexibility to exchange shifts for personal needs with proper approval",
    "two crew members agree to swap shifts", "swap request is submitted",
    "qualifications are checked for both crew, supervisor is notified for approval, swap executes on approval",
    "Should", "Phase 3 - Week 11")
user_story(pdf, "8.04", "operations manager",
    "to view real-time alerts for late arrivals and no-shows",
    "I can take immediate action when crew do not show up for their shifts",
    "shift start time has passed", "30 minutes elapse with no check-in for a scheduled crew member",
    "late arrival alert is generated, displayed on ops dashboard, and push notification sent to supervisor",
    "Must", "Phase 3 - Week 10")
user_story(pdf, "8.05", "program manager",
    "to generate utilization reports by property, crew, and time period",
    "I can assess program efficiency and optimize crew deployment",
    "check-in and time tracking data exists for the period", "program manager requests utilization report",
    "report shows occupancy rates, hours utilized vs contracted, cost per crew day, and trend analysis",
    "Should", "Phase 3 - Week 13")
user_story(pdf, "8.06", "crew member",
    "to submit anonymous feedback about property conditions",
    "I can report issues without fear of retaliation, improving conditions for all crew",
    "crew member has an active or recent assignment", "they submit feedback via the app",
    "feedback is stored anonymously (no crew_id linked), aggregated with other feedback for that property",
    "Should", "Phase 3 - Week 13")


# ---- DOMAIN 9: COMPLIANCE & DATA PROTECTION ----
add_domain_header(pdf, 9, "COMPLIANCE & DATA PROTECTION", RED)

sub_title(pdf, "Domain Overview")
body_text(pdf, "The Compliance and Data Protection domain is the governance layer that ensures every system operation meets regulatory requirements across multiple frameworks: GDPR (EU data protection), CCPA (California consumer privacy), CMMC Level 2 (US defense contractor cybersecurity), and FAR/DFARS (federal acquisition requirements). This domain also manages CUI (Controlled Unclassified Information) handling procedures required for government contracts. It enforces data minimization, encryption standards, access controls, consent management, and audit trail integrity across all other domains.")

sub_title(pdf, "Process Specifications")
steps = [
    "Anonymization & Pseudonymization: Daily UUID rotation (Domain 1) provides pseudonymization. Contact logs use hashed identifiers. Analytics use anonymized, aggregated data. Re-identification requires key held in separate HSM.",
    "Data Minimization: System collects only data necessary for operational function. BLE scanning activates only within geofence (no off-premises collection). Contact logs retain only: contact count, duration, location hash -- not content or context of interactions.",
    "Encryption: At rest: AES-256 for all databases and file storage. In transit: TLS 1.3 for all API communication. End-to-end: BLE contact logs encrypted with per-device keys. IOTA Tangle: payload encrypted before submission. Key management via AWS KMS or Azure Key Vault.",
    "Access Controls: Role-Based Access Control (RBAC) with least privilege principle. Roles: Crew, Supervisor, Operations, Compliance, Admin, System. Multi-Factor Authentication required for all non-crew roles. Comprehensive audit logging of all data access events.",
    "Consent Management: Opt-in model for all data collection beyond operational minimum. Five consent tiers (detailed in Domain 1). Partial consent supported (e.g., check-in yes, contact tracing no). Revocable at any time with 60-second propagation. Consent history maintained for audit.",
    "Transparency & User Rights: Right to Access: crew can export all their data in machine-readable format. Right to Delete: crew can request deletion (subject to legal retention requirements). Right to Know: crew can see exactly what data is collected and who has accessed it. Right to Portability: data export in JSON/CSV format.",
    "Regular Audits & Privacy Impact Assessments: Quarterly Privacy Impact Assessments (PIAs) for all new features. Annual third-party security audits. Monthly automated compliance scans. Audit reports stored for 7 years.",
    "GDPR Compliance: Article 6 - Lawful basis for processing (consent + legitimate interest). Article 7 - Conditions for consent (freely given, specific, informed, unambiguous). Article 17 - Right to erasure. Article 20 - Right to data portability. Article 25 - Data protection by design and by default.",
    "CCPA Compliance: Section 1798.100 - Right to know what personal information is collected. Section 1798.105 - Right to request deletion. Section 1798.120 - Right to opt out of sale of personal information. GoCrew does not sell personal information -- this is stated in privacy policy.",
    "CMMC Level 2 Alignment: Implements all 110 NIST SP 800-171 practices. Covers 14 control families: Access Control, Awareness/Training, Audit, Configuration Management, Identification/Authentication, Incident Response, Maintenance, Media Protection, Physical Protection, Personnel Security, Risk Assessment, Security Assessment, System Protection, System/Information Integrity.",
    "FAR/DFARS Requirements: FAR 52.204-21: Basic safeguarding of covered contractor information systems. 15 security requirements implemented. DFARS 252.204-7012: Safeguarding covered defense information. Cyber incident reporting within 72 hours. Medium assurance certificate for DoD systems.",
    "CUI Handling Procedures: Marking: All CUI data marked with 'CUI' banner (as seen in page header). Storage: Encrypted at rest in access-controlled environments. Transit: Encrypted in transit, no unencrypted email. Access: Need-to-know basis with RBAC enforcement. Disposal: Cryptographic erasure for digital, cross-cut shred for physical.",
]
for i, step in enumerate(steps, 1):
    numbered_item(pdf, i, step)

check_page_space(pdf, 40)
sub_title(pdf, "API Endpoints")
api_endpoint(pdf, "GET", "/api/v1/compliance/audit-log?entity_type=X&entity_id=Y&from=Z&to=W",
    None, "200: {events[], total_count, page}",
    None)
api_endpoint(pdf, "POST", "/api/v1/compliance/data-export/{crew_id}",
    "{format: JSON|CSV, date_range}", "202: {export_id, status: PROCESSING, eta_seconds}",
    "Generates data export package, notifies crew when ready")
api_endpoint(pdf, "POST", "/api/v1/compliance/deletion-request",
    "{crew_id, reason, legal_hold_check}", "200: {request_id, status, retention_conflicts[]}",
    "Checks legal holds before processing deletion")
api_endpoint(pdf, "GET", "/api/v1/compliance/consent/{crew_id}",
    None, "200: {consent_tiers{}, history[], last_updated}",
    None)
api_endpoint(pdf, "POST", "/api/v1/compliance/pia",
    "{feature_name, data_types[], processing_purposes[]}", "201: {pia_id, risk_score, recommendations[]}",
    "Creates PIA record, flags high-risk features for review")

check_page_space(pdf, 30)
sub_title(pdf, "Business Rules")
rules = [
    "BR-9.01: All API calls are logged with: timestamp, user_id, resource accessed, action, IP address, user agent. No exceptions.",
    "BR-9.02: Data deletion requests must be processed within 30 days (GDPR) or 45 days (CCPA). System tracks deadline.",
    "BR-9.03: Legal hold overrides deletion requests. Crew is informed that data is under legal hold without disclosing details.",
    "BR-9.04: Encryption keys are rotated annually. Key rotation must complete within 72 hours with zero downtime.",
    "BR-9.05: Cyber incidents must be reported to DoD within 72 hours per DFARS 252.204-7012.",
    "BR-9.06: Privacy Impact Assessments are required before any feature that introduces new data collection goes to production.",
    "BR-9.07: Failed MFA attempts (3 consecutive) lock the account for 30 minutes and alert security team.",
]
for rule in rules:
    bullet(pdf, rule)

sub_title(pdf, "User Stories")
user_story(pdf, "9.01", "crew member",
    "to export all my personal data in a machine-readable format",
    "I can exercise my right to data portability under GDPR Article 20",
    "crew member is logged into the app", "they request a data export",
    "export is generated within 24 hours in JSON format, crew is notified when download is ready",
    "Must", "Phase 2 - Week 7")
user_story(pdf, "9.02", "crew member",
    "to request deletion of my personal data",
    "I can exercise my right to erasure under GDPR Article 17",
    "crew member submits deletion request", "system checks for legal holds",
    "if no holds, data is deleted within 30 days and confirmation sent; if holds exist, crew is informed",
    "Must", "Phase 2 - Week 7")
user_story(pdf, "9.03", "compliance officer",
    "to view a complete audit trail of who accessed what data and when",
    "I can investigate data access incidents and demonstrate regulatory compliance",
    "data access events have been logged", "compliance officer queries audit log",
    "all access events returned with user, resource, action, timestamp, IP, and user agent",
    "Must", "Phase 2 - Week 6")
user_story(pdf, "9.04", "system administrator",
    "encryption keys to rotate annually with zero downtime",
    "key compromise risk is minimized and compliance requirements are met",
    "annual key rotation schedule is triggered", "rotation process executes",
    "new keys are generated, data is re-encrypted, old keys are archived, and zero downtime is maintained",
    "Must", "Phase 2 - Week 8")
user_story(pdf, "9.05", "compliance officer",
    "to conduct Privacy Impact Assessments for new features before production deployment",
    "data protection risks are identified and mitigated before they affect users",
    "a new feature that collects personal data is proposed", "PIA is submitted",
    "risk score is calculated, recommendations are generated, and high-risk features are flagged for review",
    "Must", "Phase 2 - Week 8")
user_story(pdf, "9.06", "security team",
    "cyber incidents to be automatically reported within 72 hours per DFARS requirements",
    "we maintain compliance with defense contractor reporting obligations",
    "a cyber incident is detected and classified", "72-hour countdown begins",
    "incident report is auto-generated, sent to security team for review, and submitted to DoD within deadline",
    "Must", "Phase 2 - Week 8")


# ---- DOMAIN 10: ROSTER CHECK-OFF & VERIFICATION ----
add_domain_header(pdf, 10, "ROSTER CHECK-OFF & VERIFICATION", EMERALD)

sub_title(pdf, "Domain Overview")
body_text(pdf, "The Roster Check-Off domain provides the daily verification workflow where supervisors confirm that the actual crew presence matches the expected roster. This is the human-in-the-loop validation that complements the automated BLE/GPS/QR check-in system. Supervisors pull the daily expected roster, verify each crew member against it, identify discrepancies (missing crew, wrong rooms, unauthorized occupants), process late arrivals, and certify the roster as complete. This creates a dual-verification system: automated (Domain 4) + human (Domain 10).")

sub_title(pdf, "Process Flow")
steps = [
    "Supervisor Daily Roster Pull: At shift start, supervisor pulls the expected crew list for their property from Roster Core (Domain 8). List shows: crew name, room number, shift, check-in status, special notes.",
    "Crew Member Attendance Verification: Supervisor verifies each crew member on the list. Methods: visual confirmation, BLE proximity, face recognition, or crew verbal confirmation. Each crew is marked as VERIFIED, ABSENT, or UNVERIFIED.",
    "Room Occupancy Validation: Supervisor confirms crew are in their assigned rooms (for lodging verification). Can be done during walk-through or via BLE beacon data showing device in room zone.",
    "Discrepancy Identification: System flags discrepancies: crew on roster but not verified (ABSENT), crew in wrong room, devices detected but no roster entry (unauthorized), check-in data conflicts with physical observation.",
    "Late Arrival Processing: For crew not yet checked in at verification time: mark as LATE, set follow-up reminder, contact crew via app messaging, notify operations if >60 minutes late.",
    "Compliance Sign-Off: Supervisor reviews the verified roster and digitally signs off that it is complete and accurate. Sign-off includes: supervisor ID, timestamp, property, date, discrepancy notes.",
    "Report Generation: Daily roster verification report is auto-generated with: total expected, total verified, total absent, total late, discrepancies found, supervisor sign-off. Report stored and sent to operations.",
    "Escalation: Missing crew (ABSENT after 2 hours with no communication) are escalated to operations. Unauthorized occupants are escalated to security. Repeated discrepancies trigger compliance review.",
]
for i, step in enumerate(steps, 1):
    numbered_item(pdf, i, step)

check_page_space(pdf, 40)
sub_title(pdf, "API Endpoints")
api_endpoint(pdf, "GET", "/api/v1/checkoff/roster/{property_id}?date=YYYY-MM-DD",
    None, "200: {expected_crew[], check_in_status[], room_assignments[]}",
    None)
api_endpoint(pdf, "POST", "/api/v1/checkoff/verify",
    "{supervisor_id, crew_id, property_id, status, method, notes}", "200: {verification_id, status}",
    "Records individual crew verification")
api_endpoint(pdf, "POST", "/api/v1/checkoff/signoff",
    "{supervisor_id, property_id, date, notes, discrepancies[]}", "201: {signoff_id, report_url}",
    "Records sign-off, generates daily report, notifies operations")
api_endpoint(pdf, "POST", "/api/v1/checkoff/escalate",
    "{crew_id, property_id, escalation_type, details}", "201: {escalation_id, routed_to}",
    "Creates escalation, routes to ops or security based on type")

check_page_space(pdf, 50)
sub_title(pdf, "Data Model: roster_verifications")
headers = ["Column", "Type", "Constraints"]
widths = [50, 40, 100]
table_header(pdf, headers, widths, PURPLE)
cols = [
    ("id", "UUID PRIMARY KEY", "Auto-generated"),
    ("supervisor_id", "UUID NOT NULL", "FK -> users.id"),
    ("crew_id", "UUID NOT NULL", "FK -> crew_profiles.id"),
    ("property_id", "UUID NOT NULL", "FK -> properties.id"),
    ("verification_date", "DATE NOT NULL", ""),
    ("status", "VARCHAR(20)", "VERIFIED, ABSENT, LATE, UNVERIFIED"),
    ("method", "VARCHAR(20)", "VISUAL, BLE, FRS, VERBAL"),
    ("room_confirmed", "BOOLEAN", "DEFAULT FALSE"),
    ("notes", "TEXT", "NULLABLE"),
    ("created_at", "TIMESTAMPTZ", "DEFAULT NOW()"),
]
for i, row in enumerate(cols):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 30)
pdf.ln(3)
sub_title(pdf, "Business Rules")
rules = [
    "BR-10.01: Daily roster pull must include crew from all active assignments for that property and date.",
    "BR-10.02: Supervisor sign-off is required before 12:00 local time for morning verification.",
    "BR-10.03: Crew marked ABSENT for 2+ hours with no communication trigger automatic escalation.",
    "BR-10.04: Unauthorized occupant detection (device detected, no roster entry) escalates to security immediately.",
    "BR-10.05: Verification reports are retained for 7 years for compliance auditing.",
    "BR-10.06: Supervisor cannot sign off if >20% of crew are UNVERIFIED. System blocks sign-off until resolved.",
]
for rule in rules:
    bullet(pdf, rule)

sub_title(pdf, "User Stories")
user_story(pdf, "10.01", "crew supervisor",
    "to pull the daily expected roster for my property at shift start",
    "I know exactly which crew should be present and can begin verification",
    "supervisor is assigned to a property with crew today", "they open the check-off module",
    "expected crew list is displayed with names, rooms, shifts, and current check-in status",
    "Must", "Phase 3 - Week 13")
user_story(pdf, "10.02", "crew supervisor",
    "to mark each crew member as verified, absent, or late",
    "actual crew presence is recorded against the expected roster",
    "supervisor has the daily roster displayed", "they verify each crew member",
    "each crew status is updated and persisted, running totals show verified/absent/late counts",
    "Must", "Phase 3 - Week 13")
user_story(pdf, "10.03", "crew supervisor",
    "to digitally sign off that the daily roster verification is complete",
    "there is an official record of supervisor verification for compliance",
    "supervisor has verified all crew (or noted discrepancies)", "they submit sign-off",
    "sign-off is recorded with timestamp and supervisor ID, daily report is generated, ops is notified",
    "Must", "Phase 3 - Week 13")
user_story(pdf, "10.04", "operations manager",
    "to receive escalations when crew are absent for 2+ hours without communication",
    "I can take action on missing crew before it becomes a safety issue",
    "crew has been marked ABSENT for 2 hours with no response", "escalation timer triggers",
    "ops manager receives push notification and email with crew details, property, and last known status",
    "Must", "Phase 3 - Week 14")
user_story(pdf, "10.05", "security team",
    "to receive immediate alerts when unauthorized occupants are detected",
    "unauthorized property access is identified and addressed quickly",
    "BLE device is detected within geofence with no matching roster entry", "system detects discrepancy",
    "security alert is generated with device details, location, and time, routed to security team",
    "Should", "Phase 3 - Week 14")
user_story(pdf, "10.06", "compliance officer",
    "to access historical roster verification reports for any property and date",
    "I can audit past verifications and demonstrate compliance to regulators",
    "verification reports exist for the requested period", "compliance officer queries reports",
    "all reports returned with full details: crew list, verification status, discrepancies, supervisor sign-off",
    "Must", "Phase 3 - Week 14")


# ============================================================
# PART 3: INTEGRATION MAP
# ============================================================
pdf.add_page()
section_title(pdf, "PART 3: INTEGRATION MAP")

sub_title(pdf, "3.1 Domain Interconnection Matrix")
body_text(pdf, "The following matrix shows how each of the 10 domains connects to every other domain. R = Reads from, W = Writes to, E = Events (pub/sub), S = Shared data model.")

body_text(pdf, """
INTEGRATION MATRIX:
                D1   D2   D3   D4   D5   D6   D7   D8   D9   D10
D1 BLE Swarm    --   W,E  R,E  W,E  .    R    R    R    W,E  R
D2 Fraud Det    R    --   R,E  R,E  R    .    W    R    W    .
D3 Geofence     W,E  W,E  --   W,E  .    R    R    R,W  W    R
D4 Check-In     R    W    R    --   R    .    W    R,W  W    W
D5 Lodging Auth .    .    .    R    --   R    R    R,W  R    .
D6 Supervisor   R    .    R    .    R    --   E    R    R    R,W
D7 Sup Workflow  R    R    R    .    R    E    --   R    R    R,W
D8 Roster Core  W    R    W    W    W    W    W    --   R    W
D9 Compliance   R    R    R    R    R    R    R    R    --   R
D10 Check-Off   R    .    R    R    .    W    W    R    W    --
""")

sub_title(pdf, "3.2 Data Flow Between Domains")
flows = [
    "Crew Profile Data: Domain 8 (Roster Core) -> All domains. Roster Core owns crew profiles and assignments; all other domains read from it.",
    "Check-In Events: Domain 4 (Check-In) -> Domain 2 (Fraud), Domain 8 (Roster), Domain 9 (Compliance). Every check-in event flows to fraud scoring, roster update, and compliance logging.",
    "Geofence Transitions: Domain 3 (Geofence) -> Domain 1 (BLE), Domain 2 (Fraud), Domain 4 (Check-In). Geofence entry triggers BLE activation, fraud scoring context, and check-in eligibility.",
    "BLE Swarm Data: Domain 1 (BLE Swarm) -> Domain 2 (Fraud), Domain 4 (Check-In), Domain 10 (Check-Off). Swarm proximity data feeds fraud detection, auto-check-in, and supervisor verification.",
    "Authorization Data: Domain 5 (Lodging Auth) -> Domain 4 (Check-In), Domain 8 (Roster). Approved authorizations create roster assignments and enable check-in eligibility.",
    "Supervisor Activities: Domain 6/7 (Supervisor) -> Domain 8 (Roster), Domain 9 (Compliance). Supervisor verifications, reports, and sign-offs update roster state and compliance records.",
    "Compliance Policies: Domain 9 (Compliance) -> All domains. Encryption, access control, consent, and retention policies are enforced across every domain.",
    "Fraud Alerts: Domain 2 (Fraud) -> Domain 7 (Supervisors), Domain 9 (Compliance). Suspicious and Critical alerts are routed to supervisors and compliance for action.",
]
for flow in flows:
    bullet(pdf, flow)

check_page_space(pdf, 40)
sub_title(pdf, "3.3 API Dependency Chain")
body_text(pdf, "Services must start in this order to satisfy dependencies:")
numbered_item(pdf, 1, "PostgreSQL + Redis (infrastructure)")
numbered_item(pdf, 2, "Auth Service (identity provider)")
numbered_item(pdf, 3, "Domain 9 - Compliance Service (policies must be loaded before any data processing)")
numbered_item(pdf, 4, "Domain 8 - Roster Core (crew profiles and assignments)")
numbered_item(pdf, 5, "Domain 5 - Lodging Authorization (depends on Roster Core for crew data)")
numbered_item(pdf, 6, "Domain 3 - Geofence Engine (depends on Roster Core for property/assignment data)")
numbered_item(pdf, 7, "Domain 1 - BLE Swarm Service (depends on Geofence for activation boundaries)")
numbered_item(pdf, 8, "Domain 4 - Check-In Service (depends on BLE, Geofence, Roster Core)")
numbered_item(pdf, 9, "Domain 2 - Fraud Detection (depends on Check-In events, BLE data, Geofence data)")
numbered_item(pdf, 10, "Domain 6/7 - Supervisor Services (depends on all operational domains)")
numbered_item(pdf, 11, "Domain 10 - Check-Off Service (depends on Roster Core and Check-In)")

sub_title(pdf, "3.4 Shared Data Models")
body_text(pdf, "These entities are shared (read) across multiple domains:")
bullet(pdf, "crew_profiles - owned by Domain 8, read by all domains")
bullet(pdf, "properties - owned by Domain 8, read by Domains 1-7, 9, 10")
bullet(pdf, "roster_assignments - owned by Domain 8, read by Domains 3, 4, 5, 7, 10")
bullet(pdf, "geofences - owned by Domain 3, read by Domains 1, 4, 6, 7, 10")
bullet(pdf, "consent_records - owned by Domain 9, read by Domains 1, 2, 6, 7")


# ============================================================
# PART 4: SPRINT PLAN
# ============================================================
pdf.add_page()
section_title(pdf, "PART 4: SPRINT PLAN")

sub_title(pdf, "Phase 1: Check-In MVP (Weeks 1-3)")
body_text(pdf, "Goal: Deliver the core check-in workflow with lodging authorization and geofence detection. This phase provides immediate operational value by digitizing the check-in process.")

sub_sub_title(pdf, "Week 1: Foundation", NAVY)
stories_w1 = [
    "US-4.01: Crew check-in via mobile device (12-step flow)",
    "US-4.02: QR code scanning and validation",
    "US-4.03: Room number double-entry confirmation",
    "US-4.07: Assignment verification (reject unauthorized)",
    "US-5.01: Lodging authorization request submission",
    "US-5.02: Contract rate verification",
]
for s in stories_w1:
    bullet(pdf, s)

sub_sub_title(pdf, "Week 2: Core Integration", NAVY)
stories_w2 = [
    "US-4.04: Supervisor check-in notification",
    "US-4.05: IOTA Tangle event logging",
    "US-4.06: Compliance validation at check-in",
    "US-3.01: Automatic geofence entry detection",
    "US-3.06: Automatic departure detection",
    "US-5.03: Supervisor authorization approval/rejection",
    "US-5.04: PO number generation",
    "US-5.05: CrimeShield compliance screening",
]
for s in stories_w2:
    bullet(pdf, s)

sub_sub_title(pdf, "Week 3: Polish & Hardening", NAVY)
stories_w3 = [
    "US-4.08: Fraud scoring integration for check-ins",
    "US-3.02: Supervisor geofence override",
    "US-3.03: Real-time property occupancy dashboard",
    "US-3.04: Geofenced BLE activation",
    "US-3.05: Geofence event audit logging",
    "US-5.06: Tax rate lookup by jurisdiction",
]
for s in stories_w3:
    bullet(pdf, s)

pdf.ln(3)
sub_title(pdf, "Phase 2: BLE Swarm + Fraud + Compliance (Weeks 4-8)")
body_text(pdf, "Goal: Deploy the BLE swarm intelligence layer, AI fraud detection, and compliance framework. This phase introduces the decentralized presence detection and automated fraud scoring that differentiate GoCrew from conventional roster systems.")

sub_sub_title(pdf, "Week 4: BLE Foundation", TEAL)
stories = [
    "US-1.02: Daily UUID rotation",
    "US-1.05: AES-256 encryption for contact logs",
]
for s in stories:
    bullet(pdf, s)

sub_sub_title(pdf, "Week 5: Swarm Intelligence", TEAL)
stories = [
    "US-1.01: Automated swarm check-in (3+ devices)",
    "US-1.03: Consent tier management",
    "US-1.06: Swarm roster status query",
    "US-1.07: IOTA Tangle log submission",
    "US-1.10: Geofenced BLE deactivation on exit",
]
for s in stories:
    bullet(pdf, s)

sub_sub_title(pdf, "Week 6: Fraud Detection Core", TEAL)
stories = [
    "US-1.04: Alibi Engine with tamper-proof proofs",
    "US-1.08: Supervisor swarm check-in visibility",
    "US-2.01: Geographic anomaly fraud alerts",
    "US-2.03: Impossible travel detection",
    "US-2.06: Critical alert SMS/Teams delivery",
    "US-9.03: Complete audit trail access",
]
for s in stories:
    bullet(pdf, s)

sub_sub_title(pdf, "Week 7: Fraud + Compliance", TEAL)
stories = [
    "US-1.09: Legal/court order data access (Tier 5)",
    "US-2.02: Automated weekly fraud reports",
    "US-2.04: Fraud alert resolution feedback loop",
    "US-2.08: ML model auto-rollback on degradation",
    "US-9.01: Crew data export (GDPR portability)",
    "US-9.02: Crew data deletion request",
]
for s in stories:
    bullet(pdf, s)

sub_sub_title(pdf, "Week 8: Advanced Features", TEAL)
stories = [
    "US-2.05: Per-property threshold configuration",
    "US-2.07: ML model performance monitoring",
    "US-9.04: Annual encryption key rotation",
    "US-9.05: Privacy Impact Assessment workflow",
    "US-9.06: DFARS 72-hour cyber incident reporting",
]
for s in stories:
    bullet(pdf, s)

pdf.ln(3)
sub_title(pdf, "Phase 3: Supervisor + Workforce Management (Weeks 9-14)")
body_text(pdf, "Goal: Deploy the supervisor mobile applications, workforce management features, and roster verification workflows. This phase completes the full system with human-in-the-loop verification and comprehensive supervisor tooling.")

sub_sub_title(pdf, "Week 9: Roster Core", EMERALD)
stories = ["US-8.01: Crew assignment creation and management"]
for s in stories:
    bullet(pdf, s)

sub_sub_title(pdf, "Week 10: Supervisor Foundation", EMERALD)
stories = [
    "US-6.01: Unified supervisor dashboard",
    "US-6.03: Crew hours and overtime tracking",
    "US-6.08: Compliance dashboard with certification status",
    "US-7.01: Daily schedule delivery by 5 AM",
    "US-7.02: BLE-confirmed onsite supervisor arrival",
    "US-7.07: Automatic ONSITE/OFFSITE mode switching",
    "US-8.02: Schedule publishing to crew (7-day advance)",
    "US-8.04: Late arrival and no-show alerts",
]
for s in stories:
    bullet(pdf, s)

sub_sub_title(pdf, "Week 11: Supervisor Operations", EMERALD)
stories = [
    "US-6.02: Incident reporting with evidence",
    "US-6.05: Offline mode with sync",
    "US-6.07: Broadcast messaging",
    "US-6.10: Daily safety checklists",
    "US-7.03: Remote crew location monitoring",
    "US-7.05: Daily report submission",
    "US-8.03: Shift swap requests",
]
for s in stories:
    bullet(pdf, s)

sub_sub_title(pdf, "Week 12: Advanced Supervisor", EMERALD)
stories = [
    "US-6.04: Face recognition identity verification",
    "US-6.06: Property map with crew positions",
    "US-6.09: Maintenance request submission",
    "US-7.04: Virtual video check-in (offsite)",
    "US-7.06: Onsite-offsite coordination messaging",
]
for s in stories:
    bullet(pdf, s)

sub_sub_title(pdf, "Week 13: Check-Off & Reports", EMERALD)
stories = [
    "US-7.08: Late daily report notifications",
    "US-8.05: Utilization reporting and analytics",
    "US-8.06: Anonymous crew feedback",
    "US-10.01: Daily roster pull for verification",
    "US-10.02: Crew verification marking",
    "US-10.03: Supervisor digital sign-off",
]
for s in stories:
    bullet(pdf, s)

sub_sub_title(pdf, "Week 14: Escalation & Hardening", EMERALD)
stories = [
    "US-10.04: Absent crew escalation (2+ hours)",
    "US-10.05: Unauthorized occupant security alerts",
    "US-10.06: Historical verification report access",
]
for s in stories:
    bullet(pdf, s)


# ============================================================
# PART 5: APPENDIX
# ============================================================
pdf.add_page()
section_title(pdf, "PART 5: APPENDIX")

sub_title(pdf, "A. Glossary of Terms")
terms = [
    ("Alibi Engine", "Continuous tamper-proof location trail on IOTA Tangle for crew defense against false accusations."),
    ("BLE Beacon", "A Bluetooth Low Energy device that broadcasts a UUID signal at regular intervals for proximity detection."),
    ("Consent Tier", "One of five access levels controlling who can see crew proximity and location data."),
    ("CrimeShield Score", "A safety rating assigned to lodging properties based on crime statistics and incident history."),
    ("CUI", "Controlled Unclassified Information - government information requiring safeguarding per NIST SP 800-171."),
    ("Geofence", "A virtual boundary around a physical property defined by GPS coordinates and radius/polygon."),
    ("IOTA Tangle", "A directed acyclic graph (DAG) distributed ledger that supports feeless transactions."),
    ("KYC", "Know Your Customer - identity verification process linking real identity to system credentials."),
    ("NFI Check", "No Further Information check - validation that all required data fields are present."),
    ("Privacy Impact Assessment", "Formal assessment of how a system feature affects user privacy, required before production."),
    ("QR JWT", "A QR code containing a signed JSON Web Token with property identification and anti-replay nonce."),
    ("RBAC", "Role-Based Access Control - permissions assigned by role rather than individual user."),
    ("RSSI", "Received Signal Strength Indicator - measurement of BLE signal power used for proximity estimation."),
    ("Swarm Check-In", "Automated check-in triggered when 3+ crew devices mutually detect each other within geofence."),
    ("UUID Rotation", "Daily replacement of temporary Bluetooth identifier to prevent long-term tracking."),
    ("Zero-Knowledge Proof", "Cryptographic method to prove identity/status without revealing the underlying data."),
]
for term, defn in terms:
    check_page_space(pdf, 12)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*NAVY)
    pdf.cell(50, 5, term, new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK_GRAY)
    pdf.multi_cell(0, 5, defn, new_x="LMARGIN", new_y="NEXT")

pdf.ln(4)
sub_title(pdf, "B. Acronym Reference")
headers = ["Acronym", "Full Name"]
widths = [35, 155]
table_header(pdf, headers, widths)
acronyms = [
    ("ADA", "Americans with Disabilities Act (room accessibility standard)"),
    ("AES", "Advanced Encryption Standard (256-bit symmetric encryption)"),
    ("API", "Application Programming Interface"),
    ("BLE", "Bluetooth Low Energy"),
    ("CCPA", "California Consumer Privacy Act"),
    ("CMMC", "Cybersecurity Maturity Model Certification"),
    ("CUI", "Controlled Unclassified Information"),
    ("DAG", "Directed Acyclic Graph (IOTA Tangle structure)"),
    ("DFARS", "Defense Federal Acquisition Regulation Supplement"),
    ("ECDH", "Elliptic Curve Diffie-Hellman (key exchange protocol)"),
    ("FAR", "Federal Acquisition Regulation"),
    ("FRS", "Face Recognition System"),
    ("GDPR", "General Data Protection Regulation (EU)"),
    ("GPS", "Global Positioning System"),
    ("GSA", "General Services Administration (per diem rates)"),
    ("HSM", "Hardware Security Module"),
    ("IOTA", "Internet of Things Application (distributed ledger)"),
    ("JWT", "JSON Web Token"),
    ("KMS", "Key Management Service"),
    ("KYC", "Know Your Customer"),
    ("MFA", "Multi-Factor Authentication"),
    ("ML", "Machine Learning"),
    ("NIST", "National Institute of Standards and Technology"),
    ("PIA", "Privacy Impact Assessment"),
    ("PMS", "Property Management System"),
    ("PO", "Purchase Order"),
    ("RBAC", "Role-Based Access Control"),
    ("RSSI", "Received Signal Strength Indicator"),
    ("SLA", "Service Level Agreement"),
    ("TLS", "Transport Layer Security"),
    ("UUID", "Universally Unique Identifier"),
]
for i, row in enumerate(acronyms):
    table_row(pdf, row, widths, fill=(i % 2 == 0))

check_page_space(pdf, 40)
pdf.ln(4)
sub_title(pdf, "C. Document Revision History")
headers = ["Version", "Date", "Author", "Changes"]
widths = [25, 35, 50, 80]
table_header(pdf, headers, widths)
revisions = [
    ("1.0", "March 2026", "Crew Logistics Engineering", "Initial release - full system specification"),
]
for i, row in enumerate(revisions):
    table_row(pdf, row, widths, fill=False)

pdf.ln(8)
body_text(pdf, "--- END OF DOCUMENT ---")
body_text(pdf, "This document is the property of Crew Logistics. Distribution without written authorization is prohibited.")
body_text(pdf, "Document Classification: CUI // Controlled Unclassified Information")


# ============================================================
# OUTPUT
# ============================================================
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
pdf.output(OUTPUT_PATH)
print(f"PDF generated: {OUTPUT_PATH}")
print(f"Total pages: {pdf.page_no()}")
