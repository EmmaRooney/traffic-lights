import asyncio
from enum import Enum, auto
import time
from gpiozero import Button

from traffic_light import TrafficLight
from traffic_light_state import TrafficLightState

PIN_LED_RED = 2
PIN_LED_AMBER = 3
PIN_LED_GREEN = 4
PIN_LED_PEDESTRIAN = 17
PIN_BUTTON = 21

class JunctionState(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()

JUNCTION_STATES = {
    JunctionState.A: {
        0: TrafficLightState.GO#,
        #1: TrafficLightState.GO,
        #2: TrafficLightState.STOPPED
    },
    JunctionState.B: {
        0: TrafficLightState.STOPPED#,
        #1: TrafficLightState.STOPPED,
        #2: TrafficLightState.GO
    },
    JunctionState.C: {
        0: TrafficLightState.PEDESTRIAN#,
        #1: TrafficLightState.PEDESTRIAN,
        #2: TrafficLightState.PEDESTRIAN
    },
    JunctionState.D: {
        0: TrafficLightState.STOPPED#,
        #1: TrafficLightState.STOPPED,
        #2: TrafficLightState.STOPPED
    }
}


class Junction():
    def __init__(self, traffic_lights, button):
        self._button = button
        self._button.when_activated = self._on_button_press

        self._traffic_lights = traffic_lights

        self._state = asyncio.run(self._set_state(JunctionState.D))

    def _on_button_press(self):
        asyncio.run(self._set_state(JunctionState.C))

    async def _set_state(self, new_state):
        coros = [light.stop() for id, light in enumerate(self._traffic_lights) if JUNCTION_STATES[new_state][id] == TrafficLightState.STOPPED]
        await asyncio.gather(*coros)
        coros = [light.pedestrian_cross() for id, light in enumerate(self._traffic_lights) if JUNCTION_STATES[new_state][id] == TrafficLightState.PEDESTRIAN]
        await asyncio.gather(*coros)
        coros = [light.go() for id, light in enumerate(self._traffic_lights) if JUNCTION_STATES[new_state][id] == TrafficLightState.GO]
        await asyncio.gather(*coros)
        self._state = new_state
        print(f"State: {self._state}")
            

    def run(self):
        print("Run")
        asyncio.run(self._set_state(JunctionState.A))
        time.sleep(10)
        asyncio.run(self._set_state(JunctionState.B))
        time.sleep(10)
        


if __name__ == "__main__":
    button = Button(PIN_BUTTON)

    light_0 = TrafficLight(0, PIN_LED_GREEN, PIN_LED_AMBER, PIN_LED_RED, PIN_LED_PEDESTRIAN)

    lights = [light_0]

    junction = Junction(lights, button)
    
    while True:
        junction.run()