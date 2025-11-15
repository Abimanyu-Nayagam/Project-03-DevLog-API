from dotenv import load_dotenv
import subprocess

try:
    load_dotenv(override=True)
    print("Starting Flask server...")
    subprocess.Popen(["flask", "run"])
    print("Flask server started successfully")
    print("Starting React server...")
    subprocess.Popen(["npm", "run", "dev"],shell=True)
    print("React server started successfully")
except FileNotFoundError as fileerror:
    print(".env file not found")
except subprocess.CalledProcessError as commanderror:
    print(f"Error: Command failed with exit code {commanderror}")
except Exception as e:
    print(f"Error: {e}")

