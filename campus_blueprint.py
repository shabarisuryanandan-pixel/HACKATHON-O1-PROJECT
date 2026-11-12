"""
GridSense: Campus Blueprint Architecture for Jain Institute of Technology (JIT)
Models the physical campus hierarchy, base electrical loads, and telemetry nodes
tailored to all 8 GridSense optimization modules (A through H).
"""

CAMPUS_METADATA = {
    "institution_name": "Jain Institute of Technology",
    "location": "Karnataka, India",
    "grid_tariff_inr_per_kwh": 9.00,
    "peak_tariff_multiplier": 1.30,  # 30% surcharge between 18:00 - 22:00
    "contracted_max_demand_kva": 250,
    "building_blocks": ["Block A", "Block B", "Block C", "Hostel Block", "Campus Infrastructure"]
}

# Physical blueprint mapped directly to the 8 solution modules
CAMPUS_BLUEPRINT = {
    "Block A": {
        "description": "Administrative offices, faculty chambers, executive seminar halls, and main auditorium",
        "floors": 4,
        "zones": [
            {
                "id": "A_SEM_1",
                "name": "Seminar Hall 1",
                "floor": 1,
                "type": "seminar_hall",
                "capacity": 150,
                "appliances": {"ac_units": 4, "ac_tonnage_each": 2.0, "lights": 24, "projector": 1, "smartboard": 1},
                "solution_mapping": ["A", "B"]
            },
            {
                "id": "A_SEM_2",
                "name": "Seminar Hall 2",
                "floor": 2,
                "type": "seminar_hall",
                "capacity": 120,
                "appliances": {"ac_units": 3, "ac_tonnage_each": 2.0, "lights": 18, "projector": 1, "smartboard": 1},
                "solution_mapping": ["A", "B"]
            },
            {
                "id": "A_FAC_W1",
                "name": "Faculty Cabins Wing 1",
                "floor": 3,
                "type": "faculty_cabins",
                "capacity": 30,
                "appliances": {"split_acs": 6, "ac_tonnage_each": 1.5, "lights": 30, "fans": 15},
                "solution_mapping": ["B"]
            },
            {
                "id": "A_CORRIDOR",
                "name": "Block A Arterial Corridor",
                "floor": "All",
                "type": "corridor",
                "length_meters": 75,
                "lighting_zones": 3,
                "total_lights": 36,
                "solution_mapping": ["B"]
            }
        ],
        "water_coolers": [
            {"id": "WC_A1", "floor": 1, "capacity_liters": 100, "compressor_kw": 1.5, "solution_mapping": ["F"]},
            {"id": "WC_A2", "floor": 3, "capacity_liters": 100, "compressor_kw": 1.5, "solution_mapping": ["F"]}
        ]
    },
    
    "Block B": {
        "description": "First and Second-year lecture halls, standard classrooms, central staircase, and main elevator banks",
        "floors": 4,
        "zones": [
            # 8 representative classrooms covering Daylight Autonomy variants
            {
                "id": "B101", "name": "Lecture Room B101 (East-Facing)", "floor": 1, "capacity": 60,
                "daylight_orientation": "East", "window_wall_ratio": 0.45,
                "lighting_circuits": {"zone_a_window": 6, "zone_b_interior": 6},
                "appliances": {"ac_units": 2, "ac_tonnage_each": 2.0, "fans": 6, "smartboard": 1},
                "solution_mapping": ["A", "B"]
            },
            {
                "id": "B102", "name": "Lecture Room B102 (North-Facing)", "floor": 1, "capacity": 60,
                "daylight_orientation": "North", "window_wall_ratio": 0.40,
                "lighting_circuits": {"zone_a_window": 6, "zone_b_interior": 6},
                "appliances": {"ac_units": 2, "ac_tonnage_each": 2.0, "fans": 6, "smartboard": 1},
                "solution_mapping": ["A", "B"]
            },
            {
                "id": "B201", "name": "Lecture Room B201 (West-Facing)", "floor": 2, "capacity": 60,
                "daylight_orientation": "West", "window_wall_ratio": 0.30,
                "lighting_circuits": {"zone_a_window": 6, "zone_b_interior": 6},
                "appliances": {"ac_units": 2, "ac_tonnage_each": 2.0, "fans": 6, "smartboard": 1},
                "solution_mapping": ["A", "B"]
            },
            {
                "id": "B202", "name": "Lecture Room B202 (Far-Hallway)", "floor": 2, "capacity": 60,
                "daylight_orientation": "South", "window_wall_ratio": 0.25,
                "lighting_circuits": {"zone_a_window": 6, "zone_b_interior": 6},
                "appliances": {"ac_units": 2, "ac_tonnage_each": 2.0, "fans": 6, "smartboard": 1},
                "solution_mapping": ["A", "B"]
            },
            {
                "id": "B_CORRIDOR",
                "name": "Block B Central Corridor",
                "floor": "All",
                "type": "corridor",
                "length_meters": 80,
                "lighting_zones": 3,
                "total_lights": 48,
                "solution_mapping": ["B"]
            }
        ],
        "elevator_bank": {
            "id": "ELEV_BANK_B",
            "total_cars": 4,
            "car_rating_motor_kw": 8.0,
            "standby_parasitic_kw": 0.60,
            "mandatory_safety_floor": 2, # Strict minimum 2 cars active
            "solution_mapping": ["D"]
        },
        "water_coolers": [
            {"id": "WC_B1", "floor": 1, "capacity_liters": 150, "compressor_kw": 1.5, "solution_mapping": ["F"]},
            {"id": "WC_B2", "floor": 2, "capacity_liters": 150, "compressor_kw": 1.5, "solution_mapping": ["F"]},
            {"id": "WC_B3", "floor": 3, "capacity_liters": 150, "compressor_kw": 1.5, "solution_mapping": ["F"]},
            {"id": "WC_B4", "floor": 4, "capacity_liters": 150, "compressor_kw": 1.5, "solution_mapping": ["F"]}
        ]
    },

    "Block C": {
        "description": "Third & Fourth year engineering departments (CSE/ECE/Mech), hardware and computing laboratories",
        "floors": 4,
        "labs": [
            {
                "id": "C_LAB_1", "name": "Advanced Computing Lab 1 (CSE)", "floor": 1,
                "pc_count": 60, "pc_active_watts": 100, "pc_sleep_watts": 2,
                "ups_inverter_efficiency": 0.90,
                "appliances": {"ac_units": 3, "ac_tonnage_each": 2.5, "lights": 20},
                "solution_mapping": ["C", "B"]
            },
            {
                "id": "C_LAB_2", "name": "AI & Data Science Lab 2 (CSE)", "floor": 2,
                "pc_count": 60, "pc_active_watts": 110, "pc_sleep_watts": 2,
                "ups_inverter_efficiency": 0.90,
                "appliances": {"ac_units": 3, "ac_tonnage_each": 2.5, "lights": 20},
                "solution_mapping": ["C", "B"]
            },
            {
                "id": "C_LAB_3", "name": "Embedded Systems & IoT Lab (ECE)", "floor": 3,
                "pc_count": 60, "pc_active_watts": 95, "pc_sleep_watts": 2,
                "ups_inverter_efficiency": 0.90,
                "appliances": {"ac_units": 3, "ac_tonnage_each": 2.5, "lights": 20},
                "solution_mapping": ["C", "B"]
            }
        ],
        "water_coolers": [
            {"id": "WC_C1", "floor": 1, "capacity_liters": 150, "compressor_kw": 1.5, "solution_mapping": ["F"]},
            {"id": "WC_C2", "floor": 2, "capacity_liters": 150, "compressor_kw": 1.5, "solution_mapping": ["F"]},
            {"id": "WC_C3", "floor": 3, "capacity_liters": 150, "compressor_kw": 1.5, "solution_mapping": ["F"]},
            {"id": "WC_C4", "floor": 4, "capacity_liters": 150, "compressor_kw": 1.5, "solution_mapping": ["F"]}
        ]
    },

    "Hostel Block": {
        "description": "Student residential wings, dining hall, common laundry, and residential washroom blocks",
        "room_level_control_policy": {
            "mode": "sensor_kill_switch_manual_override",
            "description": "Every single hostel room equipped with presence sensing. When vacant, all room loads (fans, lights, charging points) automatically shut off completely. When an occupant enters, control returns 100% to manual user operation for full student freedom and comfort."
        },
        "wings": [
            {
                "id": "HOSTEL_W1", "name": "Hostel Wing 1 (Ground & 1st Floor)",
                "resident_capacity": 180,
                "rooms_count": 60,
                "room_occupancy_sensors": "PIR + Ultrasonic dual-tech per room",
                "geyser_bank": {"geysers_count": 8, "kw_each": 2.5, "stagger_slot": "05:30 - 06:30"},
                "solution_mapping": ["E"]
            },
            {
                "id": "HOSTEL_W2", "name": "Hostel Wing 2 (2nd & 3rd Floor)",
                "resident_capacity": 180,
                "rooms_count": 60,
                "room_occupancy_sensors": "PIR + Ultrasonic dual-tech per room",
                "geyser_bank": {"geysers_count": 8, "kw_each": 2.5, "stagger_slot": "06:30 - 07:30"},
                "solution_mapping": ["E"]
            }
        ],
        "water_pumps": [
            {"id": "HP_PUMP_1", "name": "Hostel Overhead Tank Pump 1", "rating_hp": 7.5, "kw": 5.6, "solution_mapping": ["E", "G"]},
            {"id": "HP_PUMP_2", "name": "Hostel Overhead Tank Pump 2", "rating_hp": 7.5, "kw": 5.6, "solution_mapping": ["E", "G"]}
        ],
        "canteen_cold_chain": {
            "id": "CANTEEN_COOL",
            "commercial_freezers": 3,
            "kw_each": 1.8,
            "solution_mapping": ["F"]
        }
    },

    "Campus Infrastructure": {
        "description": "Perimeter network, heavy water purification, and environmental utilities",
        "poe_access_points": {
            "total_count": 150,
            "academic_block_count": 100,
            "hostel_count": 50,
            "normal_watts_each": 20.0,
            "low_power_beacon_watts": 4.5,
            "solution_mapping": ["H"]
        },
        "heavy_motors": [
            {"id": "STP_AERATION", "name": "Sewage Treatment Plant Aeration Blower", "kw": 11.0, "flexible_run": True, "solution_mapping": ["G"]},
            {"id": "RO_PURIFICATION", "name": "Central Campus RO Water Plant", "kw": 7.5, "flexible_run": True, "solution_mapping": ["G"]},
            {"id": "MAIN_BOREWELL", "name": "Primary Borewell Pump to Sump", "kw": 9.3, "flexible_run": True, "solution_mapping": ["G"]}
        ]
    }
}

if __name__ == "__main__":
    import json
    print(f"Loaded blueprint for {CAMPUS_METADATA['institution_name']}.")
    print(f"Total building blocks: {len(CAMPUS_BLUEPRINT)}")
    total_zones = sum(len(b.get('zones', [])) + len(b.get('labs', [])) + len(b.get('wings', [])) for b in CAMPUS_BLUEPRINT.values())
    print(f"Total managed zones: {total_zones}")
