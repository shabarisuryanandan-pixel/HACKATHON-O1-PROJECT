"""
GridSense Simulation Engine: 8 Classrooms Per Floor (B101 to B108 & B201 to B208),
CAD Architectural layout with desks, luminaire fixtures, 4-lift elevator bank,
staircase, 3-zone corridor relays, and Telegram mobile alerts.
"""

def evaluate_sandbox_state(payload):
    time_str = payload.get("time", "19:30")
    temp_c = float(payload.get("temperature", 32.0))
    weather_cond = payload.get("weather", "Sunny / Daylight")
    selected_floor = int(payload.get("floor", 1))
    rooms_input = payload.get("rooms", {}) # e.g. {"B101": 25, "B108": 20, ...}

    hour = int(time_str.split(":")[0])
    minute = int(time_str.split(":")[1])
    time_float = hour + minute / 60.0

    is_daylight = (7.0 <= time_float <= 17.5) and ("Night" not in weather_cond)
    lux_level = 650 if (is_daylight and "Sunny" in weather_cond) else (280 if is_daylight else 0)

    # 8 Classrooms per floor:
    # North Wing: Bx01, Bx02, Bx03, Bx04
    # South Wing: Bx05, Bx06, Bx07, Bx08
    # Entrance/Stairs/Lifts are located at the West end (x01 / x05)
    # Far end of the 80m corridor is at the East end (x04 / x08)

    floor_prefix = f"B{selected_floor}0"
    all_rooms = {}
    for i in range(1, 9):
        r_id = f"B{selected_floor}0{i}" if i < 10 else f"B{selected_floor}{i}"
        wing = "North Wing" if i <= 4 else "South Wing"
        corridor_segment = 1 if i in [1, 5] else (2 if i in [2, 6] else 3)
        near_entrance = (i in [1, 5, 2])
        all_rooms[r_id] = {
            "id": r_id,
            "name": f"Lecture Room {r_id}",
            "wing": wing,
            "corridor_segment": corridor_segment,
            "near_entrance": near_entrance,
            "capacity": 60,
            "orientation": "North" if i <= 4 else "South"
        }

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

        # Baseline: If daytime or occupied, full lights & AC
        if is_occupied or (time_float < 17.5):
            base_light_kw = 0.60
            base_ac_kw = 3.60
            base_room_kw = 4.20
        elif time_float >= 17.5 and r_id in [f"B{selected_floor}01", f"B{selected_floor}08"]:
            base_room_kw = 4.20 # Left running blindly after hours
        else:
            base_room_kw = 0.15

        total_baseline_kw += base_room_kw

        # GridSense Optimized
        if not is_occupied:
            opt_light_state = "OFF"
            opt_ac_mode = "STANDBY"
            opt_ac_setpoint = "OFF"
            opt_room_kw = 0.02
        else:
            if is_daylight and lux_level > 300 and meta["orientation"] == "North":
                opt_light_state = "WINDOW ROWS LOCKED OFF"
                opt_light_kw = 0.25
            else:
                opt_light_state = "ON"
                opt_light_kw = 0.50

            if temp_c < 24.0:
                opt_ac_mode = "VENTILATION (Fans)"
                opt_ac_setpoint = "OFF"
                opt_ac_kw = 0.20
            elif occ < 25:
                opt_ac_mode = "ECO ADAPTIVE"
                opt_ac_setpoint = "26°C"
                opt_ac_kw = 1.80
            else:
                opt_ac_mode = "DYNAMIC COOLING"
                opt_ac_setpoint = "24°C"
                opt_ac_kw = 2.60

            opt_room_kw = round(opt_light_kw + opt_ac_kw + 0.15, 2)

        total_optimized_kw += opt_room_kw

        room_results[r_id] = {
            "id": r_id,
            "name": meta["name"],
            "wing": meta["wing"],
            "corridor_segment": meta["corridor_segment"],
            "occupancy": occ,
            "is_occupied": is_occupied,
            "lighting_glow": is_occupied,
            "lighting_state": opt_light_state,
            "ac_mode": opt_ac_mode,
            "ac_setpoint": opt_ac_setpoint,
            "baseline_kw": base_room_kw,
            "optimized_kw": opt_room_kw,
            "near_entrance": meta["near_entrance"]
        }

    # Spatial Consolidation check:
    # If a class is sitting in far rooms (x04, x08, x03, x07) while entrance rooms (x01, x05) are empty:
    far_rooms_occupied = [r for r in [f"B{selected_floor}04", f"B{selected_floor}08", f"B{selected_floor}03", f"B{selected_floor}07"] if room_results[r]["is_occupied"]]
    entrance_rooms_free = [r for r in [f"B{selected_floor}01", f"B{selected_floor}05", f"B{selected_floor}02", f"B{selected_floor}06"] if not room_results[r]["is_occupied"]]

    if far_rooms_occupied and entrance_rooms_free:
        source_r = far_rooms_occupied[0]
        target_r = entrance_rooms_free[0]
        relocation_suggestions.append({
            "from_room": source_r,
            "to_room": target_r,
            "students": room_results[source_r]["occupancy"],
            "reason": f"Isolated class in {source_r} (Far End). Relocate to {target_r} near the staircase/entrance to completely shut down 40m of corridor lighting and far-wing circuits.",
            "corridor_saved_kw": 2.2,
            "inr_per_hour_saved": 19.80
        })

    # Corridor zone states
    z1_active = room_results[f"B{selected_floor}01"]["is_occupied"] or room_results[f"B{selected_floor}05"]["is_occupied"]
    z2_active = room_results[f"B{selected_floor}02"]["is_occupied"] or room_results[f"B{selected_floor}06"]["is_occupied"]
    z3_active = (room_results[f"B{selected_floor}03"]["is_occupied"] or room_results[f"B{selected_floor}07"]["is_occupied"] or
                 room_results[f"B{selected_floor}04"]["is_occupied"] or room_results[f"B{selected_floor}08"]["is_occupied"])

    corridor_state = {
        "zone1_entrance": "LIT" if z1_active else "DARK",
        "zone2_mid": "LIT" if z2_active else "DARK",
        "zone3_far": "LIT" if z3_active else "DARK"
    }

    base_corridor_kw = 4.8
    opt_corridor_kw = (1.6 if z1_active else 0.0) + (1.6 if z2_active else 0.0) + (1.6 if z3_active else 0.0)
    total_baseline_kw += base_corridor_kw
    total_optimized_kw += round(opt_corridor_kw, 2)

    # Elevator dispatch
    if time_float >= 17.5 or active_classes_count <= 2:
        elev_state = "2 Lifts Active (Mandatory Safety Minimum) | 2 Lifts Deep Sleep"
        base_elev_kw = 4.8
        opt_elev_kw = 1.4
    else:
        elev_state = "4 Lifts Active (Full Peak Schedule)"
        base_elev_kw = 9.5
        opt_elev_kw = 7.2

    total_baseline_kw += base_elev_kw
    total_optimized_kw += opt_elev_kw

    kw_saved = max(0.0, total_baseline_kw - total_optimized_kw)
    savings_pct = round((kw_saved / (total_baseline_kw + 0.001)) * 100, 1)
    inr_saved = round(kw_saved * 9.00, 2)

    return {
        "time": time_str,
        "temperature": temp_c,
        "weather": weather_cond,
        "floor": selected_floor,
        "active_classes": active_classes_count,
        "total_baseline_kw": round(total_baseline_kw, 2),
        "total_optimized_kw": round(total_optimized_kw, 2),
        "kw_saved": round(kw_saved, 2),
        "savings_percentage": savings_pct,
        "inr_per_hour_saved": inr_saved,
        "elevator_mode": elev_state,
        "corridor_state": corridor_state,
        "relocations": relocation_suggestions,
        "rooms": room_results
    }
