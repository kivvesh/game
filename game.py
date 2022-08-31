from map import Map
import time
import os
from helicopter import Helicopter as Helico
from pynput import keyboard
from clouds import Clouds
import json




tick = 1
TICK_SLEEP = 0.4
TREE_UPDATE = 50
FIRE_UPDATE = 75
CLOUDS_UPDATE = 30
MAP_W,MAP_H = 20,10



tmp = Map(MAP_W,MAP_H)

clouds = Clouds(MAP_W,MAP_H)
helico = Helico(MAP_H,MAP_W)
MOVES = {"w":(-1,0),"d":(0,1),"s":(1,0),"a":(0,-1)}

def process_key(key):
    global helicom,tick
    c = key.char.lower()
    if c in MOVES.keys():
        dx,dy = MOVES[c][0],MOVES[c][1]
        helico.move(dx,dy)
    elif c=="f":
        data = {"helicopter":helico.export_data(),
                "clouds":clouds.export_data(),
                "field":tmp.export_data(),
                "tick":tick}
        with open("level.json","w") as lvl:
            json.dump(data,lvl)
    elif c=="g":
        with open("level.json","r") as lvl:
            data = json.load(lvl)
            tick = data["tick"] or 0
            helico.import_data(data["helicopter"])
            tmp.import_data(data["field"])
            clouds.import_data(data["clouds"])

listener = keyboard.Listener(
    on_press=None,
    on_release=process_key)
listener.start()

while True:
    os.system("CLS")
    
    tmp.process_holicopter(helico,clouds)
    helico.print_stats()
    tmp.print_Map(helico,clouds)
    
    tick +=1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE ==0):
        tmp.generate_tree()
    if (tick % FIRE_UPDATE ==0):
        tmp.update_fires()
    if (tick % CLOUDS_UPDATE ==0):
        clouds.update_clouds()
    print("TICK",tick,helico.x,helico.y)


