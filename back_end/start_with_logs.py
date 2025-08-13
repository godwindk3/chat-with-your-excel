#!/usr/bin/env python3
"""
Start the FastAPI server with enhanced logging for debugging file deletion issues.
Usage: python start_with_logs.py
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    print("🚀 Starting Excel Analysis API with enhanced logging...")
    print("📝 Logs will be saved to: logs/server_YYYY-MM-DD.log")
    print("🔍 Watch for detailed file deletion logs with emojis")
    print("=" * 60)
    
    # Create logs directory if it doesn't exist
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            # Disable uvicorn's default logging format since we have our own
            access_log=True,
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
