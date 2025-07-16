# test_lights.py
# Verifies that opening the door turns on the interior lights.

import time
from libs.can_utils import send_frame, receive_frame

def test_lights_on(db, bus):
    """DoorOpen=True should produce LightsOn=1."""
    door_msg   = db.get_message_by_name("DoorStatus")
    lights_msg = db.get_message_by_name("InteriorLightStatus")

    # Send DoorOpen=True
    send_frame(bus, door_msg, {"DoorOpen": True})

    # Poll until the response with correct arbitration_id arrives
    timeout = 1.0
    deadline = time.time() + timeout
    response = None
    while time.time() < deadline:
        msg = receive_frame(bus, timeout=0.1)
        if msg and msg.arbitration_id == lights_msg.frame_id:
            response = msg
            break

    assert response, f"No response within {timeout}s"
    decoded = db.decode_message(response.arbitration_id, response.data)
    assert decoded["LightsOn"] == 1, f"Expected LightsOn=1, got {decoded['LightsOn']}"