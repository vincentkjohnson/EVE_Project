class Damnation:

    # Status Effects
    destroyed = False
    jammed = False

    shield_damage = 0
    armor_damage = 0
    hull_damage = 0

    def __init__(self):
        # Basic Information
        self.name = "Damnation"
        self.ship_type = "Damage"

        # Resistances                  EM | KIN |  TH | EX  |  HP
        self.shield_resistances_hp = [0.0, 0.20, 0.70, 0.875, 4500.0]
        self.armor_resistances_hp = [0.928, 0.922, 0.926, 0.96, 27215.0]
        self.hull_resistances_hp = [0.33, 0.33, 0.33, 0.33, 5500.0]

        # Capacitor
        self.capacitor = 3164
        self.capacitor_delta = 8.59
        self.cap_recharge_time = 562

        # Targeting
        self.max_targets = 7
        self.target_range = 87500  # kilometers
        self.scan_res = 265  # mm
        self.sensor_strength = 39.2

        # Navigation
        self.speed = 948
        self.signature = 1590

        # Damage & Utility
        self.em_dps = 534
        self.thermal_dps = 534
        self.kinetic_dps = 534
        self.explosive_dps = 534
        self.jam_strength = 5
        self.jam_cycle = 20

    def target_jammed(self):
        self.jammed = True

    def target_destroyed(self):
        self.destroyed = True
