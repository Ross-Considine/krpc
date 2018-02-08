#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=  I M P O R T   #=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
import krpc, time, sys, config

if sys.version_info >= (3,0):
    isPython3 = True
    import tkinter as tk
else:
    isPython3 = False
    import Tkinter as tk

# R O O T
#===============================================================================
root = tk.Tk()

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#  C L A S S E S   =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=


class Application():

        # C O N S T R U C T O R
    #===========================================================================

    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack()


        #=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
        #=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#   GUI ELEMENTS   =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
        #=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
        #-----------------------------------------------------------------------
        # Buttons (2 control buttons and a quit button)

        self.bttn0 = tk.Button(frame, text = "Increase Altitude +", fg="red", command=self.printalt_up)
        self.bttn0.grid(row=0, column=1)
        self.bttn1 = tk.Button(frame, text = "Decrease Altitude -", fg="blue", command=self.printalt_down)
        self.bttn1.grid(row=1, column=1)
        self.bttnQuit = tk.Button(frame, text = "Quit", fg="green", command=self.bttn_Quit)
        self.bttnQuit.grid(row=2, column=1)

        #-----------------------------------------------------------------------
        # Label Descriptions

        self.label_0 = tk.Label(frame, text="Current\nAltitude").grid(row=2, column=2)
        self.label_1 = tk.Label(frame, text="Throttle\nSetting").grid(row=0, column=2)
        self.label_2 = tk.Label(frame, text="Target Height").grid(row=1, column=2)
        #self.label_3 = tk.Label(frame, text="Label Update").grid(row=0, column=2)

        # Label Contents (to be dynamically updated)

        #self.label_4 = tk.Label(frame, text=Running).grid(row=4, column=3)
        self.label_5 = tk.Label(frame, textvariable=update_throttle).grid(row=0, column=3)
        self.label_6 = tk.Label(frame, textvariable=update_alt).grid(row=2, column=3)
        self.label_7 = tk.Label(frame, textvariable=update_target).grid(row=1, column=3)

    #--------------------------------------------------------------------------------
    # Button Click Events

    def printalt_up(self):
        print("Increase Altitude +")
        config.var1 +=1
        #var2.set="Increase Altitude"
    def printalt_down(self):
        print("Decrease Altitude -")
        config.var1 -=1
    def bttn_Quit(event):
        vessel.control.gear = True
        time.sleep(2)

        while vessel.situation == conn.space_center.VesselSituation.flying:
            control.throttle = 0.28

        control.throttle = 0.0
        group.move_left()
        time.sleep(2.5)
        group.stop()
        vessel.control.lights = False
        time.sleep(0.1)
        root.destroy()
        exit()

#-----------------------------------------------------------------------------------
# Establishes a connection to the server

conn = krpc.connect(name='Hover 1.py')
#-----------------------------------------------------------------------------------

# Variable Name Definitions

canvas = conn.ui.stock_canvas
vessel = conn.space_center.active_vessel
control = vessel.control
flight = vessel.flight(vessel.orbit.body.reference_frame)
g = 9.81

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#   Dynamic Label Definitions   #=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
# Number Variable Definitions

update_target = tk.DoubleVar()
update_target.set(config.var1)

round_update_alt = float(flight.surface_altitude)
round(round_update_alt, 2)
update_alt = tk.DoubleVar()
update_alt.set(round_update_alt)

round_update_throttle = float(control.throttle)
round(round_update_throttle, 2)
update_throttle = tk.DoubleVar()
update_throttle.set(control.throttle)

#-----------------------------------------------------------------------------------
# Creates an object representing the active vessel

vessel = conn.space_center.active_vessel
#-----------------------------------------------------------------------------------
# Turn on the RCS and SAS system, brakes on!!

vessel.control.brakes = True
time.sleep(0.1)
vessel.control.rcs = True
time.sleep(0.1)
vessel.control.sas = True
time.sleep(0.1)
vessel.control.leg = True
time.sleep(0.1)
vessel.control.lights = True
time.sleep(0.1)

#-----------------------------------------------------------------------------------
# Extend Hover Engines

group = conn.infernal_robotics.servo_group_with_name(vessel, 'Arms')
if group is None:
    print('Group not found')
    exit(1)
#for servo in group.servos:
    #print(servo.name, servo.position, end=" ")
group.move_right()
time.sleep(2.5)
group.stop()
#-----------------------------------------------------------------------------------
# Launch procedure

print('Launch!')
vessel.control.activate_next_stage()
control.throttle = 0.4

vessel.control.gear = False
#-----------------------------------------------------------------------------------
# Basic Hover Script

def calcs():
    alt_error = (config.var1 - flight.surface_altitude)
    a = g - flight.vertical_speed + alt_error
    F = vessel.mass * a
    control.throttle = F / vessel.available_thrust

    update_target.set(config.var1)
    update_alt.set(flight.surface_altitude)
    update_throttle.set(control.throttle)
    root.after(200, calcs)
#-----------------------------------------------------------------------------------
#Start Application

app = Application(root)
root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',True)
root.after_idle(calcs)
root.title("KSP HoverBot")
root.mainloop()
