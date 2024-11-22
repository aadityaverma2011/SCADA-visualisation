import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import threading
import time

base_ip = "http://172.27.113.135:8085"

# Fetch data from endpoints
def fetch_data(endpoint):
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch data: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# Update UI dynamically
def update_ui():
    while True:
        # Fetch data from endpoints
        plc1_data = fetch_data(f"{base_ip}/plc1")
        plc2_data = fetch_data(f"{base_ip}/plc2")
        plc3_data = fetch_data(f"{base_ip}/plc3")

        # Update PLC1 Temperature
        plc1_temp_label.config(text=f"Temperature: {plc1_data.get('temperature', 'N/A')} °C")

        # Update PLC2 Temperature and Dynamic Images
        plc2_temp_label.config(text=f"Temperature: {plc2_data.get('temperature', 'N/A')} °C")
        window_state = plc2_data.get("window", "close")
        curtain_state = plc2_data.get("curtain", "close")
        window_label.config(image=window_images[window_state])
        window_label.image = window_images[window_state]
        curtain_label.config(image=curtain_images[curtain_state])
        curtain_label.image = curtain_images[curtain_state]

        # Update PLC3 Temperature, AC State, and Dynamic Images
        plc3_temp_label.config(text=f"Temperature: {plc3_data.get('temperature', 'N/A')} °C")
        ac_state = plc3_data.get("AC_state", "off")
        ac_temperature = plc3_data.get("AC_temperature", "N/A")
        ac_label.config(image=ac_images[ac_state])
        ac_label.image = ac_images[ac_state]
        ac_temp_label.config(text=f"AC Temp: {ac_temperature if ac_state == 'on' else 'off'}")

        time.sleep(3)

# Toggle control button state
def toggle_control():
    global control_state
    if control_state == "OFF":
        control_state = "ON"
        control_button.config(text="Take Control: ON")
    else:
        control_state = "OFF"
        control_button.config(text="Take Control: OFF")

# Main application
root = tk.Tk()
root.title("PLC Visualizer")
root.geometry("900x700")

# Load images
plc1_image = ImageTk.PhotoImage(Image.open("plc1.png").resize((100, 100)))
plc2_image = ImageTk.PhotoImage(Image.open("plc2.png").resize((100, 100)))
plc3_image = ImageTk.PhotoImage(Image.open("plc3.png").resize((100, 100)))

window_images = {
    "open": ImageTk.PhotoImage(Image.open("window_open.png").resize((100, 100))),
    "close": ImageTk.PhotoImage(Image.open("window_close.png").resize((100, 100))),
}
curtain_images = {
    "open": ImageTk.PhotoImage(Image.open("curtain_open.png").resize((100, 100))),
    "close": ImageTk.PhotoImage(Image.open("curtain_close.png").resize((100, 100))),
}
ac_images = {
    "on": ImageTk.PhotoImage(Image.open("ac_on.png").resize((100, 100))),
    "off": ImageTk.PhotoImage(Image.open("ac_off.png").resize((100, 100))),
}

# Div1: PLCs in a single horizontal line
div1 = ttk.Frame(root)
div1.pack(pady=20)

# PLC1
plc1_container = ttk.Frame(div1)
plc1_container.pack(side=tk.LEFT, padx=10)
ttk.Label(plc1_container, image=plc1_image).pack()
plc1_temp_label = ttk.Label(plc1_container, text="Temperature: Loading...")
plc1_temp_label.pack()

# Dashed line between PLC1 and PLC2
line1_canvas = tk.Canvas(div1, width=100, height=20, bg="white", highlightthickness=0)
line1_canvas.pack(side=tk.LEFT, padx=10)
line1_canvas.create_line(10, 10, 90, 10, dash=(4, 2))  # Horizontal dashed line

# PLC2
plc2_container = ttk.Frame(div1)
plc2_container.pack(side=tk.LEFT, padx=10)
ttk.Label(plc2_container, image=plc2_image).pack()
plc2_temp_label = ttk.Label(plc2_container, text="Temperature: Loading...")
plc2_temp_label.pack()

# Dashed line between PLC2 and PLC3
line2_canvas = tk.Canvas(div1, width=100, height=20, bg="white", highlightthickness=0)
line2_canvas.pack(side=tk.LEFT, padx=10)
line2_canvas.create_line(10, 10, 90, 10, dash=(4, 2))  # Horizontal dashed line

# PLC3
plc3_container = ttk.Frame(div1)
plc3_container.pack(side=tk.LEFT, padx=10)
ttk.Label(plc3_container, image=plc3_image).pack()
plc3_temp_label = ttk.Label(plc3_container, text="Temperature: Loading...")
plc3_temp_label.pack()

# Div2: Control images below Div1
div2 = ttk.Frame(root)
div2.pack(pady=20)

# Dynamic controls (Window, Curtain, and AC) in the same row
dynamic_frame = ttk.Frame(div2)
dynamic_frame.pack(pady=20)

# Window control
window_label = ttk.Label(dynamic_frame, text="Loading...")
window_label.pack(side=tk.LEFT, padx=5)

# Curtain control
curtain_label = ttk.Label(dynamic_frame, text="Loading...")
curtain_label.pack(side=tk.LEFT, padx=5)

# AC control
ac_label = ttk.Label(dynamic_frame, text="Loading...")
ac_label.pack(side=tk.LEFT, padx=5)

# AC temperature control
ac_temp_label = ttk.Label(dynamic_frame, text="AC Temp: Loading...")
ac_temp_label.pack(side=tk.LEFT, padx=5)

# Div3: Take Control Button
div3 = ttk.Frame(root)
div3.pack(pady=20)

control_state = "OFF"  # Initial state of the control button
control_button = ttk.Button(div3, text="Take Control: OFF", command=toggle_control)
control_button.pack()

# Start update thread
threading.Thread(target=update_ui, daemon=True).start()

# Run application
root.mainloop()
