
import tkinter as tk
from pydub.generators import Square
from pyo import *
from PIL import Image, ImageTk

import sys
import io





s = Server().boot()
s.amp = 0.3
s.start()


# Create a string buffer to capture the output
output = io.StringIO()

# Redirect standard output to the string buffer
sys.stdout = output

# List all audio devices
pa_list_devices()

# Reset standard output to default
sys.stdout = sys.__stdout__

# Get the captured output as a string
device_list = output.getvalue()[15:].splitlines()

# Print or process the device list
print("heres the :",device_list)

for device in device_list:
    print("number",device.split("OUT")[0][:-2])
    print("the rest:,",device.split("OUT")[0])






#volume and freqs
amp = Sig(0.0)
carrier_base = Sig(220)
lfo_freq = Sig(0.5)

#defining 3 waves for LFO
mod_sine = Sine(freq=lfo_freq, mul=100, add=200)
mod_saw = LFO(freq=lfo_freq,type=0 ,mul=100, add=200)
mod_square = LFO(freq=lfo_freq,type=2, mul=100, add=200)

#selecting LFO
selector_LFO = Sig(0)
mod = Selector([mod_sine, mod_saw, mod_square], voice=selector_LFO)


#defining 3 waves for carrier
sine_osc = Sine(freq=carrier_base + mod, mul=amp)
saw_osc = SuperSaw(freq=carrier_base + mod, mul=amp)
square_osc = LFO(freq=carrier_base + mod, type=2, mul=amp)

#selecting carrier
selector_carrier = Sig(0)
pre_fx = Selector([sine_osc, saw_osc, square_osc], voice=selector_carrier)#.mix(2).out()


#effects section
#delay = Sig(0)
#feedback = Sig(0)
smooth_delay = SigTo(value=0, time=0.05, init=0.2)
smooth_feedback = SigTo(value=0, time=0.05, init=0.2)
d = Delay(pre_fx, delay=smooth_delay, feedback=smooth_feedback)

post_fx = d.mix(2).out()




#gui stuff
root = tk.Tk()
image = Image.open("metal.png").resize((800, 600))
bg_image = ImageTk.PhotoImage(image)
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)

# Place the background image on the canvas
canvas.create_image(0, 0, image=bg_image, anchor="nw")


#:LFO section
def update_lfo_freq(val):
    lfo_freq.value = float(val)
lfo_slider = tk.Scale(root, from_=0.1, to=10, resolution=0.01, orient=tk.HORIZONTAL,label="LFO FREQUENCY", command=update_lfo_freq,length=400)
lfo_slider.set(0.5)
lfo_slider.pack()
canvas.create_window(300, 100, window=lfo_slider)

def update_wave_lfo(val):
    selector_LFO.value = int(val)
lfo_slider = tk.Scale(root, from_=0, to=2, orient=tk.HORIZONTAL,label="LFO SWITCH", command=update_wave_lfo,length=400)
lfo_slider.set(0)
lfo_slider.pack()
canvas.create_window(300, 150, window=lfo_slider)

#CARRIER settings
def update_carrier_freq(val):
    carrier_base.value = float(val)
carrier_slider = tk.Scale(root, from_=0, to=1000, resolution=1, orient=tk.HORIZONTAL, label="CARRIER FREQUENCY", command=update_carrier_freq,length=400)
carrier_slider.set(220)
carrier_slider.pack()
canvas.create_window(300, 200, window=carrier_slider)

def update_wave_carrier(val):
    selector_carrier.value = int(val)
wave_slider = tk.Scale(root, from_=0, to=2, orient=tk.HORIZONTAL,label="CARRIER SWITCH",command=update_wave_carrier,length=400)
wave_slider.set(0)
wave_slider.pack()
canvas.create_window(300, 250, window=wave_slider)

#effects section

#delay
def update_delay(val):
    smooth_delay.value = float(val)
delay_slider = tk.Scale(root, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, label="DELAY", command=update_delay,length=400)
delay_slider.set(0.0)
delay_slider.pack()
canvas.create_window(300, 300, window=delay_slider)



def update_feedback(val):
    smooth_feedback.value = float(val)
feedback_slider = tk.Scale(root, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, label="FEEDBACK", command=update_feedback,length=400)
feedback_slider.set(0.0)
feedback_slider.pack()
canvas.create_window(300, 350, window=feedback_slider)


#amplitude
def update_amp(val):
    amp.value = float(val)
amp_slider = tk.Scale(root, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, label="AMPLITUDE", command=update_amp,length=400)
amp_slider.set(0.0)
amp_slider.pack()
canvas.create_window(300, 400, window=amp_slider)


root.title("Dub Siren Controller")
root.resizable(False, False)
root.geometry("600x600")

#632 x 894


root.mainloop()





#s.gui(locals())