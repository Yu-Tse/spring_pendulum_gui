# 🌀 Spring Pendulum Simulator (Tkinter GUI)

This is a spring pendulum simulator using Python and Tkinter for GUI. It numerically solves a 2D spring pendulum with two degrees of freedom using the Runge-Kutta method, and visualizes the result in real time.

## 🧩 Features
- Real-time GUI input for:
  - Mass
  - Spring constant
  - Initial position
  - Initial velocity
- Spring animation with coils
- Energy diagram (kinetic, potential, total)

---

## Model Description

This simulation is based on the following physical model:

* The spring pendulum is suspended from the origin, with spring constant \$k\$ and mass \$m\$.
* The position vector of the mass is \$\vec{r} = r\_x \hat{i} + r\_y \hat{j}\$, and the natural length of the spring is \$r\_0\$.
* The spring force is given by \$\vec{F}\_s = -k(|\vec{r}| - r\_0) \dfrac{\vec{r}}{|\vec{r}|}\$,
  where \$|\vec{r}| = \sqrt{r\_x^2 + r\_y^2}\$.

The forces acting on the mass are:

* Spring restoring force \$\vec{F}\_s\$
* Gravitational force \$mg\$ (downward)

According to Newton’s second law, the equations of motion are:

```
⎧ $\ddot{r}_x = -\dfrac{k (|\vec{r}| - r_0)}{m|\vec{r}|} r_x$
⎨ $\ddot{r}_y = g - \dfrac{k (|\vec{r}| - r_0)}{m|\vec{r}|} r_y$
```

Or, as two separate equations (for best compatibility):

* \$\ddot{r}\_x = -\dfrac{k (|\vec{r}| - r\_0)}{m|\vec{r}|} r\_x\$
* \$\ddot{r}\_y = g - \dfrac{k (|\vec{r}| - r\_0)}{m|\vec{r}|} r\_y\$

---

<img width="865" height="995" alt="image" src="https://github.com/user-attachments/assets/39aca4f1-9be6-446b-8c44-9e20e63ba625" />

---

## Coordinate System

> **The coordinate directions used in this program are consistent with the window (screen) coordinates: right is $+x$, down is $+y$.**
> **As a result, there is no need for additional coordinate transformations in the simulation code or when drawing the results.**
>
> You can directly use $(r_x, r_y)$ in both calculations and visualization, and the mapping to the display will be correct.

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python main.py
```

## 📸 Preview

- Left: 2D spring pendulum animation
- Right: Energy-time plot

## 🛠 Requirements

- Python 3.7+
- Tkinter (bundled with Python)
- numpy
- matplotlib

## 🙋‍♂️ Author

**Yu-Tse Wu** (吳雨澤)  
*Master’s Student at the Institute of Innovation and Semiconductor Manufacturing, National Sun Yat-sen University*

GitHub: [@Yu-Tse](https://github.com/Yu-Tse)
