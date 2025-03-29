Hello Reader, Welcome to the MISSFIT MECH GROUP STUFF

General Purpose
    Our code simulates the interaction between micro-meteors colliding with the hull of a spacecraft.
    We modle our hull as an array of springs.

We will have three main files

1. Functions.py
    This will consist of two classes and some methods
    - Classes:
        - Spring
        - Particle
    - Methods:
        - Init_Springs
        - Is_touching
        - Add_froces
        - Push_Outside
2. Spring_Particle_Interaction_Sim.py
    This function will take a text file of constants, and produce simulations. Each simulations will yield an
    energy loss delta_E.
    - It either has variable velocity, or variable mass.
    - Returns a CSV with two columns; delta_E and either mass or V_y
3. Plotter.py
    - This takes the CSV from Spring_Particle_Interaction_Sim and produces a plot
    - We will have one plot for delta_E vs V_y, and one for delta_E vs M
    - Potentially a 3d plot with all three.