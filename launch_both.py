import subprocess
import sys
import os
from pathlib import Path

def main():
    # Get the current directory
    base_dir = Path(__file__).parent
    
    # Define paths
    start_marinecode_path = base_dir / "start_marinecode.py"
    agent_path = base_dir / "MarineCode_4.0" / "MarineCode-Main" / "agent.py"
    
    # Check if files exist
    if not start_marinecode_path.exists():
        print(f"Error: {start_marinecode_path} not found")
        return
    
    if not agent_path.exists():
        print(f"Error: {agent_path} not found")
        return
    
    print("Starting MarineCode components...")
    
    try:
        # Start both processes
        process1 = subprocess.Popen([sys.executable, str(start_marinecode_path)])
        process2 = subprocess.Popen([sys.executable, str(agent_path), "console"], 
                                  cwd=str(agent_path.parent))
        
        print(f"Started start_marinecode.py (PID: {process1.pid})")
        print(f"Started agent.py (PID: {process2.pid})")
        print("Both processes are running. Press Ctrl+C to stop both.")
        
        # Wait for both processes
        process1.wait()
        process2.wait()
        
    except KeyboardInterrupt:
        print("\nStopping processes...")
        process1.terminate()
        process2.terminate()
        process1.wait()
        process2.wait()
        print("Both processes stopped.")

if __name__ == "__main__":
    main()