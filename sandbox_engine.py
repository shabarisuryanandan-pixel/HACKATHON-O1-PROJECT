"""
GridSense Simulation Engine: Evaluates interactive sandbox inputs
(Time of Day, Outdoor Weather, Zone Occupancies) and computes dynamic
lighting states, adaptive AC setpoints, spatial class relocations,
before/after energy metrics, and Telegram mobile alerts.
"""

def evaluate_sandbox_state(payload):
    time_str = payload.get("time", "19:00")
    temp_c = float(payload.get("temperature", 32.0))
    weather_cond = payload.get("weather", "Sunny / Daylight") # Sunny, Overcast, Night
    rooms_input = payload.get("rooms", {}) # {"B101": 25, "B104": 15, "A_SEM1": 0, ...}

    hour = int(time_str.split(":")[0])
    minute = int(time_str.split(":")[1])
    time_float = hour + minute / 60.0

    # 1. Daylight availability based on time & weather
    is_daylight = (7.0 <= time_float <= 17.5) and ("Night" not in weather_cond)
    lux_level = 650 if (is_daylight and "Sunny" in weather_cond) else (280 if is_daylight else 0)

    # Room registry for simulation
    all_rooms = {
        "A_SEM1": {"name": "Block A // Seminar Hall 1", "block": "Block A", "floor": 1, "capacity": 150, "orientation": "North", "near_entrance": True},
        "A_SEM2": {"name": "Block A // Seminar Hall 2", "block": "Block A", "floor": 2, "capacity": 120, "orientation": "North", "near_entrance": False},
        "B101": {"name": "Block B // Room B101", "block": "Block B", "floor": 1, "capacity": 60, "orientation": "East", "near_entrance": True},
        "B102": {"name": "Block B // Room B102", "block": "Block B", "floor": 1, "capacity": 60, "orientation": "North", "near_entrance": True},
        "B103": {"name": "Block B // Room B103", "block": "Block B", "floor": 1, "capacity": 60, "orientation": "West", "near_entrance": False},
        "B104": {"name": "Block B // Room B104 (Far End)", "block": "Block B", "floor": 1, "capacity": 60, "orientation": "West", "near_entrance": False},
        "B201": {"name": "Block B // Room B201", "block": "Block B", "floor": 2, "capacity": 60, "orientation": "East", "near_entrance": True},
        "B204": {"name": "Block B // Room B204 (Far End)", "block": "Block B", "floor": 2, "capacity": 60, "orientation": "West", "near_entrance": False}
    }

    # Evaluate each room state
    room_results = {}
    total_baseline_kw = 0.0
    total_optimized_kw = 0.0
    active_classes_count = 0

    relocation_suggestions = []

    for r_id, meta in all_rooms.items():
        occ = int(rooms_input.get(r_id, 0))
        is_occupied = (occ > 0)
        if is_occupied:
            active_classes_count += 1

        # Traditional Baseline: If scheduled or after hours, full lights & fixed 20C AC
        if is_occupied or (time_float < 17.5) or (time_float > 17.5 and r_id in ["B101", "B104", "A_SEM1"]):
            base_light_kw = 0.60
            base_ac_kw = 4.0 if "SEM" in r_id else 3.2
            base_av_kw = 0.35
            base_room_kw = round(base_light_kw + base_ac_kw + base_av_kw, 2)
        else:
            base_room_kw = 0.15 # Parasitic standby

        total_baseline_kw += base_room_kw

        # GridSense Optimized:
        if not is_occupied:
            # 100% automated kill
            opt_light_state = "OFF"
            opt_light_kw = 0.0
            opt_ac_mode = "STANDBY / OFF"
            opt_ac_setpoint = "OFF"
            opt_ac_kw = 0.02
            opt_av_state = "SLEEP (<3W)"
            opt_room_kw = 0.02
        else:
            # Module A1: Daylight-linked lighting
            if is_daylight and lux_level > 300 and meta["orientation"] in ["East", "North"]:
                opt_light_state = "50% (Window Rows Locked OFF)"
                opt_light_kw = 0.25
            else:
                opt_light_state = "ON (Full)"
                opt_light_kw = 0.50

            # Module A2: Adaptive AC
            if temp_c < 24.0:
                opt_ac_mode = "VENTILATION ONLY (Fans Active)"
                opt_ac_setpoint = "OFF"
                opt_ac_kw = 0.20 # Fans only
            elif occ < 25:
                opt_ac_mode = "ECO ADAPTIVE (Setpoint: 26°C)"
                opt_ac_setpoint = "26°C"
                opt_ac_kw = 1.80
            else:
                opt_ac_mode = "DYNAMIC COOLING (Setpoint: 24°C)"
                opt_ac_setpoint = "24°C"
                opt_ac_kw = 2.60

            opt_av_state = "ACTIVE"
            opt_room_kw = round(opt_light_kw + opt_ac_kw + 0.25, 2)

        total_optimized_kw += opt_room_kw

        room_results[r_id] = {
            "id": r_id,
            "name": meta["name"],
            "block": meta["block"],
            "floor": meta["floor"],
            "occupancy": occ,
            "is_occupied": is_occupied,
            "lighting_state": opt_light_state,
            "lighting_glow": (opt_light_state != "OFF"),
            "ac_mode": opt_ac_mode,
            "ac_setpoint": opt_ac_setpoint,
            "av_state": opt_av_state,
            "baseline_kw": base_room_kw,
            "optimized_kw": opt_room_kw,
            "near_entrance": meta["near_entrance"]
        }

    # Module B: Spatial Consolidation Detection
    # If a class is isolated in a far-end room (B104 or B204) while near-entrance rooms (B101, B102) are vacant:
    if room_results["B104"]["is_occupied"] and not room_results["B101"]["is_occupied"]:
        relocation_suggestions.append({
            "from_room": "B104 (Far End Corridor)",
            "to_room": "B101 (Near Staircase)",
            "students": room_results["B104"]["occupancy"],
            "reason": "Consolidate to entrance. Allows de-energizing 40m of corridor lighting & Block B Far Wing.",
            "corridor_saved_kw": 1.8,
            "inr_per_hour_saved": 16.20
        })

    if room_results["B204"]["is_occupied"] and not room_results["B102"]["is_occupied"]:
        relocation_suggestions.append({
            "from_room": "B204 (Floor 2 Far End)",
            "to_room": "B102 (Floor 1 Entrance)",
            "students": room_results["B204"]["occupancy"],
            "reason": "Move Floor 2 class to Floor 1. Allows complete power shutdown of Floor 2 wing & elevator call demand.",
            "corridor_saved_kw": 2.4,
            "inr_per_hour_saved": 21.60
        })

    # Corridor and Elevator logic
    # Corridors: 3 zones per floor
    b_floor1_far_lit = room_results["B103"]["is_occupied"] or room_results["B104"]["is_occupied"]
    b_floor2_far_lit = room_results["B204"]["is_occupied"]

    corridor_state = {
        "floor1_zone1_entrance": "ON" if (room_results["B101"]["is_occupied"] or room_results["B102"]["is_occupied"]) else "OFF",
        "floor1_zone2_mid": "ON" if room_results["B103"]["is_occupied"] else "OFF",
        "floor1_zone3_far": "ON" if room_results["B104"]["is_occupied"] else "OFF",
        "floor2_wing": "ON" if (room_results["B201"]["is_occupied"] or room_results["B204"]["is_occupied"]) else "OFF"
    }

    # Add corridor baseline vs optimized
    base_corridor_kw = 4.2
    opt_corridor_kw = 0.6 if (not b_floor1_far_lit and not b_floor2_far_lit) else 2.1
    total_baseline_kw += base_corridor_kw
    total_optimized_kw += opt_corridor_kw

    # Elevator dynamic staging
    if time_float >= 17.5 or active_classes_count <= 2:
        elevator_mode = "2 Lifts Active (Mandatory Safety Floor) | 2 Lifts Deep Sleep"
        base_elev_kw = 4.8
        opt_elev_kw = 1.4
    else:
        elevator_mode = "4 Lifts Active (Rush Schedule)"
        base_elev_kw = 9.5
        opt_elev_kw = 7.2

    total_baseline_kw += base_elev_kw
    total_optimized_kw += opt_elev_kw

    kw_saved = max(0.0, total_baseline_kw - total_optimized_kw)
    savings_pct = round((kw_saved / (total_baseline_kw + 0.001)) * 100, 1)
    inr_per_hour_saved = round(kw_saved * 9.00, 2)

    return {
        "time": time_str,
        "temperature": temp_c,
        "weather": weather_cond,
        "lux_level": lux_level,
        "active_classes": active_classes_count,
        "total_baseline_kw": round(total_baseline_kw, 2),
        "total_optimized_kw": round(total_optimized_kw, 2),
        "kw_saved": round(kw_saved, 2),
        "savings_percentage": savings_pct,
        "inr_per_hour_saved": inr_per_hour_saved,
        "elevator_mode": elevator_mode,
        "corridor_state": corridor_state,
        "relocations": relocation_suggestions,
        "rooms": room_results
    }
