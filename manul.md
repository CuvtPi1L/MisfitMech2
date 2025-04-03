This code was written in such a way that to get the plots, you only have to run plot_energy_vs_vy.py. Nothing else needs to be run directly to generate the plot. 

To change any constants (like the timesteps per simulation), you only need to go into the constants.txt file and change it directly, as SPsimulation.py reads the .txt file directly. 

To get more points on the energy loss vs velocity plot, you need to go under def main(): on plot_energy_vs_vy.py and find where it says num_points and set it equal to the number of points you want on the plot. 

Increasing the number of timesteps per simulation and the number of simulations may help smooth out the graph, though the included picture here with 10000 timesteps and 1500 simulations was still jagged. 
