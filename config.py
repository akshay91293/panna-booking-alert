# config.py

PARK_NAME = "Panna Tiger Reserve"

PARK_ID = 3

URL = f"https://forest.mponline.gov.in/Search.aspx?park={PARK_ID}"

TELEGRAM_ENABLED = True


FIELD_METADATA = {

    "to_dt": {
        "label": "Backend Season End Date",
        "weight": 5
    },

    "rule_image": {
        "label": "Rule Book Image",
        "weight": 4
    },

    "important_notes": {
        "label": "Important Notes",
        "weight": 3
    },

    "single_seat_banner": {
        "label": "Single Seat Banner",
        "weight": 1
    },

    "tatkal_banner": {
        "label": "Tatkal Banner",
        "weight": 1
    },

    "park_name": {
        "label": "Park Name",
        "weight": 0
    }

}
