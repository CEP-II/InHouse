from statemachine import StateMachine, State
from readWrite import LightController

class LightMachine(StateMachine):
    def __init__(self,  controller:LightController):
        self.LC = controller
        self.prev_state_index = -2
        self.states_list = [LightMachine.bed, LightMachine.room1, LightMachine.room2, LightMachine.room3, LightMachine.room_bath]
        super().__init__()

    bed = State(initial=True)
    room1 = State()
    room2 = State()
    room3 = State()
    room_bath = State()
    alarm = State(final=True)
    
    trigger_sens_bed = bed.to.itself(internal=True) | room1.to(bed) | room2.to(bed) | room3.to(bed) | room_bath.to(bed)
    trigger_sens1 = bed.to(room1) | room1.to.itself(internal=True) | room2.to(room1) | room3.to(room1) | room_bath.to(room1)
    trigger_sens2 = bed.to(room2) | room1.to(room2) | room2.to(room1) | room3.to(room1) | room_bath.to(room1)
    trigger_sens3 = bed.to(room3) | room1.to(room3) | room2.to(room3) | room3.to(room2) | room_bath.to(room2)
    trigger_sens4 = bed.to(room_bath) | room1.to(room_bath) | room2.to(room_bath) | room3.to(room_bath) | room_bath.to(room3)

    trigger_alarm = bed.to(alarm) | room1.to(alarm) | room2.to(alarm) | room3.to(alarm) | room_bath.to(alarm)

    def on_enter_state(self, event, state):
        print(f"Entered state {state.id} with event {event}.")
        print("\n")
        print(self.states_list)
        print("\n")
        print(self.states_list[0])

        pos = self.states_list.index(state)

        # Bed, turn off all lights
        if pos == 0:
            for i, light in enumerate(self.LC.lights):
                self.LC.turnOff(i)

        # Walked right (excluding bathroom)
        elif self.prev_state_index < pos and pos != len(self.states)-1:
            for i, light in enumerate(self.LC.lights):
                # Lights to turn on
                # Current room
                if i == pos-1:
                    self.LC.turnOn(i, "green")
                # Next room
                elif i == pos:
                    self.LC.turnOn(i, "white")
                # Turn off all others
                else:
                    self.LC.turnOff(i)

        # Walked left or entered bathroom
        else:
            for i, light in enumerate(self.LC.lights):
                # Lights to turn on
                # Current room
                if i == pos-1:
                    self.LC.turnOn(i, "green")
                # Next room
                elif i == pos-2:
                    self.LC.turnOn(i, "white")

                # Turn off all others
                else:
                    self.LC.turnOff(i)


        self.prev_state_index = pos