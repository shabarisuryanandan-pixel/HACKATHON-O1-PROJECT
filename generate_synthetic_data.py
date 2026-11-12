"""
GridSense: 7-Day Synthetic Telemetry & Waste Index Scoring (WIS) Engine
Generates realistic 15-minute interval time-series data for Monday through Sunday
(672 steps) across all campus zones, modeling baseline waste vs GridSense interventions.
"""

import json
import math
import random
from datetime import datetime, timedelta
from campus_blueprint import CAMPUS_BLUEPRINT, CAMPUS_METADATA

def get_day_type(day_idx):
    # 0 = Monday, ..., 4 = Friday, 5 = Saturday, 6 = Sunday
    if day_idx < 5:
        return "weekday"
    elif day_idx == 5:
        return "saturday"
    else:
        return "sunday"

def get_ambient_weather(hour, minute):
    time_float = hour + minute / 60.0
    # Temperature model: Low of 22C at 05:00, Peak of 35C at 14:30
    temp = 28.5 + 6.5 * math.sin((time_float - 9.0) * math.pi / 12.0)
    # Daylight lux model: 0 before 06:00 and after 18:30, peak 750 lux at 12:00
    if 6.0 <= time_float <= 18.5:
        lux = 750.0 * math.sin((time_float - 6.0) * math.pi / 12.5)
    else:
        lux = 0.0
    return round(temp, 1), round(max(0.0, lux), 1)

def simulate_zone_step(zone_id, zone_type, day_type, hour, minute, temp, lux):
    time_float = hour + minute / 60.0
    is_core_academic = (8.5 <= time_float <= 16.5) and (day_type == "weekday")
    is_after_hours = (16.5 < time_float <= 22.0) and (day_type == "weekday")
    is_late_night = (time_float > 22.0 or time_float < 6.0)

    # 1. Occupancy Simulation
    if is_core_academic:
        base_occupants = random.randint(35, 58)
        wifi_clients = base_occupants + random.randint(5, 15) # laptops + phones
        erp_scheduled = True
    elif is_after_hours:
        # After hours: few students or empty, but baseline leaves things running!
        if zone_id in ["B101", "C_LAB_1", "A_SEM_1"]:
            base_occupants = random.randint(3, 8)
            wifi_clients = base_occupants + random.randint(1, 4)
            erp_scheduled = (time_float <= 18.0) # Unofficial after 18:00
        else:
            base_occupants = 0
            wifi_clients = 0
            erp_scheduled = False
    elif day_type == "saturday" and 9.0 <= time_float <= 13.0:
        base_occupants = random.randint(10, 25)
        wifi_clients = base_occupants + 4
        erp_scheduled = True
    else:
        base_occupants = 0
        wifi_clients = 0
        erp_scheduled = False

    # 2. Baseline Power Draw (WITHOUT GridSense) vs GridSense Optimized Draw
    if zone_type == "classroom":
        # Baseline: 2 ACs (4 kW) + all lights (0.6 kW) + smartboard (0.3 kW) = ~4.9 kW
        baseline_kw = 4.9 if (is_core_academic or (is_after_hours and random.random() < 0.65)) else 0.4
        
        # GridSense Optimized:
        if base_occupants == 0 and not erp_scheduled:
            gridsense_kw = 0.02 # Standby only
        else:
            # Module A1: If high lux and morning, Zone A lights off (-0.3 kW)
            lighting_kw = 0.15 if (lux > 300 and 8.5 <= time_float <= 13.0) else 0.5
            # Module A2: Climate scaled AC (26C on partial, 24C on full, off on mild)
            if base_occupants < 25 and temp < 28:
                ac_kw = 1.6 # 1 AC at 26C + fans
            else:
                ac_kw = 2.8 # 2 ACs optimized
            # Module A4: AV sleep
            av_kw = 0.25 if base_occupants > 10 else 0.01
            gridsense_kw = round(lighting_kw + ac_kw + av_kw, 2)

    elif zone_type == "lab":
        # 60 PCs (6 kW active, 0.12 kW sleep) + 3 ACs (6 kW) + lights (0.8 kW)
        if is_core_academic:
            baseline_kw = 12.8
            gridsense_kw = 10.5 # Optimized fans + PC sleep
        elif is_after_hours:
            # Baseline keeps 60 PCs idling at 100W each + AC running!
            baseline_kw = 10.2
            # Module C: GridSense forces S3 sleep (2W) + shuts off AC
            gridsense_kw = 0.18 # 60 * 2W + minimal baseline
        else:
            baseline_kw = 3.5 # Many PCs left on overnight
            gridsense_kw = 0.15

    elif zone_type == "elevator":
        # 4 lifts. Running motor ~8 kW, standby ~0.6 kW each
        if is_core_academic:
            baseline_kw = 12.0
            gridsense_kw = 9.5
        elif is_after_hours or is_late_night:
            baseline_kw = 4.8 # All 4 lifts idle drawing 4 * 0.6 = 2.4 kW + occasional trips
            # Module D: Exactly 2 lifts in deep sleep, 2 lifts active (mandatory safety floor)
            gridsense_kw = 1.4 # 2 * 0.6 + rare trip
        else:
            baseline_kw = 3.2
            gridsense_kw = 1.3

    elif zone_type == "water_cooler":
        # 1.5 kW compressor
        if is_late_night or (day_type == "sunday"):
            baseline_kw = 1.2 # Constantly chilling at 3 AM!
            gridsense_kw = 0.0 # Module F: Interlocked timer cuts off
        else:
            baseline_kw = 1.2
            gridsense_kw = 1.2

    else:
        # Default zone
        baseline_kw = 2.0 if is_core_academic else 1.2
        gridsense_kw = 1.5 if is_core_academic else 0.1

    # 3. Calculate GridSense Waste Index Score (WIS: 0 to 100)
    # Sub-scores (0 to 10 scale)
    occ_score = 10.0 if (base_occupants == 0 and not erp_scheduled) else max(0.0, 10.0 - (base_occupants / 5.0))
    climate_score = min(10.0, max(0.0, (temp - 24.0) * 0.8))
    energy_score = min(10.0, max(0.0, (baseline_kw / (gridsense_kw + 0.1)) * 2.0))
    sched_score = 10.0 if is_late_night else (6.0 if is_after_hours else 1.0)

    # Weighted master WIS formula:
    # WIS = (O * 0.60 + C * 0.23 + E * 0.21 + S * 0.12) / 1.16 * 10
    raw_wis = (occ_score * 0.60) + (climate_score * 0.23) + (energy_score * 0.21) + (sched_score * 0.12)
    wis = int(min(100, max(0, round((raw_wis / 1.16) * 10))))

    # Safety veto: if scheduled, reduce WIS by 20 points
    if erp_scheduled and wis > 25:
        wis = max(10, wis - 20)

    # Saved kWh during this 15 min (0.25 hr) interval
    saved_kwh = max(0.0, (baseline_kw - gridsense_kw) * 0.25)

    return {
        "occupants": base_occupants,
        "wifi_clients": wifi_clients,
        "erp_scheduled": erp_scheduled,
        "temp_c": temp,
        "lux": lux,
        "baseline_kw": round(baseline_kw, 2),
        "gridsense_kw": round(gridsense_kw, 2),
        "saved_kwh": round(saved_kwh, 3),
        "wis": wis
    }

