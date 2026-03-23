#!/usr/bin/env python3
"""Generate GoCrew Requirements & Epics PDF using fpdf2."""

from fpdf import FPDF
import os

# Color scheme
NAVY = (27, 42, 74)
TEAL = (13, 115, 119)
GOLD = (196, 151, 42)
EMERALD = (5, 150, 105)
RED = (220, 38, 38)
DARK_GRAY = (74, 85, 104)
WHITE = (255, 255, 255)
LIGHT_GRAY = (240, 242, 245)
MEDIUM_GRAY = (200, 205, 212)


class GCPdf(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=25)
        self.is_cover = False

    def header(self):
        if self.is_cover:
            return
        if self.page_no() <= 1:
            return
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*NAVY)
        self.cell(0, 6, "GOCREW | REQUIREMENTS & EPICS", align="L", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*TEAL)
        self.set_line_width(0.5)
        self.line(10, 12, 200, 12)
        self.ln(4)

    def footer(self):
        if self.is_cover:
            return
        if self.page_no() <= 1:
            return
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*DARK_GRAY)
        self.cell(0, 10, f"Crew Logistics | Confidential", align="L")
        self.set_x(-30)
        self.cell(0, 10, f"Page {self.page_no()}", align="R")


def safe(text):
    """Replace unicode chars with ASCII equivalents."""
    return (text
            .replace("\u2013", "-")
            .replace("\u2014", "-")
            .replace("\u2018", "'")
            .replace("\u2019", "'")
            .replace("\u201c", '"')
            .replace("\u201d", '"')
            .replace("\u2022", "-")
            .replace("\u2026", "...")
            .replace("\u00b7", "-")
            .replace("\u2192", "->")
            .replace("\u2265", ">=")
            .replace("\u2264", "<=")
            .replace("\u00a0", " ")
            )


def add_cover(pdf):
    pdf.is_cover = True
    pdf.add_page()
    # Navy background block
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, 210, 297, "F")

    # Teal accent bar
    pdf.set_fill_color(*TEAL)
    pdf.rect(0, 80, 210, 4, "F")
    pdf.rect(0, 213, 210, 4, "F")

    # Title block
    pdf.set_y(95)
    pdf.set_font("Helvetica", "B", 36)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 18, safe("GOCREW SMART CHECK-IN"), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 20)
    pdf.set_text_color(*GOLD)
    pdf.cell(0, 12, safe("REQUIREMENTS SPECIFICATION"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 12, safe("& ENGINEERING BACKLOG"), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 8, safe("Document: GC-REQ-001"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, safe("Date: March 2026"), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*TEAL)
    # Stats bar
    stats = "49 Features  |  10 Epics  |  55 User Stories  |  14 API Endpoints"
    pdf.cell(0, 10, safe(stats), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(25)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*MEDIUM_GRAY)
    pdf.cell(0, 6, safe("Crew Logistics"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, safe("Confidential - Internal Use Only"), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.is_cover = False


def section_title(pdf, text, level=1):
    """Add a section title."""
    if level == 1:
        pdf.add_page()
        pdf.set_fill_color(*NAVY)
        pdf.set_text_color(*WHITE)
        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 14, safe("  " + text), fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
    elif level == 2:
        pdf.ln(3)
        pdf.set_fill_color(*TEAL)
        pdf.set_text_color(*WHITE)
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, safe("  " + text), fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
    elif level == 3:
        pdf.ln(2)
        pdf.set_text_color(*NAVY)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, safe(text), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)


def body_text(pdf, text):
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK_GRAY)
    pdf.multi_cell(0, 4.5, safe(text), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)


def bullet_list(pdf, items):
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK_GRAY)
    for item in items:
        pdf.cell(5, 4.5, "")
        pdf.multi_cell(0, 4.5, safe("- " + item), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)


def label_value(pdf, label, value):
    x = pdf.get_x()
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*TEAL)
    pdf.cell(35, 5, safe(label + ":"))
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK_GRAY)
    pdf.multi_cell(0, 5, safe(value), new_x="LMARGIN", new_y="NEXT")


def add_feature(pdf, name, desc, inputs, outputs, api, data_stored, acceptance):
    """Add a feature block."""
    check_space(pdf, 60)
    section_title(pdf, name, level=3)
    body_text(pdf, desc)
    label_value(pdf, "Inputs", inputs)
    label_value(pdf, "Outputs", outputs)
    label_value(pdf, "API Endpoint", api)
    if data_stored:
        label_value(pdf, "Data Stored", data_stored)
    label_value(pdf, "Acceptance", acceptance)
    pdf.ln(2)


def check_space(pdf, needed_mm):
    if pdf.get_y() + needed_mm > 275:
        pdf.add_page()


def add_table_header(pdf, cols):
    """cols = list of (label, width)"""
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*NAVY)
    pdf.set_text_color(*WHITE)
    for label, w in cols:
        pdf.cell(w, 6, safe(label), border=1, fill=True)
    pdf.ln()


def add_table_row(pdf, cols, values, alt=False):
    """cols = list of (label, width), values = list of strings."""
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(*DARK_GRAY)
    if alt:
        pdf.set_fill_color(*LIGHT_GRAY)
    else:
        pdf.set_fill_color(*WHITE)
    max_h = 5
    # Calculate needed heights
    x_start = pdf.get_x()
    y_start = pdf.get_y()
    heights = []
    for i, (_, w) in enumerate(cols):
        # Estimate lines needed
        text = safe(values[i])
        char_w = pdf.get_string_width("x")
        chars_per_line = max(1, int(w / char_w))
        lines = max(1, len(text) // chars_per_line + 1)
        heights.append(lines * 4)
    row_h = max(heights)
    row_h = max(row_h, 5)

    if y_start + row_h > 275:
        pdf.add_page()
        add_table_header(pdf, cols)
        y_start = pdf.get_y()

    for i, (_, w) in enumerate(cols):
        x = x_start + sum(c[1] for c in cols[:i])
        pdf.set_xy(x, y_start)
        pdf.multi_cell(w, 4, safe(values[i]), border=1, fill=True, new_x="RIGHT", new_y="TOP")
    pdf.set_xy(x_start, y_start + row_h)


def add_api_table(pdf, method, path, auth, req_body, resp_body, side_effects, errors):
    check_space(pdf, 40)
    section_title(pdf, f"{method} {path}", level=3)

    label_value(pdf, "Auth Required", auth)
    pdf.ln(1)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 5, safe("Request Body:"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*DARK_GRAY)
    for field in req_body:
        pdf.cell(8, 4, "")
        pdf.multi_cell(0, 4, safe("- " + field), new_x="LMARGIN", new_y="NEXT")

    pdf.ln(1)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 5, safe("Response Body:"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*DARK_GRAY)
    for field in resp_body:
        pdf.cell(8, 4, "")
        pdf.multi_cell(0, 4, safe("- " + field), new_x="LMARGIN", new_y="NEXT")

    pdf.ln(1)
    label_value(pdf, "Side Effects", side_effects)
    label_value(pdf, "Error Cases", errors)
    pdf.ln(3)


def add_user_story(pdf, story_id, title, role, action, benefit, criteria, priority, sprint, deps):
    check_space(pdf, 50)
    # Story ID and title
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*NAVY)
    pdf.cell(25, 6, safe(story_id))
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 6, safe(title), new_x="LMARGIN", new_y="NEXT")

    # User story sentence
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*DARK_GRAY)
    pdf.multi_cell(0, 4.5, safe(f'As a {role}, I want {action}, so that {benefit}.'), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    # Acceptance criteria
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 4.5, safe("Acceptance Criteria:"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*DARK_GRAY)
    for c in criteria:
        pdf.cell(5, 4, "")
        pdf.multi_cell(0, 4, safe("- " + c), new_x="LMARGIN", new_y="NEXT")

    # Meta row
    pdf.ln(1)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*EMERALD)
    pdf.cell(30, 4.5, safe(f"Priority: {priority}"))
    pdf.set_text_color(*GOLD)
    pdf.cell(40, 4.5, safe(f"Sprint: {sprint}"))
    pdf.set_text_color(*DARK_GRAY)
    pdf.cell(0, 4.5, safe(f"Dependencies: {deps}"), new_x="LMARGIN", new_y="NEXT")

    # Separator
    pdf.set_draw_color(*MEDIUM_GRAY)
    pdf.set_line_width(0.2)
    pdf.line(10, pdf.get_y() + 1, 200, pdf.get_y() + 1)
    pdf.ln(3)


