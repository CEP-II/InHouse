from statemachine import StateMachine, State
from readWrite import LightController

class LightMachine(StateMachine):
    def __init__(self):
        self.LC = LightController()
        self.LC.add_light("zigbee2mqtt/0xbc33acfffe8b8d7c/set") # Light room 0
        self.LC.add_light("Some address") # Light room 1
        self.LC.add_light("Some address") # Light room 2
        self.LC.add_light("Some address") # Light room 3

    bed = State(initial=True)
    room0 = State()
    room1 = State()
    room2 = State()
    room_bath = State()
    alarm = State(final=True)
    
    trigger_sens_bed = bed.to(room0) | room0.to(bed)

    trigger_sens1 = room0.to(room1) | room1.to(room0)

    trigger_sens2 = room1.to(room2) | room2.to(room1)

    trigger_sens3 = room2.to(room_bath) | room_bath.to(room2)

    trigger_alarm = room0.to(alarm) | room1.to(alarm) | room2.to(alarm) | room_bath.to(alarm) | bed.to(alarm)

    # def on_exit_state(self, event, state):
    #     print("Exiting " + state.id)
    #     if state.id == 'room1':
    #         if event == "trigger_sens2":
    #             print("Turn on room2")
    #             print("Turn on room_bath")
    #             print("Turn off room1")
    #         elif event == "trigger_sens1":
    #             print("Turn on room0")
    #             print("Turn off room1")
    #     if state.id == 'room0':
    #         print("Turn on room1")
    #         print("Turn on room2")
    #         print("Turn off room0")
    #     if state.id == 'room2':
    #         if event == "trigger_sens3":
    #             print("Turn on room_bath")
    #             print("Turn off room2")
    #         elif event == "trigger_sens2":
    #             print("Turn on room0")
    #             print("Turn on room1")
    #             print("Turn of room2")


    def on_enter_state(self, event, state):
        print("Entered: " + state.id)

        # Turn on all lights
        if state.id == 'alarm':
            for i in range(self.LC.lights_size):
                self.LC.turnOn(i)

sm = LightMachine()

sm.trigger_sens1()
sm.trigger_sens2()
sm.trigger_sens2()