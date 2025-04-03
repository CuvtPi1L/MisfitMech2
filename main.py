import os
from sim_code.SPsimulation import *

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