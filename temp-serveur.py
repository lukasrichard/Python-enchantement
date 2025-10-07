
# Variables simples
isopar = 8000    # Niveau isopar (cl)
pompe = 0     # Niveau pompe (cl)
tete = 0         # Position tête (0-15)
mode = 0         # 0=auto, 1=manuel
aut_flamme = 0   # Autorisation flamme (0/1)
act_flamme = 0   # Activation flamme (0/1)
cycle = 0        # Début de cycle (0/1)
progress = 0
pompe_charger = 0
bonne_position = 0

bar = None
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusServerContext, ModbusSequentialDataBlock, ModbusDeviceContext
from threading import Thread
import time
from tkinter import ttk
import tkinter as tk

if __name__ == "__main__":
    # Création du datastore Modbus avec un registre de 10 mots
    device = ModbusDeviceContext(
        co=ModbusSequentialDataBlock(0, [True]*10),    # en marche initialement
        hr=ModbusSequentialDataBlock(0, [200]*10)  # 20.0°C initial
    )
    context = ModbusServerContext(devices=device, single=True)

# Modbus context
store = {
	0x00: {
		'di': ModbusSequentialDataBlock(0, [0]*10),
		'co': ModbusSequentialDataBlock(0, [0]*10),
		'hr': ModbusSequentialDataBlock(0, [isopar, pompe, tete, mode, cycle, progress, bonne_position] + [0]*6),
		'ir': ModbusSequentialDataBlock(0, [0]*10)
	}
}
def update_modbus(slave_id=0x00):
    global isopar, pompe, tete, mode, aut_flamme, act_flamme, cycle, progress
    store[slave_id]['hr'].setValues(0, [isopar, pompe, tete, mode, cycle, progress, bonne_position] + [0]*7)
    store[slave_id]['co'].setValues(0, [aut_flamme, act_flamme] + [0]*8)
	




def run_modbus_server():
	print("Serveur Modbus TCP dragon parade démarré sur le port 5020...")
	StartTcpServer(context, address=("localhost", 5020))


def set_mode_auto():
	global mode , aut_flamme, pompe, bonne_position, act_flamme, tete, pompe_charger, isopar
	mode = 0
	
if pompe > 700:
	pompe_charger = 1
else :
	pompe_charger = 0
			

	


def set_mode_manuel():
	global mode
	mode = 1

def active_flamme():
	global act_flamme
	act_flamme = 1
	time.sleep(4)
	act_flamme = 0

if pompe > 700:
		pompe_charger = 1
else :
		pompe_charger = 0
if tete == 8:
		bonne_position = 1
else:
		bonne_position = 0 

def lancement_cycle():
	global progress, tete , act_flamme, pompe, pompe_charger, bonne_position
	diminution()
	progress = 0
	recharge()
	while progress < 15:
		while tete != 7:
			tete = tete + 1
			move_head(tete)
			time.sleep(0.2)
			update_status()
		progress = progress + 1
		root.update()
		time.sleep(1)
		while tete != 3:
			tete = tete - 1
			move_head(tete)
			time.sleep(0.2)
		progress = progress + 1
		move_head(tete)
		update_status()
		root.update()
		time.sleep(1)
		while tete != 5:
			tete = tete + 1
			move_head(tete)
			time.sleep(0.2)
		progress = progress + 1
		move_head(tete)
		update_status()
		root.update()
		time.sleep(1)
		while tete != 8:
			tete = tete + 1
			move_head(tete)
			time.sleep(0.2)
		progress = progress + 1
		move_head(tete)
		update_status()
		root.update()
		flamme()	
		time.sleep(5)
		while tete != 2:
			tete = tete - 1
			move_head(tete)
			time.sleep(0.2)
		progress = progress + 1
		recharge()
		move_head(tete)
		update_status()
		while tete != 0:
			tete = tete - 1
			move_head(tete)
			time.sleep(0.2)
		root.update()
		time.sleep(1)
		update_modbus()
	

def escamotage_bas():
	global tete
	while tete > 0:
		diminution()
