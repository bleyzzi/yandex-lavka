class AddCorrectRequestCourier:
    empty_request = {
        "couriers": []
    }
    one_request = {
        "couriers": [
            {
                "courier_type": "AUTO",
                "regions": [
                    1
                ],
                "working_hours": [
                    "12:00-14:00"
                ]
            }
        ]
    }
    many_requests = {
        "couriers": [
            {
                "courier_type": "AUTO",
                "regions": [
                    1
                ],
                "working_hours": [
                    "12:00-14:00"
                ]
            },
            {
                "courier_type": "FOOT",
                "regions": [
                    1, 2, 3
                ],
                "working_hours": [
                    "10:00-12:00",
                    "15:00-17:00"
                ]
            }
        ]
    }
    all_requests = [empty_request, one_request, many_requests]


class AddIncorrectRequestCourier:
    none_request = None
    empty_request = {}
    one_request_with_incorrect_field = {"aaaa": []}
    one_request_with_incorrect_courier_type = {
        "couriers": [
            {
                "courier_type": "aaaa",
                "regions": [
                    1
                ],
                "working_hours": [
                    "12:00-14:00"
                ]
            }
        ]
    }
    one_request_with_incorrect_regions = {
        "couriers": [
            {
                "courier_type": "aaaa",
                "regions": [
                    1,
                    "a"
                ],
                "working_hours": [
                    "12:00-14:00"
                ]
            }
        ]
    }
    one_request_with_incorrect_working_hours = {
        "couriers": [
            {
                "courier_type": "aaaa",
                "regions": [
                    1,
                    "a"
                ],
                "working_hours": [
                    "12:aa-14:bb"
                ]
            }
        ]
    }
    many_incorrect_couriers = {
        "couriers": [
            {"courier_type": "aaa", "regions": [1], "working_hours": ["12:00-14:00"]},
            {"courier_type": "AUTO", "regions": [1, "a"], "working_hours": ["12:00-14:00"]},
            {"courier_type": "BIKE", "regions": [1], "working_hours": ["1-14:00"]},
            {"courier_type": "AUTO", "regions": [], "working_hours": ["12:00-14:00"]},
            {"courier_type": "FOOT", "regions": {}, "working_hours": ["12:0"]}
        ]
    }
    all_requests_400 = [one_request_with_incorrect_courier_type, many_incorrect_couriers]
    all_requests_422 = [none_request, empty_request, one_request_with_incorrect_field]