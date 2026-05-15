import frappe
from frappe.utils import today, add_days, add_months, now_datetime

def execute():
    frappe.flags.in_test = True # Bypass some strict validations for seeding if needed
    print("Starting Aviation ERPNext Data Seeding...")

    seed_airports()
    seed_airlines()
    seed_engine_types()
    seed_engines()
    seed_aircraft_types()
    seed_aircraft()
    seed_routes()
    seed_crew_qualifications()
    seed_crew_members()
    seed_part_numbers()
    seed_maintenance_tasks()
    seed_airworthiness_directives()
    seed_hazard_types()
    seed_ground_handling_companies()

    seed_aircraft_certificates()
    seed_flight_plans()
    seed_flight_operations()
    seed_crew_licences()
    seed_crew_duty_records()
    seed_maintenance_work_orders()
    seed_safety_reports()
    
    frappe.db.commit()
    print("Seeding Complete!")

def get_or_create(doctype, filters, data):
    if not frappe.db.exists(doctype, filters):
        doc = frappe.new_doc(doctype)
        doc.update(data)
        doc.insert(ignore_permissions=True, ignore_mandatory=True)
        return doc.name
    return frappe.db.get_value(doctype, filters, "name")

def seed_airports():
    airports = [
        {"icao_code": "VABB", "iata_code": "BOM", "airport_name": "Chhatrapati Shivaji Maharaj", "city": "Mumbai", "country": "India", "elevation_ft": 39, "latitude": 19.0886, "longitude": 72.8679},
        {"icao_code": "VIDP", "iata_code": "DEL", "airport_name": "Indira Gandhi International", "city": "New Delhi", "country": "India", "elevation_ft": 777, "latitude": 28.5562, "longitude": 77.1000},
        {"icao_code": "VOBL", "iata_code": "BLR", "airport_name": "Kempegowda International", "city": "Bengaluru", "country": "India", "elevation_ft": 3000, "latitude": 13.1986, "longitude": 77.7066},
        {"icao_code": "OMDB", "iata_code": "DXB", "airport_name": "Dubai International", "city": "Dubai", "country": "United Arab Emirates", "elevation_ft": 62, "latitude": 25.2528, "longitude": 55.3644},
        {"icao_code": "EGLL", "iata_code": "LHR", "airport_name": "Heathrow", "city": "London", "country": "United Kingdom", "elevation_ft": 83, "latitude": 51.4700, "longitude": -0.4543},
        {"icao_code": "KJFK", "iata_code": "JFK", "airport_name": "John F. Kennedy International", "city": "New York", "country": "United States", "elevation_ft": 13, "latitude": 40.6413, "longitude": -73.7781},
        {"icao_code": "WSSS", "iata_code": "SIN", "airport_name": "Singapore Changi", "city": "Singapore", "country": "Singapore", "elevation_ft": 22, "latitude": 1.3644, "longitude": 103.9915}
    ]
    for apt in airports:
        get_or_create("Airport", {"icao_code": apt["icao_code"]}, apt)
    print("Airports seeded.")

def seed_airlines():
    airlines = [
        {"icao_designator": "AIC", "iata_code": "AI", "airline_name": "Air India", "telephony_callsign": "AIRINDIA"},
        {"icao_designator": "IGO", "iata_code": "6E", "airline_name": "IndiGo", "telephony_callsign": "IFLY"},
        {"icao_designator": "UAE", "iata_code": "EK", "airline_name": "Emirates", "telephony_callsign": "EMIRATES"},
        {"icao_designator": "DLH", "iata_code": "LH", "airline_name": "Lufthansa", "telephony_callsign": "LUFTHANSA"},
        {"icao_designator": "SIA", "iata_code": "SQ", "airline_name": "Singapore Airlines", "telephony_callsign": "SINGAPORE"}
    ]
    for al in airlines:
        get_or_create("Airline", {"icao_designator": al["icao_designator"]}, al)
    print("Airlines seeded.")

def seed_engine_types():
    types = [
        {"model_designation": "CFM56-7B26", "manufacturer": "CFM International", "thrust_kn": 115.6},
        {"model_designation": "LEAP-1A26", "manufacturer": "CFM International", "thrust_kn": 115.6},
        {"model_designation": "V2527-A5", "manufacturer": "IAE", "thrust_kn": 118.3},
        {"model_designation": "GE90-115B", "manufacturer": "GE Aviation", "thrust_kn": 511.0}
    ]
    for et in types:
        get_or_create("Engine Type", {"model_designation": et["model_designation"]}, et)
    print("Engine Types seeded.")

