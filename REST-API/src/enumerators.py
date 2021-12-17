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

class EmergencyTasks(Enum):
    INVALID = -1
    NOTASK = 0b00
    STOP = 0b01
    RETURN = 0b10

emergencyTasksSwitch = {
    0b00: EmergencyTasks.NOTASK,
    0b01: EmergencyTasks.STOP,
    0b10: EmergencyTasks.RETURN
}
