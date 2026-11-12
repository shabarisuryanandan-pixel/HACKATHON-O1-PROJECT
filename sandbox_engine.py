"""
GridSense Simulation Engine (JIT Campus Block B Digital Twin)
Supports:
- 12-hour AM/PM time formatting everywhere
- 8 Classrooms (B101-B104 Left Wing, B105-B108 Right Wing) + 3 Labs (LAB1, LAB2, LAB3)
- Two-stage evaluation: Unmanaged Baseline State (with realistic partial/full wasted lights) vs Simulated Optimized State
- Wing Consolidation (relocating isolated classes from one wing to the other to shut down an entire wing)
- Proportional Lift Staging (L1, L2 in Left Wing; L3, L4 in Right Wing) based on class count and wing headcount
- Staircase, Corridor, and Faculty Lounge smart zoning
- 3-Part Natural Report Template + Session Suggestions Log
"""

import random

ROOM_META = {
    "B101": {"id": "B101", "label": "CR B-101", "name": "Classroom B-101", "wing": "Left", "type": "classroom", "capacity": 60, "near_stairs": "MAIN"},
    "B102": {"id": "B102", "label": "CR B-102", "name": "Classroom B-102", "wing": "Left", "type": "classroom", "capacity": 60, "near_stairs": "MAIN"},
    "B103": {"id": "B103", "label": "CR B-103", "name": "Classroom B-103", "wing": "Left", "type": "classroom", "capacity": 60, "near_stairs": "SW"},
    "B104": {"id": "B104", "label": "CR B-104", "name": "Classroom B-104", "wing": "Left", "type": "classroom", "capacity": 60, "near_stairs": "SW"},
    "B105": {"id": "B105", "label": "CR B-105", "name": "Classroom B-105", "wing": "Right", "type": "classroom", "capacity": 60, "near_stairs": "MAIN"},
    "B106": {"id": "B106", "label": "CR B-106", "name": "Classroom B-106", "wing": "Right", "type": "classroom", "capacity": 60, "near_stairs": "MAIN"},
    "B107": {"id": "B107", "label": "CR B-107", "name": "Classroom B-107", "wing": "Right", "type": "classroom", "capacity": 60, "near_stairs": "SE"},
    "B108": {"id": "B108", "label": "CR B-108", "name": "Classroom B-108", "wing": "Right", "type": "classroom", "capacity": 60, "near_stairs": "SE"},
    "LAB1": {"id": "LAB1", "label": "Lab B-1", "name": "Lab B-1 (Hardware)", "wing": "Left", "type": "lab", "capacity": 45, "near_stairs": "MAIN"},
    "LAB2": {"id": "LAB2", "label": "Lab B-2", "name": "Lab B-2 (Comm)", "wing": "Right", "type": "lab", "capacity": 45, "near_stairs": "MAIN"},
    "LAB3": {"id": "LAB3", "label": "Comp Lab B-3", "name": "Computer Lab B-3", "wing": "Right", "type": "lab", "capacity": 50, "near_stairs": "SE"},
}

LEFT_CLASSROOMS = ["B101", "B102", "B103", "B104"]
RIGHT_CLASSROOMS = ["B105", "B106", "B107", "B108"]
ALL_LIBS_AND_ROOMS = ["B101", "B102", "B103", "B104", "B105", "B106", "B107", "B108", "LAB1", "LAB2", "LAB3"]


