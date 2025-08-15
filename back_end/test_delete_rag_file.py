#!/usr/bin/env python3
"""
Test script for RAG file deletion functionality
"""

import requests
import json

API_BASE = "http://localhost:8000/api"

def test_delete_rag_file():
    print("🧪 Testing RAG File Delete Functionality")
    print("=" * 50)
    
    # Test 1: List RAG files
    print("\n📂 Test 1: Listing RAG files")
    try:
        response = requests.get(f"{API_BASE}/rag/files")
        if response.status_code == 200:
            files = response.json()
            print(f"✅ Found {len(files)} RAG files")
            for file in files:
                print(f"   - {file['filename']} (ID: {file['fileId']})")
            
            if len(files) == 0:
                print("ℹ️  No files to test deletion. Upload a file first.")
                return
                
        else:
            print(f"❌ Failed to list files: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error listing files: {e}")
        return
    
    # Test 2: List RAG sessions before deletion
    print("\n💬 Test 2: Listing RAG sessions before deletion")
    try:
        response = requests.get(f"{API_BASE}/rag/sessions")
        if response.status_code == 200:
            sessions_before = response.json()
            print(f"✅ Found {len(sessions_before)} RAG sessions before deletion")
            for session in sessions_before:
                print(f"   - {session['sessionName']} for file {session['filename']}")
        else:
            print(f"❌ Failed to list sessions: {response.status_code}")
    except Exception as e:
        print(f"❌ Error listing sessions: {e}")
    
    # Test 3: Test delete functionality (interactive)
    print("\n🗑️  Test 3: File deletion test")
    print("This test requires manual confirmation.")
    print("Please use the web interface to test file deletion:")
    print(f"1. Go to: http://localhost:3000/rag")
    print("2. Switch to 'Choose Existing' tab")
    print("3. Click the 🗑️ button on a file")
    print("4. Confirm deletion")
    print("5. Verify file is removed from list")
    print("6. Check that related sessions are also deleted")
    
    # Test 4: Verify API endpoint works
    print("\n🔧 Test 4: API endpoint verification")
    if len(files) > 0:
        test_file = files[0]
        print(f"Testing delete endpoint for file: {test_file['filename']}")
        print(f"Endpoint: DELETE {API_BASE}/rag/file/{test_file['fileId']}")
        print("⚠️  This would actually delete the file - skipping automatic test")
        print("   Use manual testing through web interface instead")
    
    print("\n" + "=" * 50)
    print("🎯 RAG file deletion test information provided!")
    print("Use the web interface to test the actual deletion functionality.")

if __name__ == "__main__":
    test_delete_rag_file()
