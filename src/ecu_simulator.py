# ecu_simulator.py
# Simulates an ECU: listens to DoorStatus and replies with InteriorLightStatus.

import threading
import time
from libs.dbc_loader import load_dbc
from libs.can_utils import init_bus, send_frame, receive_frame

class ECUSimulator(threading.Thread):
    def __init__(self, interface='virtual', channel='0', bitrate=500000):
        super().__init__(daemon=True)
        # Load DBC definitions
        db = load_dbc('config/vehicle.dbc')
        self.door_msg   = db.get_message_by_name("DoorStatus")
        self.lights_msg = db.get_message_by_name("InteriorLightStatus")
        # Initialize CAN bus
        self.bus = init_bus(interface=interface, channel=channel, bitrate=bitrate)
        self._stop_event = threading.Event()

    def run(self):
        print("🔌 ECU Simulator started. Waiting for DoorStatus...")
        while not self._stop_event.is_set():
            msg = receive_frame(self.bus, timeout=0.1)
            if msg and msg.arbitration_id == self.door_msg.frame_id:
                data = self.door_msg.decode(msg.data)
                response = {"LightsOn": bool(data.get("DoorOpen"))}
                send_frame(self.bus, self.lights_msg, response)
            time.sleep(0.01)
        # Shutdown bus on stop
        self.bus.shutdown()
        print("🛑 ECU Simulator stopped.")

    def stop(self):
        """Signal the simulator thread to stop and wait for it."""
        self._stop_event.set()
        self.join()