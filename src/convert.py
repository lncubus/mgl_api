import json
from random import random, uniform

from numpy import interp

def roundTo(val, prec=3):
    return round(val, prec-len(str(int(val))))

estimates = {
    "march_engine": {
        "thrust": {-3: 700, 0: 1000, 5: 1500},
        "thrust_rev": {0: 0},
        "accel": {-3: 16, 0: 20, 5: 28},
        "slowdown": {-1: 16, 0: 20, 2: 28},
        "accel_rev": {0: 0},
        "slowdown_rev": {0: 0},
        "heat_prod": {-3: 100, 0: 80, 5: 60},
        "volume": {-1: 315, 0: 277.5, 2: 240}
    },
    "shunter": {
        "turn": {-3: 45, 0: 60, 5: 80},
        "strafe": {0: 0},
        "strafe_acc": {0: 0},
        "strafe_slow": {0: 0},
        "turn_acc": {-3: 80, 0: 90, 5: 105},
        "turn_slow": {-3: 80, 0: 90, 5: 105},
        "heat_prod": {-3: 92, 0: 80, 5: 60},
        "volume": {-1: 210, 0: 185, 2: 160},
    },
    "radar": {
        "range_max": {-3: 30, 0: 40, 5: 50},
        "angle_min": {-2: 25, 0: 20, 3: 15},
        "angle_max": {-2: 30, 0: 35, 3: 40},
        "angle_change": {-3: 0.8, 0: 1, 5: 1.2},
        "range_change": {-3: 0.8, 0: 1, 5: 1.2},
        "rotate_speed": {-3: 10, 0: 12, 5: 15},
        "volume": {-1: 210, 0: 185, 2: 160},
    }

}

model = {
    "company": "pre",
    "node_type_code": "radar",
    "name": "AN/ZPY-1 Starlite",
    "size": "medium",
    "params": {
        "range_max": -1,
        "angle_min": 1,
        "angle_max": 1,
        # "angle_change": 1,
        # "range_change": 1,
        "rotate_speed": 2,
        # "volume": -1,
    }
}
if __name__ == "__main__":
    est = estimates[model['node_type_code']]

    advance = sum(model['params'].values()) / sum([max(arr) for arr in est.values()])
    model['level'] = 2 if advance > 0.9 else 1 if advance > 0.45 else 0

    for name, arr in est.items():
        val = interp(model['params'].get(name, 0), list(arr.keys()), list(arr.values()))
        accuracy = 0.02
        val = roundTo(val * (uniform(1 - accuracy, 1+ accuracy)))
        model['params'][name] = val

    print(json.dumps(model))
