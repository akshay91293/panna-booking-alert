URL = "https://forest.mponline.gov.in/Search.aspx?park=3"

PARK_NAME = "Panna Monitor"

DATES_TO_CHECK = [
    "1 October",
    "2 October",
    "3 October"
]

# Daily Health Report (24-hour IST)
DAILY_HEALTH_REPORT_HOUR = 9


# -----------------------------
# Website Change Classification
# -----------------------------

FIELD_METADATA = {

    "to_dt": {
        "label": "Booking season updated",
        "weight": 10
    },

    "important_notes": {
        "label": "Important notes updated",
        "weight": 8
    },

    "rule_image": {
        "label": "Rule book updated",
        "weight": 7
    },

    "tatkal_banner": {
        "label": "Tatkal booking dates updated",
        "weight": 2
    },

    "single_seat_banner": {
        "label": "Single-seat booking dates updated",
        "weight": 2
    }
}


# Fields that should immediately notify

IMPORTANT_FIELDS = {
    "to_dt",
    "important_notes",
    "rule_image"
}


# Fields that appear only in Daily Health Report

INFO_FIELDS = {
    "tatkal_banner",
    "single_seat_banner"
}


# Status text shown in Telegram

STATUS_TEXT = {

    "PARK_CLOSED": "Park Closed",

    "POSSIBLY_OPEN": "Booking Available",

    "UNKNOWN": "Unable to Verify"
}
