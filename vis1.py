import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import threading
import time

base_ip = "http://192.168.86.14:5000"  # Update with your server's IP

# Fetch data from an endpoint
def fetch_data(endpoint):
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch data: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# Update the UI periodically
def update_ui():
    while True:
        # Fetch data for all PLCs
        plc1_data = fetch_data(f"{base_ip}/plc1")
        plc2_data = fetch_data(f"{base_ip}/plc2")
        plc3_data = fetch_data(f"{base_ip}/plc3")

        # Update PLC1 data
        plc1_temp_label.config(text=f"Temperature: {plc1_data.get('temperature', 'N/A')} °C")

        # Update PLC2 data
        plc2_temp_label.config(text=f"Temperature: {plc1_data.get('temperature', 'N/A')} °C")  # Shared temperature
        window_state = "open" if plc2_data.get("window", 0) == 1 else "close"
        curtain_state = "open" if plc2_data.get("curtain", 0) == 1 else "close"
        window_label.config(image=window_images[window_state])
        window_label.image = window_images[window_state]
        curtain_label.config(image=curtain_images[curtain_state])
        curtain_label.image = curtain_images[curtain_state]

        # Update PLC3 data
        ac_state = "on" if plc3_data.get("ac_state", 0) == 1 else "off"
        ac_temp = plc3_data.get("ac_temp", "N/A")
        ac_label.config(image=ac_images[ac_state])
        ac_label.image = ac_images[ac_state]
        ac_temp_label.config(text=f"AC Temp: {ac_temp if ac_state == 'on' else 'Off'}")

        time.sleep(1)

# Toggle control state
def toggle_control():
    global control_state
    if control_state == "OFF":
        control_state = "ON"
        control_button.config(text="Take Control: ON")
        set_control_parameters("on")
        set_controls_frame.pack(pady=20)
    else:
        control_state = "OFF"
        control_button.config(text="Take Control: OFF")
        set_control_parameters("off")
        set_controls_frame.pack_forget()

# Send control parameters to all PLCs
def set_control_parameters(state):
    try:
        requests.post(f"{base_ip}/plc1/update", json={"control": state})
        requests.post(f"{base_ip}/plc2", json={"control": state})
        requests.post(f"{base_ip}/plc3", json={"control": state})
        print(f"Control set to {state}")
    except Exception as e:
        print(f"Error setting control parameters: {e}")

# Apply control settings
def set_plc_values():
    plc1_temp = plc1_temp_input.get()
    window_state = window_state_var.get()
    curtain_state = curtain_state_var.get()
    ac_state = ac_state_var.get()
    ac_temp = ac_temp_input.get() if ac_state == "on" else None

    try:
        if plc1_temp:
            requests.post(f"{base_ip}/plc1/update", json={"temperature": plc1_temp})

        if window_state:
            window_state_int = 1 if window_state == "open" else 0
            requests.post(f"{base_ip}/plc2", json={"window": window_state_int})

        if curtain_state:
            curtain_state_int = 1 if curtain_state == "open" else 0
            requests.post(f"{base_ip}/plc2", json={"curtain": curtain_state_int})

        if ac_state:
            ac_state_int = 1 if ac_state == "on" else 0
            requests.post(f"{base_ip}/plc3", json={"ac_state": ac_state_int})

            if ac_state == "on" and ac_temp:
                requests.post(f"{base_ip}/plc3", json={"ac_temp": ac_temp})

        print("PLC values updated successfully.")
    except Exception as e:
        print(f"Error updating PLC values: {e}")

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

# Div1: PLCs in a row
div1 = ttk.Frame(root)
div1.pack(pady=20)

plc1_container = ttk.Frame(div1)
plc1_container.pack(side=tk.LEFT, padx=10)
ttk.Label(plc1_container, image=plc1_image).pack()
plc1_temp_label = ttk.Label(plc1_container, text="Temperature: Loading...")
plc1_temp_label.pack()

plc2_container = ttk.Frame(div1)
plc2_container.pack(side=tk.LEFT, padx=10)
ttk.Label(plc2_container, image=plc2_image).pack()
plc2_temp_label = ttk.Label(plc2_container, text="Temperature: Loading...")
plc2_temp_label.pack()

plc3_container = ttk.Frame(div1)
plc3_container.pack(side=tk.LEFT, padx=10)
ttk.Label(plc3_container, image=plc3_image).pack()
plc3_temp_label = ttk.Label(plc3_container, text="Temperature: Loading...")
plc3_temp_label.pack()

# Div2: Controls
div2 = ttk.Frame(root)
div2.pack(pady=20)

window_label = ttk.Label(div2, text="Loading...")
window_label.pack(side=tk.LEFT, padx=5)

curtain_label = ttk.Label(div2, text="Loading...")
curtain_label.pack(side=tk.LEFT, padx=5)

ac_label = ttk.Label(div2, text="Loading...")
ac_label.pack(side=tk.LEFT, padx=5)

ac_temp_label = ttk.Label(div2, text="AC Temp: Loading...")
ac_temp_label.pack(side=tk.LEFT, padx=5)

# Div3: Control button
div3 = ttk.Frame(root)
div3.pack(pady=20)

control_state = "OFF"
control_button = ttk.Button(div3, text="Take Control: OFF", command=toggle_control)
control_button.pack()

# Div4: Set control inputs
set_controls_frame = ttk.Frame(root)
set_controls_frame.pack_forget()

plc1_temp_input = ttk.Entry(set_controls_frame)
plc1_temp_input.grid(row=0, column=1, padx=5, pady=5)
ttk.Label(set_controls_frame, text="Set PLC1 Temperature").grid(row=0, column=0, padx=5, pady=5)

window_state_var = ttk.Combobox(set_controls_frame, values=["open", "close"])
window_state_var.grid(row=1, column=1, padx=5, pady=5)
ttk.Label(set_controls_frame, text="Set Window").grid(row=1, column=0, padx=5, pady=5)

curtain_state_var = ttk.Combobox(set_controls_frame, values=["open", "close"])
curtain_state_var.grid(row=2, column=1, padx=5, pady=5)
ttk.Label(set_controls_frame, text="Set Curtain").grid(row=2, column=0, padx=5, pady=5)

ac_state_var = ttk.Combobox(set_controls_frame, values=["on", "off"])
ac_state_var.grid(row=3, column=1, padx=5, pady=5)
ttk.Label(set_controls_frame, text="Set AC").grid(row=3, column=0, padx=5, pady=5)

ac_temp_input = ttk.Entry(set_controls_frame)
ac_temp_input.grid(row=4, column=1, padx=5, pady=5)
ttk.Label(set_controls_frame, text="Set AC Temperature").grid(row=4, column=0, padx=5, pady=5)

apply_button = ttk.Button(set_controls_frame, text="Apply", command=set_plc_values)
apply_button.grid(row=5, columnspan=2, pady=10)

# Start UI update thread
threading.Thread(target=update_ui, daemon=True).start()

# Run application
root.mainloop()
