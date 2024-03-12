import json
table = {
    "Age_Years": {
        "Total": 22714,
        "23_or_younger": None,
        "24_or_older": 8576
    },
    "Students": {
        "Undergraduate": {
            "23_or_younger": 12785,
            "24_or_older": 2922,
            "Total": 15707
        },
        "Postgraduate": {
            "23_or_younger": 1353,
            "24_or_older": None,
            "Total": None
        }
    }
}

table_json = json.dumps(table)
print(table_json)
