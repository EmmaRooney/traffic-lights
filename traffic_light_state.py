from enum import Enum, auto

class TrafficLightState(Enum):
    GO = auto()
    STOPPING = auto()
    STOPPED = auto()
    STARTING = auto()
    PEDESTRIAN = auto()