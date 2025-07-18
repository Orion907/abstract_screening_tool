#!/usr/bin/env python3
"""
Abstract Screening Tool Demo Launcher

This script launches the Streamlit demo application.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Launch the Streamlit demo application."""
    
    # Get the directory of this script
    script_dir = Path(__file__).parent
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Path to the main Streamlit app
    app_path = script_dir / "src" / "ui" / "streamlit_app.py"
    
    # Check if the app file exists
    if not app_path.exists():
        print(f"❌ Error: Streamlit app not found at {app_path}")
        sys.exit(1)
    
    print("🚀 Launching Abstract Screening Tool Demo...")
    print(f"📁 Working directory: {script_dir}")
    print(f"📄 App file: {app_path}")
    
    # Launch Streamlit
    try:
        subprocess.run([
            "streamlit", "run", str(app_path),
            "--server.headless", "false",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()