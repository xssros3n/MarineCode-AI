import subprocess
import sys
import os
from pathlib import Path

def launch_jarvis():
    """Launch both start_jarvis.py and agent.py simultaneously"""
    
    # Get current directory
    base_dir = Path(__file__).parent
    
    # Define paths
    start_jarvis_path = base_dir / "start_jarvis.py"
    agent_path = base_dir / "Jarvis_4.0" / "MarineCode-Main" / "agent.py"
    
    try:
        # Start start_jarvis.py
        print("Starting Jarvis main system...")
        process1 = subprocess.Popen([sys.executable, str(start_jarvis_path)])
        
        # Start agent.py with console command
        print("Starting Jarvis voice agent...")
        process2 = subprocess.Popen([sys.executable, str(agent_path), "console"], 
                                   cwd=str(agent_path.parent))
        
        print("Both Jarvis components are running!")
        print("Press Ctrl+C to stop both processes")
        
        # Wait for both processes
        process1.wait()
        process2.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down Jarvis...")
        process1.terminate()
        process2.terminate()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    launch_jarvis()