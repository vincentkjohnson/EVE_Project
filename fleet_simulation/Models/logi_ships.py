class Guardian:

    # Status Effects
    destroyed = False
    jammed = False

    shield_damage = 0
    armor_damage = 0
    hull_damage = 0

    def __init__(self):
        # Basic Information
        self.name = "Guardian"
        self.ship_type = "Logistics"

        # Resistances                  EM  |  KIN |  TH  |  EX   |  HP
        self.shield_resistances_hp = [0.125, 0.300, 0.738, 0.891, 1319.0]
        self.armor_resistances_hp = [0.781, 0.797, 0.836, 0.912, 11182.0]
        self.hull_resistances_hp = [0.598, 0.598, 0.598, 0.598, 2505.0]

        # Capacitor
        self.capacitor = 2812
        self.capacitor_delta = 58.1
        self.cap_recharge_time = 375

        # Targeting
        self.max_targets = 10
        self.target_range = 81250  # kilometers
        self.scan_res = 481  # mm
        self.sensor_strength = 131

        # Navigation
        self.speed = 605
        self.signature = 70

        # Remote Reps
        self.remote_armor = 394
        self.remote_cap = 62.2

    def target_jammed(self):
        self.jammed = True

    def target_destroyed(self):
        self.destroyed = True
