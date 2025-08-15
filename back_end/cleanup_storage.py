"""
Storage cleanup utility
Cleans up test files and temporary data
"""
import os
import shutil
import glob
import time
from pathlib import Path

def cleanup_test_files():
    """Clean up test files and temporary RAG data"""
    print("🧹 Cleaning up test files and storage...")
    
    base_dir = Path(__file__).parent
    storage_dir = base_dir / "storage"
    
    if not storage_dir.exists():
        print("   ℹ️  No storage directory found")
        return
    
    # Clean test CSV files
    test_csvs = list(storage_dir.glob("*test*.csv"))
    for csv_file in test_csvs:
        try:
            csv_file.unlink()
            print(f"   ✅ Removed: {csv_file.name}")
        except Exception as e:
            print(f"   ⚠️  Could not remove {csv_file.name}: {e}")
    
    # Clean test text files
    test_txts = list(storage_dir.glob("*test*.txt")) + list(storage_dir.glob("*ml_guide*.txt")) + list(storage_dir.glob("*tech_terms*.txt"))
    for txt_file in test_txts:
        try:
            txt_file.unlink()
            print(f"   ✅ Removed: {txt_file.name}")
        except Exception as e:
            print(f"   ⚠️  Could not remove {txt_file.name}: {e}")
    
    # Clean old RAG data (older than 1 hour)
    rag_data_dir = storage_dir / "rag_data"
    if rag_data_dir.exists():
        current_time = time.time()
        
        for rag_folder in rag_data_dir.iterdir():
            if rag_folder.is_dir():
                # Check if folder is old (older than 1 hour)
                folder_time = rag_folder.stat().st_mtime
                if current_time - folder_time > 3600:  # 1 hour
                    try:
                        shutil.rmtree(rag_folder)
                        print(f"   ✅ Removed old RAG data: {rag_folder.name}")
                    except Exception as e:
                        print(f"   ⚠️  Could not remove RAG data {rag_folder.name}: {e}")
    
    # Clean test session files
    session_files = list(storage_dir.glob("session_*.json"))
    for session_file in session_files:
        try:
            # Only remove if older than 10 minutes
            if time.time() - session_file.stat().st_mtime > 600:
                session_file.unlink()
                print(f"   ✅ Removed old session: {session_file.name}")
        except Exception as e:
            print(f"   ⚠️  Could not remove {session_file.name}: {e}")
    
    print("🎉 Cleanup completed!")

if __name__ == "__main__":
    cleanup_test_files()