def seed_engines():
    engines = [
        {"serial_number": "890123", "engine_type_ref": "CFM56-7B26", "status": "Serviceable (Pool)", "total_hours": 12000, "total_cycles": 8500},
        {"serial_number": "890124", "engine_type_ref": "CFM56-7B26", "status": "Serviceable (Pool)", "total_hours": 12050, "total_cycles": 8520},
        {"serial_number": "990100", "engine_type_ref": "LEAP-1A26", "status": "Serviceable (Pool)", "total_hours": 4500, "total_cycles": 3200},
        {"serial_number": "990101", "engine_type_ref": "LEAP-1A26", "status": "Serviceable (Pool)", "total_hours": 4510, "total_cycles": 3205},
        {"serial_number": "V12345", "engine_type_ref": "V2527-A5", "status": "In Shop", "total_hours": 25000, "total_cycles": 15000}
    ]
    for eng in engines:
        get_or_create("Engine", {"serial_number": eng["serial_number"]}, eng)
    print("Engines seeded.")

def seed_aircraft_types():
    types = [
        {"type_designator": "B738", "manufacturer": "Boeing", "model_name": "737-800", "wake_turbulence_category": "M", "aircraft_category": "Aeroplane", "number_of_engines": 2, "engine_type_ref": "CFM56-7B26", "typical_pax_capacity": 189, "is_etops_capable": 1, "etops_rating_minutes": 120},
        {"type_designator": "A320", "manufacturer": "Airbus", "model_name": "A320neo", "wake_turbulence_category": "M", "aircraft_category": "Aeroplane", "number_of_engines": 2, "engine_type_ref": "LEAP-1A26", "typical_pax_capacity": 180, "is_etops_capable": 1, "etops_rating_minutes": 120},
        {"type_designator": "B77W", "manufacturer": "Boeing", "model_name": "777-300ER", "wake_turbulence_category": "H", "aircraft_category": "Aeroplane", "number_of_engines": 2, "engine_type_ref": "GE90-115B", "typical_pax_capacity": 396, "is_etops_capable": 1, "etops_rating_minutes": 330}
    ]
    for at in types:
        get_or_create("Aircraft Type", {"type_designator": at["type_designator"]}, at)
    print("Aircraft Types seeded.")

def seed_aircraft():
    aircrafts = [
        {"registration": "VT-ABX", "aircraft_type": "B738", "airline": "AIC", "status": "Active", "msn": "40123", "manufacture_date": "2015-05-10", "total_airframe_hours": 25000, "total_airframe_cycles": 18000, "current_engine_1": "890123", "current_engine_2": "890124"},
        {"registration": "VT-IGO", "aircraft_type": "A320", "airline": "IGO", "status": "Active", "msn": "8500", "manufacture_date": "2019-11-20", "total_airframe_hours": 12000, "total_airframe_cycles": 8500, "current_engine_1": "990100", "current_engine_2": "990101"},
        {"registration": "VT-ALM", "aircraft_type": "B77W", "airline": "AIC", "status": "Scheduled Maintenance", "msn": "35000", "manufacture_date": "2010-08-15", "total_airframe_hours": 65000, "total_airframe_cycles": 15000},
        {"registration": "A6-EMA", "aircraft_type": "B77W", "airline": "UAE", "status": "Active", "msn": "42000", "manufacture_date": "2016-02-10", "total_airframe_hours": 35000, "total_airframe_cycles": 8000},
        {"registration": "9V-SWA", "aircraft_type": "B77W", "airline": "SIA", "status": "Active", "msn": "34500", "manufacture_date": "2008-12-05", "total_airframe_hours": 70000, "total_airframe_cycles": 16000}
    ]
    for ac in aircrafts:
        get_or_create("Aircraft", {"registration": ac["registration"]}, ac)
    print("Aircraft seeded.")

