#!/usr/bin/env python3
"""
View the latest server logs with real-time tail functionality.
Usage: python view_logs.py [--follow]
"""

import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

def find_latest_log():
    """Find the most recent log file"""
    logs_dir = Path(__file__).parent / "logs"
    if not logs_dir.exists():
        print("❌ Logs directory doesn't exist yet. Start the server first.")
        return None
    
    log_files = list(logs_dir.glob("server_*.log"))
    if not log_files:
        print("❌ No log files found. Start the server first.")
        return None
    
    # Get the most recent log file
    latest_log = max(log_files, key=lambda f: f.stat().st_mtime)
    return latest_log

def tail_file(filepath, follow=False):
    """Tail a file, optionally following new lines"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Read existing content
            content = f.read()
            if content:
                print(content, end='')
            
            if follow:
                print(f"\n{'='*60}")
                print(f"📖 Following log file: {filepath}")
                print(f"🔄 Press Ctrl+C to stop")
                print(f"{'='*60}")
                
                # Follow new lines
                while True:
                    line = f.readline()
                    if line:
                        print(line, end='')
                    else:
                        time.sleep(0.1)
                        
    except KeyboardInterrupt:
        print("\n🛑 Stopped following logs")
    except Exception as e:
        print(f"❌ Error reading log file: {e}")

def main():
    parser = argparse.ArgumentParser(description="View server logs")
    parser.add_argument("--follow", "-f", action="store_true", 
                       help="Follow the log file for new entries")
    args = parser.parse_args()
    
    latest_log = find_latest_log()
    if not latest_log:
        return
    
    print(f"📄 Viewing log file: {latest_log}")
    print(f"📅 Last modified: {datetime.fromtimestamp(latest_log.stat().st_mtime)}")
    print(f"📊 File size: {latest_log.stat().st_size} bytes")
    print("=" * 60)
    
    tail_file(latest_log, follow=args.follow)

if __name__ == "__main__":
    main()
