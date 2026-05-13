import frappe

def after_install():
    create_roles()
    create_default_airports()
    create_default_aircraft_types()

def create_roles():
    roles = [
        "Aviation Manager",
        "Flight Operations Officer",
        "Maintenance Engineer",
        "Crew Scheduler",
        "Ground Operations Supervisor",
        "Safety Officer",
        "Load Controller"
    ]
    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({"doctype": "Role", "role_name": role, "desk_access": 1}).insert()
    frappe.db.commit()

def create_default_airports():
    """Seed common Indian airports."""
    airports = [
        {"icao_code": "VABB", "iata_code": "BOM", "airport_name": "Chhatrapati Shivaji Maharaj International Airport", "city": "Mumbai", "country": "India", "timezone": "+05:30"},
        {"icao_code": "VIDP", "iata_code": "DEL", "airport_name": "Indira Gandhi International Airport", "city": "New Delhi", "country": "India", "timezone": "+05:30"},
        {"icao_code": "VOBL", "iata_code": "BLR", "airport_name": "Kempegowda International Airport", "city": "Bengaluru", "country": "India", "timezone": "+05:30"},
        {"icao_code": "VOMM", "iata_code": "MAA", "airport_name": "Chennai International Airport", "city": "Chennai", "country": "India", "timezone": "+05:30"},
        {"icao_code": "VECC", "iata_code": "CCU", "airport_name": "Netaji Subhas Chandra Bose International Airport", "city": "Kolkata", "country": "India", "timezone": "+05:30"},
    ]
    for ap in airports:
        if not frappe.db.exists("Airport", ap["icao_code"]):
            doc = frappe.new_doc("Airport")
            doc.update(ap)
            doc.is_active = 1
            doc.insert()

def create_default_aircraft_types():
    """Seed common aircraft types."""
    types = [
        {"type_designator": "B738", "manufacturer": "Boeing", "model_name": "737-800", "wake_turbulence_category": "M", "aircraft_category": "Aeroplane", "number_of_engines": 2},
        {"type_designator": "A320", "manufacturer": "Airbus", "model_name": "A320-200", "wake_turbulence_category": "M", "aircraft_category": "Aeroplane", "number_of_engines": 2},
        {"type_designator": "A321", "manufacturer": "Airbus", "model_name": "A321-200", "wake_turbulence_category": "M", "aircraft_category": "Aeroplane", "number_of_engines": 2},
        {"type_designator": "B77W", "manufacturer": "Boeing", "model_name": "777-300ER", "wake_turbulence_category": "H", "aircraft_category": "Aeroplane", "number_of_engines": 2},
        {"type_designator": "AT76", "manufacturer": "ATR", "model_name": "ATR 72-600", "wake_turbulence_category": "M", "aircraft_category": "Aeroplane", "number_of_engines": 2},
    ]
    for at in types:
        if not frappe.db.exists("Aircraft Type", at["type_designator"]):
            doc = frappe.new_doc("Aircraft Type")
            doc.update(at)
            doc.is_active = 1
            doc.insert()
    frappe.db.commit()
