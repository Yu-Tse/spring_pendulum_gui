import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

params = {"g": 9.81, "dt": 0.001, "k": 10.0, "r0": 1.0, "m": 1.0,
          "rx": 1.2, "ry": 0.0, "drx": 0.0, "dry": 0.0}
t = 0
energy_data = []

def f1(x, y):
    r = np.hypot(x, y)
    return -params["k"] * (r - params["r0"]) * x / (params["m"] * r)

def f2(x, y):
    r = np.hypot(x, y)
    return params["g"] - params["k"] * (r - params["r0"]) * y / (params["m"] * r)

def runge_kutta(x, dx, y, dy):
    dt = params["dt"]
    k1x = dt * dx; k1y = dt * dy
    d1x = dt * f1(x, y); d1y = dt * f2(x, y)
    k2x = dt * (dx + d1x / 2); k2y = dt * (dy + d1y / 2)
    d2x = dt * f1(x + k1x / 2, y + k1y / 2); d2y = dt * f2(x + k1x / 2, y + k1y / 2)
    k3x = dt * (dx + d2x / 2); k3y = dt * (dy + d2y / 2)
    d3x = dt * f1(x + k2x / 2, y + k2y / 2); d3y = dt * f2(x + k2x / 2, y + k2y / 2)
    k4x = dt * (dx + d3x); k4y = dt * (dy + d3y)
    d4x = dt * f1(x + k3x, y + k3y); d4y = dt * f2(x + k3x, y + k3y)
    x2 = x + (k1x + 2*k2x + 2*k3x + k4x) / 6
    dx2 = dx + (d1x + 2*d2x + 2*d3x + d4x) / 6
    y2 = y + (k1y + 2*k2y + 2*k3y + k4y) / 6
    dy2 = dy + (d1y + 2*d2y + 2*d3y + d4y) / 6
    return x2, dx2, y2, dy2

def draw_spring(x, y, coils=20):
    r = np.hypot(x, y)
    theta = np.arctan2(y, x)
    points = []
    for i in range(coils + 1):
        t = r * i / coils
        offset = 0.1 * r * (-1)**i
        px = t * np.cos(theta) - offset * np.sin(theta)
        py = t * np.sin(theta) + offset * np.cos(theta)
        points.append((px, py))
    if points:
        sx, sy = zip(*points)
        return list(sx), list(sy)
    else:
        return [], []



root = tk.Tk()
root.title("Spring Pendulum Simulator")

def create_entry(label, key, row):
    ttk.Label(root, text=label).grid(column=0, row=row, sticky=tk.W)
    entry = ttk.Entry(root); entry.grid(column=1, row=row)
    entry.insert(0, str(params[key])); entries[key] = entry

def start_simulation():
    for key in entries:
        try: params[key] = float(entries[key].get())
        except ValueError: pass
    ani.event_source.start()

entries = {}; row = 0
for label, key in [("Mass (m)", "m"), ("Spring Constant (k)", "k"), ("Initial x", "rx"), ("Initial vx", "drx")]:
    create_entry(label, key, row); row += 1

start_btn = ttk.Button(root, text="Start", command=start_simulation)
start_btn.grid(column=0, row=row, columnspan=2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=2, rowspan=row+1)

ax1.set_xlim(-2, 2); ax1.set_ylim(-2, 2); ax1.set_aspect('equal')
spring_line, = ax1.plot([], [], 'b-')
mass_dot, = ax1.plot([], [], 'ro')

ax2.set_xlim(0, 10); ax2.set_ylim(0, 10)
kin_line, = ax2.plot([], [], label="Kinetic")
pot_line, = ax2.plot([], [], label="Potential")
tot_line, = ax2.plot([], [], label="Total")
ax2.legend()

def update(frame):
    global t

    for _ in range(10):
        params["rx"], params["drx"], params["ry"], params["dry"] = runge_kutta(
            params["rx"], params["drx"], params["ry"], params["dry"]
        )
        t += params["dt"]
        r = np.hypot(params["rx"], params["ry"])
        v2 = params["drx"]**2 + params["dry"]**2
        KE = 0.5 * params["m"] * v2
        PE = 0.5 * params["k"] * (r - params["r0"])**2 + params["m"] * params["g"] * params["ry"]
        energy_data.append((t, KE, PE, KE + PE))
    try:
        sx, sy = draw_spring(params["rx"], -params["ry"])
        # 強制轉換為list，並檢查長度，避免None或空
        if not (isinstance(sx, (list, tuple)) and isinstance(sy, (list, tuple)) and len(sx) > 0 and len(sy) > 0):
            sx, sy = [], []
        spring_line.set_data(sx, sy)
        mass_dot.set_data([params["rx"]], [-params["ry"]])  # 注意要用list或tuple
    except Exception as e:
        print("Error in draw_spring or mass_dot:", e)
        spring_line.set_data([], [])
        mass_dot.set_data([], [])

    if len(energy_data) > 0:
        times, ke, pe, te = zip(*energy_data)
        kin_line.set_data(times, ke)
        pot_line.set_data(times, pe)
        tot_line.set_data(times, te)
        ax2.set_xlim(0, max(10, t))
        ax2.set_ylim(0, max(te) * 1.1)
    return spring_line, mass_dot, kin_line, pot_line, tot_line


ani = FuncAnimation(fig, update, interval=20, blit=False, cache_frame_data=False)
ani.event_source.stop()
root.mainloop()
