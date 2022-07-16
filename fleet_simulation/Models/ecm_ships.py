class ArmorScorpion:

    # Status Effects
    destroyed = False
    jammed = False

    shield_damage = 0
    armor_damage = 0
    hull_damage = 0

    def __init__(self):
        # Basic Information
        self.name = "Armor Scorpion"
        self.ship_type = "Electronic Attack Ship"

        # Resistances                  EM  |  KIN |  TH  |  EX   |  HP
        self.shield_resistances_hp = [0.125, 0.300, 0.475, 0.562, 9625.0]
        self.armor_resistances_hp = [0.905, 0.895, 0.857, 0.866, 33091.0]
        self.hull_resistances_hp = [0.598, 0.598, 0.598, 0.598, 8938.0]

        # Capacitor
        self.capacitor = 6875
        self.capacitor_delta = 2.48
        self.cap_recharge_time = 825

        # Targeting
        self.max_targets = 10
        self.target_range = 176  # kilometers
        self.scan_res = 232  # mm
        self.sensor_strength = 60.6

        # Navigation
        self.speed = 104
        self.signature = 440

        # Electronic Counter Measures
        self.jam_strength = 8.75
        self.jam_modules = 6
        self.jam_cycle = 20

    def target_jammed(self):
        self.jammed = True

    def target_destroyed(self):
        self.destroyed = True
