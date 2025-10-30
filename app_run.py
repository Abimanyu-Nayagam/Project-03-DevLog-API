from dotenv import load_dotenv
import subprocess

try:
    load_dotenv(override=True)
    commands =["flask", "run"]
    subprocess.run(commands)
    print("Flask Server Started successfully")
except FileNotFoundError as fileerror:
    print(".env file not found")
except subprocess.CalledProcessError as commanderror:
    print(f"Error: Command failed with exit code {commanderror}")
except Exception as e:
    print(f"Error: {e}")

