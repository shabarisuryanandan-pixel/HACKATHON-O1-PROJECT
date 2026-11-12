from fastapi.testclient import TestClient
from unittest.mock import patch

import main
from sandbox_engine import evaluate_sandbox_state, format_12h, generate_random_timetable


def test_format_12h():
    assert format_12h(7.0) == "07:00 AM"
    assert format_12h(12.0) == "12:00 PM"
    assert format_12h(19.5) == "07:30 PM"
    assert format_12h(21.5) == "09:30 PM"


def test_capacity_aware_wing_consolidation():
    # 55 students in B108 (60 cap) + 3 in Left Wing (B101, B102, B103 active -> only B104 60 cap is free)
    res = evaluate_sandbox_state({
        "time": "02:00 PM",
        "temperature": 32,
        "weather": "Sunny / Daylight",
        "rooms": {"B101": 35, "B102": 30, "B103": 28, "B108": 55},
    })
    assert len(res["relocations"]) == 1
    assert res["relocations"][0]["from_room"] == "B108"
    assert res["relocations"][0]["to_room"] == "B104"

    # 55 students in B108 when B101 and B104 are ALREADY occupied (only 48-seat B102/B103 free -> cannot move!)
    res_no_fit = evaluate_sandbox_state({
        "time": "02:00 PM",
        "temperature": 32,
        "weather": "Sunny / Daylight",
        "rooms": {"B101": 40, "B104": 40, "B108": 55},
    })
    assert res_no_fit["relocations"] == []


def test_multi_class_wing_consolidation():
    # 2 classes in Left Wing + 2 small classes in Right Wing -> consolidates Right Wing into Left Wing
    res = evaluate_sandbox_state({
        "time": "03:00 PM",
        "temperature": 33,
        "weather": "Sunny / Daylight",
        "rooms": {"B101": 35, "B102": 30, "B106": 25, "B108": 28},
    })
    assert len(res["relocations"]) == 2
    assert res["right_wing_people"] == 0
    assert res["elevator_mode"].startswith("2 Lifts Active: L1 & L2 ON")


def test_curfew_shutdown_after_1030pm():
    res = evaluate_sandbox_state({
        "time": "10:30 PM",
        "temperature": 27,
        "weather": "Night",
        "rooms": {"B101": 40, "B108": 30},
    })
    assert res["active_classes"] == 0
    assert res["total_optimized_kw"] == 0.0
    assert res["savings_percentage"] == 100.0
    assert "Complete Building Shutdown" in res["elevator_mode"]


def test_temperature_coupled_baseline():
    cool = evaluate_sandbox_state({"time": "08:00 AM", "temperature": 22, "weather": "Sunny / Daylight", "rooms": {"B101": 35}})
    hot = evaluate_sandbox_state({"time": "08:00 AM", "temperature": 36, "weather": "Sunny / Daylight", "rooms": {"B101": 35}})
    assert hot["total_baseline_kw"] > cool["total_baseline_kw"]


def test_timetable_includes_curfew_slots():
    tt = generate_random_timetable(seed=42)["schedule"]
    assert tt[-2]["time_12h"] == "10:30 PM"
    assert tt[-1]["time_12h"] == "11:00 PM"
    assert tt[-1]["active_count"] == 0


def test_api_evaluate_pydantic_and_background_dispatch():
    client = TestClient(main.app)
    with patch("main.dispatch_auto_notification") as mock_dispatch:
        resp = client.post(
            "/api/sandbox/evaluate",
            json={
                "time": "02:00 PM",
                "temperature": 32,
                "weather": "Sunny / Daylight",
                "rooms": {"B101": 35, "B102": 30, "B103": 28, "B108": 25},
                "simulate": True,
                "mode": "Variable Mode",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["dispatch"]["status"] == "queued_background"
        assert mock_dispatch.called

    # Validation check: out-of-range temperature returns 422
    bad_resp = client.post("/api/sandbox/evaluate", json={"temperature": 999})
    assert bad_resp.status_code == 422

    # Persisted suggestions endpoint returns data
    sugg_resp = client.get("/api/suggestions")
    assert sugg_resp.status_code == 200
    assert len(sugg_resp.json()["suggestions"]) >= 1
