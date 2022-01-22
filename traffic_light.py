import asyncio
import time

from gpiozero import LED

from traffic_light_state import TrafficLightState


class TrafficLight():
    def __init__(self, id, pin_green, pin_amber, pin_red, pin_ped, initial_state=TrafficLightState.STOPPED) -> None:
        self._id = id
        self._state = initial_state
        self._led_green = LED(pin_green)
        self._led_amber = LED(pin_amber)
        self._led_red = LED(pin_red)
        self._led_pedestrian = LED(pin_ped)
        self._set_initial_state(initial_state)

    def _state_stopped(self):
        self._led_pedestrian.off()
        self._led_green.off()
        self._led_amber.off()
        self._led_red.on()

    def _state_go(self):
        self._led_pedestrian.off()
        self._led_green.on()
        self._led_amber.off()
        self._led_red.off()

    def _state_stopping(self):
        self._led_pedestrian.off()
        self._led_green.off()
        self._led_amber.on()
        self._led_red.off()


    def _state_starting(self):
        self._led_pedestrian.off()
        self._led_green.off()
        self._led_amber.on()
        self._led_red.on()

    def _state_pedestrian_cross(self):
        self._led_green.off()
        self._led_amber.off()
        self._led_red.on()
        self._led_pedestrian.on()

    def _set_initial_state(self, state):
        if state == TrafficLightState.STOPPED:
            self._state_stopped()
        elif state == TrafficLightState.STOPPING:
            self._state_stopping()
        elif state == TrafficLightState.STARTING:
            self._state_starting()
        elif state == TrafficLightState.GO:
            self._state_go()
        elif state == TrafficLightState.PEDESTRIAN:
            self._state_pedestrian_cross()

    def get_state(self):
        return self._state

    def get_id(self):
        return self._id

    async def go(self):
        if self._state == TrafficLightState.STOPPING or self._state == TrafficLightState.PEDESTRIAN:
            await asyncio.sleep(2)
            self._state_stopped()
            self._state = TrafficLightState.STOPPED
        if self._state == TrafficLightState.STOPPED:
            await asyncio.sleep(5)
            self._state_starting()
            self._state = TrafficLightState.STARTING
        if self._state == TrafficLightState.STARTING:
            await asyncio.sleep(2)
            self._state_go()
            self._state = TrafficLightState.GO


    async def stop(self):
        if self._state == TrafficLightState.STARTING:
            await asyncio.sleep(2)
            self._state_go()
            self._state = TrafficLightState.GO
        if self._state == TrafficLightState.GO:
            await asyncio.sleep(2)
            self._state_stopping()
            self._state = TrafficLightState.STOPPING
        if self._state == TrafficLightState.STOPPING or self._state == TrafficLightState.PEDESTRIAN:
            await asyncio.sleep(2)
            self._state_stopped()
            self._state = TrafficLightState.STOPPED

    async def pedestrian_cross(self):
        await self.stop()
        await asyncio.sleep(2)
        self._state_pedestrian_cross()
        self._state = TrafficLightState.PEDESTRIAN