def seed_routes():
    routes = [
        {"route_name": "BOM-DEL", "departure_airport": "VABB", "destination_airport": "VIDP", "distance_nm": 612, "estimated_time_hours": 2.1},
        {"route_name": "DEL-BLR", "departure_airport": "VIDP", "destination_airport": "VOBL", "distance_nm": 920, "estimated_time_hours": 2.6},
        {"route_name": "BOM-DXB", "departure_airport": "VABB", "destination_airport": "OMDB", "distance_nm": 1040, "estimated_time_hours": 3.1},
        {"route_name": "DEL-LHR", "departure_airport": "VIDP", "destination_airport": "EGLL", "distance_nm": 3630, "estimated_time_hours": 9.6},
        {"route_name": "BOM-SIN", "departure_airport": "VABB", "destination_airport": "WSSS", "distance_nm": 2100, "estimated_time_hours": 5.5}
    ]
    for r in routes:
        get_or_create("Route", {"route_name": r["route_name"]}, r)
    print("Routes seeded.")

def seed_crew_qualifications():
    quals = [
        {"qualification_name": "ATPL", "category": "Flight Crew"},
        {"qualification_name": "CPL", "category": "Flight Crew"},
        {"qualification_name": "Class 1 Medical", "category": "Safety"},
        {"qualification_name": "SEP", "category": "Safety"},
        {"qualification_name": "CRM", "category": "Safety"}
    ]
    for q in quals:
        get_or_create("Crew Qualification Type", {"qualification_name": q["qualification_name"]}, q)
    print("Crew Qualifications seeded.")

def seed_crew_members():
    crew = [
        {"full_name": "Capt. Rajan Sharma", "crew_type": "Flight Crew", "status": "Active", "date_of_birth": "1980-05-15", "base_airport": "VIDP", "max_fdp_hours": 13},
        {"full_name": "FO. Aman Verma", "crew_type": "Flight Crew", "status": "Active", "date_of_birth": "1992-08-20", "base_airport": "VABB", "max_fdp_hours": 13},
        {"full_name": "Capt. Sarah Jenkins", "crew_type": "Flight Crew", "status": "Active", "date_of_birth": "1978-11-30", "base_airport": "OMDB", "max_fdp_hours": 13},
        {"full_name": "Priya Patel", "crew_type": "Cabin Crew", "status": "Active", "date_of_birth": "1995-02-14", "base_airport": "VIDP"},
        {"full_name": "Rahul Singh", "crew_type": "Cabin Crew", "status": "Active", "date_of_birth": "1996-07-22", "base_airport": "VABB"},
        {"full_name": "Amit Kumar", "crew_type": "Engineering Crew", "status": "Active", "date_of_birth": "1985-09-10", "base_airport": "VIDP"}
    ]
    for c in crew:
        get_or_create("Crew Member", {"full_name": c["full_name"]}, c)
    print("Crew Members seeded.")

def seed_part_numbers():
    parts = [
        {"part_number": "114-1000-01", "description": "Main Landing Gear Wheel", "part_category": "Overhaul Required", "unit_of_measure": "Nos"},
        {"part_number": "8-420-02", "description": "Brake Assembly", "part_category": "Overhaul Required", "unit_of_measure": "Nos"},
        {"part_number": "NAS1149F0363P", "description": "Washer, Flat", "part_category": "Expendable", "unit_of_measure": "Nos"},
        {"part_number": "NYCO-GN22", "description": "Aero Grease", "part_category": "Consumable", "unit_of_measure": "Kg"}
    ]
    for p in parts:
        get_or_create("Part Number", {"part_number": p["part_number"]}, p)
    print("Part Numbers seeded.")

def seed_maintenance_tasks():
    tasks = [
        {"task_id": "A320-32-10-01", "description": "Main Landing Gear Lubrication", "aircraft_type": "A320", "task_type": "Routine", "interval_hours": 500},
        {"task_id": "B738-29-00-01", "description": "Hydraulic Fluid Servicing", "aircraft_type": "B738", "task_type": "Routine", "interval_days": 7},
        {"task_id": "ENG-72-00-01", "description": "Engine Borescope Inspection", "aircraft_type": "B77W", "task_type": "Detailed Inspection", "interval_cycles": 1000}
    ]
    for t in tasks:
        get_or_create("Maintenance Task Card", {"task_id": t["task_id"]}, t)
    print("Maintenance Task Cards seeded.")

def seed_airworthiness_directives():
    ads = [
        {"ad_number": "FAA-2023-0123", "ad_title": "Inspection of Forward Fuselage", "issuing_authority": "FAA", "issue_date": "2023-05-10", "effective_date": "2023-06-01", "compliance_type": "Mandatory", "applicability_description": "All B738"},
        {"ad_number": "EASA-2024-0045", "ad_title": "Engine Fan Blade Inspection", "issuing_authority": "EASA", "issue_date": "2024-01-15", "effective_date": "2024-02-01", "compliance_type": "Mandatory", "applicability_description": "A320 LEAP engines"}
    ]
    for ad in ads:
        get_or_create("Airworthiness Directive", {"ad_number": ad["ad_number"]}, ad)
    print("Airworthiness Directives seeded.")