def generate_7_day_telemetry():
    telemetry = []
    start_date = datetime(2026, 11, 16, 0, 0) # Monday 00:00
    
    sample_zones = [
        {"id": "B101", "name": "Lecture Room B101 (East-Facing)", "type": "classroom", "block": "Block B"},
        {"id": "B201", "name": "Lecture Room B201 (West-Facing)", "type": "classroom", "block": "Block B"},
        {"id": "C_LAB_1", "name": "Advanced Computing Lab 1 (CSE)", "type": "lab", "block": "Block C"},
        {"id": "A_SEM_1", "name": "Seminar Hall 1", "type": "classroom", "block": "Block A"},
        {"id": "ELEV_BANK_B", "name": "4-Lift Elevator Bank", "type": "elevator", "block": "Block B"},
        {"id": "WC_B1", "name": "Block B Water Cooler", "type": "water_cooler", "block": "Block B"}
    ]

    total_kwh_baseline = 0.0
    total_kwh_gridsense = 0.0

    print("Generating 7 days of 15-minute telemetry (672 intervals)...")
    for step in range(672):
        curr_time = start_date + timedelta(minutes=step * 15)
        day_idx = curr_time.weekday() # 0 = Mon, 6 = Sun
        day_type = get_day_type(day_idx)
        hour = curr_time.hour
        minute = curr_time.minute
        temp, lux = get_ambient_weather(hour, minute)

        step_data = {
            "timestamp": curr_time.strftime("%Y-%m-%d %H:%M"),
            "day": curr_time.strftime("%A"),
            "day_type": day_type,
            "temp_c": temp,
            "lux": lux,
            "zones": {}
        }

        for z in sample_zones:
            z_res = simulate_zone_step(z["id"], z["type"], day_type, hour, minute, temp, lux)
            step_data["zones"][z["id"]] = z_res
            total_kwh_baseline += z_res["baseline_kw"] * 0.25
            total_kwh_gridsense += z_res["gridsense_kw"] * 0.25

        telemetry.append(step_data)

    total_saved_kwh = total_kwh_baseline - total_kwh_gridsense
    total_saved_inr = total_saved_kwh * CAMPUS_METADATA["grid_tariff_inr_per_kwh"]

    summary = {
        "institution": CAMPUS_METADATA["institution_name"],
        "intervals_generated": len(telemetry),
        "days_modeled": 7,
        "total_baseline_kwh": round(total_kwh_baseline, 1),
        "total_gridsense_kwh": round(total_kwh_gridsense, 1),
        "total_saved_kwh": round(total_saved_kwh, 1),
        "savings_percentage": round((total_saved_kwh / total_kwh_baseline) * 100, 1),
        "total_saved_inr": round(total_saved_inr, 2)
    }

    with open("synthetic_telemetry.json", "w") as f:
        json.dump({"summary": summary, "telemetry": telemetry}, f, indent=2)

    print("Telemetry generation complete.")
    print(f"Total 7-day Baseline: {summary['total_baseline_kwh']} kWh")
    print(f"Total 7-day GridSense: {summary['total_gridsense_kwh']} kWh")
    print(f"Saved: {summary['total_saved_kwh']} kWh ({summary['savings_percentage']}%)")
    print(f"Weekly Financial Savings: INR {summary['total_saved_inr']}")

if __name__ == "__main__":
    generate_7_day_telemetry()
