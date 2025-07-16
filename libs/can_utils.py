# can_utils.py
# Provides CAN bus initialization, send_frame and receive_frame functions.

import can

def init_bus(interface='virtual', channel='0', bitrate=500000):
    """
    Initialize and return a CAN Bus instance.
    interface: backend name (virtual, socketcan, etc.)
    channel: channel identifier (for virtual use '0')
    bitrate: bus speed in bits per second
    """
    return can.Bus(
        interface=interface,
        channel=channel,
        bitrate=bitrate,
        receive_own_messages=True
    )

def send_frame(bus, message, data):
    """
    Encode and send a CAN frame.
    bus: CAN Bus instance
    message: cantools Message object
    data: dict mapping signal names to values
    """
    frame = can.Message(
        arbitration_id=message.frame_id,
        data=message.encode(data),
        is_extended_id=False
    )
    bus.send(frame)
    return frame

def receive_frame(bus, timeout=1.0):
    """
    Receive a CAN frame from the bus within timeout seconds.
    Returns can.Message or None.
    """
    return bus.recv(timeout)