def escamotage_haut():
	global tete
	while tete < 8:
		augementation()
	
def augementation():
    global tete
    if tete < 8:
        tete += 1
        move_head(tete)
        update_status()
        root.update()
        time.sleep(0.5)

def diminution():
    global tete
    if tete > 0:
        tete -= 1
        move_head(tete)
        update_status()
        root.update()
        time.sleep(0.5)
		
def move_head(tete):
    # Position de la tête (y = haut/bas en fonction de val)
    y_offset = 200 - tete * 15  # 0 = bas, 8 = haut
    # Mise à jour de la tête
    canvas.coords(head, 250, y_offset, 300, y_offset + 40)
    # Mise à jour du "cou" reliant le corps et la tête
    canvas.coords(neck, 200, 200, 250, y_offset + 20)
    root.update()
def recharge():
	global act_flamme, aut_flamme, pompe, pompe_charger, bonne_position, isopar, tete
	while pompe < 1000:
			pompe = pompe + 100
			isopar = isopar - 100
			root.update()
			time.sleep(0.2)	

def flamme():
	global act_flamme, aut_flamme, pompe, pompe_charger, bonne_position, isopar, tete
	act_flamme = 1
	for i in range(3):
			pompe = pompe - 50
			root.update()
			time.sleep(0.2) 
			i = i+1
	act_flamme = 0
	
def update_status():
	global progress, tete, pompe, act_flamme, pompe_charger, isopar
	status = f"Isopar: {isopar/1000} L | Pompe: {pompe} cl | Tête: {tete} | Mode: {'Auto' if mode==0 else 'Manuel'} | Autorisation Flamme: {aut_flamme} | Flamme Active: {act_flamme} \n Escamotage Tete : {'Haut' if tete == 8 else 'Bas' if tete == 0 else 'En mouvement'}"
	status_var.set(status)
	root.after(10, update_status)


		


	
	


if __name__ == "__main__":
	Thread(target=run_modbus_server, daemon=True).start()
	
	root = tk.Tk()
	root.title("Enchantement - Supervision")
	bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
	bar['value'] = progress
	if bar['value'] == 15:
		progress = 0
		cycle = 0
	
	status_var = tk.StringVar()
	status_label = tk.Label(root, textvariable=status_var, font=("Arial", 14))
	status_label.pack(pady=10)
	btn_auto = tk.Button(root, text="Mode Auto", command=set_mode_auto, width=15)
	btn_auto.pack(pady=5)
	btn_manuel = tk.Button(root, text="Mode Manuel", command=set_mode_manuel, width=15)
	btn_manuel.pack(pady=5)
	btn_manuel = tk.Button(root, text="Mode Cycle_auto", command=lancement_cycle, width=15)
	btn_manuel.pack(pady=5)
	btn_flamme = tk.Button(root, text="Activer Flamme", command=active_flamme, width=15)
	btn_flamme.pack(pady=5)
	btn_escamotage = tk.Button(root, text="Escamoter Bas", command=escamotage_bas, width=15)
	btn_escamotage.pack(pady=19)
	btn_escamotage2 = tk.Button(root, text="Escamoter Haut", command=escamotage_haut, width=15)
	btn_escamotage2.pack(pady=5, padx=15)
	
	canvas = tk.Canvas(root, width=400, height=300, bg="white")
	canvas.pack()
	canvas.create_line(100, 200, 200, 200, width=4)  
	canvas.create_line(120, 220, 180, 220, width=3) 
	canvas.create_line(100, 200, 50, 230, width=3)
	canvas.create_line(140, 200, 140, 250, width=2)
	canvas.create_line(180, 200, 180, 250, width=2)
	neck = canvas.create_line(200, 200, 250, 200, width=3)
	head = canvas.create_rectangle(250, 200, 300, 220, fill="lightgray")
	update_status()
	root.mainloop()
	
	
		


print("Serveur Modbus TCP démarré sur le port 502...")
StartTcpServer(context, address=("0.0.0.0", 502))
