# test_lights.py
# Verifies interior lights follow the door state: on when open, off when closed.

import time
import pytest
from libs.can_utils import send_frame, receive_frame

@pytest.mark.parametrize("door_open, expected_lights", [
    (True, 1),
    (False, 0),
])
def test_lights(db, bus, door_open, expected_lights):
    """
    Sends DoorStatus.DoorOpen = door_open and expects
    InteriorLightStatus.LightsOn == expected_lights.
    """
    door_msg   = db.get_message_by_name("DoorStatus")
    lights_msg = db.get_message_by_name("InteriorLightStatus")

    # Send the door frame
    send_frame(bus, door_msg, {"DoorOpen": door_open})

    # Polling loop to catch the lights response
    timeout = 1.0
    deadline = time.time() + timeout
    response = None
    while time.time() < deadline:
        msg = receive_frame(bus, timeout=0.1)
        if msg and msg.arbitration_id == lights_msg.frame_id:
            response = msg
            break

    assert response, f"No response within {timeout}s for DoorOpen={door_open}"
    decoded = db.decode_message(response.arbitration_id, response.data)
    assert decoded["LightsOn"] == expected_lights, (
        f"Expected LightsOn={expected_lights}, got {decoded['LightsOn']}"
    )