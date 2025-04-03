# File: plot_energy_vs_vy.py
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import sys
import os

def run_single_simulation(vy_value, constants_file='constants.txt', simulation_script='SPsimulation.py'):
    """
    Runs the simulation script SPsimulation.py for a given V_y
    and returns the calculated energy loss.
    """
    # Ensure the simulation script exists
    if not os.path.exists(simulation_script):
        print(f"Error: Simulation script '{simulation_script}' not found.", file=sys.stderr)
        return None

    # Ensure the constants file exists
    if not os.path.exists(constants_file):
         print(f"Error: Constants file '{constants_file}' not found.", file=sys.stderr)
         return None

    # Use the same Python interpreter that is running this script
    python_executable = sys.executable
    command = [
        python_executable,
        simulation_script,
        '--vy', str(vy_value),
        '--constants', constants_file
    ]

    try:
        # Run the simulation script as a subprocess
        # Setting cwd might be necessary if functions.py isn't found otherwise
        # cwd = os.path.dirname(os.path.abspath(__file__)) # Get dir of this script
        result = subprocess.run(
            command,
            capture_output=True,    # Capture stdout and stderr
            text=True,              # Decode output as text (UTF-8 default)
            check=True,             # Raise CalledProcessError if script fails (exit code != 0)
            timeout=300             # Add a timeout (e.g., 5 minutes per run)
            # cwd=cwd              # Set working directory if needed
        )
        # The simulation script should print only the energy loss value
        energy_loss = float(result.stdout.strip())
        print(f"  Successfully ran for V_y = {vy_value:<10.2f} -> Energy Loss = {energy_loss:.4e}")
        return energy_loss

    except subprocess.CalledProcessError as e:
        print(f"Error running simulation for V_y = {vy_value}: Process failed.", file=sys.stderr)
        print(f"  Command : {' '.join(e.cmd)}", file=sys.stderr)
        print(f"  Exit Code: {e.returncode}", file=sys.stderr)
        # Print stderr first as it likely contains the error message from the script
        if e.stderr:
             print(f"  Stderr  :\n{e.stderr.strip()}", file=sys.stderr)
        if e.stdout:
             print(f"  Stdout  :\n{e.stdout.strip()}", file=sys.stderr)
        return None # Indicate failure

    except ValueError:
        # This happens if the script printed something that isn't a valid float
        print(f"Error parsing energy loss for V_y = {vy_value}. Unexpected output.", file=sys.stderr)
        print(f"  Stdout received:\n{result.stdout.strip()}", file=sys.stderr)
        return None # Indicate failure

    except subprocess.TimeoutExpired:
        print(f"Error: Simulation timed out for V_y = {vy_value} (limit: 300s)", file=sys.stderr)
        return None # Indicate failure

    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred while running simulation for V_y = {vy_value}: {e}", file=sys.stderr)
        return None

def main():
    # --- Configuration ---
    simulation_script_name = 'SPsimulation.py'
    constants_file_name = 'constants.txt'

    # Define the range and number of V_y values to test (negative for downward velocity)
    vy_start = -5000.0   # m/s
    vy_end = -20000.0  # m/s
    num_points = 150      # Number of simulation runs

    # Generate the V_y values using numpy's linspace
    vy_values_to_test = np.linspace(vy_start, vy_end, num_points)

    # --- Run Simulations & Collect Data ---
    results_vy = []
    results_energy_loss = []

    print(f"Starting simulations using '{simulation_script_name}'...")
    print(f"Testing {num_points} V_y values from {vy_start:.1f} to {vy_end:.1f} m/s.")

    for vy in vy_values_to_test:
        energy_loss = run_single_simulation(vy, constants_file_name, simulation_script_name)

        # Only store results if the simulation ran successfully and returned a value
        if energy_loss is not None:
            results_vy.append(vy)
            results_energy_loss.append(energy_loss)
        else:
            print(f"  Skipping V_y = {vy:.2f} due to simulation error.")

    # --- Plotting ---
    if not results_vy:
        print("\nNo simulation results collected successfully. Cannot generate plot.")
        return

    print(f"\nCollected {len(results_vy)} results. Generating plot...")

    plt.figure(figsize=(10, 6)) # Adjust figure size as needed

    # Create the plot (Energy Loss vs V_y)
    plt.plot(results_vy, results_energy_loss, marker='o', linestyle='-', color='royalblue', label='Simulation Results')

    # Add labels and title
    plt.xlabel("Initial Vertical Velocity (V_y) [m/s]")
    plt.ylabel("Energy Loss [Joules]")
    plt.title("Projectile Energy Loss vs. Initial Vertical Velocity")

    # Add grid for better readability
    plt.grid(True, linestyle='--', alpha=0.6)

    # Optional: Invert x-axis if you want higher speeds (more negative V_y) to the right
    # plt.gca().invert_xaxis()

    # Add legend
    plt.legend()

    # Optional: Save the plot to a file
    plot_filename = 'energy_loss_vs_vy_plot.png'
    try:
        plt.savefig(plot_filename)
        print(f"Plot successfully saved to '{plot_filename}'")
    except Exception as e:
        print(f"Error saving plot to '{plot_filename}': {e}", file=sys.stderr)

    # Display the plot
    plt.show()

if __name__ == "__main__":
    main()