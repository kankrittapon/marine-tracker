Marine Tracker RevA

REQUIREMENTS_TRACEABILITY_MATRIX_ADDENDUM

วางไฟล์นี้ไว้ที่:

docs/REQUIREMENTS_TRACEABILITY_MATRIX.md

แล้วนำเนื้อหาด้านล่างไปต่อท้ายไฟล์เดิม

RTM-021 --- Cold Boot Performance

Status: Approved

Requirement: - ระบบต้องบูตเองหลังใส่แบตเตอรี่หรือไฟกลับมา

Target: - Bootloader < 2 s - Modem Ready < 15 s - System Ready < 30 s

Related ADR: - ADR-003 - ADR-006 - ADR-008

Verification: - ถอดแบต 60 วินาที - ใส่กลับ - จับเวลาจนเชื่อมต่อเครือข่าย

Acceptance: - พร้อมใช้งานภายใน 30 วินาที

RTM-022 --- Position Acquisition

Status: Approved

Requirement: - Hot Start < 10 s - Warm Start < 30 s - Cold Start <120 s

Verification: - Outdoor TTFF Test

RTM-023 --- Data Integrity

Status: Approved

Requirement: - ไฟดับระหว่างเขียนข้อมูลต้องไม่ทำให้ข้อมูลสำคัญเสียหาย

Verification: - Power Cut During Flash Write

RTM-024 --- Autonomous Recovery

Status: Approved

Requirement: - ระบบต้องกู้คืนตัวเองจาก LTE, TCP, MQTT, GNSS, Firmware Hang,SIM Removal และ Brownout

Verification: - Fault Injection Test

RTM-025 --- Energy Budget

Status: Approved

Requirement: - ต้องมี Energy Budget สำหรับ Sleep, Idle, GNSS, LTE TX และBoot

Verification: - Power Profiling

RTM-026 --- Environmental Survivability

Status: Approved

Requirement: - รองรับ -20°C ถึง +60°C - RH 95% - Salt Air - IP67 ขั้นต่ำ -ENIG PCB - Conformal Coating

Verification: - Environmental Test

เพิ่มท้าย Traceability Matrix

Req       ADR       Schematic     PCB    Firmware     Verification     Status

RTM-021   ADR-003   ✔             ✔      ✔            Cold Boot Test   ApprovedADR-006ADR-008

RTM-022   ADR-004   ✔             ✔      ✔            TTFF Test        Approved

RTM-023   ADR-008   ✔             ✔      ✔            Power Loss Test  Approved

RTM-024   ADR-008   ✔             ✔      ✔            Fault Injection  ApprovedADR-009

RTM-025   ADR-002   ✔             ✔      ✔            Power Profiling  ApprovedADR-009