import json
import os

def create_aviation_workspace():
    return {
        "charts": [],
        "content": json.dumps([
            {"id": "cb-fleet", "type": "card", "data": {"card_name": "Fleet Management", "col": 12}},
            {"id": "cb-ops", "type": "card", "data": {"card_name": "Flight Operations", "col": 12}},
            {"id": "cb-crew", "type": "card", "data": {"card_name": "Crew Management", "col": 12}},
            {"id": "cb-mro", "type": "card", "data": {"card_name": "Maintenance (MRO)", "col": 12}},
            {"id": "cb-safety", "type": "card", "data": {"card_name": "Safety & SMS", "col": 12}},
            {"id": "cb-reports", "type": "card", "data": {"card_name": "Reports & Analytics", "col": 12}}
        ]),
        "creation": "2024-05-18 00:00:00.000000",
        "developer_mode_only": 0,
        "disable_user_customization": 0,
        "docstatus": 0,
        "doctype": "Workspace",
        "for_user": "",
        "hide_custom": 0,
        "icon": "airplane",
        "idx": 0,
        "is_default": 0,
        "is_hidden": 0,
        "is_standard": 1,
        "label": "Aviation",
        "links": [
            {"hidden": 0, "idx": 1, "is_query_report": 0, "label": "Fleet Management", "link_count": 0, "onboard": 1, "title": "Fleet Management", "type": "Card Break"},
            {"dependencies": "", "hidden": 0, "idx": 2, "is_query_report": 0, "label": "Aircraft", "link_count": 0, "link_to": "Aircraft", "link_type": "DocType", "onboard": 1, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 3, "is_query_report": 0, "label": "Aircraft Type", "link_count": 0, "link_to": "Aircraft Type", "link_type": "DocType", "onboard": 1, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 4, "is_query_report": 0, "label": "Engine", "link_count": 0, "link_to": "Engine", "link_type": "DocType", "onboard": 1, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 5, "is_query_report": 0, "label": "Engine Type", "link_count": 0, "link_to": "Engine Type", "link_type": "DocType", "onboard": 0, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 6, "is_query_report": 0, "label": "Airline", "link_count": 0, "link_to": "Airline", "link_type": "DocType", "onboard": 0, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 7, "is_query_report": 0, "label": "Airport", "link_count": 0, "link_to": "Airport", "link_type": "DocType", "onboard": 0, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 8, "is_query_report": 0, "label": "Aircraft Certificate", "link_count": 0, "link_to": "Aircraft Certificate", "link_type": "DocType", "onboard": 1, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 9, "is_query_report": 0, "label": "Part Number", "link_count": 0, "link_to": "Part Number", "link_type": "DocType", "onboard": 0, "type": "Link"},
            {"hidden": 0, "idx": 10, "is_query_report": 0, "label": "Flight Operations", "link_count": 0, "onboard": 1, "title": "Flight Operations", "type": "Card Break"},
            {"dependencies": "", "hidden": 0, "idx": 11, "is_query_report": 0, "label": "Flight Plan", "link_count": 0, "link_to": "Flight Plan", "link_type": "DocType", "onboard": 1, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 12, "is_query_report": 0, "label": "Flight Operation", "link_count": 0, "link_to": "Flight Operation", "link_type": "DocType", "onboard": 1, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 13, "is_query_report": 0, "label": "Route", "link_count": 0, "link_to": "Route", "link_type": "DocType", "onboard": 0, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 14, "is_query_report": 0, "label": "Fuel Uplift", "link_count": 0, "link_to": "Fuel Uplift", "link_type": "DocType", "onboard": 0, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 15, "is_query_report": 0, "label": "Load Sheet", "link_count": 0, "link_to": "Load Sheet", "link_type": "DocType", "onboard": 1, "type": "Link"},
            {"hidden": 0, "idx": 16, "is_query_report": 0, "label": "Crew Management", "link_count": 0, "onboard": 1, "title": "Crew Management", "type": "Card Break"},
            {"dependencies": "", "hidden": 0, "idx": 17, "is_query_report": 0, "label": "Crew Member", "link_count": 0, "link_to": "Crew Member", "link_type": "DocType", "onboard": 1, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 18, "is_query_report": 0, "label": "Crew Licence", "link_count": 0, "link_to": "Crew Licence", "link_type": "DocType", "onboard": 1, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 19, "is_query_report": 0, "label": "Crew Duty Record", "link_count": 0, "link_to": "Crew Duty Record", "link_type": "DocType", "onboard": 1, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 20, "is_query_report": 0, "label": "Crew Qualification Type", "link_count": 0, "link_to": "Crew Qualification Type", "link_type": "DocType", "onboard": 0, "type": "Link"},
            {"hidden": 0, "idx": 21, "is_query_report": 0, "label": "Maintenance (MRO)", "link_count": 0, "onboard": 1, "title": "Maintenance (MRO)", "type": "Card Break"},
            {"dependencies": "", "hidden": 0, "idx": 22, "is_query_report": 0, "label": "Maintenance Work Order", "link_count": 0, "link_to": "Maintenance Work Order", "link_type": "DocType", "onboard": 1, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 23, "is_query_report": 0, "label": "Maintenance Task Card", "link_count": 0, "link_to": "Maintenance Task Card", "link_type": "DocType", "onboard": 0, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 24, "is_query_report": 0, "label": "Airworthiness Directive", "link_count": 0, "link_to": "Airworthiness Directive", "link_type": "DocType", "onboard": 1, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 25, "is_query_report": 0, "label": "Service Bulletin", "link_count": 0, "link_to": "Service Bulletin", "link_type": "DocType", "onboard": 0, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 26, "is_query_report": 0, "label": "Component Overhaul Record", "link_count": 0, "link_to": "Component Overhaul Record", "link_type": "DocType", "onboard": 0, "type": "Link"},
            {"hidden": 0, "idx": 27, "is_query_report": 0, "label": "Safety & SMS", "link_count": 0, "onboard": 1, "title": "Safety & SMS", "type": "Card Break"},
            {"dependencies": "", "hidden": 0, "idx": 28, "is_query_report": 0, "label": "Safety Occurrence Report", "link_count": 0, "link_to": "Safety Occurrence Report", "link_type": "DocType", "onboard": 1, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 29, "is_query_report": 0, "label": "Hazard Register", "link_count": 0, "link_to": "Hazard Register", "link_type": "DocType", "onboard": 0, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 30, "is_query_report": 0, "label": "Safety Investigation", "link_count": 0, "link_to": "Safety Investigation", "link_type": "DocType", "onboard": 0, "type": "Link"},
            {"hidden": 0, "idx": 31, "is_query_report": 0, "label": "Reports & Analytics", "link_count": 0, "onboard": 1, "title": "Reports & Analytics", "type": "Card Break"},
            {"dependencies": "", "hidden": 0, "idx": 32, "is_query_report": 1, "label": "Aircraft Utilization", "link_count": 0, "link_to": "Aircraft Utilization", "link_type": "Report", "onboard": 0, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 33, "is_query_report": 1, "label": "Flight Operations Summary", "link_count": 0, "link_to": "Flight Operations Summary", "link_type": "Report", "onboard": 0, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 34, "is_query_report": 1, "label": "Crew Duty Report", "link_count": 0, "link_to": "Crew Duty Report", "link_type": "Report", "onboard": 0, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 35, "is_query_report": 1, "label": "Maintenance Due Report", "link_count": 0, "link_to": "Maintenance Due Report", "link_type": "Report", "onboard": 0, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 36, "is_query_report": 1, "label": "AD SB Compliance Report", "link_count": 0, "link_to": "AD SB Compliance Report", "link_type": "Report", "onboard": 0, "type": "Link"},
            {"dependencies": "", "hidden": 0, "idx": 37, "is_query_report": 1, "label": "Safety Occurrence Report (Report)", "link_count": 0, "link_to": "Safety Occurrence Report", "link_type": "Report", "onboard": 0, "type": "Link"}
        ],
        "modified": "2024-05-18 00:00:00.000000",
        "modified_by": "Administrator",
        "module": "Aviation",
        "name": "Aviation",
        "owner": "Administrator",
        "public": 1,
        "restrict_to_domain": "",
        "roles": [],
        "sequence_id": 1.0,
        "shortcuts": [],
        "title": "Aviation"
    }

