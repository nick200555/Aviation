# ✈️ AviationOS — Standard Operating Procedure (SOP)
### Functional Guide for Aviation Operators & Airlines

---

> **Document Version:** 1.0  
> **Application:** Aviation ERPNext v15  
> **Audience:** Airline Operations, Flight Crew, Maintenance Engineers, Safety Officers  
> **Support:** ops-support@aviation.bizaxl.org

---

## 📋 Table of Contents

1. [Getting Started — First Login](#1-getting-started--first-login)
2. [Module 1 — Fleet Management](#2-module-1--fleet-management)
3. [Module 2 — Flight Operations](#3-module-2--flight-operations)
4. [Module 3 — Crew Management](#4-module-3--crew-management)
5. [Module 4 — Maintenance (MRO)](#5-module-4--maintenance-mro)
6. [Module 5 — Ground Operations](#6-module-5--ground-operations)
7. [Module 6 — Safety & SMS](#7-module-6--safety--sms)
8. [Module 7 — Airworthiness & Compliance](#8-module-7--airworthiness--compliance)
9. [Module 8 — Reports & Analytics](#9-module-8--reports--analytics)
10. [Daily / Weekly / Monthly Operating Checklist](#10-daily--weekly--monthly-operating-checklist)
11. [User Roles & Who Does What](#11-user-roles--who-does-what)
12. [Frequently Asked Questions](#12-frequently-asked-questions)
13. [Support & Contact](#13-support--contact)

---

## 1. Getting Started — First Login

### 1.1 Access the Application

1. Open your browser and navigate to your Aviation ERP URL:  
   `https://aviation.bizaxl.org`
2. Login with your credentials provided by the IT department.
3. On the left sidebar, click on the **Aviation** workspace.
4. You will see the **Aviation Dashboard** with quick-access cards and module links:
   - 🛫 Active Flights
   - 🔧 Open Work Orders
   - ⚠️ Pending Safety Reports
   - 👤 Crew on Duty

---

### 1.2 Initial Setup (One-Time — Admin Only)

> **Who does this:** System Administrator or Operations Head

| Step | Action | Where |
|---|---|---|
| 1 | Configure Airports | Aviation → Ground Ops → Airport |
| 2 | Setup Aircraft Types | Aviation → Fleet → Aircraft Type |
| 3 | Initialize Airline Profile | Aviation → Fleet → Airline |
| 4 | Seed Initial Demo Data | `bench --site aviation.bizaxl.org execute aviation.aviation.setup.seed_data.execute` |

---

### 1.3 Assign User Roles

> **Who does this:** Administrator

Go to **ERPNext → Users** and assign the appropriate aviation roles to each staff member:

| Role | Responsibility |
|---|---|
| Aviation Manager | Full access to all modules and reporting |
| Flight Operations Officer | Flight planning, load sheets, and dispatch |
| Maintenance Engineer | Work orders, task cards, and airworthiness |
| Crew Scheduler | Roster management and duty records |
| Safety Officer | Incident reporting and investigations |

---

## 2. Module 1 — Fleet Management

> **Purpose:** Centrally manage your aircraft assets, engines, and regulatory certifications to ensure maximum fleet availability.

---

### 2.1 SOP — Adding a New Aircraft

**Who:** Fleet Manager / Engineering Admin  
**When:** When a new aircraft is added to the fleet

| Step | Action |
|---|---|
| 1 | Navigate to **Fleet Management → Aircraft** |
| 2 | Click **+ New** |
| 3 | Enter **Registration** (e.g., VT-ABX) |
| 4 | Select the **Aircraft Type** and **Airline** |
| 5 | Enter **Manufacture Date** and **MSN** (Manufacturer Serial Number) |
| 6 | Input initial **Total Airframe Hours** and **Cycles** |
| 7 | Attach the **Certificate of Registration** in the sidebar |
| 8 | Click **Save** |

✅ **Expected Result:** Aircraft record is created. Utilization tracking begins from the entered hours/cycles.

---

### 2.2 SOP — Tracking Aircraft Certificates

**Who:** Compliance Officer  
**When:** Upon issuance or renewal of any certificate

| Step | Action |
|---|---|
| 1 | Go to **Fleet Management → Aircraft Certificate** |
| 2 | Click **+ New** |
| 3 | Select the **Aircraft** |
| 4 | Select **Certificate Type** (e.g., C of A, C of R, Radio License) |
| 5 | Enter **Certificate Number** and **Issuing Authority** |
| 6 | Set **Issue Date** and **Expiry Date** |
| 7 | Click **Save** |

> **Tip:** The system auto-calculates "Days to Expiry". Expiring certificates will appear highlighted in the **Airworthiness Dashboard**.

---

## 3. Module 2 — Flight Operations

> **Purpose:** Execute the flight lifecycle from initial planning to post-flight recording and fuel reconciliation.

---

### 3.1 SOP — Creating a Flight Plan

**Who:** Flight Dispatcher / Pilot  
**When:** Prior to flight departure

| Step | Action |
|---|---|
| 1 | Go to **Flight Operations → Flight Plan** |
| 2 | Click **+ New** |
| 3 | Enter **Flight Number** and **Flight Date** |
| 4 | Select **Aircraft** and **Route** |
| 5 | Set **ETD** and **ETA** (UTC) |
| 6 | Enter **Trip Fuel** and **Block Fuel** estimates |
| 7 | Assign **Crew Members** in the assignments table |
| 8 | Set Status to **Filed** and Click **Submit** |

✅ **Expected Result:** Flight appears on the Dispatch Dashboard. Crew receive notification of assignment.

---

### 3.2 SOP — Generating a Load Sheet

**Who:** Load Controller / Captain  
**When:** After boarding is complete, before engine start

| Step | Action |
|---|---|
| 1 | Navigate to **Flight Operations → Load Sheet** |
| 2 | Click **+ New** |
| 3 | Link to the active **Flight Operation** |
| 4 | Enter **Dry Operating Weight (DOW)** |
| 5 | Input **Passenger Count** and **Cargo/Baggage Weights** |
| 6 | Verify **Zero Fuel Weight** and **Take-off Fuel** |
| 7 | Check that **Take-off Weight** is within aircraft limits |
| 8 | Click **Save** (and print for Captain's signature) |

---

### 3.3 SOP — Post-Flight Record (Flight Operation)

**Who:** Captain / Flight Operations Officer  
**When:** Within 30 minutes of "On-Blocks"

| Step | Action |
|---|---|
| 1 | Open the **Flight Operation** record linked to the Flight Plan |
| 2 | Enter actual times: **Off-Block**, **Takeoff**, **Landing**, **On-Block** |
| 3 | Input **Fuel on Arrival** (to calculate actual consumption) |
| 4 | Record any **Delays** with IATA delay codes |
| 5 | Enter **Tech Log** entry number if any defects occurred |
| 6 | Set Status to **Completed** and Click **Submit** |

✅ **Expected Result:** Aircraft total hours and cycles are auto-updated. Fuel consumption metrics are generated.

---

## 4. Module 3 — Crew Management

> **Purpose:** Ensure all flight and cabin crew are qualified, licensed, and operating within fatigue safety limits.

---

### 4.1 SOP — Managing Crew Licences

**Who:** Crew Training / HR  
**When:** Upon licence renewal or rating upgrade

| Step | Action |
|---|---|
| 1 | Go to **Crew Management → Crew Licence** |
| 2 | Select the **Crew Member** |
| 3 | Enter **Licence Number** and **Licence Type** (e.g., ATPL, CPL) |
| 4 | Input **Medical Class** and **Medical Expiry Date** |
| 5 | Attach a digital copy of the license document |
| 6 | Click **Save** |

---

### 4.2 SOP — Logging Duty Records (FDP Tracking)

**Who:** Crew Member / Scheduler  
**When:** After completion of every duty period

| Step | Action |
|---|---|
| 1 | Go to **Crew Management → Crew Duty Record** |
| 2 | Link the **Flight Operation** (if applicable) |
| 3 | Enter **Duty Start (UTC)** and **Duty End (UTC)** |
| 4 | Select **Role on Flight** (Captain, FO, etc.) |
| 5 | Click **Submit** |

✅ **Expected Result:** System calculates **Flight Duty Period (FDP)** and **Block Hours**. Any regulatory exceedance is auto-flagged for Safety review.

---

## 5. Module 4 — Maintenance (MRO)

> **Purpose:** Execute scheduled and unscheduled maintenance while maintaining strict compliance with Airworthiness Directives (AD).

---

### 5.1 SOP — Executing a Maintenance Work Order

**Who:** Maintenance Planner / Engineer  
**When:** When aircraft enters maintenance (e.g., A-Check, Line Maint)

| Step | Action |
|---|---|
| 1 | Go to **Maintenance → Maintenance Work Order** |
| 2 | Click **+ New** |
| 3 | Select the **Aircraft** and **Maintenance Type** |
| 4 | Add **Task Cards** to the tasks table (e.g., Filter Change, Inspection) |
| 5 | Once work starts, set Status to **In Progress** |
| 6 | Upon completion, enter **Release to Service** details |
| 7 | Enter **LAME Licence Number** and **Release Date** |
| 8 | Click **Submit** |

---

### 5.2 SOP — AD Compliance Tracking

**Who:** Quality Manager  
**When:** Upon receipt of a new AD from FAA/EASA/DGCA

| Step | Action |
|---|---|
| 1 | Go to **Maintenance → Airworthiness Directive** and create the AD record |
| 2 | Navigate to **AD Compliance Record** |
| 3 | Select the **AD** and the affected **Aircraft** |
| 4 | Set **Compliance Status** (e.g., Complied - Terminating, Pending) |
| 5 | Enter **Compliance Date** and **Hours/Cycles** at compliance |
| 6 | Save |

---

## 6. Module 5 — Ground Operations

> **Purpose:** Coordinate airport services, ground handling, and fuel uplifts to ensure on-time performance.

---

### 6.1 SOP — Ground Handling Orders

**Who:** Ground Ops Manager  
**When:** 24 hours prior to flight arrival

| Step | Action |
|---|---|
| 1 | Go to **Ground Operations → Ground Handling Order** |
| 2 | Select the **Handling Company** and **Airport** |
| 3 | Enter the **Flight Number** and **Service Date** |
| 4 | Tick required services (e.g., Catering, Pushback, Cleaning) |
| 5 | Click **Save** |

---

## 7. Module 6 — Safety & SMS

> **Purpose:** Proactively identify hazards and investigate occurrences to maintain the highest safety standards.

---

### 7.1 SOP — Reporting a Safety Occurrence

**Who:** Any Staff Member (Pilot, Engineer, Ground Crew)  
**When:** Immediately following any safety incident or near-miss

| Step | Action |
|---|---|
| 1 | Go to **Safety & SMS → Safety Occurrence Report** |
| 2 | Select **Occurrence Type** (e.g., Hazard, Incident, Bird Strike) |
| 3 | Enter **Date** and **Summary** |
| 4 | Provide a detailed **Narrative** of what happened |
| 5 | Select **Severity** (Minor, Moderate, Major, Critical) |
| 6 | Set **is_anonymous** if reporter wishes to remain confidential |
| 7 | Click **Submit** |

✅ **Expected Result:** Safety Officer is notified. Report enters the Investigation pipeline.

---

### 7.2 SOP — Managing the Hazard Register

**Who:** Safety Officer  
**When:** Weekly during safety review meetings

| Step | Action |
|---|---|
| 1 | Go to **Safety & SMS → Hazard Register** |
| 2 | Click **+ New** to log a systemic risk (e.g., Fatigue in Night Ops) |
| 3 | Assign a **Risk Assessment** (High/Medium/Low) |
| 4 | Detail the **Mitigation Plan** |
| 5 | Set Status to **Open** until mitigation is verified |

---

## 8. Module 7 — Airworthiness & Compliance

> **Purpose:** Monitor fleet-wide regulatory health and prepare for aviation authority audits.

---

### 8.1 SOP — Audit Readiness Review

**Who:** Quality & Compliance Manager  
**When:** Monthly

1. Navigate to **Airworthiness → AD SB Compliance Report**.
2. Verify all "Mandatory" ADs are marked as "Complied".
3. Check **Aircraft Certificate Dashboard** for any documents expiring within 30 days.
4. Ensure all **Crew Licences** in the active roster are valid.

---

## 9. Module 8 — Reports & Analytics

> **Purpose:** Data-driven decision making via specialized aviation reports.

| Report Name | Purpose | Key Filters |
|---|---|---|
| Aircraft Utilization | Track flight hours/cycles by registration | Aircraft, Date Range |
| Crew Duty Report | Monitor FDP and rest periods | Crew Member, Month |
| Maintenance Due Report | Predict upcoming checks based on utilization | Forecast Hours |
| Safety Occurrence Report | Trend analysis of incidents | Severity, Location |

---

## 10. Daily / Weekly / Monthly Operating Checklist

### 10.1 Daily Checklist (Morning Dispatch)

| Task | Responsible |
|---|---|
| ☐ Review Daily Flight Schedule | Flight Ops |
| ☐ Verify Crew Medical & Licence Validity | Crewing |
| ☐ Check Aircraft Serviceable Status | MRO |
| ☐ Monitor Morning Weather & NOTAMs | Dispatch |
| ☐ Review Safety Reports from previous 24h | Safety |

---

### 10.2 Weekly Review

| Task | Responsible |
|---|---|
| ☐ Reconcile Fuel Uplifts vs Flight Logs | Ground Ops |
| ☐ Update Maintenance Forecast (Hours/Cycles) | MRO |
| ☐ Conduct Hazard Mitigation Review | Safety |
| ☐ Audit Crew Duty Records for FDP violations | Crewing |

---

### 10.3 Monthly Compliance Audit

| Task | Responsible |
|---|---|
| ☐ Review Aircraft Certificate Expiries (30/60/90 days) | Quality |
| ☐ Generate Fleet Utilization Summary | Management |
| ☐ Review Open Safety Investigations | Safety |
| ☐ Verify AD Compliance Parity with Authority Portals | Engineering |

---

## 11. User Roles & Who Does What

| Feature | Admin | Pilot | MRO | Dispatch | Safety |
|---|---|---|---|---|---|
| Aircraft Setup | ✅ | 👁 | 👁 | 👁 | ❌ |
| Flight Planning | 👁 | ✅ | ❌ | ✅ | ❌ |
| Post-Flight Logs | 👁 | ✅ | ❌ | 👁 | ❌ |
| Work Orders | 👁 | ❌ | ✅ | ❌ | ❌ |
| Safety Reporting | ✅ | ✅ | ✅ | ✅ | ✅ |
| Investigations | 👁 | ❌ | 👁 | ❌ | ✅ |
| Compliance Reports| ✅ | ❌ | ✅ | 👁 | ✅ |

---

## 12. Frequently Asked Questions

**Q1: How do I assign crew to a flight?**  
A: Open the **Flight Plan**, go to the **Crew Assignments** table, select the staff member and their role (e.g., Captain), and save. The system will alert you if their license is expired.

---

**Q2: Why isn't my aircraft utilization updating?**  
A: Utilization only updates when a **Flight Operation** record is marked as "Completed" and **Submitted**. Check the Status of your latest flight log.

---

**Q3: How do I report a bird strike?**  
A: Create a new **Safety Occurrence Report**, set the Occurrence Type to "Bird Strike", and fill in the details including altitude and aircraft registration.

---

**Q4: Can I enter duty hours without a flight?**  
A: Yes. Use the **Crew Duty Record** and leave the Flight Operation field blank (e.g., for Office Duty, Training, or Standby).

---

## 13. Support & Contact

For technical issues, login resets, or to report a system bug:

📧 **Email:** support@aviation.bizaxl.org  
📞 **Ops Hot-line:** +91-XXX-XXX-XXXX  
💬 **Slack:** #aviation-ops-erp  
🌐 **Documentation:** `https://docs.aviation.bizaxl.org`

---
*End of Standard Operating Procedure (SOP)*
