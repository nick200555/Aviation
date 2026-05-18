app_name = "aviation"
app_title = "Aviation Management"
app_publisher = "Aviation Team"
app_description = "Comprehensive Aviation Management System for ERPNext v15+"
app_email = "admin@aviation.org"
app_license = "mit"

# DocTypes to be exported as fixtures
fixtures = [
    {
        "dt": "Role",
        "filters": [
            ["name", "in", [
                "Aviation Manager",
                "Flight Operations Officer",
                "Maintenance Engineer",
                "Crew Scheduler",
                "Ground Operations Supervisor",
                "Safety Officer",
                "Load Controller"
            ]]
        ]
    },
    {
        "dt": "Workflow",
        "filters": [
            ["document_type", "in", [
                "Maintenance Work Order",
                "Flight Plan",
                "Safety Occurrence Report"
            ]]
        ]
    },
    {
        "dt": "Notification",
        "filters": [
            ["document_type", "in", [
                "Aircraft Certificate",
                "Crew Licence",
                "Airworthiness Directive",
                "Maintenance Work Order",
                "Flight Plan",
                "Launch Campaign",
                "Space Weather Alert",
                "Conjunction Assessment",
                "Aerospace Quality NCR"
            ]]
        ]
    },
    {
        "dt": "Workspace",
        "filters": [["name", "in", ["AeroSpaceOS"]]]
    },
    {
        "dt": "Module Def",
        "filters": [["name", "in", ["Aviation"]]]
    },
    {
        "dt": "Dashboard",
        "filters": [["name", "in", [
            "Aviation Dashboard",
            "Space Operations Dashboard"
        ]]]
    },
    {
        "dt": "Dashboard Chart",
        "filters": [
            ["chart_name", "in", [
                "Aircraft Utilization Trend",
                "Fleet Airworthiness Status",
                "Maintenance Workload",
                "Safety Reports Trend",
                "Active Spacecraft by Type",
                "Launch Campaign Status",
                "Propellant Consumption Trend",
                "Conjunction Risk Overview",
                "Space Weather Severity",
                "NCR Severity Distribution"
            ]]
        ]
    },
    {
        "dt": "Print Format",
        "filters": [
            ["doc_type", "in", [
                "Maintenance Work Order",
                "Flight Plan",
                "Load Sheet",
                "Aircraft Certificate"
            ]]
        ]
    }
]

# Hooks for document events are handled directly in each DocType's Python controller class.
# Frappe automatically calls validate(), on_submit(), on_cancel(), on_update(), after_insert()
# class methods without needing explicit doc_events registration here.
doc_events = {}


# Scheduled Tasks
scheduler_events = {
    "hourly": [
        # Aviation (existing)
        "aviation.aviation.utils.scheduler.check_certificate_expiry",
        "aviation.aviation.utils.scheduler.check_crew_licence_expiry",
        "aviation.aviation.utils.scheduler.update_aircraft_flight_times",
        # Space — AeroSpaceOS (new)
        "aviation.aviation.utils.space_scheduler.ingest_scheduled_telemetry",
        "aviation.aviation.utils.space_scheduler.monitor_collision_risks",
        "aviation.aviation.utils.space_scheduler.check_spacecraft_health"
    ],
    "daily": [
        # Aviation (existing)
        "aviation.aviation.utils.scheduler.check_ad_due_items",
        "aviation.aviation.utils.scheduler.check_maintenance_overdue",
        "aviation.aviation.utils.scheduler.send_duty_limit_warnings",
        "aviation.aviation.utils.scheduler.generate_daily_ops_summary",
        # Space — AeroSpaceOS (new)
        "aviation.aviation.utils.space_scheduler.check_itar_compliance",
        "aviation.aviation.utils.space_scheduler.check_propellant_levels",
        "aviation.aviation.utils.space_scheduler.update_orbit_data"
    ],
    "weekly": [
        # Aviation (existing)
        "aviation.aviation.utils.scheduler.generate_weekly_safety_report",
        "aviation.aviation.utils.scheduler.generate_crew_utilisation_report",
        # Space — AeroSpaceOS (new)
        "aviation.aviation.utils.space_scheduler.generate_launch_readiness_report",
        "aviation.aviation.utils.space_scheduler.review_open_ncrs"
    ]
}

# Jinja Filters
jinja = {
    "methods": [
        "aviation.aviation.utils.jinja.get_aircraft_status",
        "aviation.aviation.utils.jinja.get_crew_duty_remaining",
        "aviation.aviation.utils.jinja.format_flight_time"
    ]
}

# Whitelisted Methods — Aviation (existing) + Space (new per Space_gap.md)
whitelisted_methods = {
    # Aviation (existing)
    "aviation.aviation.api.fleet_api.get_aircraft_status": True,
    "aviation.aviation.api.crew_api.get_crew_availability": True,
    "aviation.aviation.api.flight_api.get_flight_schedule": True,
    "aviation.aviation.api.maintenance_api.get_maintenance_due": True,
    "aviation.aviation.api.safety_api.submit_safety_report": True,
    # Space — AeroSpaceOS (from Space_gap.md blueprint)
    "aviation.aviation.api.spaceflight_api.ingest_telemetry": True,
    "aviation.aviation.api.spaceflight_api.get_satellite_trajectory": True,
    "aviation.aviation.api.spaceflight_api.get_ground_station_schedule": True,
    "aviation.aviation.api.spaceflight_api.calculate_collision_probability": True,
    "aviation.aviation.api.spaceflight_api.update_propellant_levels": True,
}
