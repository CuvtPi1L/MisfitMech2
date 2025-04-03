# File: SPsimulation.py
import numpy as np
import pandas as pd
import ast
import argparse  # Import argparse module
import sys       # To potentially print status messages to stderr

# Import functions from functions.py (make sure it's in the same directory)
try:
    from functions import Projectile, Spring, init_springs, is_touching, add_forces, push_outside
except ImportError:
    print("Error: functions.py not found. Make sure it's in the same directory.", file=sys.stderr)
    sys.exit(1)


def read_constants(filename="constants.txt"):
    """Reads constants from a specified file, handling inline comments."""
    constants = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Remove full-line comments and strip whitespace first
                line = line.split('#', 1)[0].strip()
                
                if line and '=' in line:  # Ensure line is not empty and contains an assignment
                    try:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        # The value part might still have had a comment removed,
                        # but we split it first, so value should be clean now.
                        value = value.strip() 

                        # Try converting to int, then float, else keep as string
                        try:
                            constants[key] = int(value)
                        except ValueError:
                            try:
                                constants[key] = float(value)
                            except ValueError:
                                # If it's neither int nor float, keep it as string (useful for future options)
                                # print(f"Warning: Could not convert value for '{key}' to number, keeping as string: '{value}'", file=sys.stderr)
                                constants[key] = value 
                    except ValueError:
                        # Handles cases where line has '=' but not in key=value format properly
                        print(f"Warning: Skipping malformed line in {filename}: {line}", file=sys.stderr)
                        
    except FileNotFoundError:
        print(f"Error: Constants file '{filename}' not found.", file=sys.stderr)
        sys.exit(1) # Exit if constants file is missing
    except Exception as e:
        print(f"Error reading constants file '{filename}': {e}", file=sys.stderr)
        sys.exit(1) # Exit on other file reading errors
        
    # --- Crucial Check: Ensure all required constants are loaded ---
    required_keys = ['N_springs', 'dx', 'm', 'k', 'M', 'V_X_projectile', 
                     'X_projectile_start', 'Y_projectile_start', 'R', 'dt', 
                     'timesteps', 'epsilon']
    missing_keys = [key for key in required_keys if key not in constants]
    if missing_keys:
        print(f"Error: Missing required constants in '{filename}': {', '.join(missing_keys)}", file=sys.stderr)
        sys.exit(1)
    # --- End Check ---
        
    return constants

def run_simulation(constants, V_y_initial):
    """Runs a single simulation for a given initial V_y and returns energy loss."""
    try:
        # Extract constants safely
        N_springs = int(constants['N_springs'])
        dx = float(constants['dx'])
        m = float(constants['m'])
        k = float(constants['k'])
        M = float(constants['M'])
        V_X = float(constants['V_X_projectile'])
        X = float(constants['X_projectile_start'])
        Y = float(constants['Y_projectile_start'])
        R = float(constants['R'])
        dt = float(constants['dt'])
        timesteps = int(constants['timesteps'])
        epsilon = float(constants['epsilon'])
    except KeyError as e:
        print(f"Error: Missing constant '{e}' in constants file.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid numeric value for a constant: {e}", file=sys.stderr)
        sys.exit(1)

    # Initialize simulation components
    springs = init_springs(N_springs, dx, k, m)
    projectile = Projectile(M, V_X, V_y_initial, X, Y, R) # Use V_y_initial here

    # Calculate initial energy
    # Using getEnergy() handles non-zero V_X if needed
    initial_energy = projectile.getEnergy()
    # If V_X is always 0, this is simpler:
    # initial_energy = 0.5 * M * V_y_initial**2

    # --- Simulation Loop ---
    for i in range(timesteps):
        for spring in springs:
            if is_touching(spring, projectile, epsilon):
                push_outside(spring, projectile, epsilon)

        Force = add_forces(springs, projectile, epsilon)
        projectile.update(Force[0], Force[1], dt)

        for spring in springs:
            restoring_F_X = -spring.get_F_X()
            restoring_F_Y = -spring.get_F_Y()
            spring.update(restoring_F_X, restoring_F_Y, dt)
    # --- End Simulation Loop ---

    final_energy = projectile.getEnergy()
    energy_loss = initial_energy - final_energy

    return energy_loss


def main():
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Run spring collision simulation for a single V_y.")
    parser.add_argument('--vy', type=float, required=True,
                        help='Initial vertical velocity (V_y) for the projectile (m/s).')
    parser.add_argument('--constants', type=str, default='constants.txt',
                        help='Path to the constants file (default: constants.txt).')
    args = parser.parse_args()
    # --- End Argument Parsing ---

    # Read constants from file specified
    constants = read_constants(args.constants)

    # Get the single V_y value from command line
    v_y = args.vy

    # Run simulation for the single V_y provided
    energy_loss = run_simulation(constants, v_y)

    # --- Output ---
    # Print *only* the final energy loss value to standard output.
    # This allows the calling script to easily capture it.
    print(f"{energy_loss}")

    # Optional: Print status to standard error (stderr) for monitoring
    # print(f"Simulation complete for V_y = {v_y:.2f} m/s. Energy Loss: {energy_loss:.4e}", file=sys.stderr)


if __name__ == "__main__":
    main()