def format_12h(time_float: float) -> str:
    """Convert float hour (e.g. 19.5) to 12-hour AM/PM string (e.g. '07:30 PM')."""
    total_minutes = int(round(time_float * 60))
    hours_24 = (total_minutes // 60) % 24
    minutes = total_minutes % 60
    period = "AM" if hours_24 < 12 else "PM"
    hours_12 = hours_24 % 12
    if hours_12 == 0:
        hours_12 = 12
    return f"{hours_12:02d}:{minutes:02d} {period}"


def parse_time_input(time_val) -> tuple[float, str]:
    """Accept float (19.5), '19:30', or '07:30 PM' and return (time_float, formatted_12h)."""
    if isinstance(time_val, (int, float)):
        tf = float(time_val)
        return tf, format_12h(tf)

    s = str(time_val).strip().upper()
    try:
        if "AM" in s or "PM" in s:
            is_pm = "PM" in s
            clean = s.replace("AM", "").replace("PM", "").strip()
            parts = clean.split(":")
            h = int(parts[0])
            m = int(parts[1]) if len(parts) > 1 else 0
            if is_pm and h != 12:
                h += 12
            elif not is_pm and h == 12:
                h = 0
            tf = h + m / 60.0
            return tf, format_12h(tf)
        elif ":" in s:
            parts = s.split(":")
            h = int(parts[0])
            m = int(parts[1]) if len(parts) > 1 else 0
            tf = h + m / 60.0
            return tf, format_12h(tf)
        else:
            tf = float(s)
            return tf, format_12h(tf)
    except Exception:
        return 19.5, "07:30 PM"


def generate_random_timetable(seed=None) -> dict:
    """
    Generate a realistic full-day timetable in 12-hour AM/PM format.
    Morning peak has more classes (4-6 rooms), afternoon has moderate (3-4 rooms),
    evening has 1-2 isolated classes, and night/early morning has 0-1.
    """
    rng = random.Random(seed)
    slots = [
        {"time_float": 7.0,  "label": "07:00 AM", "temp": 24, "weather": "Sunny / Daylight", "profile": "early"},
        {"time_float": 8.0,  "label": "08:00 AM", "temp": 26, "weather": "Sunny / Daylight", "profile": "morning_peak"},
        {"time_float": 9.0,  "label": "09:00 AM", "temp": 28, "weather": "Sunny / Daylight", "profile": "morning_peak"},
        {"time_float": 10.0, "label": "10:00 AM", "temp": 30, "weather": "Sunny / Daylight", "profile": "morning_peak"},
        {"time_float": 11.0, "label": "11:00 AM", "temp": 32, "weather": "Sunny / Daylight", "profile": "midday"},
        {"time_float": 12.0, "label": "12:00 PM", "temp": 34, "weather": "Sunny / Daylight", "profile": "afternoon_light"},
        {"time_float": 13.0, "label": "01:00 PM", "temp": 35, "weather": "Sunny / Daylight", "profile": "lunch"},
        {"time_float": 14.0, "label": "02:00 PM", "temp": 34, "weather": "Sunny / Daylight", "profile": "afternoon"},
        {"time_float": 15.0, "label": "03:00 PM", "temp": 33, "weather": "Sunny / Daylight", "profile": "afternoon"},
        {"time_float": 16.0, "label": "04:00 PM", "temp": 31, "weather": "Sunny / Daylight", "profile": "late_afternoon"},
        {"time_float": 18.0, "label": "06:00 PM", "temp": 29, "weather": "Night", "profile": "evening"},
        {"time_float": 19.5, "label": "07:30 PM", "temp": 28, "weather": "Night", "profile": "evening_isolated"},
        {"time_float": 21.5, "label": "09:30 PM", "temp": 27, "weather": "Night", "profile": "curfew_shutdown"},
        {"time_float": 22.0, "label": "10:00 PM", "temp": 26, "weather": "Night", "profile": "curfew_shutdown"},
    ]

    schedule = []
    for slot in slots:
        prof = slot["profile"]
        rooms = {rid: 0 for rid in ALL_LIBS_AND_ROOMS}

        if prof == "early":
            # E.g. 07:00 AM: 2 or 3 morning tutorial classes (like B101, B102, B105)
            chosen = ["B101", "B102", "B105"]
            for r in chosen:
                rooms[r] = rng.randint(24, 38)
        elif prof == "morning_peak":
            # 5 to 7 active rooms across classrooms and labs
            chosen_cr = rng.sample(LEFT_CLASSROOMS + RIGHT_CLASSROOMS, k=rng.randint(4, 6))
            chosen_labs = rng.sample(["LAB1", "LAB2", "LAB3"], k=rng.randint(1, 2))
            for r in chosen_cr:
                rooms[r] = rng.randint(32, 56)
            for l in chosen_labs:
                rooms[l] = rng.randint(25, 42)
        elif prof == "midday":
            chosen_cr = rng.sample(LEFT_CLASSROOMS + RIGHT_CLASSROOMS, k=4)
            chosen_labs = rng.sample(["LAB1", "LAB2", "LAB3"], k=1)
            for r in chosen_cr:
                rooms[r] = rng.randint(28, 50)
            for l in chosen_labs:
                rooms[l] = rng.randint(22, 38)
        elif prof == "afternoon_light":
            # 12:00 PM: 3 classes (great candidate for Block C natural daylight suggestion & wing consolidation)
            chosen = ["B101", "B102", "B108"]
            for r in chosen:
                rooms[r] = rng.randint(25, 42)
        elif prof == "lunch":
            # Only 1 lab or 1 class running during lunch
            rooms["LAB3"] = rng.randint(15, 25)
        elif prof == "afternoon":
            # 3 in one wing, 1 in the other wing -> triggers wing consolidation
            left_pick = rng.sample(LEFT_CLASSROOMS, k=3)
            right_pick = rng.sample(RIGHT_CLASSROOMS, k=1)
            for r in left_pick:
                rooms[r] = rng.randint(28, 46)
            for r in right_pick:
                rooms[r] = rng.randint(22, 34)
            rooms["LAB1"] = rng.randint(20, 35)
        elif prof == "late_afternoon":
            chosen = rng.sample(RIGHT_CLASSROOMS, k=2) + rng.sample(LEFT_CLASSROOMS, k=1)
            for r in chosen:
                rooms[r] = rng.randint(20, 35)
        elif prof == "evening":
            # 2 classes in Right Wing, 1 in Left Wing
            rooms["B106"] = rng.randint(24, 36)
            rooms["B108"] = rng.randint(22, 34)
            rooms["B103"] = rng.randint(18, 28)
        elif prof == "evening_isolated":
            # 1 isolated evening class in B108
            rooms["B108"] = rng.randint(20, 30)
        elif prof == "curfew_shutdown":
            # No classes after 9:30 PM / 10:00 PM -> complete building shutdown
            pass

        active_list = [f"{ROOM_META[k]['label']} ({v})" for k, v in rooms.items() if v > 0]
        summary_text = ", ".join(active_list) if active_list else (
            "Building Shutdown (No Classes After 9:30 PM)" if prof == "curfew_shutdown" else "All Rooms Vacant"
        )
        schedule.append({
            "time_float": slot["time_float"],
            "time_12h": slot["label"],
            "temperature": slot["temp"],
            "weather": slot["weather"],
            "rooms": rooms,
            "active_count": sum(1 for v in rooms.values() if v > 0),
            "total_students": sum(rooms.values()),
            "summary": summary_text
        })

    return {"schedule": schedule}


def evaluate_sandbox_state(payload: dict) -> dict:
    time_raw = payload.get("time", "07:30 PM")
    time_float, time_12h = parse_time_input(time_raw)
    temp_c = float(payload.get("temperature", 32.0))
    weather_cond = payload.get("weather", "Sunny / Daylight")
    rooms_input = payload.get("rooms", {})

    is_daylight = (7.0 <= time_float <= 17.5) and ("Night" not in weather_cond)
    is_working_hours = (7.0 <= time_float <= 17.5)
    is_afternoon_sun = (11.5 <= time_float <= 15.5) and is_daylight
    is_curfew_shutdown = (time_float >= 21.5) or (time_float < 6.0)

    # Clean occupancy map for all 11 spaces
    raw_occ = {}
    for rid in ALL_LIBS_AND_ROOMS:
        val = int(rooms_input.get(rid, 0) or 0)
        raw_occ[rid] = max(0, min(60, val))

    # =========================================================================
    # 1. UNMANAGED BASELINE STATE (Before Simulation)
    # =========================================================================
    # Deterministic pseudo-random pattern so empty rooms show natural unmanaged waste
    # (some vacant rooms have 2 lights ON / 2 OFF, some have all 4 ON, some are OFF)
    baseline_rooms = {}
    total_baseline_kw = 0.0

    waste_patterns = {
        "B101": [True, True, False, False],
        "B102": [True, False, True, False],
        "B103": [False, False, False, False],
        "B104": [True, True, True, True],
        "B105": [True, True, False, False],
        "B106": [False, False, False, False],
        "B107": [False, True, False, True],
        "B108": [True, True, True, True],
        "LAB1": [True, True, False, False],
        "LAB2": [False, False, False, False],
        "LAB3": [True, True, False, False],
    }

    for rid, meta in ROOM_META.items():
        occ = raw_occ[rid]
        is_occ = occ > 0
        max_ac_kw = 4.5 if meta["type"] == "lab" else 3.4

        if is_occ:
            b_lights = [True, True, True, True]
            b_ac_setpoint = "20°C"
            b_ac_kw = max_ac_kw
            b_light_kw = 0.60
            b_plug_kw = 1.20 if meta["type"] == "lab" else 0.20
        else:
            b_lights = waste_patterns.get(rid, [False, False, False, False])
            lit_count = sum(1 for x in b_lights if x)
            b_light_kw = round(lit_count * 0.15, 2)
            # In unmanaged baseline, rooms with 4 lights left on also often have AC left on at 22°C
            if lit_count == 4:
                b_ac_setpoint = "22°C (Left ON)"
                b_ac_kw = round(max_ac_kw * 0.75, 2)
            elif lit_count > 0:
                b_ac_setpoint = "24°C (Idle)"
                b_ac_kw = round(max_ac_kw * 0.35, 2)
            else:
                b_ac_setpoint = "OFF"
                b_ac_kw = 0.0
            b_plug_kw = 0.45 if meta["type"] == "lab" else 0.08

        b_total_kw = round(b_light_kw + b_ac_kw + b_plug_kw, 2)
        total_baseline_kw += b_total_kw

        baseline_rooms[rid] = {
            "id": rid,
            "label": meta["label"],
            "wing": meta["wing"],
            "type": meta["type"],
            "occupancy": occ,
            "is_occupied": is_occ,
            "lights": b_lights,
            "lights_on_count": sum(1 for x in b_lights if x),
            "ac_setpoint": b_ac_setpoint,
            "kw": b_total_kw,
            "relocated_from": None,
            "relocated_to": None
        }

    # Baseline common areas: all 4 lifts active, both corridors lit, all stairs lit
    baseline_common = {
        "lifts": {"L1": True, "L2": True, "L3": True, "L4": True},
        "left_corridor": True,
        "right_corridor": True,
        "main_stairs": True,
        "sw_stairs": True,
        "se_stairs": True,
        "faculty_lounge": True,
        "seminar_hall": False
    }
    baseline_lifts_kw = 8.8
    baseline_corridors_kw = 4.6
    total_baseline_kw = round(total_baseline_kw + baseline_lifts_kw + baseline_corridors_kw, 2)

    # =========================================================================
    # 2. SPATIAL CONSOLIDATION & RELOCATION ENGINE (Simulated State)
    # =========================================================================
    sim_occ = {rid: 0 for rid in ALL_LIBS_AND_ROOMS} if is_curfew_shutdown else dict(raw_occ)
    relocations = []

    left_active_crs = [r for r in LEFT_CLASSROOMS if sim_occ[r] > 0]
    right_active_crs = [r for r in RIGHT_CLASSROOMS if sim_occ[r] > 0]
    left_free_crs = [r for r in LEFT_CLASSROOMS if sim_occ[r] == 0]
    right_free_crs = [r for r in RIGHT_CLASSROOMS if sim_occ[r] == 0]

    left_labs_active = (sim_occ["LAB1"] > 0)
    right_labs_active = (sim_occ["LAB2"] > 0 or sim_occ["LAB3"] > 0)

    # Case A: 3 classes in Left Wing + 1 in Right Wing, OR >=1 in Left Wing + 1 isolated in far Right Wing (B106-B108)
    if is_curfew_shutdown:
        pass
    elif (
        len(right_active_crs) == 1
        and len(left_free_crs) >= 1
        and not right_labs_active
        and (len(left_active_crs) == 3 or (len(left_active_crs) >= 1 and right_active_crs[0] in ["B106", "B107", "B108"]))
    ):
        src = right_active_crs[0]
        dst = left_free_crs[0]
        moved_students = sim_occ[src]
        sim_occ[dst] = moved_students
        sim_occ[src] = 0
        relocations.append({
            "from_room": src,
            "from_label": ROOM_META[src]["label"],
            "to_room": dst,
            "to_label": ROOM_META[dst]["label"],
            "students": moved_students,
            "reason": f"Relocate {moved_students} students from {ROOM_META[src]['label']} (Right Wing) to {ROOM_META[dst]['label']} (Left Wing) to consolidate classes into the Left Wing and shut down the entire Right Wing."
        })

    # Case B: 3 classes in Right Wing + 1 in Left Wing, OR >=1 in Right Wing + 1 isolated in far Left Wing (B102-B104)
    elif (
        len(left_active_crs) == 1
        and len(right_free_crs) >= 1
        and not left_labs_active
        and (len(right_active_crs) == 3 or (len(right_active_crs) >= 1 and left_active_crs[0] in ["B102", "B103", "B104"]))
    ):
        src = left_active_crs[0]
        dst = right_free_crs[0]
        moved_students = sim_occ[src]
        sim_occ[dst] = moved_students
        sim_occ[src] = 0
        relocations.append({
            "from_room": src,
            "from_label": ROOM_META[src]["label"],
            "to_room": dst,
            "to_label": ROOM_META[dst]["label"],
            "students": moved_students,
            "reason": f"Relocate {moved_students} students from {ROOM_META[src]['label']} (Left Wing) to {ROOM_META[dst]['label']} (Right Wing) to consolidate classes into the Right Wing and shut down the entire Left Wing."
        })

    # Case C: Single isolated class on the entire floor in a far room (B103, B104, B107, B108)
    elif (len(left_active_crs) + len(right_active_crs)) == 1:
        only_cr = (left_active_crs + right_active_crs)[0]
        if only_cr in ["B103", "B104", "B107", "B108"]:
            # Move near Main Stairs: B101 if Left or no labs, or B105 if Right labs are active
            dst = "B105" if (right_labs_active and not left_labs_active) else "B101"
            if sim_occ[dst] == 0:
                moved_students = sim_occ[only_cr]
                sim_occ[dst] = moved_students
                sim_occ[only_cr] = 0
                relocations.append({
                    "from_room": only_cr,
                    "from_label": ROOM_META[only_cr]["label"],
                    "to_room": dst,
                    "to_label": ROOM_META[dst]["label"],
                    "students": moved_students,
                    "reason": f"Relocate isolated class ({moved_students} students) from far room {ROOM_META[only_cr]['label']} to {ROOM_META[dst]['label']} next to the Main Staircase to cut off far-wing corridor circuits."
                })

    # =========================================================================
    # 3. SIMULATED (OPTIMIZED) ROOM STATES
    # =========================================================================
    simulated_rooms = {}
    total_optimized_kw = 0.0
    reloc_from_map = {r["from_room"]: r["to_room"] for r in relocations}
    reloc_to_map = {r["to_room"]: r["from_room"] for r in relocations}

    for rid, meta in ROOM_META.items():
        occ = sim_occ[rid]
        is_occ = occ > 0

        if not is_occ:
            s_lights = [False, False, False, False]
            s_ac_setpoint = "OFF"
            s_kw = 0.0 if is_curfew_shutdown else 0.02
        else:
            # Smart Luminaire Control:
            # If daytime sunny & <= 25 students, or low headcount (<= 18), turn on 2 of 4 lights
            if (is_daylight and "Sunny" in weather_cond and occ <= 30) or occ <= 18:
                s_lights = [True, True, False, False]
                s_light_kw = 0.25
            else:
                s_lights = [True, True, True, True]
                s_light_kw = 0.50

            # Dynamic AC Setpoint by Temperature + Headcount
            if temp_c <= 24.0:
                s_ac_setpoint = "OFF (Fans)"
                s_ac_kw = 0.18
            elif temp_c >= 33.0 and occ >= 35:
                s_ac_setpoint = "23°C"
                s_ac_kw = 2.90 if meta["type"] == "lab" else 2.40
            elif temp_c >= 30.0 or occ >= 28:
                s_ac_setpoint = "24°C"
                s_ac_kw = 2.50 if meta["type"] == "lab" else 2.10
            elif temp_c >= 27.0:
                s_ac_setpoint = "26°C"
                s_ac_kw = 1.90 if meta["type"] == "lab" else 1.55
            else:
                s_ac_setpoint = "27°C"
                s_ac_kw = 1.40 if meta["type"] == "lab" else 1.15

            s_plug_kw = 0.85 if meta["type"] == "lab" else 0.12
            s_kw = round(s_light_kw + s_ac_kw + s_plug_kw, 2)

        total_optimized_kw += s_kw

        simulated_rooms[rid] = {
            "id": rid,
            "label": meta["label"],
            "wing": meta["wing"],
            "type": meta["type"],
            "occupancy": occ,
            "is_occupied": is_occ,
            "lights": s_lights,
            "lights_on_count": sum(1 for x in s_lights if x),
            "ac_setpoint": s_ac_setpoint,
            "kw": s_kw,
            "relocated_from": reloc_to_map.get(rid),
            "relocated_to": reloc_from_map.get(rid)
        }

    # =========================================================================
    # 4. WING POPULATIONS & DYNAMIC LIFT STAGING
    # =========================================================================
    left_rooms_active = [r for r in (LEFT_CLASSROOMS + ["LAB1"]) if sim_occ[r] > 0]
    right_rooms_active = [r for r in (RIGHT_CLASSROOMS + ["LAB2", "LAB3"]) if sim_occ[r] > 0]
    total_active_count = len(left_rooms_active) + len(right_rooms_active)

    left_people = sum(sim_occ[r] for r in (LEFT_CLASSROOMS + ["LAB1"]))
    right_people = sum(sim_occ[r] for r in (RIGHT_CLASSROOMS + ["LAB2", "LAB3"]))
    total_people = left_people + right_people

    lifts_state = {"L1": False, "L2": False, "L3": False, "L4": False}

    if is_curfew_shutdown:
        lift_summary = "0 Lifts Active (Complete Building Shutdown - All Breakers OFF)"
    elif total_active_count == 0:
        lift_summary = "0 Lifts Active (All 4 Lifts in Deep Sleep)"
    elif total_active_count <= 3:
        # 2 lifts active near the active wing(s)
        if left_people > 0 and right_people == 0:
            lifts_state["L1"] = True
            lifts_state["L2"] = True
            lift_summary = f"2 Lifts Active: L1 & L2 ON (Left Wing: {left_people} people) | L3 & L4 OFF"
        elif right_people > 0 and left_people == 0:
            lifts_state["L3"] = True
            lifts_state["L4"] = True
            lift_summary = f"2 Lifts Active: L3 & L4 ON (Right Wing: {right_people} people) | L1 & L2 OFF"
        else:
            lifts_state["L1"] = True
            lifts_state["L3"] = True
            lift_summary = f"2 Lifts Active: L1 (Left: {left_people}p) & L3 (Right: {right_people}p) ON | L2 & L4 OFF"
    elif total_active_count == 4:
        # If one wing is completely empty (0 people) after consolidation, only turn on the 2 lifts in the active wing
        if right_people == 0:
            lifts_state["L1"] = True
            lifts_state["L2"] = True
            lift_summary = f"2 Lifts Active: L1 & L2 ON (Left Wing Consolidated: {left_people}p) | Right Wing L3 & L4 OFF"
        elif left_people == 0:
            lifts_state["L3"] = True
            lifts_state["L4"] = True
            lift_summary = f"2 Lifts Active: L3 & L4 ON (Right Wing Consolidated: {right_people}p) | Left Wing L1 & L2 OFF"
        elif left_people >= right_people:
            lifts_state["L1"] = True
            lifts_state["L2"] = True
            lifts_state["L3"] = True
            lift_summary = f"3 Lifts Active: 2 Left (L1, L2 for {left_people}p) + 1 Right (L3 for {right_people}p) | L4 OFF"
        else:
            lifts_state["L1"] = True
            lifts_state["L3"] = True
            lifts_state["L4"] = True
            lift_summary = f"3 Lifts Active: 1 Left (L1 for {left_people}p) + 2 Right (L3, L4 for {right_people}p) | L2 OFF"
    else:
        # 5 or more active rooms -> all 4 lifts active
        lifts_state = {"L1": True, "L2": True, "L3": True, "L4": True}
        lift_summary = f"4 Lifts Active: L1, L2, L3, L4 ON (Peak Load: {total_active_count} rooms, {total_people} people)"

    active_lifts_count = sum(1 for v in lifts_state.values() if v)
    opt_lifts_kw = 0.0 if is_curfew_shutdown else round(active_lifts_count * 1.85 + (4 - active_lifts_count) * 0.10, 2)

    # =========================================================================
    # 5. CORRIDORS, STAIRS & FACULTY LOUNGE
    # =========================================================================
    left_corridor_on = len(left_rooms_active) > 0
    right_corridor_on = len(right_rooms_active) > 0

    main_stairs_on = total_active_count > 0
    sw_stairs_on = (sim_occ["B103"] > 0 or sim_occ["B104"] > 0)
    se_stairs_on = (sim_occ["B107"] > 0 or sim_occ["B108"] > 0 or sim_occ["LAB3"] > 0)
    faculty_lounge_on = is_working_hours and (total_active_count > 0)

    if is_curfew_shutdown:
        opt_corridors_kw = 0.0
        total_optimized_kw = 0.0
    else:
        opt_corridors_kw = (
            (1.4 if left_corridor_on else 0.0) +
            (1.4 if right_corridor_on else 0.0) +
            (0.45 if main_stairs_on else 0.05) +
            (0.35 if sw_stairs_on else 0.0) +
            (0.35 if se_stairs_on else 0.0) +
            (0.65 if faculty_lounge_on else 0.0)
        )
        total_optimized_kw = round(total_optimized_kw + opt_lifts_kw + opt_corridors_kw, 2)

    simulated_common = {
        "lifts": lifts_state,
        "left_corridor": left_corridor_on,
        "right_corridor": right_corridor_on,
        "main_stairs": main_stairs_on,
        "sw_stairs": sw_stairs_on,
        "se_stairs": se_stairs_on,
        "faculty_lounge": faculty_lounge_on,
        "seminar_hall": False
    }

    # =========================================================================
    # 6. SAVINGS & 3-PART NATURAL REPORT GENERATION
    # =========================================================================
    kw_saved = round(max(0.0, total_baseline_kw - total_optimized_kw), 2)
    savings_pct = round((kw_saved / max(0.1, total_baseline_kw)) * 100, 1)
    inr_saved = round(kw_saved * 9.00, 2)

    # Part 1 & 2: Suggestion + Actions Taken
    if is_curfew_shutdown:
        part1_suggestion = f"Campus Curfew ({time_12h}): No classes permitted after 09:30 PM. Complete Block B building shutdown enforced."
        part2_actions = "Main building breakers tripped OFF: all 11 classrooms & labs, all 4 lifts (L1-L4), corridors, staircases, and Faculty Lounge completely shut down (0.0 kW)."
    else:
        suggestion_parts = []
        if relocations:
            for rel in relocations:
                suggestion_parts.append(rel["reason"])
        else:
            if total_active_count == 0:
                suggestion_parts.append("No active classes scheduled. Maintain full floor deep-sleep lockdown.")
            elif left_people > 0 and right_people == 0:
                suggestion_parts.append(f"All {total_active_count} active sessions ({left_people} students) are already consolidated in the Left Wing. Keep Right Wing isolated.")
            elif right_people > 0 and left_people == 0:
                suggestion_parts.append(f"All {total_active_count} active sessions ({right_people} students) are already consolidated in the Right Wing. Keep Left Wing isolated.")
            else:
                suggestion_parts.append(f"Balanced multi-wing load ({left_people} in Left Wing, {right_people} in Right Wing). No cross-wing relocation required.")

        if is_afternoon_sun and 1 <= total_active_count <= 3:
            suggestion_parts.append(
                f"Daylight Advisory ({time_12h}): Shift the {total_active_count} active class(es) to Block C sun-facing studios to use natural sunlight and eliminate daytime artificial lighting load."
            )
        elif time_float >= 18.0 and 1 <= total_active_count <= 3:
            suggestion_parts.append(
                f"Evening Advisory ({time_12h}): Consolidate after-hours study groups to Ground Floor near Main Security Gate to power down upper floor risers."
            )

        part1_suggestion = " ".join(suggestion_parts)

        # Part 2: Actions Taken (Lifts, Lights, Corridors, ACs)
        active_lifts_list = [k for k, v in lifts_state.items() if v]
        off_lifts_list = [k for k, v in lifts_state.items() if not v]
        off_rooms_count = sum(1 for r in simulated_rooms.values() if not r["is_occupied"])
        half_lit_rooms = [r["label"] for r in simulated_rooms.values() if r["is_occupied"] and r["lights_on_count"] == 2]

        corridors_off = []
        if not left_corridor_on:
            corridors_off.append("Left Wing Corridor")
        if not right_corridor_on:
            corridors_off.append("Right Wing Corridor")
        if not sw_stairs_on:
            corridors_off.append("SW Stairs")
        if not se_stairs_on:
            corridors_off.append("SE Stairs")
        if not faculty_lounge_on:
            corridors_off.append("Faculty Lounge")

        actions_list = []
        if active_lifts_list:
            actions_list.append(f"Lifts {', '.join(active_lifts_list)} ON; {', '.join(off_lifts_list) if off_lifts_list else 'none'} switched OFF.")
        else:
            actions_list.append("All 4 Lifts (L1-L4) switched to Deep Sleep.")

        actions_list.append(f"Cut power to {off_rooms_count} vacant rooms.")
        if half_lit_rooms:
            actions_list.append(f"Dimmed {', '.join(half_lit_rooms)} to 2/4 luminaires (daylight/occupancy harvest).")
        if corridors_off:
            actions_list.append(f"Isolated {', '.join(corridors_off)}.")

        part2_actions = " ".join(actions_list)

    # Part 3: Energy & Financial Savings
    part3_savings = (
        f"Power reduced from {total_baseline_kw} kW to {total_optimized_kw} kW "
        f"(Saved {kw_saved} kW / {savings_pct}% reduction | INR {inr_saved}/hr saved)."
    )

    formatted_message = (
        f"[GridSense Simulation // JIT Block B @ {time_12h}]\n"
        f"1. Suggestion: {part1_suggestion}\n"
        f"2. Actions Taken: {part2_actions}\n"
        f"3. Energy Saved: {part3_savings}"
    )

    return {
        "time_float": time_float,
        "time_12h": time_12h,
        "temperature": temp_c,
        "weather": weather_cond,
        "active_classes": total_active_count,
        "left_wing_people": left_people,
        "right_wing_people": right_people,
        "total_people": total_people,
        "total_baseline_kw": total_baseline_kw,
        "total_optimized_kw": total_optimized_kw,
        "kw_saved": kw_saved,
        "savings_percentage": savings_pct,
        "inr_per_hour_saved": inr_saved,
        "elevator_mode": lift_summary,
        "relocations": relocations,
        "baseline_state": {
            "rooms": baseline_rooms,
            "common": baseline_common,
            "total_kw": total_baseline_kw
        },
        "simulated_state": {
            "rooms": simulated_rooms,
            "common": simulated_common,
            "total_kw": total_optimized_kw
        },
        "report": {
            "suggestion": part1_suggestion,
            "actions_taken": part2_actions,
            "energy_saved": part3_savings,
            "formatted_message": formatted_message
        }
    }
