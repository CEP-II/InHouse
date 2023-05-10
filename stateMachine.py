from statemachine import StateMachine, State
from readWrite import LightController

class LightMachine(StateMachine):
    def __init__(self,  controller:LightController):
        super().__init__()
        self.LC = controller

    bed = State(initial=True)
    room1 = State()
    room2 = State()
    room3 = State()
    room_bath = State()
    alarm = State(final=True)
    
    trigger_sens_bed = bed.to.itself() | room1.to(bed)
    trigger_sens1 = bed.to(room1) | room1.to.itself()
    trigger_sens2 = room1.to(room2) | room2.to(room1)
    trigger_sens3 = room2.to(room3) | room3.to(room2)
    trigger_sens4 = room3.to(room_bath) | room_bath.to(room3)

    trigger_alarm = bed.to(alarm) | room1.to(alarm) | room2.to(alarm) | room3.to(alarm) | room_bath.to(alarm) 

    def on_exit_state(self, event, state):
        print("Exiting " + state.id + " with event: " + event)

        # Exiting bed
        if state.id == 'bed':
            if event == "trigger_sens1":
                self.LC.turnOn(0)
                self.LC.turnOn(1)
        

        # Exiting room 1
        if state.id == 'room1':
            # Go to bed
            if event == "trigger_sens_bed":
                self.LC.turnOff(0)
                self.LC.turnOff(1)

            # Go right
            elif event == "trigger_sens2":
                self.LC.turnOff(0)
                self.LC.turnOn(1)
                self.LC.turnOn(2)
        
        # Exiting room 2
        if state.id == 'room2':
            # Go right
            if event == "trigger_sens3":
                self.LC.turnOff(1)
                self.LC.turnOn(2)
                self.LC.turnOn(3)
                
            # Go left
            elif event == "trigger_sens2":
                self.LC.turnOff(1)
                self.LC.turnOff(2)
                self.LC.turnOn(0)

        # Exiting room 3
        if state.id == 'room3':
            # Go right
            if event == "trigger_sens4":
                self.LC.turnOff(1)
                self.LC.turnOn(3)
                
            # Go left
            elif event == "trigger_sens3":
                self.LC.turnOff(2)
                self.LC.turnOff(3)
                self.LC.turnOn(1)
                self.LC.turnOn(0)

        # Exiting bath
        if state.id == 'room_bath':
            self.LC.turnOff(3)
            self.LC.turnOn(1)            

    def on_enter_state(self, event, state):
        print("Entered: " + state.id)
        if state.id == 'alarm':
            self.LC.alarm()



# controller = LightController()
# controller.add_light("zigbee2mqtt/0xbc33acfffe8b8d7c/set")
# controller.add_light("zigbee2mqtt/0xbc33acfffe8b8d7c/set")
# controller.add_light("zigbee2mqtt/0xbc33acfffe8b8d7c/set")
# controller.add_light("zigbee2mqtt/0xbc33acfffe8b8d7c/set")
# #controller.turnOff(0)

# sm = LightMachine(controller)
# sm.trigger_sens_bed()
# sm.trigger_sens_bed()
# sm.trigger_sens1()
# print(sm.LC.activeLights())
# sm.trigger_sens2()
# print(sm.LC.activeLights())
# sm.trigger_sens3()
# print(sm.LC.activeLights())
# sm.trigger_sens4()
# print(sm.LC.activeLights())
# sm.trigger_sens4()
# print(sm.LC.activeLights())
# sm.trigger_sens3()
# print(sm.LC.activeLights())
# sm.trigger_sens2()
# print(sm.LC.activeLights())
# sm.trigger_sens1()
# print(sm.LC.activeLights())
# sm.trigger_sens_bed()
# print(sm.LC.activeLights())