def build_pdf():
    pdf = GCPdf()

    # ==============================
    # COVER PAGE
    # ==============================
    add_cover(pdf)

    # ==============================
    # TABLE OF CONTENTS
    # ==============================
    pdf.add_page()
    section_title_inline(pdf, "TABLE OF CONTENTS")
    toc_items = [
        ("PART 1: REQUIREMENTS SPECIFICATION", ""),
        ("  Epic 1: Crew Check-In", "8 features"),
        ("  Epic 2: Check-Out & Stay Management", "6 features"),
        ("  Epic 3: Wallet & Pass", "4 features"),
        ("  Epic 4: Fraud Detection & FRS", "8 features"),
        ("  Epic 5: BLE Proximity & Swarm", "7 features"),
        ("  Epic 6: Property Portal", "5 features"),
        ("  Epic 7: Notifications", "4 features"),
        ("  Epic 8: Crew Experience", "5 features"),
        ("  Epic 9: Compliance & Legal", "4 features"),
        ("  Epic 10: Analytics & Intelligence", "4 features"),
        ("", ""),
        ("PART 2: INPUT/OUTPUT MAPPING BY FEATURE", "14 endpoints"),
        ("", ""),
        ("PART 3: EPICS & USER STORIES", "55 stories"),
    ]
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*DARK_GRAY)
    for item, note in toc_items:
        if item == "":
            pdf.ln(3)
            continue
        if item.startswith("  "):
            pdf.cell(10, 6, "")
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(120, 6, safe(item.strip()))
        else:
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(130, 6, safe(item))
        if note:
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(*TEAL)
            pdf.cell(0, 6, safe(note))
            pdf.set_text_color(*DARK_GRAY)
        pdf.ln()

    # ==============================
    # PART 1: REQUIREMENTS SPECIFICATION
    # ==============================
    section_title(pdf, "PART 1: REQUIREMENTS SPECIFICATION")
    body_text(pdf, "This section defines the functional requirements for the GoCrew Smart Check-In system. "
              "The platform enables crew members to check into contracted hotel properties via QR code scan "
              "or self-service scan, with a seven-layer Fraud Risk Score engine, BLE proximity detection, "
              "swarm mesh crew-to-crew verification, wallet pass integration, and a progressive web application. "
              "Pricing model: $2 per crew member per day.")

    body_text(pdf, "System components: QR Token Engine (JWT-signed tokens), Geofence GPS Verification, "
              "7-Layer Fraud Risk Score (FRS), BLE Beacon Proximity, Swarm Mesh Crew-to-Crew Detection, "
              "Wallet Pass (Apple .pkpass + PWA home screen), Progressive Web Application.")

    # ---- EPIC 1 ----
    section_title(pdf, "EPIC 1: CREW CHECK-IN", level=2)
    body_text(pdf, "Core check-in workflows enabling crew to register their arrival at a property. "
              "Supports front-desk scan, self-service scan, automated swarm detection, photo verification, "
              "and digital signature capture. All check-ins produce a signed audit record.")

    add_feature(pdf,
        "F1.1 QR Check-In (Front Desk Scan)",
        "Front desk staff scans the crew member's QR code displayed on their device. The QR contains "
        "a JWT token with crew ID, assignment ID, and expiration. System validates token, verifies "
        "assignment against the property, and records check-in with timestamp and operator ID.",
        "JWT QR token (crew device screen), property operator scan via webcam or handheld scanner",
        "Check-in record created, confirmation screen displayed, SMS/email sent to crew, real-time roster updated",
        "POST /api/checkin",
        "checkins table: id, crew_id, assignment_id, property_id, room_number, check_in_time, method='qr_frontdesk', operator_id, frs_score, gps_lat, gps_lng, ble_beacon_id",
        "Crew receives confirmation within 3 seconds of scan; FRS score computed and stored; roster updated in real-time"
    )

    add_feature(pdf,
        "F1.2 Self-Service Check-In (Crew Scans Property QR)",
        "Crew member scans a QR code posted at the property lobby using their phone camera. The property "
        "QR encodes the property ID and a rotating nonce. The crew's PWA validates their assignment, captures "
        "GPS coordinates, checks BLE beacon proximity, and submits the check-in.",
        "Property QR code scanned by crew phone camera, GPS coordinates (auto-captured), BLE beacon signal (auto-detected), crew JWT auth token",
        "Check-in record created, room number confirmation prompt, wallet pass updated, confirmation notification sent",
        "POST /api/checkin",
        "checkins table: same schema plus method='self_service', device_fingerprint, ble_rssi, gps_accuracy_m",
        "GPS must be within 200m of property coordinates; BLE beacon must be detected; crew prompted for room number"
    )

    add_feature(pdf,
        "F1.3 Room Number Confirmation",
        "After QR scan, crew enters their assigned room number using a numeric keypad. Double-entry "
        "pattern: crew enters room number, then re-enters to confirm. Only digits allowed, 1-6 characters. "
        "System validates against expected room assignment if available.",
        "Room number (string, digits only, 1-6 chars), confirmation re-entry of room number",
        "Room number stored on check-in record, mismatch triggers re-entry prompt, confirmed room displayed on wallet pass",
        "PATCH /api/checkin/{id}/room",
        "checkins.room_number, checkins.room_confirmed_at",
        "Double entry must match; only numeric input accepted; room number appears on wallet pass after confirmation"
    )

    add_feature(pdf,
        "F1.4 Undo Check-In (15-Minute Window)",
        "Crew or front desk can undo a check-in within 15 minutes of creation. After 15 minutes the "
        "check-in is locked and requires supervisor override. Undo soft-deletes the record and logs the "
        "reversal with reason code.",
        "Check-in ID, reason for undo (dropdown: wrong_property, wrong_room, accidental, other), operator or crew auth",
        "Check-in marked as reversed, roster updated, wallet pass reverted to pre-check-in state, audit log entry created",
        "DELETE /api/checkin/{id}",
        "checkins.status='reversed', checkin_reversals: id, checkin_id, reason, reversed_by, reversed_at",
        "Undo available within 15 minutes; after 15 minutes returns 403 with 'window_expired'; audit trail preserved"
    )

    add_feature(pdf,
        "F1.5 Automated Swarm Check-In",
        "When 3 or more already-checked-in crew devices detect a new crew device via BLE mesh at the lobby "
        "beacon, the system can auto-check-in the new crew member without requiring a QR scan. The crew "
        "member receives a push notification asking them to confirm their room number. This reduces friction "
        "for late arrivals when other crew are already present.",
        "BLE mesh detection from 3+ corroborating crew devices, new crew device BLE broadcast, lobby beacon signal, crew assignment verification",
        "Auto-check-in record created with method='swarm_auto', room confirmation prompt sent via push notification, FRS score computed",
        "POST /api/checkin (triggered by POST /api/ble/report)",
        "checkins: method='swarm_auto', swarm_corroborators (array of crew_ids), ble_consensus_score",
        "Minimum 3 corroborating devices required; crew must still confirm room number; FRS score must be below alert threshold"
    )

    add_feature(pdf,
        "F1.6 Check-In Confirmation SMS/Email",
        "Immediately after successful check-in, system sends confirmation via SMS and email. Message "
        "includes property name, room number, check-in time, check-out date, and a link to the wallet pass. "
        "SMS uses Twilio; email uses SendGrid with branded HTML template.",
        "Crew phone number, crew email, check-in record details, property information",
        "SMS delivered (Twilio webhook confirmation), email delivered (SendGrid event), delivery status logged",
        "Triggered by POST /api/checkin (side effect)",
        "notifications table: id, crew_id, type='checkin_confirm', channel='sms'|'email', sent_at, delivered_at, provider_id",
        "SMS sent within 5 seconds of check-in; email sent within 30 seconds; delivery failures retried 3x"
    )

    add_feature(pdf,
        "F1.7 Photo Verification (Selfie Match)",
        "Optional layer: crew takes a selfie at check-in which is compared against their profile photo "
        "using facial similarity scoring. Score below threshold triggers manual review. Photos stored "
        "encrypted with 30-day retention policy. Used for high-security assignments or disputed check-ins.",
        "Live selfie image (JPEG, min 640x480), profile photo on file, crew_id for matching",
        "Similarity score (0.0-1.0), match_result (pass/review/fail), flagged for manual review if below 0.7 threshold",
        "POST /api/checkin/{id}/verify-photo",
        "photo_verifications: id, checkin_id, similarity_score, result, selfie_s3_key, reviewed_by, reviewed_at",
        "Photo captured with liveness detection (blink/head-turn); similarity >= 0.7 auto-passes; < 0.7 flags for review"
    )

    add_feature(pdf,
        "F1.8 Digital Signature Capture",
        "Crew member signs on the device touchscreen to acknowledge check-in terms (hotel policies, "
        "company travel policy acknowledgment). Signature stored as SVG path data with timestamp and "
        "device metadata. Required for government/DoD assignments.",
        "Touch/mouse signature input (SVG path data), device metadata (user agent, screen size), check-in ID",
        "Signature record created and linked to check-in, PDF receipt generated with embedded signature, compliance record updated",
        "POST /api/checkin/{id}/signature",
        "signatures: id, checkin_id, svg_data, device_meta, captured_at, ip_address",
        "Signature canvas minimum 200x80px; SVG data must contain at least 10 path points (prevents empty/trivial signatures)"
    )

    # ---- EPIC 2 ----
    section_title(pdf, "EPIC 2: CHECK-OUT & STAY MANAGEMENT", level=2)
    body_text(pdf, "Manages the full lifecycle of a crew stay from check-out through extensions, "
              "early departures, room changes, and automated detection of missed check-outs and no-shows.")

    add_feature(pdf,
        "F2.1 Check-Out with Confirmation",
        "Crew initiates check-out via the PWA or front desk triggers it. System records departure time, "
        "calculates stay duration, updates roster, and sends confirmation. Crew rates the property (optional). "
        "Check-out generates a billing event for the $2/crew/day calculation.",
        "Crew auth token or operator auth, check-in ID, optional feedback rating",
        "Check-out record created, billing event generated, roster updated, confirmation SMS/email sent, wallet pass updated to 'completed'",
        "POST /api/checkout",
        "checkouts: id, checkin_id, checkout_time, stay_nights, billing_amount, method, operator_id; billing_events: id, checkout_id, amount, status",
        "Stay nights calculated as ceil(checkout - checkin in hours / 24); billing event = stay_nights * $2; confirmation sent within 5 seconds"
    )

    add_feature(pdf,
        "F2.2 Extend Stay Request",
        "Crew requests to extend their stay beyond the original assignment end date. Request goes to "
        "operations for approval. System checks property availability and contract rate. Approved extensions "
        "update the assignment end date and wallet pass.",
        "Crew auth, assignment_id, new_end_date, reason for extension (dropdown + free text)",
        "Extension request created (pending), notification sent to operations, auto-approved if within contract terms and property confirms availability",
        "POST /api/stay/extend",
        "stay_extensions: id, assignment_id, original_end, requested_end, reason, status='pending'|'approved'|'denied', approved_by, approved_at",
        "Request submitted within 2 seconds; operations notified via push; auto-approval if <= 3 days and property has capacity"
    )

    add_feature(pdf,
        "F2.3 Early Departure Request",
        "Crew reports leaving earlier than planned. System updates assignment, triggers early check-out, "
        "adjusts billing, and notifies operations. Captures reason for departure analytics.",
        "Crew auth, assignment_id, actual_departure_date, reason (dropdown: project_change, personal, reassignment, other)",
        "Early departure recorded, check-out triggered, billing adjusted, operations notified, replacement crew workflow triggered if needed",
        "POST /api/stay/early-departure",
        "early_departures: id, assignment_id, original_end, actual_end, reason, billing_adjustment",
        "Billing recalculated to actual stay nights; operations notified within 1 minute; departure reason captured for analytics"
    )

    add_feature(pdf,
        "F2.4 Room Change",
        "Crew or front desk records a room change during a stay. Old room number is archived, new room "
        "number recorded. Wallet pass updates with new room. Change logged in audit trail.",
        "Crew or operator auth, checkin_id, new_room_number (digits only, double entry), reason for change",
        "Room number updated on check-in record, wallet pass refreshed, audit entry created, property notified",
        "POST /api/stay/room-change",
        "room_changes: id, checkin_id, old_room, new_room, reason, changed_at, changed_by",
        "New room validated via double-entry; wallet pass updated within 5 seconds; full change history preserved"
    )

    add_feature(pdf,
        "F2.5 Missed Check-Out Alerts",
        "Hourly cron job scans for crew past their assignment end date who have not checked out. "
        "System sends escalating alerts: first to crew, then to operations, then to property. "
        "BLE data used to determine if crew is still physically present.",
        "Scheduled scan (hourly), assignment end dates, check-out records, BLE last-seen data",
        "Missed check-out alert created, SMS/push sent to crew, escalation to operations after 2 hours, property notified after 4 hours",
        "Triggered by scheduler (side effect of cron job)",
        "missed_checkout_alerts: id, checkin_id, detected_at, crew_notified_at, ops_notified_at, property_notified_at, resolved_at, resolution",
        "First alert to crew at assignment end + 1 hour; escalation to ops at + 3 hours; property at + 5 hours"
    )

    add_feature(pdf,
        "F2.6 No-Show Detection",
        "Daily scan at 23:59 property local time identifies crew with assignments starting that day who "
        "never checked in. System flags as no-show, notifies operations, and triggers the no-show escalation "
        "chain. FRS score adjusted for no-show history.",
        "Scheduled scan (daily 23:59 local), assignment start dates, check-in records",
        "No-show record created, operations notified, escalation chain triggered, FRS historical factor updated",
        "Triggered by scheduler",
        "no_shows: id, assignment_id, crew_id, property_id, detection_date, escalation_level, resolved_at, resolution_reason",
        "Detection at 23:59 local time; operations notified within 5 minutes; FRS L4 behavioral baseline updated"
    )

    # ---- EPIC 3 ----
    section_title(pdf, "EPIC 3: WALLET & PASS", level=2)
    body_text(pdf, "Digital credential management giving crew a convenient, always-accessible representation "
              "of their assignment and check-in status, accessible even without internet.")

    add_feature(pdf,
        "F3.1 Wallet Pass Display (Boarding-Pass Style)",
        "PWA displays a boarding-pass-style card with crew name, property name, room number, check-in date, "
        "check-out date, assignment status, and QR code. Card uses the GoCrew brand colors. Updates in real-time "
        "as assignment status changes.",
        "Crew auth token, assignment data, check-in status, property information",
        "Rendered boarding-pass card in PWA, QR code for front desk scanning, dynamic status updates (upcoming/active/completed)",
        "GET /api/assignment/{id}",
        "No additional storage - reads from assignments and checkins tables",
        "Card renders in under 1 second; QR code regenerates every 60 seconds with rotating nonce; works offline via service worker cache"
    )

    add_feature(pdf,
        "F3.2 Save to Home Screen (PWA Install)",
        "PWA triggers the browser's Add to Home Screen prompt. Crew installs GoCrew as a standalone app "
        "with custom icon, splash screen, and offline support. Service worker caches active assignment data.",
        "User interaction (tap 'Install' button), PWA manifest.json, service worker registration",
        "App installed to home screen, offline-capable cached assignment, push notification permission requested",
        "Client-side only (no API call)",
        "No server-side storage - manifest and service worker assets cached on device",
        "Install prompt shown after 2nd visit; offline mode shows last-known assignment; push permission requested on install"
    )

    add_feature(pdf,
        "F3.3 Calendar Event Save",
        "Crew can save their assignment as a calendar event (.ics download or native calendar API). "
        "Event includes check-in date, check-out date, property address, and contact info. "
        "Two events created: check-in reminder (day before) and check-out reminder (morning of).",
        "Assignment data (dates, property address, contact info), crew calendar permission",
        "ICS file generated and downloaded, or native calendar event created, with reminders set",
        "GET /api/assignment/{id}/calendar",
        "No additional storage - generates ICS from assignment data",
        "ICS file validates in Apple Calendar, Google Calendar, Outlook; reminders set at correct times"
    )

    add_feature(pdf,
        "F3.4 Apple Wallet .pkpass (Production)",
        "Server generates a signed .pkpass file for Apple Wallet. Requires Apple Developer certificate and "
        "server-side signing. Pass displays as boarding-pass type with barcode, crew info, property info, "
        "and dynamic updates via push. Pass updates when assignment status changes.",
        "Apple Developer Team ID, pass type identifier, signing certificates (.p12), crew and assignment data",
        "Signed .pkpass file delivered to crew device, pass appears in Apple Wallet, push updates configured for status changes",
        "GET /api/assignment/{id}/wallet-pass",
        "wallet_passes: id, assignment_id, serial_number, pass_type_id, last_updated, push_token",
        "Pass validates in Apple Wallet; barcode scannable; push updates delivered within 30 seconds of status change"
    )

    # ---- EPIC 4 ----
    section_title(pdf, "EPIC 4: FRAUD DETECTION & FRS", level=2)
    body_text(pdf, "The 7-layer Fraud Risk Score (FRS) engine computes a composite score from 0 (no risk) to 100 "
              "(maximum risk) across identity, geospatial, temporal, behavioral, financial, roster, and network "
              "dimensions. Each layer scores 0-100 independently; composite is a weighted average. Thresholds: "
              "0-30 green (auto-approve), 31-60 yellow (flag for review), 61-100 red (block + alert).")

    add_feature(pdf,
        "F4.1 FRS Composite Scoring Engine",
        "Aggregates all seven layer scores into a single composite using configurable weights. Default weights: "
        "L1 Identity 20%, L2 Geospatial 20%, L3 Temporal 15%, L4 Behavioral 15%, L5 Financial 10%, "
        "L6 Roster 10%, L7 Network 10%. Composite determines auto-approve/flag/block decision.",
        "Individual layer scores (L1-L7), weight configuration, check-in context data",
        "Composite FRS score (0-100), risk_level (green/yellow/red), decision (approve/flag/block), layer breakdown",
        "POST /api/frs/score",
        "frs_scores: id, checkin_id, composite_score, risk_level, decision, l1-l7 individual scores, weights_version, computed_at",
        "Composite computed within 500ms; all layer scores logged; decision enforced at check-in gate"
    )

    add_feature(pdf,
        "F4.2 L1 - Identity Verification",
        "Validates crew identity against the roster database. Checks: crew_id exists, crew is active, "
        "profile photo on file, email/phone verified, government ID on file (for DoD assignments). "
        "Missing verification factors increase score.",
        "crew_id, crew profile completeness (photo, email_verified, phone_verified, gov_id_on_file), assignment active status",
        "L1 score (0-100): 0 if all verified, +20 for missing photo, +20 for unverified email, +20 for unverified phone, +25 for missing gov ID, +15 for inactive status",
        "Internal computation within POST /api/frs/score",
        "frs_scores.l1_score, frs_layer_details.l1_factors (JSON array of triggered factors)",
        "Each identity factor independently scored; score = sum of triggered factor weights; max 100"
    )

    add_feature(pdf,
        "F4.3 L2 - Geospatial Verification",
        "Validates check-in location against property coordinates. Computes distance from crew GPS to "
        "property lat/lng. Also checks BLE beacon detection as secondary signal. GPS spoofing detection "
        "via consistency checks (speed between readings, accuracy field analysis).",
        "Crew device GPS (lat, lng, accuracy_m, timestamp), property GPS (lat, lng), BLE beacon detection (beacon_id, rssi), previous GPS readings",
        "L2 score (0-100): 0 if GPS within 50m and BLE detected; +30 if GPS 50-200m; +60 if GPS >200m; +20 if no BLE; +40 if GPS spoofing suspected",
        "Internal computation within POST /api/frs/score",
        "frs_scores.l2_score, frs_layer_details.l2_gps_distance_m, l2_ble_detected, l2_spoof_indicators",
        "Haversine distance computed; BLE RSSI analyzed for proximity; GPS accuracy field checked for spoofing"
    )

    add_feature(pdf,
        "F4.4 L3 - Temporal Analysis",
        "Validates check-in timing against expected patterns. Checks: is check-in within assignment date "
        "range, is time of day reasonable (not 3 AM for a standard assignment), rapid successive check-ins "
        "from same device, check-in velocity (impossible travel between properties).",
        "Check-in timestamp, assignment start/end dates, crew's check-in history (last 30 days), time zone of property",
        "L3 score (0-100): 0 if within date range and normal hours; +25 if outside date range; +15 if unusual hour; +40 if impossible travel detected; +20 if rapid successive check-ins",
        "Internal computation within POST /api/frs/score",
        "frs_scores.l3_score, frs_layer_details.l3_time_of_day, l3_within_dates, l3_velocity_kmh",
        "Travel velocity > 800 km/h between check-ins flags impossible travel; after-hours check-in = 22:00-05:00 local"
    )

    add_feature(pdf,
        "F4.5 L4 - Behavioral Baseline",
        "Builds a behavioral profile per crew member over time. Compares current check-in patterns to "
        "historical baseline: typical check-in time, frequency of room changes, no-show history, "
        "extension patterns, feedback scores. Deviations from baseline increase risk.",
        "Crew historical data (last 90 days): check-in times, no-show count, room changes, extensions, feedback avg, dispute count",
        "L4 score (0-100): 0 if behavior matches baseline; +15 per no-show in last 90 days (max 45); +20 if check-in time deviates >3 hours from avg; +15 if abnormal extension pattern; +20 if disputes > 2",
        "Internal computation within POST /api/frs/score",
        "frs_scores.l4_score, frs_layer_details.l4_baseline_deviation, l4_no_show_count, l4_dispute_count",
        "Baseline computed from minimum 3 prior stays; new crew with no history get neutral score of 10"
    )

    add_feature(pdf,
        "F4.6 L5 - Financial Cross-Reference",
        "Cross-references check-in against financial signals: is the property rate within contracted bounds, "
        "is the crew member's company account in good standing, are there duplicate billing concerns "
        "(same crew, same dates, different properties).",
        "Assignment rate vs contract rate, company account status, concurrent assignments for same crew_id, billing history",
        "L5 score (0-100): 0 if all clear; +30 if rate exceeds contract by >10%; +35 if account delinquent; +50 if concurrent overlapping assignments detected; +20 if billing disputes > 3",
        "Internal computation within POST /api/frs/score",
        "frs_scores.l5_score, frs_layer_details.l5_rate_variance_pct, l5_account_status, l5_overlap_detected",
        "Concurrent assignment overlap = same crew, overlapping date ranges, different properties = high fraud signal"
    )

    add_feature(pdf,
        "F4.7 L6 - Roster Integrity",
        "Validates the check-in against the master crew roster. Checks: is crew on the active roster for "
        "this property, was the assignment created by an authorized dispatcher, has the roster been "
        "recently modified (bulk edits increase risk), crew count vs property capacity.",
        "Master roster for property_id, assignment creation metadata, roster modification log (last 48 hours), property capacity",
        "L6 score (0-100): 0 if crew on roster and no anomalies; +40 if crew not on original roster; +20 if assignment added in last 2 hours; +25 if bulk roster edit detected; +15 if property over capacity",
        "Internal computation within POST /api/frs/score",
        "frs_scores.l6_score, frs_layer_details.l6_on_roster, l6_assignment_age_hours, l6_bulk_edit_detected",
        "Last-minute roster additions (< 2 hours) flagged; bulk edits (> 10 changes in 1 hour) flagged"
    )

    add_feature(pdf,
        "F4.8 L7 - Network/Swarm Analysis",
        "Analyzes the social/network graph of crew at the property. Checks: are the other crew members "
        "at this property from the same company, have these crew members checked in together before, "
        "is the swarm BLE mesh pattern consistent with legitimate group travel. Detects coordinated fraud.",
        "BLE mesh data (which devices see which), crew company affiliations at property, historical co-location patterns",
        "L7 score (0-100): 0 if normal group pattern; +30 if crew company mismatch with property roster; +25 if no prior co-location with any other crew; +35 if BLE mesh shows phantom device patterns; +10 if unusual device count",
        "Internal computation within POST /api/frs/score",
        "frs_scores.l7_score, frs_layer_details.l7_company_match, l7_prior_colocation, l7_phantom_devices, l7_mesh_anomaly",
        "Phantom device = BLE broadcast without matching crew record; mesh anomaly = single device claiming proximity to many"
    )

    # ---- EPIC 5 ----
    section_title(pdf, "EPIC 5: BLE PROXIMITY & SWARM", level=2)
    body_text(pdf, "Bluetooth Low Energy proximity detection and swarm mesh networking provide physical "
              "presence verification, floor-level positioning, automated check-in, and a legally defensible "
              "alibi engine. BLE operates in the background on crew devices and property-installed beacons.")

    add_feature(pdf,
        "F5.1 Beacon Detection at Property",
        "Crew device PWA detects BLE beacons installed at property locations (lobby, floors, common areas). "
        "Beacon broadcasts contain property_id and zone_id. Device reports beacon detection with RSSI and "
        "timestamp to server. Used for presence verification in FRS L2.",
        "BLE beacon broadcast (UUID=property_id, major=zone_id, minor=floor), crew device BLE scan, RSSI measurement",
        "Beacon detection event logged, presence verified for FRS, zone/floor determination, last-seen timestamp updated",
        "POST /api/ble/report",
        "ble_detections: id, crew_id, beacon_uuid, major, minor, rssi, timestamp, device_id, gps_lat, gps_lng",
        "BLE scan interval: 10 seconds active, 30 seconds background; RSSI > -70 dBm = close proximity; detection persisted within 2 seconds"
    )

    add_feature(pdf,
        "F5.2 Floor-Level Positioning",
        "Using beacon minor value (floor number) and RSSI trilateration from multiple beacons, system "
        "determines which floor the crew member is on. Requires minimum 2 beacons detected. Floor data "
        "enriches the alibi engine and emergency muster.",
        "Multiple BLE beacon detections with different minor values (floors), RSSI values for trilateration",
        "Estimated floor number, confidence level (high/medium/low based on beacon count and RSSI quality), position timestamp",
        "Computed server-side from POST /api/ble/report data",
        "ble_positions: id, crew_id, property_id, floor, confidence, position_timestamp, beacon_count",
        "Minimum 2 beacons for floor estimation; 3+ beacons = high confidence; RSSI weighted by signal quality"
    )

    add_feature(pdf,
        "F5.3 Crew-to-Crew Swarm Mesh",
        "Crew devices broadcast and scan for other crew devices using BLE peripheral/central mode. Each "
        "crew device advertises a rotating identifier (derived from crew_id + timestamp + HMAC). When crew "
        "devices detect each other, they report the mesh topology to the server. This creates a peer-to-peer "
        "corroboration network.",
        "Crew device BLE broadcast (rotating crew identifier), peer device BLE scan, RSSI between devices, timestamps",
        "Mesh topology map (which crew see which crew, with RSSI and time), peer corroboration events, swarm density metric",
        "POST /api/ble/report (includes peer_detections array)",
        "ble_peer_detections: id, observer_crew_id, observed_crew_id, rssi, timestamp, property_id, floor",
        "Rotating identifier changes every 5 minutes; HMAC prevents spoofing; bilateral detection (A sees B AND B sees A) = strong corroboration"
    )

    add_feature(pdf,
        "F5.4 Automated Swarm Check-In",
        "When 3 or more already-checked-in crew devices corroborate the presence of a new crew device at "
        "the lobby beacon zone, the system triggers an auto-check-in for that crew member. Process: "
        "(1) New device detected by 3+ peers near lobby beacon, (2) System verifies new device belongs to "
        "crew with active assignment at this property, (3) Auto-check-in created with method='swarm_auto', "
        "(4) Push notification sent to crew for room number confirmation. The crew never needs to open the "
        "app or scan a QR code - their mere physical presence is verified by the swarm.",
        "3+ peer BLE detections of new crew device (bilateral), lobby beacon detection by new device, active assignment verification, "
        "peer crew check-in status verification (all 3+ peers must be checked-in)",
        "Auto-check-in record created, push notification for room confirmation, FRS score computed with L7 swarm bonus (lower risk), "
        "corroborating peer IDs logged",
        "POST /api/checkin (auto-triggered by swarm consensus)",
        "checkins: method='swarm_auto', swarm_corroborators=[crew_ids], swarm_consensus_score, lobby_beacon_detected=true",
        "3+ bilateral peer detections required; all peers must be checked-in; lobby beacon must be in range; room confirmation within 30 minutes or check-in reversed"
    )

    add_feature(pdf,
        "F5.5 Alibi Engine",
        "Creates a continuous, tamper-proof location trail for each crew member using multiple independent "
        "data sources. The alibi record serves as exonerating evidence if crew is falsely accused of being "
        "somewhere they were not. Data sources: (1) Property BLE beacons confirming floor and zone, "
        "(2) Crew-to-crew BLE mesh confirming proximity to specific other crew, (3) Timestamp chain with "
        "cryptographic hash linking (each record includes hash of previous record). "
        "Example: Hotel claims incident in stairwell Floor 2 at 11:15 PM, but alibi data proves crew was on "
        "Floor 4 near 2 other crew phones from 10:45 PM to 11:45 PM with unbroken beacon + mesh chain.",
        "Continuous BLE beacon detections (every 30 seconds), continuous peer mesh detections, GPS periodic updates, "
        "hash chain (SHA-256 of previous record + current data), server-side timestamps",
        "Alibi report (date range query): timeline of locations with confidence scores, corroborating witnesses "
        "(other crew devices), beacon confirmations, hash chain integrity verification, exportable PDF for legal use",
        "GET /api/ble/alibi/{crewId}?from=ISO&to=ISO",
        "alibi_chain: id, crew_id, timestamp, floor, zone, beacon_ids, peer_crew_ids, gps_lat, gps_lng, "
        "prev_hash, record_hash, chain_status",
        "Hash chain unbroken = tamper-proof; 3+ corroborating data sources at each point = legally defensible; "
        "report exportable as signed PDF with chain verification"
    )

    add_feature(pdf,
        "F5.6 Buddy Check-In Detection",
        "Detects when one crew member attempts to check in for another (buddy punching). Analyzed by "
        "comparing the device that initiated check-in with the expected device for that crew member. "
        "If crew A's phone checks in crew B, the system flags the discrepancy. BLE mesh data used to "
        "verify the actual crew member is physically present.",
        "Device fingerprint at check-in, expected device fingerprint for crew_id, BLE mesh - is the crew's own device present?",
        "Buddy punch flag raised, FRS score increased by 40 points, alert to operations, check-in held for manual review",
        "Computed during POST /api/checkin",
        "buddy_punch_flags: id, checkin_id, expected_device_id, actual_device_id, crew_device_ble_present, flagged_at, resolution",
        "Device mismatch + crew's own device not in BLE mesh = high confidence buddy punch; device mismatch but crew device in mesh = possible legitimate (new phone)"
    )

    add_feature(pdf,
        "F5.7 Emergency Muster",
        "Emergency button on property portal triggers immediate BLE muster scan. System compiles list of "
        "all crew detected via BLE at the property in the last 5 minutes, cross-references with roster, "
        "and displays accounted/missing/unknown lists. BLE floor data shows where crew were last seen.",
        "Emergency muster trigger (property portal button), BLE detections (last 5 minutes), active roster for property",
        "Muster report: accounted (crew detected + on roster), missing (on roster + not detected), unknown (detected + not on roster), "
        "last known floor/zone for each crew, timestamp of last detection",
        "GET /api/ble/muster/{propertyId}",
        "muster_events: id, property_id, triggered_at, triggered_by, crew_accounted, crew_missing, crew_unknown, resolved_at",
        "Muster report generated within 10 seconds; all crew accounted with last-seen location; missing crew list sent to operations immediately"
    )

    # ---- EPIC 6 ----
    section_title(pdf, "EPIC 6: PROPERTY PORTAL", level=2)
    body_text(pdf, "Web-based portal for property front desk staff and supervisors to manage crew check-ins, "
              "view arrivals, and handle operational workflows.")

    add_feature(pdf,
        "F6.1 Expected Arrivals Dashboard",
        "Property portal displays today's expected arrivals with crew name, company, assignment dates, "
        "and check-in status. Color-coded: gray (not arrived), green (checked in), red (no-show), "
        "yellow (late). Auto-refreshes every 60 seconds.",
        "Property ID, date, roster assignments for property on that date",
        "Arrivals list with status indicators, sortable by name/company/status/time, count summaries (expected/arrived/pending/no-show)",
        "GET /api/arrivals/{propertyId}?date=YYYY-MM-DD",
        "No additional storage - reads from assignments and checkins tables",
        "Dashboard loads in under 2 seconds; auto-refresh every 60 seconds; accurate count of expected vs arrived"
    )

    add_feature(pdf,
        "F6.2 QR Scanner (Webcam)",
        "Property portal includes a webcam-based QR scanner for front desk check-in. Uses the device "
        "camera (laptop webcam or USB camera) to scan crew QR codes. Supports continuous scanning "
        "mode for processing multiple crew in sequence.",
        "Webcam video feed, QR code on crew device screen, property operator session",
        "QR decoded, JWT validated, check-in triggered, confirmation displayed, ready for next scan within 2 seconds",
        "Client-side QR decode triggers POST /api/checkin",
        "No additional storage for scanner - check-in records stored per F1.1",
        "Camera access granted via browser permission; QR decoded in under 1 second; continuous mode allows rapid sequential scans"
    )

    add_feature(pdf,
        "F6.3 Real-Time Roster Status",
        "Live view of all crew currently checked in at the property. Shows room number, check-in time, "
        "expected check-out, company, and BLE last-seen status. Filterable by floor, company, and status. "
        "WebSocket connection for real-time updates.",
        "Property ID, WebSocket connection for real-time updates",
        "Live roster grid with crew details, BLE presence indicators, filter/sort controls, export to CSV",
        "GET /api/arrivals/{propertyId} + WebSocket /ws/roster/{propertyId}",
        "No additional storage - real-time view of existing data",
        "WebSocket delivers updates within 1 second of check-in/out event; roster exportable to CSV"
    )

    add_feature(pdf,
        "F6.4 Check-Out Override (Supervisor PIN)",
        "Supervisor can force a check-out for crew who left without checking out. Requires 6-digit "
        "supervisor PIN for authorization. Creates check-out record with method='supervisor_override'. "
        "PIN validated server-side with rate limiting (5 attempts per hour).",
        "Supervisor PIN (6 digits), checkin_id to check out, reason for override",
        "Check-out created with override flag, billing event generated, audit trail with supervisor ID, crew notified",
        "POST /api/checkout with supervisor_pin in body",
        "checkouts: method='supervisor_override', override_by, override_reason; supervisor_pins: hashed_pin, property_id, operator_id",
        "PIN validated server-side; 5 attempt limit per hour; full audit trail of override actions"
    )

    add_feature(pdf,
        "F6.5 Emergency Muster Button",
        "Red emergency button on property portal triggers the BLE muster scan (see F5.7). Available to "
        "all authenticated property staff. Sends immediate push notification to all checked-in crew. "
        "Displays muster results in real-time as BLE data comes in.",
        "Emergency button tap, property_id, operator_id, optional incident description",
        "Muster triggered, push notification to all crew at property, BLE scan initiated, results displayed in real-time",
        "POST /api/ble/muster/{propertyId}/trigger, then GET /api/ble/muster/{propertyId}",
        "muster_events table per F5.7",
        "Muster initiated within 1 second of button press; push notifications delivered to all crew; results stream in real-time"
    )

    # ---- EPIC 7 ----
    section_title(pdf, "EPIC 7: NOTIFICATIONS", level=2)
    body_text(pdf, "Multi-channel notification system ensuring crew and operations stay informed throughout "
              "the check-in lifecycle.")

    add_feature(pdf,
        "F7.1 Push Notifications",
        "PWA push notifications via Web Push API (VAPID). Triggers: check-out reminder (morning of "
        "departure), extension approval/denial, swarm auto-check-in confirmation, emergency muster. "
        "Crew can manage notification preferences.",
        "Push subscription (VAPID keys), notification payload (title, body, action URL), crew preferences",
        "Push notification delivered to device, tap opens relevant PWA screen, delivery receipt logged",
        "Triggered as side effect of various operations",
        "push_subscriptions: crew_id, endpoint, p256dh, auth; notifications: id, crew_id, type, channel='push', sent_at, tapped_at",
        "Push delivered within 5 seconds; tap opens correct context; preferences respected"
    )

    add_feature(pdf,
        "F7.2 SMS Alerts",
        "Twilio SMS for critical notifications: check-in confirmation, missed check-out alert, no-show "
        "escalation, emergency muster. SMS used as fallback when push is unavailable. Rate limited to "
        "10 SMS per crew per day.",
        "Crew phone number (E.164 format), message template, Twilio credentials, rate limit check",
        "SMS delivered via Twilio, delivery status tracked via webhook, message ID logged",
        "Triggered as side effect of various operations (Twilio API)",
        "sms_messages: id, crew_id, to_number, message, twilio_sid, status, sent_at, delivered_at",
        "Delivery within 10 seconds; rate limit 10/crew/day; delivery status tracked"
    )

    add_feature(pdf,
        "F7.3 Email Receipts",
        "SendGrid transactional email for check-in confirmation, check-out receipt (with stay summary "
        "and billing), extension approval, and weekly stay summary. HTML templates with GoCrew branding.",
        "Crew email address, email template ID, dynamic template data, SendGrid API key",
        "Email delivered via SendGrid, open/click tracking, branded HTML with stay details",
        "Triggered as side effect of various operations (SendGrid API)",
        "email_messages: id, crew_id, to_email, template_id, sendgrid_id, status, sent_at, opened_at",
        "Delivery within 30 seconds; branded template renders in all major email clients; open tracking enabled"
    )

    add_feature(pdf,
        "F7.4 No-Show Escalation Chain",
        "Automated escalation for no-shows: (1) Hour 0 - SMS/push to crew, (2) Hour +2 - email to crew + "
        "notify operations, (3) Hour +4 - notify property + flag in dashboard, (4) Hour +8 - escalate to "
        "account manager. Chain stops if crew checks in or responds at any level.",
        "No-show detection event, crew contact info, escalation schedule, operations contact, account manager contact",
        "Escalation events at each tier, notifications sent, dashboard flag, chain halted on resolution",
        "Triggered by no-show detection cron job",
        "no_show_escalations: id, no_show_id, level (1-4), triggered_at, notification_ids, resolved_at",
        "Each level triggers on schedule unless resolved; resolution at any level halts chain; full escalation history preserved"
    )

    # ---- EPIC 8 ----
    section_title(pdf, "EPIC 8: CREW EXPERIENCE", level=2)
    body_text(pdf, "Features focused on crew convenience, support access, and engagement within the PWA.")

    add_feature(pdf,
        "F8.1 Property Contact Info",
        "PWA displays property phone number, email, address, and directions link (opens maps app). "
        "Tap-to-call and tap-to-email functionality. Address links to Google Maps or Apple Maps based "
        "on device detection.",
        "Property data (phone, email, address, lat/lng), crew device platform detection",
        "Contact card displayed, tap-to-call initiates phone call, tap-to-email opens email client, tap-address opens maps",
        "GET /api/assignment/{id} (includes property data)",
        "No additional storage - reads from properties table",
        "Phone number is tap-to-call; email is tap-to-email; address opens native maps app"
    )

    add_feature(pdf,
        "F8.2 24/7 Support Button",
        "Floating support button in PWA opens support channel. Options: call support hotline, send "
        "text message to support, open FAQ. Support button visible on all screens. Context-aware: "
        "passes crew_id and current assignment to support agent.",
        "Crew auth, current assignment context, support channel selection",
        "Call initiated, or SMS composed with context pre-filled, or FAQ displayed, support interaction logged",
        "Client-side action (no API call for initiation, logging via POST /api/support/interaction)",
        "support_interactions: id, crew_id, assignment_id, channel, initiated_at, resolved_at",
        "Support button visible on all screens; context automatically passed; 24/7 availability"
    )

    add_feature(pdf,
        "F8.3 Post-Checkout Feedback",
        "After check-out, crew is prompted to rate the property: 5-star rating plus optional tags "
        "(clean, comfortable, quiet, good_location, friendly_staff, good_breakfast, parking, wifi). "
        "Free-text comment optional. Feedback aggregated for property analytics.",
        "Crew auth, checkin_id (completed stay), star rating (1-5), selected tags (multi-select), optional comment (max 500 chars)",
        "Feedback record created, property rating recalculated, thank-you confirmation displayed",
        "POST /api/feedback",
        "feedback: id, checkin_id, crew_id, property_id, rating, tags (JSON array), comment, submitted_at",
        "Prompt shown within 1 hour of check-out; rating required, tags and comment optional; aggregate updates in real-time"
    )

    add_feature(pdf,
        "F8.4 Check-In History",
        "PWA displays crew's check-in history: past stays with property name, dates, duration, and "
        "rating given. Searchable and filterable by date range, property, and city. Supports pagination.",
        "Crew auth, optional filters (date_from, date_to, property_name, city), pagination (page, per_page)",
        "Paginated list of past stays with property details, dates, duration, rating, and receipt link",
        "GET /api/history/{crewId}?page=1&per_page=20&from=ISO&to=ISO",
        "No additional storage - reads from checkins, checkouts, assignments, properties, feedback tables",
        "History loads in under 2 seconds; pagination with 20 items per page; filterable by date, property, city"
    )

    add_feature(pdf,
        "F8.5 Multiple Assignments Switcher",
        "Crew with overlapping or sequential assignments can switch between them in the PWA. Dropdown "
        "shows all active/upcoming assignments with property name and dates. Switching updates the "
        "wallet pass display and all context-dependent features.",
        "Crew auth, list of active and upcoming assignments for crew_id",
        "Assignment switcher dropdown, wallet pass updates on switch, all features reference selected assignment",
        "GET /api/assignments/{crewId}?status=active,upcoming",
        "No additional storage - reads from assignments table",
        "Switcher shows all active/upcoming assignments; wallet pass updates within 1 second of switch; selected assignment persisted in session"
    )

    # ---- EPIC 9 ----
    section_title(pdf, "EPIC 9: COMPLIANCE & LEGAL", level=2)
    body_text(pdf, "Legal, compliance, and regulatory requirements for operating a crew lodging platform "
              "handling personally identifiable information (PII) and potentially Controlled Unclassified Information (CUI).")

    add_feature(pdf,
        "F9.1 Terms of Service",
        "Crew must accept Terms of Service on first use and after any TOS update. Acceptance is recorded "
        "with timestamp, version, and device info. TOS covers: platform usage, data collection, billing "
        "terms, liability, dispute resolution.",
        "TOS document (versioned HTML), crew auth, acceptance interaction (tap 'I Accept')",
        "Acceptance record created, crew granted access, TOS version locked for crew until next update",
        "POST /api/legal/accept-tos",
        "tos_acceptances: id, crew_id, tos_version, accepted_at, device_meta, ip_address",
        "Acceptance required before any check-in; new version requires re-acceptance; acceptance record immutable"
    )

    add_feature(pdf,
        "F9.2 Privacy Policy",
        "Privacy policy accessible from PWA settings. Covers: data collected (GPS, BLE, photos, signatures), "
        "data retention periods, third-party sharing, CCPA/state privacy rights, data deletion requests. "
        "Must be updated when new data collection features are added.",
        "Privacy policy document (versioned HTML), crew acknowledgment interaction",
        "Policy displayed, acknowledgment recorded, data deletion request workflow available",
        "GET /api/legal/privacy-policy (display), POST /api/legal/data-deletion-request (action)",
        "privacy_acknowledgments: id, crew_id, policy_version, acknowledged_at; data_deletion_requests: id, crew_id, requested_at, completed_at",
        "Policy accessible in 1 tap from settings; data deletion request processed within 30 days; acknowledgment recorded"
    )

    add_feature(pdf,
        "F9.3 CMMC L2 Audit Trail",
        "For DoD/government assignments, system maintains Cybersecurity Maturity Model Certification (CMMC) "
        "Level 2 compliant audit trail. All access, modifications, and exports of CUI are logged with "
        "user, timestamp, action, and resource. Logs are immutable (append-only) and retained for 3 years.",
        "All system events (authentication, data access, modifications, exports), user identity, timestamp, resource affected",
        "Immutable audit log entries, compliance reports, audit trail query API for assessors",
        "GET /api/compliance/audit-trail?from=ISO&to=ISO&resource=X (assessor access)",
        "cmmc_audit_log: id, user_id, action, resource_type, resource_id, timestamp, ip_address, user_agent, details_json (append-only table, no UPDATE/DELETE)",
        "All CUI access logged; logs immutable (append-only, no updates or deletes); 3-year retention; queryable by assessors"
    )

    add_feature(pdf,
        "F9.4 CUI Handling Procedures",
        "Controlled Unclassified Information (CUI) handling for government crew data. Encryption at rest "
        "(AES-256) and in transit (TLS 1.3). Access controls with role-based permissions. CUI marking on "
        "all applicable records. Data residency requirements (US-only servers).",
        "CUI classification rules, encryption configuration, RBAC policies, data residency configuration",
        "CUI-marked records, encrypted storage, access-controlled endpoints, US-only data residency, compliance reports",
        "Configuration-level (no specific API endpoint - applied across all endpoints handling CUI)",
        "All CUI tables: encrypted at rest (AES-256), TLS 1.3 in transit, CUI marking column, access_log foreign key",
        "AES-256 at rest; TLS 1.3 in transit; RBAC enforced; US-only servers; CUI marking on all applicable records"
    )

    # ---- EPIC 10 ----
    section_title(pdf, "EPIC 10: ANALYTICS & INTELLIGENCE", level=2)
    body_text(pdf, "Data analytics and intelligence features providing insights for operations, sales, "
              "and property management.")

    add_feature(pdf,
        "F10.1 Property Rating Aggregation",
        "Aggregates crew feedback ratings per property. Computes: average rating, rating distribution "
        "(1-5 star breakdown), top tags, sentiment from comments, trend over time (30/60/90 day rolling). "
        "Used for property selection and contract negotiation.",
        "Feedback records (rating, tags, comments), property_id, date range, minimum review count threshold",
        "Aggregate rating (weighted average), distribution chart data, top 5 tags with frequency, sentiment score, trend line data",
        "GET /api/analytics/property-rating/{propertyId}",
        "property_ratings_cache: property_id, avg_rating, review_count, tag_frequencies, sentiment_avg, computed_at (refreshed hourly)",
        "Minimum 5 reviews for rating display; hourly cache refresh; trend data available for 90-day lookback"
    )

    add_feature(pdf,
        "F10.2 Predictive No-Show Scoring",
        "ML model predicts probability of no-show for each upcoming assignment. Features: crew historical "
        "no-show rate, day of week, property distance from crew home, weather at destination, assignment "
        "duration, and time since last assignment. Score used for proactive operations outreach.",
        "Crew history (no-shows, total assignments), assignment metadata, weather API data, distance calculation",
        "No-show probability (0.0-1.0) for each upcoming assignment, ranked list of highest-risk assignments",
        "GET /api/analytics/no-show-predictions/{date}",
        "no_show_predictions: assignment_id, predicted_probability, features_json, model_version, computed_at",
        "Predictions computed daily at 06:00; probability > 0.6 triggers proactive outreach; model retrained monthly"
    )

    add_feature(pdf,
        "F10.3 Occupancy Analytics (via BLE)",
        "BLE beacon data used to compute property occupancy analytics: peak lobby times, average floor "
        "occupancy, common area utilization, check-in time distribution. Aggregated and anonymized - "
        "no individual tracking in analytics views.",
        "BLE detection data (aggregated, anonymized), property zones, time periods",
        "Occupancy heatmaps (time x zone), peak usage times, utilization percentages, trend comparisons",
        "GET /api/analytics/occupancy/{propertyId}",
        "occupancy_analytics: property_id, zone, hour_of_day, avg_device_count, day_of_week, computed_date",
        "Data anonymized (no crew IDs in analytics); hourly granularity; 90-day lookback; exportable charts"
    )

    add_feature(pdf,
        "F10.4 Contract Rate Enforcement",
        "Monitors actual billing rates against contracted rates per property. Alerts when charges deviate "
        "beyond threshold. Dashboard shows: contracted rate, actual average, variance, and trend. "
        "Supports multi-tier contracts (per diem, weekly, monthly rates).",
        "Contract rate schedules (property_id, tier, rate), actual billing events, variance threshold configuration",
        "Rate compliance dashboard, variance alerts, trend analysis, contract renewal recommendations",
        "GET /api/analytics/rate-compliance/{propertyId}",
        "rate_compliance: property_id, period, contracted_rate, actual_avg, variance_pct, alert_triggered, computed_at",
        "Variance > 5% triggers alert; dashboard shows 12-month trend; supports per diem, weekly, monthly rate tiers"
    )

    # ==============================
    # PART 2: INPUT/OUTPUT MAPPING
    # ==============================
    section_title(pdf, "PART 2: INPUT/OUTPUT MAPPING BY FEATURE")
    body_text(pdf, "Detailed request/response specifications for each API endpoint. All endpoints require "
              "HTTPS. Authentication via Bearer JWT token unless noted. All responses include standard "
              "envelope: { success: boolean, data: object, error: { code: string, message: string } }.")

    add_api_table(pdf,
        "POST", "/api/token/generate",
        "API key (server-to-server) or crew JWT",
        [
            "crew_id: string (UUID) - required",
            "assignment_id: string (UUID) - required",
            "purpose: enum('checkin','display','wallet') - required",
            "ttl_minutes: integer (default 60, max 1440) - optional",
        ],
        [
            "token: string (signed JWT)",
            "expires_at: ISO 8601 datetime",
            "qr_data: string (base64 encoded QR payload)",
            "token_id: string (UUID for tracking)",
        ],
        "Writes to tokens table: id, crew_id, assignment_id, purpose, issued_at, expires_at, revoked",
        "400: missing required fields; 401: invalid API key/JWT; 404: crew_id or assignment_id not found; 409: active token already exists for this purpose"
    )

    add_api_table(pdf,
        "POST", "/api/token/validate",
        "Property operator JWT or server API key",
        [
            "token: string (JWT from QR scan) - required",
            "property_id: string (UUID) - required for cross-check",
            "scanner_type: enum('webcam','handheld','ble') - required",
        ],
        [
            "valid: boolean",
            "crew_id: string (UUID)",
            "assignment_id: string (UUID)",
            "crew_name: string",
            "assignment_dates: { start: ISO date, end: ISO date }",
            "property_match: boolean (token property matches scanner property)",
            "token_age_seconds: integer",
        ],
        "Writes to token_validations table: id, token_id, validated_at, property_id, scanner_type, result",
        "400: malformed token; 401: invalid auth; 410: token expired; 422: token valid but property mismatch"
    )

    add_api_table(pdf,
        "POST", "/api/checkin",
        "Crew JWT (self-service) or property operator JWT (front desk)",
        [
            "assignment_id: string (UUID) - required",
            "method: enum('qr_frontdesk','self_service','swarm_auto') - required",
            "room_number: string (digits, 1-6 chars) - optional (can be added later)",
            "gps: { lat: float, lng: float, accuracy_m: float } - required for self_service",
            "ble: { beacon_id: string, rssi: integer } - optional",
            "device_fingerprint: string - required for self_service",
            "operator_id: string (UUID) - required for qr_frontdesk",
            "swarm_data: { corroborators: [crew_ids], consensus_score: float } - required for swarm_auto",
            "token: string (JWT) - required for qr_frontdesk",
        ],
        [
            "checkin_id: string (UUID)",
            "status: enum('active','pending_room')",
            "frs: { composite_score: integer, risk_level: enum, decision: enum, layers: { l1-l7: integer } }",
            "wallet_pass_url: string (URL to updated pass)",
            "checked_in_at: ISO 8601 datetime",
            "property: { name: string, address: string, phone: string }",
        ],
        "Writes checkin record; triggers FRS computation; sends SMS + email confirmation; updates real-time roster WebSocket; generates billing event start",
        "400: missing fields; 401: invalid auth; 403: FRS score > 60 (blocked); 404: assignment not found; 409: already checked in; 422: GPS outside geofence (>200m)"
    )

    add_api_table(pdf,
        "POST", "/api/checkout",
        "Crew JWT or property operator JWT",
        [
            "checkin_id: string (UUID) - required",
            "method: enum('crew_initiated','operator_initiated','supervisor_override','auto_missed') - required",
            "supervisor_pin: string (6 digits) - required for supervisor_override",
            "feedback: { rating: integer 1-5, tags: [string], comment: string } - optional",
        ],
        [
            "checkout_id: string (UUID)",
            "stay_summary: { nights: integer, check_in: ISO datetime, check_out: ISO datetime, property: string, room: string }",
            "billing: { amount: float, calculation: string, status: 'pending' }",
            "wallet_pass_url: string (updated pass with 'completed' status)",
        ],
        "Writes checkout record; generates billing event; sends confirmation SMS + email receipt; updates roster WebSocket; closes wallet pass",
        "400: missing fields; 401: invalid auth; 403: invalid supervisor PIN or rate limit exceeded; 404: checkin not found; 409: already checked out"
    )

    add_api_table(pdf,
        "GET", "/api/assignment/{id}",
        "Crew JWT (own assignments) or operator JWT (property assignments)",
        [
            "id: string (UUID) - path parameter - required",
            "include: string (comma-separated: 'property','checkin','wallet') - query param - optional",
        ],
        [
            "assignment: { id, crew_id, property_id, start_date, end_date, status, room_number, rate_per_day, company_id }",
            "property: { id, name, address, phone, email, lat, lng, timezone } (if include=property)",
            "checkin: { id, status, checked_in_at, room_number, frs_score } (if include=checkin)",
            "wallet: { pass_url, qr_data, status } (if include=wallet)",
        ],
        "Reads only - no writes; logs access in CMMC audit trail for CUI assignments",
        "401: invalid auth; 403: not authorized to view this assignment; 404: assignment not found"
    )

    add_api_table(pdf,
        "POST", "/api/frs/score",
        "Server-to-server API key (internal service call)",
        [
            "crew_id: string (UUID) - required",
            "assignment_id: string (UUID) - required",
            "checkin_context: { gps: object, ble: object, device: string, timestamp: ISO, method: string } - required",
            "weights_override: { l1-l7: float, sum must equal 1.0 } - optional",
        ],
        [
            "composite_score: integer (0-100)",
            "risk_level: enum('green','yellow','red')",
            "decision: enum('approve','flag','block')",
            "layers: { l1: { score, factors }, l2: { score, factors }, ... l7: { score, factors } }",
            "weights_used: { l1-l7: float }",
            "computed_at: ISO 8601 datetime",
        ],
        "Writes FRS score record; if yellow/red, writes alert record; if red, triggers operations notification",
        "400: missing fields; 401: invalid API key; 404: crew_id or assignment_id not found; 500: scoring engine timeout"
    )

    add_api_table(pdf,
        "GET", "/api/arrivals/{propertyId}",
        "Property operator JWT",
        [
            "propertyId: string (UUID) - path parameter - required",
            "date: string (YYYY-MM-DD) - query param - default today",
            "status: enum('all','expected','arrived','noshow','late') - query param - default 'all'",
        ],
        [
            "arrivals: [{ crew_id, crew_name, company, assignment_id, start_date, end_date, status, checked_in_at, room_number, ble_last_seen }]",
            "summary: { total_expected: int, arrived: int, pending: int, no_show: int, late: int }",
            "property: { id, name, timezone }",
        ],
        "Reads only - no writes",
        "401: invalid auth; 403: operator not authorized for this property; 404: property not found"
    )

    add_api_table(pdf,
        "POST", "/api/ble/report",
        "Crew JWT (device reports automatically)",
        [
            "crew_id: string (UUID) - required",
            "device_id: string - required",
            "beacons: [{ uuid: string, major: int, minor: int, rssi: int }] - required",
            "peers: [{ peer_id: string, rssi: int }] - optional (swarm mesh detections)",
            "gps: { lat: float, lng: float, accuracy_m: float } - optional",
            "timestamp: ISO 8601 datetime - required",
        ],
        [
            "processed: boolean",
            "actions: [{ type: enum('swarm_checkin_eligible','muster_updated','alibi_recorded'), details: object }]",
            "property_detected: { id: string, name: string, zone: string, floor: int } or null",
        ],
        "Writes BLE detection records; writes peer detection records; updates alibi chain; may trigger swarm auto-check-in; updates muster data",
        "400: missing fields; 401: invalid auth; 429: rate limited (max 6 reports per minute per device)"
    )

    add_api_table(pdf,
        "GET", "/api/ble/muster/{propertyId}",
        "Property operator JWT",
        [
            "propertyId: string (UUID) - path parameter - required",
            "window_minutes: integer (default 5, max 30) - query param - optional",
        ],
        [
            "muster: { triggered_at: ISO datetime, status: enum('active','resolved') }",
            "accounted: [{ crew_id, name, floor, zone, last_seen: ISO datetime, confidence: enum }]",
            "missing: [{ crew_id, name, last_known_floor, last_known_zone, last_seen: ISO datetime }]",
            "unknown: [{ device_id, floor, zone, last_seen: ISO datetime }]",
            "summary: { total_roster: int, accounted: int, missing: int, unknown: int }",
        ],
        "Reads BLE data + roster; writes muster_event record on first access",
        "401: invalid auth; 403: operator not authorized for property; 404: property not found; 503: insufficient BLE data"
    )

    add_api_table(pdf,
        "POST", "/api/stay/extend",
        "Crew JWT",
        [
            "assignment_id: string (UUID) - required",
            "new_end_date: string (YYYY-MM-DD) - required",
            "reason: enum('project_extension','weather','travel_disruption','personal','other') - required",
            "notes: string (max 500 chars) - optional",
        ],
        [
            "extension_id: string (UUID)",
            "status: enum('pending','auto_approved','denied')",
            "original_end_date: string (YYYY-MM-DD)",
            "new_end_date: string (YYYY-MM-DD)",
            "auto_approved: boolean (true if <= 3 days and property has capacity)",
            "estimated_additional_cost: float",
        ],
        "Writes stay_extensions record; if auto-approved, updates assignment end_date; notifies operations; updates wallet pass",
        "400: missing fields; 401: invalid auth; 404: assignment not found; 409: pending extension already exists; 422: new_end_date before current end_date"
    )

    add_api_table(pdf,
        "POST", "/api/stay/early-departure",
        "Crew JWT",
        [
            "assignment_id: string (UUID) - required",
            "actual_departure_date: string (YYYY-MM-DD) - required",
            "reason: enum('project_change','personal','reassignment','emergency','other') - required",
            "notes: string (max 500 chars) - optional",
        ],
        [
            "departure_id: string (UUID)",
            "original_end_date: string (YYYY-MM-DD)",
            "actual_end_date: string (YYYY-MM-DD)",
            "billing_adjustment: { original_amount: float, adjusted_amount: float, refund: float }",
            "checkout_triggered: boolean",
        ],
        "Writes early_departures record; triggers check-out if crew currently checked in; adjusts billing; notifies operations",
        "400: missing fields; 401: invalid auth; 404: assignment not found; 422: departure_date after assignment end_date"
    )

    add_api_table(pdf,
        "POST", "/api/stay/room-change",
        "Crew JWT or property operator JWT",
        [
            "checkin_id: string (UUID) - required",
            "new_room_number: string (digits, 1-6 chars) - required",
            "confirm_room_number: string (must match new_room_number) - required",
            "reason: enum('maintenance','upgrade','request','error','other') - required",
        ],
        [
            "change_id: string (UUID)",
            "old_room: string",
            "new_room: string",
            "changed_at: ISO 8601 datetime",
            "wallet_pass_url: string (updated pass)",
        ],
        "Writes room_changes record; updates checkin.room_number; refreshes wallet pass; logs audit entry",
        "400: missing fields or room numbers don't match; 401: invalid auth; 404: checkin not found; 422: room number invalid format"
    )

    add_api_table(pdf,
        "POST", "/api/feedback",
        "Crew JWT",
        [
            "checkin_id: string (UUID) - required (must be a completed stay)",
            "rating: integer (1-5) - required",
            "tags: [string] - optional (enum: clean, comfortable, quiet, good_location, friendly_staff, good_breakfast, parking, wifi)",
            "comment: string (max 500 chars) - optional",
        ],
        [
            "feedback_id: string (UUID)",
            "submitted_at: ISO 8601 datetime",
            "property_avg_rating: float (updated aggregate)",
            "thank_you_message: string",
        ],
        "Writes feedback record; updates property_ratings_cache; triggers thank-you notification",
        "400: missing fields or invalid rating; 401: invalid auth; 404: checkin not found; 409: feedback already submitted for this stay; 422: checkin not completed"
    )

    add_api_table(pdf,
        "GET", "/api/history/{crewId}",
        "Crew JWT (own history only)",
        [
            "crewId: string (UUID) - path parameter - required",
            "page: integer (default 1) - query param",
            "per_page: integer (default 20, max 100) - query param",
            "from: string (YYYY-MM-DD) - query param - optional",
            "to: string (YYYY-MM-DD) - query param - optional",
            "property_id: string (UUID) - query param - optional filter",
        ],
        [
            "stays: [{ assignment_id, property: { name, city, state }, check_in: ISO, check_out: ISO, nights: int, room: string, rating: int, billing_amount: float }]",
            "pagination: { page: int, per_page: int, total_items: int, total_pages: int }",
            "summary: { total_stays: int, total_nights: int, avg_rating_given: float, total_billed: float }",
        ],
        "Reads only; logs access in CMMC audit trail",
        "401: invalid auth; 403: cannot view other crew's history; 404: crew not found"
    )

    # ==============================
    # PART 3: EPICS & USER STORIES
    # ==============================
    section_title(pdf, "PART 3: EPICS & USER STORIES")
    body_text(pdf, "55 user stories organized across 10 epics. Each story follows the standard format with "
              "Given/When/Then acceptance criteria. Priority levels: Must (required for MVP), Should (important "
              "but not blocking), Could (nice to have). Sprint assignments map to the 21-day build plan "
              "(3 sprints of 7 days each).")

    # EPIC 1 STORIES
    section_title(pdf, "EPIC 1: CREW CHECK-IN (8 Stories)", level=2)

    add_user_story(pdf, "GC-E1-S01", "QR Check-In via Front Desk",
        "property front desk operator", "scan a crew member's QR code to check them in",
        "the crew is registered as present and the roster updates in real-time",
        [
            "Given a crew member presents their QR code, When the operator scans it with the webcam scanner, Then the system validates the JWT and creates a check-in record within 3 seconds",
            "Given the JWT is expired or invalid, When scanned, Then the system displays an error with reason and does not create a check-in",
            "Given a successful scan, When check-in is created, Then the crew receives SMS and email confirmation within 5 seconds",
        ],
        "Must", "Week 1 (Days 1-3)", "Token engine (POST /api/token/generate)")

    add_user_story(pdf, "GC-E1-S02", "Self-Service QR Check-In",
        "crew member", "scan the property's QR code with my phone to check myself in",
        "I can check in without waiting for front desk assistance",
        [
            "Given I have an active assignment at this property, When I scan the property QR code, Then the PWA validates my assignment, captures GPS/BLE, and creates a check-in",
            "Given my GPS is more than 200m from the property, When I attempt to check in, Then the system blocks the check-in with a geofence error",
            "Given successful self-service check-in, When complete, Then I am prompted to enter and confirm my room number",
        ],
        "Must", "Week 1 (Days 1-3)", "Property QR codes deployed, PWA shell")

    add_user_story(pdf, "GC-E1-S03", "Room Number Confirmation",
        "crew member", "enter and confirm my room number after check-in",
        "my assignment record shows the correct room and my wallet pass displays it",
        [
            "Given I just checked in, When I enter a room number, Then I must re-enter it to confirm (double entry)",
            "Given I enter non-numeric characters, When I submit, Then the input is rejected with a validation message",
            "Given both entries match, When confirmed, Then the room number appears on my wallet pass within 5 seconds",
        ],
        "Must", "Week 1 (Days 2-3)", "GC-E1-S01 or GC-E1-S02")

    add_user_story(pdf, "GC-E1-S04", "Undo Check-In Within 15 Minutes",
        "crew member or operator", "undo a check-in within 15 minutes if it was made in error",
        "accidental check-ins can be corrected without supervisor involvement",
        [
            "Given a check-in was created less than 15 minutes ago, When I request undo with a reason, Then the check-in is reversed and the roster updates",
            "Given a check-in was created more than 15 minutes ago, When I request undo, Then the system returns a 403 error with 'window_expired'",
            "Given an undo is performed, When complete, Then the reversal is logged in the audit trail with the reason",
        ],
        "Should", "Week 1 (Days 4-5)", "GC-E1-S01")

    add_user_story(pdf, "GC-E1-S05", "Automated Swarm Check-In",
        "crew member arriving at a property where 3+ crew are already checked in",
        "be automatically checked in when my phone is detected by other crew devices",
        "I don't need to open the app or scan any QR code",
        [
            "Given 3+ checked-in crew devices detect my phone via BLE mesh near the lobby beacon, When bilateral detection is confirmed, Then the system auto-checks me in with method='swarm_auto'",
            "Given I am auto-checked-in, When the check-in is created, Then I receive a push notification to confirm my room number",
            "Given I do not confirm my room number within 30 minutes, When the timeout expires, Then the auto-check-in is reversed",
        ],
        "Could", "Week 3 (Days 15-18)", "BLE mesh (GC-E5-S03), push notifications (GC-E7-S01)")

    add_user_story(pdf, "GC-E1-S06", "Check-In Confirmation Notifications",
        "crew member", "receive SMS and email confirmation after checking in",
        "I have a record of my check-in with property details and wallet pass link",
        [
            "Given a successful check-in, When the record is created, Then SMS is sent via Twilio within 5 seconds and email via SendGrid within 30 seconds",
            "Given SMS delivery fails, When Twilio reports failure, Then the system retries up to 3 times with exponential backoff",
        ],
        "Must", "Week 1 (Days 4-5)", "Twilio and SendGrid integration")

    add_user_story(pdf, "GC-E1-S07", "Photo Verification at Check-In",
        "property operator on a high-security assignment", "verify crew identity via selfie comparison",
        "I can confirm the person checking in matches their profile photo",
        [
            "Given photo verification is enabled for this assignment, When the crew takes a selfie, Then the system compares it to their profile photo and returns a similarity score",
            "Given the similarity score is below 0.7, When the comparison completes, Then the check-in is flagged for manual review and the operator is alerted",
            "Given liveness detection, When the crew takes the selfie, Then the system requires a blink or head turn to prevent photo-of-a-photo attacks",
        ],
        "Could", "Week 3 (Days 18-20)", "Profile photo storage, facial comparison service")

    add_user_story(pdf, "GC-E1-S08", "Digital Signature Capture",
        "crew member on a government/DoD assignment", "provide my digital signature to acknowledge check-in terms",
        "there is a legally binding record of my acceptance of the property and travel policies",
        [
            "Given signature capture is required for this assignment type, When I draw my signature on the touchscreen, Then the SVG path data is stored with timestamp and device metadata",
            "Given the signature has fewer than 10 path points, When I submit, Then the system rejects it as trivial and asks me to sign again",
            "Given a valid signature, When captured, Then a PDF receipt is generated with the embedded signature for compliance records",
        ],
        "Should", "Week 2 (Days 10-12)", "CMMC audit trail (GC-E9-S03)")

    # EPIC 2 STORIES
    section_title(pdf, "EPIC 2: CHECK-OUT & STAY MANAGEMENT (6 Stories)", level=2)

    add_user_story(pdf, "GC-E2-S01", "Check-Out with Confirmation",
        "crew member", "check out of my hotel through the PWA",
        "my stay is properly closed with accurate billing and I receive a receipt",
        [
            "Given I am currently checked in, When I initiate check-out, Then the system records my departure time and calculates stay nights as ceil(hours/24)",
            "Given check-out is complete, When billing is calculated, Then the amount equals stay_nights * $2 and a billing event is created",
            "Given successful check-out, When complete, Then I receive an email receipt with stay summary and my wallet pass updates to 'completed'",
        ],
        "Must", "Week 1 (Days 3-5)", "GC-E1-S01, billing engine")

    add_user_story(pdf, "GC-E2-S02", "Extend Stay Request",
        "crew member", "request an extension to my stay beyond the original end date",
        "I can stay longer when my project timeline changes without manual coordination",
        [
            "Given I have an active assignment, When I submit an extension request, Then the request is created with status 'pending'",
            "Given the extension is 3 days or fewer and the property has capacity, When submitted, Then the request is auto-approved and the assignment end date is updated",
            "Given the extension requires approval, When operations approves, Then my wallet pass and assignment dates update immediately",
        ],
        "Should", "Week 2 (Days 8-10)", "GC-E2-S01, operations notification flow")

    add_user_story(pdf, "GC-E2-S03", "Early Departure Request",
        "crew member", "report that I am departing earlier than planned",
        "billing is adjusted and operations can arrange replacement crew if needed",
        [
            "Given I have an active assignment, When I submit an early departure, Then the system adjusts billing to actual stay nights and triggers check-out",
            "Given early departure is recorded, When operations is notified, Then they receive the departure reason for analytics and can trigger replacement workflow",
        ],
        "Should", "Week 2 (Days 8-10)", "GC-E2-S01")

    add_user_story(pdf, "GC-E2-S04", "Room Change During Stay",
        "crew member or operator", "record a room change during my stay",
        "my wallet pass and records reflect the correct current room number",
        [
            "Given I am checked in, When I submit a room change with double-entry confirmation, Then the old room is archived and new room is recorded",
            "Given a room change is recorded, When complete, Then my wallet pass updates within 5 seconds and the change is logged in the audit trail",
        ],
        "Should", "Week 2 (Days 10-11)", "GC-E1-S03")

    add_user_story(pdf, "GC-E2-S05", "Missed Check-Out Alerts",
        "operations team", "be alerted when crew members miss their check-out time",
        "we can follow up and ensure accurate billing and roster records",
        [
            "Given a crew member is past their assignment end date without checking out, When the hourly scan detects this, Then an alert is created and SMS is sent to the crew",
            "Given the crew has not responded after 2 hours, When the escalation triggers, Then operations is notified via push and dashboard flag",
            "Given the crew has not responded after 4 hours, When the second escalation triggers, Then the property is notified",
        ],
        "Must", "Week 2 (Days 11-12)", "Cron scheduler, notification engine")

    add_user_story(pdf, "GC-E2-S06", "No-Show Detection",
        "operations team", "be notified when crew fail to check in on their assignment start date",
        "we can take immediate action to resolve housing gaps and contact the crew",
        [
            "Given a crew member has an assignment starting today, When 23:59 local time arrives without a check-in, Then the system creates a no-show record",
            "Given a no-show is detected, When the record is created, Then the escalation chain begins and FRS L4 behavioral baseline is updated",
            "Given the escalation chain is active, When the crew eventually checks in, Then the chain is halted and the no-show is resolved",
        ],
        "Must", "Week 2 (Days 11-12)", "Cron scheduler, FRS engine")

    # EPIC 3 STORIES
    section_title(pdf, "EPIC 3: WALLET & PASS (4 Stories)", level=2)

    add_user_story(pdf, "GC-E3-S01", "Wallet Pass Display",
        "crew member", "see my assignment as a boarding-pass-style card in the PWA",
        "I have quick access to my property details, room number, and QR code",
        [
            "Given I have an active assignment, When I open the PWA, Then I see a branded boarding-pass card with crew name, property, room, dates, and QR code",
            "Given my assignment status changes, When the update is processed, Then the card updates in real-time (upcoming -> active -> completed)",
            "Given I am offline, When I open the PWA, Then the service worker serves the last-cached version of my pass",
        ],
        "Must", "Week 1 (Days 2-4)", "Assignment data model, QR token engine")

    add_user_story(pdf, "GC-E3-S02", "Save to Home Screen (PWA Install)",
        "crew member", "install GoCrew as an app on my home screen",
        "I can access it quickly like a native app with offline support",
        [
            "Given I have visited the PWA at least twice, When the install prompt appears, Then I can add GoCrew to my home screen with custom icon and splash screen",
            "Given I have installed the PWA, When I open it offline, Then my last-known assignment and wallet pass are displayed from cache",
        ],
        "Should", "Week 1 (Days 5-7)", "PWA manifest, service worker")

    add_user_story(pdf, "GC-E3-S03", "Calendar Event Save",
        "crew member", "save my assignment dates to my phone calendar",
        "I get reminders for check-in and check-out without manually creating events",
        [
            "Given I have an active assignment, When I tap 'Add to Calendar', Then an ICS file is downloaded or native calendar event is created",
            "Given the calendar event is created, When the dates arrive, Then I receive a check-in reminder (day before) and check-out reminder (morning of departure)",
        ],
        "Could", "Week 2 (Days 12-13)", "GC-E3-S01")

    add_user_story(pdf, "GC-E3-S04", "Apple Wallet .pkpass",
        "crew member with an iPhone", "add my assignment pass to Apple Wallet",
        "I can access my check-in pass from the lock screen and receive push updates",
        [
            "Given Apple Developer certificates are configured, When I tap 'Add to Apple Wallet', Then a signed .pkpass file is generated and added to my Wallet",
            "Given my pass is in Apple Wallet, When my assignment status changes, Then the pass updates via push notification within 30 seconds",
            "Given the pass is in my Wallet, When I arrive at the property, Then the pass appears on my lock screen for quick access",
        ],
        "Could", "Week 3 (Days 15-17)", "Apple Developer account, server signing infrastructure")

    # EPIC 4 STORIES
    section_title(pdf, "EPIC 4: FRAUD DETECTION & FRS (8 Stories)", level=2)

    add_user_story(pdf, "GC-E4-S01", "FRS Composite Score Computation",
        "system", "compute a composite fraud risk score from 7 layers",
        "every check-in is automatically assessed for fraud risk with a clear approve/flag/block decision",
        [
            "Given a check-in is initiated, When the FRS engine is invoked, Then all 7 layers are scored independently and a weighted composite is computed within 500ms",
            "Given composite score 0-30, When computed, Then decision = 'approve' and check-in proceeds automatically",
            "Given composite score 31-60, When computed, Then decision = 'flag' and check-in proceeds but operations is alerted for review",
            "Given composite score 61-100, When computed, Then decision = 'block' and check-in is rejected with 403 error",
        ],
        "Must", "Week 2 (Days 8-10)", "All L1-L7 layer implementations")

    add_user_story(pdf, "GC-E4-S02", "L1 Identity Verification Layer",
        "system", "verify crew identity completeness before check-in",
        "crew with incomplete profiles are flagged as higher risk",
        [
            "Given a crew member has all verification factors (photo, email, phone, gov ID), When L1 is scored, Then the score is 0",
            "Given a crew member is missing verification factors, When L1 is scored, Then the score increases by the weight of each missing factor (20 per missing item)",
        ],
        "Must", "Week 1 (Days 5-7)", "Crew profile data model")

    add_user_story(pdf, "GC-E4-S03", "L2 Geospatial Verification Layer",
        "system", "verify the crew member is physically at the property",
        "remote or spoofed check-ins are detected and blocked",
        [
            "Given GPS within 50m of property and BLE beacon detected, When L2 is scored, Then the score is 0",
            "Given GPS more than 200m from property, When L2 is scored, Then the score includes +60 for distance violation",
            "Given GPS readings show impossible speed between updates, When analyzed, Then +40 is added for spoofing suspicion",
        ],
        "Must", "Week 2 (Days 8-9)", "Property GPS coordinates, BLE beacon deployment")

    add_user_story(pdf, "GC-E4-S04", "L3 Temporal Analysis Layer",
        "system", "analyze the timing of check-in attempts for anomalies",
        "check-ins outside expected windows or showing impossible travel are flagged",
        [
            "Given check-in is within assignment dates and normal hours, When L3 is scored, Then the score is 0",
            "Given check-in is outside the assignment date range, When L3 is scored, Then +25 is added",
            "Given crew checked in at Property A 1 hour ago and Property B is 1000km away, When L3 computes travel velocity, Then +40 is added for impossible travel",
        ],
        "Must", "Week 2 (Days 9-10)", "Check-in history, timezone data")

    add_user_story(pdf, "GC-E4-S05", "L4 Behavioral Baseline Layer",
        "system", "compare current check-in behavior to the crew member's historical baseline",
        "deviations from established patterns are flagged as increased risk",
        [
            "Given the crew has 3+ prior stays with consistent patterns, When L4 is scored, Then deviations from baseline increase the score",
            "Given the crew is new with no history, When L4 is scored, Then a neutral score of 10 is assigned",
            "Given the crew has 2+ no-shows in the last 90 days, When L4 is scored, Then +30 is added to the score",
        ],
        "Should", "Week 2 (Days 10-11)", "Historical check-in data, 90-day lookback")

    add_user_story(pdf, "GC-E4-S06", "L5 Financial Cross-Reference Layer",
        "system", "cross-reference check-in against financial and billing signals",
        "billing anomalies and account issues are surfaced before check-in completes",
        [
            "Given the property rate is within 10% of the contract rate and no overlapping assignments exist, When L5 is scored, Then the score is 0",
            "Given concurrent overlapping assignments are detected for the same crew, When L5 is scored, Then +50 is added as a high fraud signal",
        ],
        "Should", "Week 2 (Days 11-12)", "Contract rate data, billing history")

    add_user_story(pdf, "GC-E4-S07", "L6 Roster Integrity Layer",
        "system", "validate check-in against the master crew roster",
        "unauthorized additions and bulk roster manipulation are detected",
        [
            "Given crew is on the original roster with no recent modifications, When L6 is scored, Then the score is 0",
            "Given crew was added to the roster less than 2 hours before check-in, When L6 is scored, Then +20 is added for last-minute addition",
            "Given more than 10 roster changes were made in the last hour, When L6 is scored, Then +25 is added for bulk edit detection",
        ],
        "Should", "Week 2 (Days 12-13)", "Roster modification audit log")

    add_user_story(pdf, "GC-E4-S08", "L7 Network/Swarm Analysis Layer",
        "system", "analyze the social and BLE mesh network patterns at the property",
        "coordinated fraud and phantom device patterns are detected",
        [
            "Given crew's company matches the property roster and BLE mesh shows normal patterns, When L7 is scored, Then the score is 0",
            "Given BLE mesh shows phantom device broadcasts without matching crew records, When L7 is scored, Then +35 is added",
            "Given a single device claims BLE proximity to an abnormal number of other devices, When L7 is scored, Then mesh anomaly is flagged",
        ],
        "Could", "Week 3 (Days 15-17)", "BLE mesh data (GC-E5-S03)")

    # EPIC 5 STORIES
    section_title(pdf, "EPIC 5: BLE PROXIMITY & SWARM (7 Stories)", level=2)

    add_user_story(pdf, "GC-E5-S01", "Property Beacon Detection",
        "crew member's device", "detect BLE beacons installed at the property",
        "my physical presence at the property is verified for check-in and the alibi engine",
        [
            "Given BLE beacons are installed at the property, When my device is within range, Then beacon UUID, major (zone), and minor (floor) are reported to the server every 10 seconds",
            "Given beacon RSSI is greater than -70 dBm, When reported, Then the system classifies this as close proximity for FRS L2",
            "Given I am in background mode, When a beacon is detected, Then the scan still occurs at 30-second intervals",
        ],
        "Must", "Week 2 (Days 8-10)", "BLE beacon hardware, PWA BLE API")

    add_user_story(pdf, "GC-E5-S02", "Floor-Level Positioning",
        "system", "determine which floor a crew member is on using BLE beacon data",
        "the alibi engine and emergency muster have floor-level accuracy",
        [
            "Given 2+ beacons with different floor values are detected, When RSSI trilateration is computed, Then the estimated floor is determined with confidence level",
            "Given only 1 beacon is detected, When floor is estimated, Then confidence is 'low' and the beacon's floor value is used as best guess",
            "Given 3+ beacons are detected, When trilateration is computed, Then confidence is 'high' with the strongest RSSI signal weighted highest",
        ],
        "Should", "Week 2 (Days 10-12)", "GC-E5-S01")

    add_user_story(pdf, "GC-E5-S03", "Crew-to-Crew Swarm Mesh",
        "crew member's device", "detect and be detected by other crew devices via BLE",
        "a peer-to-peer corroboration network verifies mutual presence",
        [
            "Given my device is advertising a rotating crew identifier, When another crew device scans, Then they report detecting my identifier with RSSI",
            "Given both devices detect each other (bilateral detection), When reported, Then the system records strong corroboration of co-location",
            "Given the rotating identifier changes every 5 minutes with HMAC, When a third party attempts to replay an old identifier, Then the server rejects it as expired",
        ],
        "Should", "Week 2 (Days 12-14)", "GC-E5-S01, rotating identifier HMAC key management")

    add_user_story(pdf, "GC-E5-S04", "Automated Swarm Check-In Trigger",
        "system", "auto-check-in a crew member when 3+ peers corroborate their presence at the lobby",
        "crew arriving at a staffed property with existing crew present can check in without any interaction",
        [
            "Given 3+ checked-in crew devices bilaterally detect a new crew device at the lobby beacon zone, When all 3+ peers are verified as checked-in, Then auto-check-in is triggered",
            "Given auto-check-in is triggered, When the crew member's assignment is verified active, Then a check-in is created with method='swarm_auto' and a push notification requests room confirmation",
            "Given the crew member does not confirm their room within 30 minutes, When the timeout expires, Then the auto-check-in is reversed and logged",
        ],
        "Could", "Week 3 (Days 15-18)", "GC-E5-S03, GC-E7-S01, GC-E1-S03")

    add_user_story(pdf, "GC-E5-S05", "Alibi Engine - Continuous Location Trail",
        "crew member", "have a tamper-proof, continuously recorded location trail",
        "I have legally defensible evidence of my location if falsely accused of an incident",
        [
            "Given I am at the property, When BLE beacons and peer devices detect me, Then every 30 seconds a new alibi record is created with floor, zone, peer witnesses, and chained SHA-256 hash",
            "Given an alibi query for a time range, When the report is generated, Then it shows a timeline with location, confidence, corroborating peers, and hash chain integrity status",
            "Given the hotel claims an incident on Floor 2 at 11:15 PM, When the alibi report for 10:45-11:45 PM shows Floor 4 with 2 corroborating crew peers and unbroken hash chain, Then the crew member has exonerating evidence",
            "Given any record in the chain is tampered with, When hash chain verification is run, Then the break point is identified and flagged as compromised",
        ],
        "Should", "Week 3 (Days 15-18)", "GC-E5-S01, GC-E5-S02, GC-E5-S03")

    add_user_story(pdf, "GC-E5-S06", "Buddy Check-In Detection",
        "system", "detect when one crew member attempts to check in for another (buddy punching)",
        "fraudulent proxy check-ins are caught and flagged for investigation",
        [
            "Given crew A's device initiates a check-in for crew B, When the device fingerprint does not match crew B's registered device, Then a buddy punch flag is raised",
            "Given a buddy punch flag is raised, When BLE mesh data shows crew B's own device is NOT present at the property, Then FRS score increases by 40 and the check-in is held for review",
            "Given the device mismatch occurs but crew B's device IS detected via BLE, When analyzed, Then the system allows it as a possible legitimate scenario (new phone) with reduced flag severity",
        ],
        "Should", "Week 3 (Days 18-19)", "GC-E5-S03, device fingerprinting")

    add_user_story(pdf, "GC-E5-S07", "Emergency Muster via BLE",
        "property operator", "trigger an emergency muster to account for all crew at the property",
        "we can quickly identify who is accounted for and who is missing during an emergency",
        [
            "Given the emergency muster button is pressed, When the BLE scan compiles data from the last 5 minutes, Then a muster report is generated within 10 seconds",
            "Given the muster report is generated, When displayed, Then it shows accounted (detected + on roster), missing (on roster + not detected), and unknown (detected + not on roster) with last floor/zone",
            "Given crew are in the missing list, When the muster is active, Then operations is immediately notified with the missing crew list",
        ],
        "Must", "Week 3 (Days 17-19)", "GC-E5-S01, GC-E5-S02, property roster")

    # EPIC 6 STORIES
    section_title(pdf, "EPIC 6: PROPERTY PORTAL (5 Stories)", level=2)

    add_user_story(pdf, "GC-E6-S01", "Expected Arrivals Dashboard",
        "property front desk operator", "see today's expected crew arrivals with their status",
        "I can prepare for incoming crew and identify who has not yet arrived",
        [
            "Given I am logged into the property portal, When I view the arrivals dashboard, Then I see all crew expected today with color-coded status (gray=not arrived, green=checked in, red=no-show, yellow=late)",
            "Given the dashboard is displayed, When a crew member checks in, Then the dashboard auto-refreshes within 60 seconds to show the updated status",
            "Given I want to see a different date, When I select a date, Then the arrivals for that date are displayed",
        ],
        "Must", "Week 1 (Days 5-7)", "Assignment data model, roster import")

    add_user_story(pdf, "GC-E6-S02", "Webcam QR Scanner",
        "property front desk operator", "scan crew QR codes using my computer's webcam",
        "I can check in crew quickly without specialized hardware",
        [
            "Given I click the scan button on the portal, When my webcam activates, Then it continuously scans for QR codes and decodes them in under 1 second",
            "Given a QR code is decoded, When the JWT is validated, Then the check-in is created and I see confirmation with crew name and room assignment",
            "Given I am in continuous scan mode, When one check-in completes, Then the scanner is ready for the next crew within 2 seconds",
        ],
        "Must", "Week 1 (Days 5-7)", "GC-E1-S01, webcam access permission")

    add_user_story(pdf, "GC-E6-S03", "Real-Time Roster Status",
        "property front desk operator", "see a live view of all crew currently checked in at my property",
        "I know exactly who is here, their room numbers, and their status",
        [
            "Given I am viewing the roster, When a check-in or check-out occurs, Then the roster updates in real-time via WebSocket within 1 second",
            "Given I need to find a specific crew member, When I filter by floor, company, or status, Then the roster filters instantly",
            "Given I need a report, When I click export, Then a CSV is downloaded with the current roster data",
        ],
        "Must", "Week 2 (Days 8-10)", "WebSocket infrastructure, GC-E6-S01")

    add_user_story(pdf, "GC-E6-S04", "Supervisor Check-Out Override",
        "property supervisor", "force a check-out for crew who left without checking out",
        "the roster stays accurate and billing is calculated correctly",
        [
            "Given I enter my 6-digit supervisor PIN, When the PIN is validated server-side, Then I can select a crew member and force their check-out",
            "Given I have attempted 5 incorrect PINs in the last hour, When I try again, Then the system rate-limits me and returns a 403 error",
            "Given I successfully override a check-out, When complete, Then the checkout record shows method='supervisor_override' with my operator ID and reason in the audit trail",
        ],
        "Should", "Week 2 (Days 12-13)", "GC-E2-S01, supervisor PIN management")

    add_user_story(pdf, "GC-E6-S05", "Emergency Muster Button on Portal",
        "property staff member", "press an emergency muster button to account for all crew",
        "crew safety is prioritized during emergencies with real-time accounting",
        [
            "Given I press the red emergency muster button, When the request is sent, Then the BLE muster scan initiates within 1 second and push notifications are sent to all checked-in crew",
            "Given the muster is active, When BLE data streams in, Then the portal displays accounted, missing, and unknown crew in real-time",
            "Given the emergency is resolved, When I close the muster, Then the event is logged with final accounting and resolution timestamp",
        ],
        "Must", "Week 3 (Days 17-19)", "GC-E5-S07, push notification infrastructure")

    # EPIC 7 STORIES
    section_title(pdf, "EPIC 7: NOTIFICATIONS (4 Stories)", level=2)

    add_user_story(pdf, "GC-E7-S01", "Push Notifications via Web Push",
        "crew member", "receive push notifications for important check-in events",
        "I stay informed about check-out reminders, approvals, and emergencies even when the app is closed",
        [
            "Given I have granted push notification permission, When a trigger event occurs (check-out reminder, extension approval, swarm check-in, muster), Then I receive a push notification within 5 seconds",
            "Given I tap the push notification, When the PWA opens, Then it navigates to the relevant screen for that notification",
            "Given I want to manage my preferences, When I open notification settings, Then I can toggle notification types on/off",
        ],
        "Must", "Week 2 (Days 8-10)", "VAPID key pair, service worker")

    add_user_story(pdf, "GC-E7-S02", "SMS Alerts via Twilio",
        "crew member", "receive SMS alerts for critical events when push is unavailable",
        "I am still notified of check-in confirmations, missed check-outs, and emergencies",
        [
            "Given a critical event occurs and my phone number is on file, When SMS is triggered, Then Twilio delivers the message within 10 seconds",
            "Given SMS delivery fails, When Twilio reports failure via webhook, Then the system retries up to 3 times",
            "Given I have already received 10 SMS today, When another SMS is triggered, Then it is suppressed and the event is logged (rate limit protection)",
        ],
        "Must", "Week 1 (Days 5-7)", "Twilio account, phone number verification")

    add_user_story(pdf, "GC-E7-S03", "Email Receipts via SendGrid",
        "crew member", "receive email receipts for check-in, check-out, and stay changes",
        "I have a permanent email record of all my lodging activity",
        [
            "Given a check-in or check-out occurs, When the notification is triggered, Then a branded HTML email is sent via SendGrid within 30 seconds",
            "Given the email contains check-out receipt, When rendered, Then it includes stay summary (property, dates, nights, room, billing amount)",
            "Given the email is delivered, When I open it, Then open tracking is recorded for analytics",
        ],
        "Should", "Week 2 (Days 10-12)", "SendGrid account, email templates")

    add_user_story(pdf, "GC-E7-S04", "No-Show Escalation Chain",
        "operations manager", "have no-shows automatically escalated through a defined chain",
        "no-shows are handled promptly with increasing urgency until resolved",
        [
            "Given a no-show is detected, When Hour 0 begins, Then SMS and push are sent to the crew member",
            "Given the crew has not responded by Hour +2, When the second level triggers, Then email is sent to crew and operations is notified via push and dashboard",
            "Given the crew has not responded by Hour +4, When the third level triggers, Then the property is notified and the dashboard shows a red flag",
            "Given the crew checks in at any point during escalation, When the check-in is recorded, Then the escalation chain is immediately halted and the no-show is resolved",
        ],
        "Must", "Week 2 (Days 12-14)", "GC-E2-S06, notification infrastructure")

    # EPIC 8 STORIES
    section_title(pdf, "EPIC 8: CREW EXPERIENCE (5 Stories)", level=2)

    add_user_story(pdf, "GC-E8-S01", "Property Contact Information",
        "crew member", "see the property's phone number, email, and address with tap-to-action",
        "I can easily contact the hotel or get directions without searching for the information",
        [
            "Given I have an active assignment, When I view the property info section, Then I see phone (tap-to-call), email (tap-to-email), and address (tap-to-open maps)",
            "Given I am on an iPhone, When I tap the address, Then Apple Maps opens with directions; on Android, Google Maps opens",
        ],
        "Must", "Week 1 (Days 5-7)", "Property data model")

    add_user_story(pdf, "GC-E8-S02", "24/7 Support Access",
        "crew member", "access support at any time through the PWA",
        "I can get help with check-in issues, emergencies, or questions regardless of time of day",
        [
            "Given I am on any screen in the PWA, When I tap the floating support button, Then I see options to call the support hotline, send a text, or view FAQ",
            "Given I choose to text support, When the messaging opens, Then my crew ID and current assignment context are pre-populated for the support agent",
        ],
        "Must", "Week 2 (Days 10-12)", "Support phone number, FAQ content")

    add_user_story(pdf, "GC-E8-S03", "Post-Checkout Feedback",
        "crew member", "rate the property and provide feedback after my stay",
        "my experience helps improve property selection for future crew",
        [
            "Given I have checked out within the last hour, When I open the PWA, Then I am prompted to rate the property (1-5 stars) and select optional tags",
            "Given I submit feedback, When the rating is recorded, Then the property's aggregate rating is recalculated in real-time",
            "Given I have already submitted feedback for this stay, When I try again, Then the system returns a 409 conflict error",
        ],
        "Should", "Week 2 (Days 13-14)", "GC-E2-S01")

    add_user_story(pdf, "GC-E8-S04", "Check-In History",
        "crew member", "view my past check-in history with all stay details",
        "I can reference past stays for expense reports and personal records",
        [
            "Given I tap the history tab, When the list loads, Then I see paginated past stays with property name, dates, duration, room, and rating",
            "Given I want to find a specific stay, When I filter by date range or property name, Then the list filters to matching results",
            "Given I want to see more stays, When I scroll to the bottom, Then the next page loads automatically (infinite scroll)",
        ],
        "Should", "Week 2 (Days 13-14)", "Check-in/checkout data model")

    add_user_story(pdf, "GC-E8-S05", "Multiple Assignments Switcher",
        "crew member with multiple assignments", "switch between my active and upcoming assignments",
        "I can manage multiple hotel stays from a single app",
        [
            "Given I have 2+ active or upcoming assignments, When I open the assignment switcher, Then I see a dropdown with property names and date ranges",
            "Given I select a different assignment, When the switch occurs, Then the wallet pass, property info, and all context-dependent features update within 1 second",
        ],
        "Could", "Week 3 (Days 18-20)", "GC-E3-S01, assignment data model")

    # EPIC 9 STORIES
    section_title(pdf, "EPIC 9: COMPLIANCE & LEGAL (4 Stories)", level=2)

    add_user_story(pdf, "GC-E9-S01", "Terms of Service Acceptance",
        "crew member", "accept the Terms of Service before using the platform",
        "Crew Logistics has a legal record of my agreement to platform terms",
        [
            "Given I am a first-time user or TOS has been updated, When I launch the PWA, Then I must accept the current TOS version before proceeding",
            "Given I accept the TOS, When the acceptance is recorded, Then it includes my crew_id, TOS version, timestamp, device info, and IP address",
            "Given the TOS is updated, When I next open the PWA, Then I must re-accept the new version before any actions are available",
        ],
        "Must", "Week 1 (Days 3-5)", "TOS content, legal review")

    add_user_story(pdf, "GC-E9-S02", "Privacy Policy Access",
        "crew member", "read the privacy policy and request data deletion",
        "I understand what data is collected and can exercise my privacy rights",
        [
            "Given I navigate to Settings, When I tap Privacy Policy, Then the current versioned policy is displayed in full",
            "Given I want my data deleted, When I submit a data deletion request, Then the request is logged and processed within 30 days per CCPA requirements",
        ],
        "Must", "Week 1 (Days 3-5)", "Privacy policy content, legal review")

    add_user_story(pdf, "GC-E9-S03", "CMMC L2 Audit Trail",
        "compliance assessor", "query an immutable audit trail of all CUI access and modifications",
        "Crew Logistics maintains CMMC Level 2 compliance for government assignments",
        [
            "Given any user accesses or modifies CUI data, When the action occurs, Then an immutable audit log entry is created with user, action, resource, timestamp, and IP",
            "Given the audit log table, When a DELETE or UPDATE statement is attempted, Then the database rejects the operation (append-only enforcement)",
            "Given an assessor needs compliance data, When they query the audit trail API, Then results are filterable by date range, user, and resource type",
        ],
        "Must", "Week 2 (Days 10-14)", "Database append-only table, RBAC for assessor role")

    add_user_story(pdf, "GC-E9-S04", "CUI Handling Procedures",
        "system administrator", "configure and enforce CUI handling across the platform",
        "all government crew data is protected according to NIST SP 800-171 requirements",
        [
            "Given CUI data is stored at rest, When the storage layer processes it, Then AES-256 encryption is applied automatically",
            "Given CUI data is transmitted, When the request is made, Then TLS 1.3 is enforced (TLS 1.2 and below rejected)",
            "Given a user without the 'cui_access' role attempts to view CUI data, When the request is made, Then a 403 is returned and the attempt is logged in the CMMC audit trail",
        ],
        "Must", "Week 2 (Days 10-14)", "Encryption infrastructure, RBAC model, US-only hosting")

    # EPIC 10 STORIES
    section_title(pdf, "EPIC 10: ANALYTICS & INTELLIGENCE (4 Stories)", level=2)

    add_user_story(pdf, "GC-E10-S01", "Property Rating Aggregation",
        "operations manager", "see aggregated crew ratings for each property",
        "we can make data-driven property selection and contract negotiation decisions",
        [
            "Given a property has 5 or more crew reviews, When I view the property analytics, Then I see average rating, distribution (1-5 stars), top tags, and 90-day trend",
            "Given a property has fewer than 5 reviews, When I view the analytics, Then the rating is shown as 'insufficient data' to prevent small-sample bias",
            "Given the analytics cache, When it is refreshed hourly, Then the aggregate data is current within 1 hour of the latest feedback submission",
        ],
        "Should", "Week 3 (Days 17-19)", "GC-E8-S03, feedback data accumulation")

    add_user_story(pdf, "GC-E10-S02", "Predictive No-Show Scoring",
        "operations manager", "see predicted no-show probabilities for upcoming assignments",
        "we can proactively contact at-risk crew before they become no-shows",
        [
            "Given daily predictions are computed at 06:00, When I view the predictions dashboard, Then I see all upcoming assignments ranked by no-show probability",
            "Given a prediction probability exceeds 0.6, When displayed, Then the assignment is highlighted in red and a proactive outreach suggestion is shown",
            "Given the ML model is retrained monthly, When new training data is available, Then the model version is updated and previous predictions are archived",
        ],
        "Could", "Week 3 (Days 19-21)", "Historical no-show data, weather API integration, ML pipeline")

    add_user_story(pdf, "GC-E10-S03", "Occupancy Analytics via BLE",
        "property manager", "see anonymized occupancy analytics derived from BLE beacon data",
        "we can optimize staffing and resource allocation based on actual usage patterns",
        [
            "Given BLE detection data is collected, When it is aggregated, Then all crew identifiers are removed and only device counts per zone per hour are retained",
            "Given I view the occupancy dashboard, When I select a time period, Then I see heatmaps showing peak usage times and zone utilization percentages",
            "Given 90 days of data are available, When I compare periods, Then trend analysis shows week-over-week and month-over-month changes",
        ],
        "Could", "Week 3 (Days 19-21)", "GC-E5-S01, 90+ days of BLE data")

    add_user_story(pdf, "GC-E10-S04", "Contract Rate Enforcement",
        "finance analyst", "monitor actual billing rates against contracted rates per property",
        "rate deviations are caught early and contract compliance is enforced",
        [
            "Given contract rates are loaded for each property, When actual billing events are processed, Then variance between contracted and actual rates is computed",
            "Given variance exceeds 5%, When the threshold is breached, Then an alert is generated and the property is flagged on the compliance dashboard",
            "Given the dashboard is viewed, When the analyst selects a property, Then a 12-month trend of contracted vs actual rates is displayed",
        ],
        "Should", "Week 3 (Days 19-21)", "Contract rate data, billing event history")

    # ==============================
    # APPENDIX: SPRINT PLAN SUMMARY
    # ==============================
    section_title(pdf, "APPENDIX: SPRINT PLAN SUMMARY")

    body_text(pdf, "The 21-day build plan is organized into three 7-day sprints. Story assignments are "
              "designed to manage dependencies and deliver incremental value.")

    section_title(pdf, "Sprint 1: Days 1-7 (Foundation)", level=3)
    bullet_list(pdf, [
        "GC-E1-S01: QR Check-In via Front Desk",
        "GC-E1-S02: Self-Service QR Check-In",
        "GC-E1-S03: Room Number Confirmation",
        "GC-E1-S06: Check-In Confirmation Notifications",
        "GC-E3-S01: Wallet Pass Display",
        "GC-E3-S02: Save to Home Screen (PWA Install)",
        "GC-E4-S02: L1 Identity Verification Layer",
        "GC-E6-S01: Expected Arrivals Dashboard",
        "GC-E6-S02: Webcam QR Scanner",
        "GC-E7-S02: SMS Alerts via Twilio",
        "GC-E8-S01: Property Contact Information",
        "GC-E9-S01: Terms of Service Acceptance",
        "GC-E9-S02: Privacy Policy Access",
    ])

    section_title(pdf, "Sprint 2: Days 8-14 (Core Features)", level=3)
    bullet_list(pdf, [
        "GC-E1-S04: Undo Check-In Within 15 Minutes",
        "GC-E1-S08: Digital Signature Capture",
        "GC-E2-S01: Check-Out with Confirmation",
        "GC-E2-S02: Extend Stay Request",
        "GC-E2-S03: Early Departure Request",
        "GC-E2-S04: Room Change During Stay",
        "GC-E2-S05: Missed Check-Out Alerts",
        "GC-E2-S06: No-Show Detection",
        "GC-E3-S03: Calendar Event Save",
        "GC-E4-S01: FRS Composite Score Computation",
        "GC-E4-S03: L2 Geospatial Verification Layer",
        "GC-E4-S04: L3 Temporal Analysis Layer",
        "GC-E4-S05: L4 Behavioral Baseline Layer",
        "GC-E4-S06: L5 Financial Cross-Reference Layer",
        "GC-E4-S07: L6 Roster Integrity Layer",
        "GC-E5-S01: Property Beacon Detection",
        "GC-E5-S02: Floor-Level Positioning",
        "GC-E5-S03: Crew-to-Crew Swarm Mesh",
        "GC-E6-S03: Real-Time Roster Status",
        "GC-E6-S04: Supervisor Check-Out Override",
        "GC-E7-S01: Push Notifications via Web Push",
        "GC-E7-S03: Email Receipts via SendGrid",
        "GC-E7-S04: No-Show Escalation Chain",
        "GC-E8-S02: 24/7 Support Access",
        "GC-E8-S03: Post-Checkout Feedback",
        "GC-E8-S04: Check-In History",
        "GC-E9-S03: CMMC L2 Audit Trail",
        "GC-E9-S04: CUI Handling Procedures",
    ])

    section_title(pdf, "Sprint 3: Days 15-21 (Advanced & Polish)", level=3)
    bullet_list(pdf, [
        "GC-E1-S05: Automated Swarm Check-In",
        "GC-E1-S07: Photo Verification at Check-In",
        "GC-E3-S04: Apple Wallet .pkpass",
        "GC-E4-S08: L7 Network/Swarm Analysis Layer",
        "GC-E5-S04: Automated Swarm Check-In Trigger",
        "GC-E5-S05: Alibi Engine - Continuous Location Trail",
        "GC-E5-S06: Buddy Check-In Detection",
        "GC-E5-S07: Emergency Muster via BLE",
        "GC-E6-S05: Emergency Muster Button on Portal",
        "GC-E8-S05: Multiple Assignments Switcher",
        "GC-E10-S01: Property Rating Aggregation",
        "GC-E10-S02: Predictive No-Show Scoring",
        "GC-E10-S03: Occupancy Analytics via BLE",
        "GC-E10-S04: Contract Rate Enforcement",
    ])

    # Save
    output_path = "/Users/bretthogan/Library/CloudStorage/OneDrive-CrewFacilities.comLLC/GOCREW Roster Management/GC001 Review Current Roster Management Process/GoCrew_Requirements_Epics.pdf"
    pdf.output(output_path)
    print(f"PDF saved to: {output_path}")
    print(f"Pages: {pdf.page_no()}")


def section_title_inline(pdf, text):
    """Section title without adding a new page."""
    pdf.set_fill_color(*NAVY)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 12, safe("  " + text), fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)


if __name__ == "__main__":
    build_pdf()