def seed_hazard_types():
    hazards = [
        {"hazard_type": "BIRD", "description": "Bird Strike Risk"},
        {"hazard_type": "FOD", "description": "Foreign Object Debris on Ramp"},
        {"hazard_type": "WX-TS", "description": "Severe Thunderstorms"},
        {"hazard_type": "FATIGUE", "description": "Crew Fatigue"},
        {"hazard_type": "SYSTEM", "description": "Aircraft System Failure"}
    ]
    for h in hazards:
        get_or_create("Hazard Type", {"hazard_type": h["hazard_type"]}, h)
    print("Hazard Types seeded.")

def seed_ground_handling_companies():
    ghc = [
        {"company_name": "Air India Airport Services", "base_airport": "VIDP"},
        {"company_name": "Celebi Aviation", "base_airport": "VABB"},
        {"company_name": "Dnata", "base_airport": "OMDB"}
    ]
    for g in ghc:
        get_or_create("Ground Handling Company", {"company_name": g["company_name"]}, g)
    print("Ground Handling Companies seeded.")

def seed_aircraft_certificates():
    certs = [
        {"aircraft": "VT-ABX", "certificate_type": "Other", "certificate_number": "CR-1234", "issue_date": "2015-05-15", "issuing_authority": "DGCA India", "status": "Valid"},
        {"aircraft": "VT-ABX", "certificate_type": "Certificate of Airworthiness", "certificate_number": "CA-1234", "issue_date": "2023-05-15", "expiry_date": add_days(today(), 180), "issuing_authority": "DGCA India", "status": "Valid"},
        {"aircraft": "VT-IGO", "certificate_type": "Other", "certificate_number": "CR-5678", "issue_date": "2019-11-25", "issuing_authority": "DGCA India", "status": "Valid"},
        {"aircraft": "VT-IGO", "certificate_type": "Certificate of Airworthiness", "certificate_number": "CA-5678", "issue_date": "2023-11-25", "expiry_date": add_days(today(), 200), "issuing_authority": "DGCA India", "status": "Valid"}
    ]
    for c in certs:
        get_or_create("Aircraft Certificate", {"aircraft": c["aircraft"], "certificate_type": c["certificate_type"]}, c)
    print("Aircraft Certificates seeded.")

def seed_flight_plans():
    import frappe.utils
    
    capt_name = frappe.db.get_value("Crew Member", {"full_name": "Capt. Rajan Sharma"}, "name")
    fo_name = frappe.db.get_value("Crew Member", {"full_name": "FO. Aman Verma"}, "name")
    
    fps = [
        {"flight_number": "AI101", "aircraft": "VT-ALM", "flight_date": today(), "departure_airport": "VIDP", "destination_airport": "KJFK", "etd_utc": now_datetime(), "eta_utc": frappe.utils.add_to_date(now_datetime(), hours=15), "trip_fuel_kg": 95000, "block_fuel_kg": 100000, "status": "Activated"},
        {"flight_number": "6E204", "aircraft": "VT-IGO", "flight_date": today(), "departure_airport": "VABB", "destination_airport": "VIDP", "etd_utc": now_datetime(), "eta_utc": frappe.utils.add_to_date(now_datetime(), hours=2), "trip_fuel_kg": 4500, "block_fuel_kg": 6000, "status": "Filed"},
        {"flight_number": "AI805", "aircraft": "VT-ABX", "flight_date": today(), "departure_airport": "VIDP", "destination_airport": "VOBL", "etd_utc": now_datetime(), "eta_utc": frappe.utils.add_to_date(now_datetime(), hours=3), "trip_fuel_kg": 5000, "block_fuel_kg": 6500, "status": "Completed"},
        {"flight_number": "EK500", "aircraft": "A6-EMA", "flight_date": today(), "departure_airport": "OMDB", "destination_airport": "VABB", "etd_utc": now_datetime(), "eta_utc": frappe.utils.add_to_date(now_datetime(), hours=4), "trip_fuel_kg": 12000, "block_fuel_kg": 15000, "status": "Completed"},
        {"flight_number": "SQ422", "aircraft": "9V-SWA", "flight_date": today(), "departure_airport": "WSSS", "destination_airport": "VABB", "etd_utc": now_datetime(), "eta_utc": frappe.utils.add_to_date(now_datetime(), hours=5), "trip_fuel_kg": 20000, "block_fuel_kg": 24000, "status": "Filed"}
    ]
    for fp in fps:
        fp["crew_assignments"] = [
            {"crew_member": capt_name, "role": "Captain", "is_active_crew": 1},
            {"crew_member": fo_name, "role": "First Officer", "is_active_crew": 1}
        ]
        name = get_or_create("Flight Plan", {"flight_number": fp["flight_number"], "flight_date": fp["flight_date"]}, fp)
        # Attempt to submit if in valid state, but ignore if it fails
        try:
            doc = frappe.get_doc("Flight Plan", name)
            if doc.docstatus == 0:
                doc.submit()
        except Exception as e:
            print("Flight Plan Submit Error:", e)
    print("Flight Plans seeded.")

