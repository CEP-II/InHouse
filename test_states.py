from stateMachine import LightMachine
from readWrite import LightController
import json

class mock_Light:
    def __init__(self, name):
        self.name = name

        broker_address = "localhost"
        broker_port = 1883
        # self.client = mqtt.Client()
        # self.client.connect(broker_address, broker_port)

        self.state = False
    
    def publish(self, message):
        # self.client.publish(self.name, message)
        pass
    
    def get_state(self):
        return self.state
    
    def set_state(self, s: bool):
        self.state = s


class mock_LightController:
    ### Initializes the connection to the light component
    def __init__(self):
        # message to pass for off
        broker_out_off = {"state":"OFF"}
        self.data_out_off = json.dumps(broker_out_off)

        # message to pass for alarm
        data_alarm = {"state": "ON", "color":{"r":255,"g":0,"b":0}}
        self.data_alarm = json.dumps(data_alarm)

        # array containing the lights
        self.lights = []

    # Function for getting color dictionary
    def get_color_dictionary(self, color_key):
        colors = {
            'red': {'r': 255, 'g': 0, 'b': 0},
            'green': {'r': 0, 'g': 255, 'b': 0},
            'blue': {'r': 0, 'g': 0, 'b': 255},
            'white': {'r': 255, 'g': 255, 'b': 255}
        }

        if color_key in colors:
            color_value = colors[color_key]
            color_dict = {
                'state': 'ON',
                'color': {
                    'r': color_value['r'],
                    'g': color_value['g'],
                    'b': color_value['b']
                }
            }
        else:
            # White if not recognized
            color_dict = {
                'state': 'ON',
                'color': {
                    'r': color_value['r'],
                    'g': color_value['g'],
                    'b': color_value['b']
                }
            }
        return color_dict

    ### add a new light
    def add_light(self, adress):
        light = mock_Light(adress)
        self.lights.append(light)

    ### Turns on the light with ID and color
    def turnOn(self, ID, color: str):
        print(f"Turn on light: {ID+1} with color {color}")
        self.lights[ID].set_state(True)
        message = json.dumps(self.get_color_dictionary(color))
        # self.lights[ID].publish(message)
        
    def alarm(self, ID):
        print("alarm")
        self.lights[ID].set_state(True)
        message = json.dumps(self.data_alarm)
        # self.lights[ID].publish(message)

    ### Turns off the ligh with ID; IDt
    def turnOff(self, ID):
        self.lights[ID].set_state(False)
        message = self.data_out_off                 # Message to turn off
        # self.lights[ID].publish(message)     # Publishes to self.name aka topic
    
    ### Terminates the connection
    def terminate(self, client):
        client.disconnect()                 # Disconnects the client

    def activeLights(self):
        active = []
        for index, light in enumerate(self.lights):
            if light.get_state() == True:
                active.append(index)
        return active

def test_transitions():
    lc = LightController()
    sm = LightMachine(lc)

    assert sm._get_initial_state().id == "bed"
    sm.trigger_sens_bed
    assert sm.current_state.id == "bed"
    sm.trigger_sens1()
    assert sm.current_state.id == "room1"
    sm.trigger_sens2()
    assert sm.current_state.id == "room2"
    sm.trigger_sens3()
    assert sm.current_state.id == "room3"
    sm.trigger_sens4()
    assert sm.current_state.id == "room_bath"
    sm.trigger_sens4()
    assert sm.current_state.id == "room3"
    sm.trigger_sens3()
    assert sm.current_state.id == "room2"
    sm.trigger_sens2()
    assert sm.current_state.id == "room1"
    sm.trigger_sens1()
    assert sm.current_state.id == "room1"
    sm.trigger_sens_bed()
    assert sm.current_state.id == "bed"
    sm.trigger_sens4()
    assert sm.current_state.id == "room_bath"
    sm.trigger_sens2()
    assert sm.current_state.id == "room1"

def test_lights():
    lc = mock_LightController()
    sm = LightMachine(lc)
    lc.add_light("zigbee0")
    lc.add_light("zigbee1")
    lc.add_light("zigbee2")
    lc.add_light("zigbee3")
    assert lc.activeLights() == []
    sm.trigger_sens1()
    assert lc.activeLights() == [0, 1]
    sm.trigger_sens_bed()
    assert lc.activeLights() == []
    sm.trigger_sens2()
    assert lc.activeLights() == [1, 2]
    sm.trigger_sens3()
    assert lc.activeLights() == [2, 3]
    sm.trigger_sens4()
    assert lc.activeLights() == [2, 3]
    sm.trigger_sens4()
    assert lc.activeLights() == [1, 2]