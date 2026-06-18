import time
import threading
from memory import Memory
from config import load_offsets

class Trainer:
    def __init__(self):
        self.mem = Memory()
        self.offsets = load_offsets()
        self.running = True
        self.features = {
            'auto_harvest': False,
            'auto_plant': False,
            'infinite_coins': False,
            'auto_roll_pets': False,
            'speed_multiplier': False,
            'auto_clicker': False
        }
        self.speed_value = 1.0

    def _write_offset(self, key, value, type='int'):
        addr = self.offsets.get(key)
        if addr is None:
            return
        if type == 'int':
            self.mem.write_int(addr, value)
        elif type == 'float':
            self.mem.write_float(addr, value)

    def _read_offset(self, key, type='int'):
        addr = self.offsets.get(key)
        if addr is None:
            return None
        if type == 'int':
            return self.mem.read_int(addr)
        elif type == 'float':
            return self.mem.read_float(addr)

    def infinite_coins(self, enable):
        self.features['infinite_coins'] = enable
        if enable:
            self._write_offset('coins_offset', 999999999, 'int')
        else:
            # restore original? we just leave it, but we could reset
            pass

    def speed_multiplier(self, enable, value=2.0):
        self.features['speed_multiplier'] = enable
        self.speed_value = value if enable else 1.0
        self._write_offset('growth_speed_offset', self.speed_value, 'float')

    def auto_harvest_loop(self):
        while self.running:
            if self.features['auto_harvest']:
                status = self._read_offset('plant_status_offset', 'int')
                if status == 1:  # 1 = mature
                    # simulate click or write harvest action
                    self._write_offset('plot_state_offset', 2, 'int')  # 2 = harvest
                    time.sleep(0.1)
            time.sleep(0.5)

    def auto_plant_loop(self):
        while self.running:
            if self.features['auto_plant']:
                # check if plot empty
                plot_state = self._read_offset('plot_state_offset', 'int')
                if plot_state == 0:  # empty
                    # plant seed
                    self._write_offset('plot_state_offset', 1, 'int')  # 1 = planted
                    time.sleep(0.2)
            time.sleep(0.5)

    def auto_roll_pets_loop(self):
        while self.running:
            if self.features['auto_roll_pets']:
                # simulate buying egg
                self._write_offset('pet_rarity_offset', 5, 'int')  # 5 = legendary
                time.sleep(1)

    def start(self):
        threads = [
            threading.Thread(target=self.auto_harvest_loop, daemon=True),
            threading.Thread(target=self.auto_plant_loop, daemon=True),
            threading.Thread(target=self.auto_roll_pets_loop, daemon=True)
        ]
        for t in threads:
            t.start()

        # main loop for commands
        try:
            while self.running:
                cmd = input("> ").strip().lower()
                if cmd == "harvest on":
                    self.features['auto_harvest'] = True
                    print("Auto Harvest enabled")
                elif cmd == "harvest off":
                    self.features['auto_harvest'] = False
                    print("Auto Harvest disabled")
                elif cmd == "plant on":
                    self.features['auto_plant'] = True
                    print("Auto Plant enabled")
                elif cmd == "plant off":
                    self.features['auto_plant'] = False
                    print("Auto Plant disabled")
                elif cmd == "coins on":
                    self.infinite_coins(True)
                    print("Infinite Coins enabled")
                elif cmd == "coins off":
                    self.infinite_coins(False)
                    print("Infinite Coins disabled")
                elif cmd == "speed on":
                    self.speed_multiplier(True, 2.5)
                    print("Speed Multiplier enabled (x2.5)")
                elif cmd == "speed off":
                    self.speed_multiplier(False)
                    print("Speed Multiplier disabled")
                elif cmd == "roll on":
                    self.features['auto_roll_pets'] = True
                    print("Auto Roll Pets enabled")
                elif cmd == "roll off":
                    self.features['auto_roll_pets'] = False
                    print("Auto Roll Pets disabled")
                elif cmd == "exit":
                    self.running = False
                    print("Shutting down...")
                    break
                else:
                    print("Commands: harvest on/off, plant on/off, coins on/off, speed on/off, roll on/off, exit")
        except KeyboardInterrupt:
            self.running = False
