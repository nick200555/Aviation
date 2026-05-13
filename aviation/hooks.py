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
                "Flight Plan"
            ]]
        ]
    },
    {
        "dt": "Workspace",
        "filters": [["name", "in", ["Aviation"]]]
    },
    {
        "dt": "Module Def",
        "filters": [["name", "in", ["Aviation"]]]
    },
    {
        "dt": "Dashboard",
        "filters": [["name", "in", ["Aviation Dashboard"]]]
    },
    {
        "dt": "Dashboard Chart",
        "filters": [
            ["chart_name", "in", [
                "Aircraft Utilization Trend",
                "Fleet Airworthiness Status",
                "Maintenance Workload",
                "Safety Reports Trend"
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
        "aviation.aviation.utils.scheduler.check_certificate_expiry",
        "aviation.aviation.utils.scheduler.check_crew_licence_expiry",
        "aviation.aviation.utils.scheduler.update_aircraft_flight_times"
    ],
    "daily": [
        "aviation.aviation.utils.scheduler.check_ad_due_items",
        "aviation.aviation.utils.scheduler.check_maintenance_overdue",
        "aviation.aviation.utils.scheduler.send_duty_limit_warnings",
        "aviation.aviation.utils.scheduler.generate_daily_ops_summary"
    ],
    "weekly": [
        "aviation.aviation.utils.scheduler.generate_weekly_safety_report",
        "aviation.aviation.utils.scheduler.generate_crew_utilisation_report"
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

# Whitelisted Methods
whitelisted_methods = {
    "aviation.aviation.api.fleet_api.get_aircraft_status": True,
    "aviation.aviation.api.crew_api.get_crew_availability": True,
    "aviation.aviation.api.flight_api.get_flight_schedule": True,
    "aviation.aviation.api.maintenance_api.get_maintenance_due": True,
    "aviation.aviation.api.safety_api.submit_safety_report": True,
}