def create_aerospaceos_workspace(aviation):
    ws = dict(aviation)
    ws["name"] = "AeroSpaceOS"
    ws["label"] = "AeroSpaceOS"
    ws["title"] = "AeroSpaceOS"
    ws["icon"] = "rocket"
    
    content = json.loads(ws["content"])
    content.extend([
        {"id": "cb-spacecraft", "type": "card", "data": {"card_name": "Spacecraft & Satellites", "col": 12}},
        {"id": "cb-launch", "type": "card", "data": {"card_name": "Launch & Mission Control", "col": 12}},
        {"id": "cb-orbital", "type": "card", "data": {"card_name": "Orbital Operations", "col": 12}},
        {"id": "cb-cryogenic", "type": "card", "data": {"card_name": "Cryogenic Logistics", "col": 12}},
        {"id": "cb-compliance", "type": "card", "data": {"card_name": "Aerospace Compliance", "col": 12}}
    ])
    ws["content"] = json.dumps(content)
    
    links = list(ws["links"])
    start_idx = 38
    new_links = [
        {"hidden": 0, "idx": start_idx, "is_query_report": 0, "label": "Spacecraft & Satellites", "link_count": 0, "onboard": 1, "title": "Spacecraft & Satellites", "type": "Card Break"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+1, "is_query_report": 0, "label": "Spacecraft Asset", "link_count": 0, "link_to": "Spacecraft Asset", "link_type": "DocType", "onboard": 1, "type": "Link"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+2, "is_query_report": 0, "label": "Launch Vehicle Component", "link_count": 0, "link_to": "Launch Vehicle Component", "link_type": "DocType", "onboard": 1, "type": "Link"},
        
        {"hidden": 0, "idx": start_idx+3, "is_query_report": 0, "label": "Launch & Mission Control", "link_count": 0, "onboard": 1, "title": "Launch & Mission Control", "type": "Card Break"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+4, "is_query_report": 0, "label": "Launch Campaign", "link_count": 0, "link_to": "Launch Campaign", "link_type": "DocType", "onboard": 1, "type": "Link"},
        
        {"hidden": 0, "idx": start_idx+6, "is_query_report": 0, "label": "Orbital Operations", "link_count": 0, "onboard": 1, "title": "Orbital Operations", "type": "Card Break"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+7, "is_query_report": 0, "label": "Orbit Parameter", "link_count": 0, "link_to": "Orbit Parameter", "link_type": "DocType", "onboard": 1, "type": "Link"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+8, "is_query_report": 0, "label": "Ground Station Pass", "link_count": 0, "link_to": "Ground Station Pass", "link_type": "DocType", "onboard": 1, "type": "Link"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+9, "is_query_report": 0, "label": "Conjunction Assessment", "link_count": 0, "link_to": "Conjunction Assessment", "link_type": "DocType", "onboard": 1, "type": "Link"},
        
        {"hidden": 0, "idx": start_idx+10, "is_query_report": 0, "label": "Cryogenic Logistics", "link_count": 0, "onboard": 1, "title": "Cryogenic Logistics", "type": "Card Break"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+11, "is_query_report": 0, "label": "Propellant Load Log", "link_count": 0, "link_to": "Propellant Load Log", "link_type": "DocType", "onboard": 1, "type": "Link"},
        
        {"hidden": 0, "idx": start_idx+12, "is_query_report": 0, "label": "Aerospace Compliance", "link_count": 0, "onboard": 1, "title": "Aerospace Compliance", "type": "Card Break"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+13, "is_query_report": 0, "label": "ITAR EAR Access Control", "link_count": 0, "link_to": "ITAR EAR Access Control", "link_type": "DocType", "onboard": 1, "type": "Link"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+14, "is_query_report": 0, "label": "Aerospace Quality NCR", "link_count": 0, "link_to": "Aerospace Quality NCR", "link_type": "DocType", "onboard": 1, "type": "Link"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+15, "is_query_report": 0, "label": "Space Weather Alert", "link_count": 0, "link_to": "Space Weather Alert", "link_type": "DocType", "onboard": 1, "type": "Link"}
    ]
    
    space_reports = [
        {"dependencies": "", "hidden": 0, "idx": start_idx+16, "is_query_report": 1, "label": "Spacecraft Utilization Report", "link_count": 0, "link_to": "Spacecraft Utilization Report", "link_type": "Report", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+17, "is_query_report": 1, "label": "Launch Campaign Status Report", "link_count": 0, "link_to": "Launch Campaign Status Report", "link_type": "Report", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+18, "is_query_report": 1, "label": "Propellant Usage Report", "link_count": 0, "link_to": "Propellant Usage Report", "link_type": "Report", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+19, "is_query_report": 1, "label": "Conjunction Risk Report", "link_count": 0, "link_to": "Conjunction Risk Report", "link_type": "Report", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+20, "is_query_report": 1, "label": "Space Weather Impact Report", "link_count": 0, "link_to": "Space Weather Impact Report", "link_type": "Report", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+21, "is_query_report": 1, "label": "ITAR Compliance Report", "link_count": 0, "link_to": "ITAR Compliance Report", "link_type": "Report", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "idx": start_idx+22, "is_query_report": 1, "label": "Aerospace NCR Report", "link_count": 0, "link_to": "Aerospace NCR Report", "link_type": "Report", "onboard": 0, "type": "Link"}
    ]
    
    links.extend(new_links)
    
    # insert space_reports into Reports card. Wait, we'll just append them at the end.
    links.extend(space_reports)
    ws["links"] = links
    
    ws["shortcuts"] = []
    
    return ws

def save_workspace(ws, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(ws, f, indent=1)
        
    init_path = os.path.join(os.path.dirname(path), "__init__.py")
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write("# Copyright (c) 2024, Aviation Team and contributors\n")

aviation = create_aviation_workspace()
save_workspace(aviation, r"c:\Seria Internship\Avation\aviation\aviation\aviation\workspace\aviation\aviation.json")
save_workspace(create_aerospaceos_workspace(aviation), r"c:\Seria Internship\Avation\aviation\aviation\aviation\workspace\aerospaceos\aerospaceos.json")
