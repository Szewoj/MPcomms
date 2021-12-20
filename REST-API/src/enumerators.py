from enum import Enum

class Modes(Enum):
    INVALID = -1
    STANDBY = 0b00
    AUTOMATIC = 0b01
    MANUAL = 0b10

modeSwitch = {
    0b00: Modes.STANDBY,
    0b01: Modes.AUTOMATIC,
    0b10: Modes.MANUAL
}

class EmergencyActions(Enum):
    INVALID = -1
    NOTASK = 0b00
    STOP = 0b01
    RETURN = 0b10

emergencyActionsSwitch = {
    0b00: EmergencyActions.NOTASK,
    0b01: EmergencyActions.STOP,
    0b10: EmergencyActions.RETURN
}