def seed_flight_operations():
    import frappe.utils
    # Only for completed flight plans
    fps = frappe.get_all("Flight Plan", filters={"status": "Completed"})
    for fp in fps:
        fdoc = frappe.get_doc("Flight Plan", fp.name)
        ops = {
            "flight_plan": fdoc.name,
            "flight_number": fdoc.flight_number,
            "aircraft": fdoc.aircraft,
            "flight_date": fdoc.flight_date,
            "departure_airport": fdoc.departure_airport,
            "destination_airport": fdoc.destination_airport,
            "off_block_time": now_datetime(),
            "takeoff_time": frappe.utils.add_to_date(now_datetime(), minutes=15),
            "landing_time": frappe.utils.add_to_date(now_datetime(), hours=2),
            "on_block_time": frappe.utils.add_to_date(now_datetime(), hours=2, minutes=15),
            "status": "Completed"
        }
        name = get_or_create("Flight Operation", {"flight_plan": fdoc.name}, ops)
        try:
            doc = frappe.get_doc("Flight Operation", name)
            if doc.docstatus == 0:
                doc.submit()
        except Exception as e:
            print("Flight Operation Submit Error:", e)
    print("Flight Operations seeded.")

def seed_crew_licences():
    licences = [
        {"crew_member": frappe.db.get_value("Crew Member", {"full_name": "Capt. Rajan Sharma"}, "name"), "licence_type": "ATPL", "licence_number": "ATPL-12345", "issue_date": "2010-01-01", "expiry_date": add_days(today(), 365), "status": "Valid"},
        {"crew_member": frappe.db.get_value("Crew Member", {"full_name": "FO. Aman Verma"}, "name"), "licence_type": "CPL", "licence_number": "CPL-98765", "issue_date": "2015-05-10", "expiry_date": add_days(today(), 180), "status": "Valid"},
        {"crew_member": frappe.db.get_value("Crew Member", {"full_name": "Capt. Sarah Jenkins"}, "name"), "licence_type": "ATPL", "licence_number": "ATPL-55555", "issue_date": "2008-11-20", "expiry_date": add_days(today(), 30), "status": "Expiring Soon"}
    ]
    for l in licences:
        get_or_create("Crew Licence", {"licence_number": l["licence_number"]}, l)
    print("Crew Licences seeded.")

def seed_crew_duty_records():
    import frappe.utils
    duties = [
        {"crew_member": frappe.db.get_value("Crew Member", {"full_name": "Capt. Rajan Sharma"}, "name"), "duty_date": today(), "duty_type": "Flight Duty", "sign_on_time": now_datetime(), "sign_off_time": frappe.utils.add_to_date(now_datetime(), hours=8), "status": "Completed"},
        {"crew_member": frappe.db.get_value("Crew Member", {"full_name": "FO. Aman Verma"}, "name"), "duty_date": today(), "duty_type": "Flight Duty", "sign_on_time": now_datetime(), "sign_off_time": frappe.utils.add_to_date(now_datetime(), hours=8), "status": "Completed"},
        {"crew_member": frappe.db.get_value("Crew Member", {"full_name": "Priya Patel"}, "name"), "duty_date": today(), "duty_type": "Flight Duty", "sign_on_time": now_datetime(), "sign_off_time": frappe.utils.add_to_date(now_datetime(), hours=8), "status": "Completed"},
        {"crew_member": frappe.db.get_value("Crew Member", {"full_name": "Rahul Singh"}, "name"), "duty_date": today(), "duty_type": "Standby", "sign_on_time": now_datetime(), "sign_off_time": frappe.utils.add_to_date(now_datetime(), hours=8), "status": "Completed"},
        {"crew_member": frappe.db.get_value("Crew Member", {"full_name": "Capt. Sarah Jenkins"}, "name"), "duty_date": today(), "duty_type": "Training", "sign_on_time": now_datetime(), "sign_off_time": frappe.utils.add_to_date(now_datetime(), hours=8), "status": "Completed"}
    ]
    for d in duties:
        name = get_or_create("Crew Duty Record", {"crew_member": d["crew_member"], "duty_date": d["duty_date"], "duty_type": d["duty_type"]}, d)
        try:
            doc = frappe.get_doc("Crew Duty Record", name)
            if doc.docstatus == 0:
                doc.submit()
        except Exception as e:
            print("Crew Duty Submit Error:", e)
    print("Crew Duty Records seeded.")

