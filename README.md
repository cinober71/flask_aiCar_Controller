# flask_aiCar_Controller
Controller for gate via aiCar
  by Adam Yusenko
  git: cinober71
  ver. by 07.12.2022

Config: 

Relay - setups for relay

[Relay]

relay_on  - № of pin on RPI for 1 channel

relay_off - № of pin on RPI for 2 channel

delay_on - delay befor swich level on relay_on pin in second

delay_off - delay befor swich level on relay_off pin in second

[Flask]

port - port for server

host - URL of server

debug - 1/0 on/off flask debug

methods - methods for work with controller 

Examlpe:

http://host:port/relay/*(on/off)

on - open 1 channel of relay

off - open 2 channel of relay

returns

{

        'id': 1, 
        
        'title': u'Open gate', 
        
        'description': u'Open gate on command ',
        
        'done': True 
        
}
