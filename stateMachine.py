from statemachine import StateMachine, State
from readWrite import LightController

class LightMachine(StateMachine):
    def __init__(self):
        LC = LightController()
        LC.add_light("zigbee2mqtt/0xbc33acfffe8b8d7c/set") ### bedroom light

    room0 = State(initial=True)
    room1 = State()
    room2 = State()
    room_bath = State()
    alarm = State()
    
    trigger_bed = room0.to.itself()

    trigger_sens1 = room0.to(room1) | room1.to(room0)

    trigger_sens2 = room1.to(room2) | room2.to(room1)

    trigger_sens3 = room2.to(room_bath) | room_bath.to(room2)

    trigger_alarm = room0.to(alarm) | room1.to(alarm) | room2.to(alarm) | room_bath.to(alarm)

    def on_exit_state(self, event, state):
        print("Exiting " + state.id)
        if state.id == 'room1':
            if event == "trigger_sens2":
                print("Turn on room2")
                print("Turn on room_bath")
                print("Turn off room1")
            elif event == "trigger_sens1":
                print("Turn on room0")
                print("Turn off room1")
        if state.id == 'room0':
            print("Turn on room1")
            print("Turn on room2")
            print("Turn off room0")
        if state.id == 'room2':
            if event == "trigger_sens3":
                print("Turn on room_bath")
                print("Turn off room2")
            elif event == "trigger_sens2":
                print("Turn on room0")
                print("Turn on room1")
                print("Turn of room2")


    def on_enter_state(self, event, state):
        print("Entered: " + state.id)

sm = LightMachine()

sm.trigger_sens1()
sm.trigger_sens2()
sm.trigger_sens2()