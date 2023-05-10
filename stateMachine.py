from statemachine import StateMachine, State
from readWrite import LightController

class LightMachine(StateMachine):
    def __init__(self, controller):
        super().__init__()
        self.LC = controller
        self.LC.add_light("zigbee2mqtt/0xbc33acfffe8b8d7c/set") ### bedroom light
        self.controller = controller

    bed = State(initial=True)
    room1 = State()
    room2 = State()
    room_bath = State()
    alarm = State()
    
    trigger_bed = bed.to.itself()

    trigger_sens1 = bed.to(room1) | room1.to(bed)

    trigger_sens2 = room1.to(room2) | room2.to(room1)

    trigger_sens3 = room2.to(room_bath) | room_bath.to(room2)

    trigger_alarm = bed.to(alarm) | room1.to(alarm) | room2.to(alarm) | room_bath.to(alarm)

    def on_exit_state(self, event, state):
        print("Exiting " + state.id)
        if state.id == 'bed':
            print("Turn off bed")
            print("Turn off room1")
            self.controller.turnOff(0)
            print("Turn off room2")
            self.controller.turnOff(1)
            print("Turn off room_bath")

        

        if state.id == 'room1':
            if event == "trigger_sens2":
                print("Turn on room2")
                print("Turn on room_bath")
                print("Turn off room1")
            elif event == "trigger_sens1":
                print("Turn on bed")
                self.controller.turnOn(0)
                print("Turn off room1")
                self.controller.turnOff(1)
        
        if state.id == 'room2':
            if event == "trigger_sens3":
                print("Turn on room_bath")
                print("Turn off room2")
            elif event == "trigger_sens2":
                print("Turn on bed")
                print("Turn on room1")
                print("Turn of room2")


    def on_enter_state(self, event, state):
        print("Entered: " + state.id)

"""
controller = LightController()
controller.add_light("zigbee2mqtt/0xbc33acfffe8b8d7c/set")
controller.turnOff(0)

print("Hello")
sm = LightMachine(controller)
sm.trigger_bed()
sm.trigger_sens1()
sm.trigger_sens1()
sm.trigger_sens1()
"""