def seed_maintenance_work_orders():
    mwos = [
        {"work_order_title": "Weekly A-Check", "aircraft": "VT-ABX", "maintenance_type": "A-Check", "planned_start_date": today(), "planned_completion_date": add_days(today(), 1), "status": "Approved", "priority": "Routine", "station": "VIDP"},
        {"work_order_title": "Hydraulic Leak Rectification", "aircraft": "VT-IGO", "maintenance_type": "Line Maintenance", "planned_start_date": today(), "planned_completion_date": today(), "status": "In Progress", "priority": "Urgent", "station": "VABB"},
        {"work_order_title": "Heavy C-Check", "aircraft": "VT-ALM", "maintenance_type": "C-Check", "planned_start_date": today(), "planned_completion_date": add_days(today(), 30), "status": "In Progress", "priority": "Routine", "station": "OMDB"},
        {"work_order_title": "Engine Borescope", "aircraft": "A6-EMA", "maintenance_type": "Line Maintenance", "planned_start_date": add_days(today(), 2), "planned_completion_date": add_days(today(), 2), "status": "Approved", "priority": "Routine", "station": "OMDB"},
        {"work_order_title": "Cabin Defect Rectification", "aircraft": "9V-SWA", "maintenance_type": "Line Maintenance", "planned_start_date": today(), "planned_completion_date": today(), "status": "Completed", "priority": "Routine", "station": "WSSS"}
    ]
    for m in mwos:
        name = get_or_create("Maintenance Work Order", {"work_order_title": m["work_order_title"], "aircraft": m["aircraft"]}, m)
        try:
            doc = frappe.get_doc("Maintenance Work Order", name)
            if m["status"] == "Completed" and doc.docstatus == 0:
                doc.submit()
        except:
            pass
    print("Maintenance Work Orders seeded.")

def seed_safety_reports():
    reports = [
        {"occurrence_date": today(), "occurrence_type": "Hazard", "summary": "Bird activity spotted near Runway 27", "severity": "Minor", "reported_by": frappe.session.user, "status": "Under Investigation", "location_airport": "VABB"},
        {"occurrence_date": add_days(today(), -2), "occurrence_type": "Incident", "summary": "Tug struck landing gear door", "severity": "Moderate", "reported_by": frappe.session.user, "status": "Under Investigation", "aircraft": "VT-IGO", "location_airport": "VIDP"},
        {"occurrence_date": add_days(today(), -5), "occurrence_type": "Voluntary Report", "summary": "Slippery apron surface during rain", "severity": "Minor", "reported_by": frappe.session.user, "status": "Closed", "location_airport": "VOBL"},
        {"occurrence_date": add_days(today(), -10), "occurrence_type": "Incident", "summary": "TCAS RA in cruise", "severity": "Major", "reported_by": frappe.session.user, "status": "Closed", "aircraft": "VT-ABX", "flight_number": "AI805"},
        {"occurrence_date": today(), "occurrence_type": "Hazard", "summary": "FOD found on taxiway N", "severity": "Minor", "reported_by": frappe.session.user, "status": "Submitted", "location_airport": "OMDB"}
    ]
    for r in reports:
        name = get_or_create("Safety Occurrence Report", {"summary": r["summary"]}, r)
        try:
            doc = frappe.get_doc("Safety Occurrence Report", name)
            if doc.docstatus == 0:
                doc.submit()
        except:
            pass
    print("Safety Occurrence Reports seeded.")
