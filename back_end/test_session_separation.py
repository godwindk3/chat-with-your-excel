#!/usr/bin/env python3
"""
Test script to verify session separation between pandas and RAG
"""

import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8000/api"

def test_session_separation():
    print("🧪 Testing Session Separation between Pandas and RAG")
    print("=" * 60)
    
    # Test 1: Get pandas sessions
    print("\n📊 Test 1: Getting pandas sessions")
    try:
        response = requests.get(f"{API_BASE}/sessions")
        if response.status_code == 200:
            pandas_sessions = response.json()
            print(f"✅ Found {len(pandas_sessions)} pandas sessions")
            for session in pandas_sessions:
                session_type = session.get('sessionType', 'pandas')
                if session_type != 'pandas':
                    print(f"❌ ERROR: Found non-pandas session in pandas endpoint: {session}")
                else:
                    print(f"   ✓ Pandas session: {session['sessionId']} (type: {session_type})")
        else:
            print(f"❌ Failed to get pandas sessions: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting pandas sessions: {e}")
    
    # Test 2: Get RAG sessions  
    print("\n🤖 Test 2: Getting RAG sessions")
    try:
        response = requests.get(f"{API_BASE}/rag/sessions")
        if response.status_code == 200:
            rag_sessions = response.json()
            print(f"✅ Found {len(rag_sessions)} RAG sessions")
            for session in rag_sessions:
                session_type = session.get('sessionType', 'rag')
                if session_type != 'rag':
                    print(f"❌ ERROR: Found non-RAG session in RAG endpoint: {session}")
                else:
                    print(f"   ✓ RAG session: {session['sessionId']} (type: {session_type})")
        else:
            print(f"❌ Failed to get RAG sessions: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting RAG sessions: {e}")
    
    # Test 3: Check all sessions count
    print("\n📈 Test 3: Session count validation")
    try:
        # Get all sessions by reading storage directly
        from app.services.session_store import list_sessions
        all_sessions = list_sessions()
        pandas_count = len([s for s in all_sessions if s.get('sessionType', 'pandas') == 'pandas'])
        rag_count = len([s for s in all_sessions if s.get('sessionType', 'pandas') == 'rag'])
        
        print(f"📊 Total sessions in storage: {len(all_sessions)}")
        print(f"   - Pandas sessions: {pandas_count}")
        print(f"   - RAG sessions: {rag_count}")
        
        # Compare with API results
        api_pandas_count = len(pandas_sessions) if 'pandas_sessions' in locals() else 0
        api_rag_count = len(rag_sessions) if 'rag_sessions' in locals() else 0
        
        if api_pandas_count == pandas_count:
            print(f"✅ Pandas API correctly returns {pandas_count} sessions")
        else:
            print(f"❌ Pandas API mismatch: API={api_pandas_count}, Storage={pandas_count}")
            
        if api_rag_count == rag_count:
            print(f"✅ RAG API correctly returns {rag_count} sessions")
        else:
            print(f"❌ RAG API mismatch: API={api_rag_count}, Storage={rag_count}")
            
    except Exception as e:
        print(f"❌ Error in session count validation: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Session separation test completed!")

if __name__ == "__main__":
    test_session_separation()
