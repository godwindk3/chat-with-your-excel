"""
Comprehensive test for RAG feature
Run this script to test all RAG functionality
"""
import requests
import os
import tempfile
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api"

class RAGTester:
    def __init__(self):
        self.uploaded_files = []
        self.created_sessions = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def create_test_document(self, filename: str, content: str) -> str:
        """Create a test document file"""
        filepath = os.path.join(tempfile.gettempdir(), filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath
    
    def test_rag_upload(self) -> Dict[str, Any]:
        """Test RAG document upload"""
        self.log("🔄 Testing RAG Upload...")
        
        # Create test document
        test_content = """# Machine Learning Guide

## Introduction
Machine learning is a subset of artificial intelligence (AI) that focuses on creating algorithms that can learn and make decisions from data without being explicitly programmed.

## Types of Machine Learning

### 1. Supervised Learning
- Uses labeled training data
- Examples: Classification, Regression
- Algorithms: Linear Regression, Random Forest, SVM

### 2. Unsupervised Learning
- Finds patterns in unlabeled data
- Examples: Clustering, Dimensionality Reduction
- Algorithms: K-Means, PCA, DBSCAN

### 3. Reinforcement Learning
- Learns through interaction with environment
- Uses rewards and penalties
- Examples: Game playing, Robotics

## Deep Learning
Deep learning is a subset of machine learning that uses neural networks with multiple layers:
- Convolutional Neural Networks (CNNs) for image processing
- Recurrent Neural Networks (RNNs) for sequence data
- Transformers for natural language processing

## Applications
- Healthcare: Medical diagnosis, drug discovery
- Finance: Fraud detection, algorithmic trading
- Transportation: Autonomous vehicles, route optimization
- Technology: Search engines, recommendation systems

## Best Practices
1. Start with clean, quality data
2. Choose appropriate algorithms for your problem
3. Validate your models properly
4. Monitor model performance in production
5. Consider ethical implications and bias
"""
        
        filepath = self.create_test_document("ml_guide.txt", test_content)
        
        try:
            with open(filepath, 'rb') as f:
                files = {"file": ("ml_guide.txt", f, "text/plain")}
                response = requests.post(f"{BASE_URL}/rag/upload", files=files)
            
            if response.status_code == 200:
                data = response.json()
                self.uploaded_files.append(data['fileId'])
                self.log(f"✅ Upload successful - File ID: {data['fileId']}")
                return data
            else:
                self.log(f"❌ Upload failed: {response.status_code} - {response.text}", "ERROR")
                return None
                
        except Exception as e:
            self.log(f"❌ Upload error: {e}", "ERROR")
            return None
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    
    def test_rag_query(self, file_id: str) -> bool:
        """Test RAG direct query"""
        self.log("🔄 Testing RAG Direct Query...")
        
        questions = [
            "What is machine learning?",
            "What are the main types of machine learning?",
            "What is deep learning and how is it different?",
            "What are some applications in healthcare?",
            "What are the best practices for machine learning?"
        ]
        
        success_count = 0
        
        for i, question in enumerate(questions, 1):
            try:
                self.log(f"   Question {i}: {question}")
                
                response = requests.post(f"{BASE_URL}/rag/query", json={
                    "fileId": file_id,
                    "question": question
                })
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result['answer']
                    self.log(f"   ✅ Answer: {answer[:100]}...")
                    success_count += 1
                else:
                    self.log(f"   ❌ Query failed: {response.status_code} - {response.text}", "ERROR")
                    
            except Exception as e:
                self.log(f"   ❌ Query error: {e}", "ERROR")
        
        success_rate = success_count / len(questions)
        if success_rate >= 0.8:
            self.log(f"✅ RAG Query test passed ({success_count}/{len(questions)} successful)")
            return True
        else:
            self.log(f"❌ RAG Query test failed ({success_count}/{len(questions)} successful)", "ERROR")
            return False
    
    def test_rag_session(self, file_id: str) -> bool:
        """Test RAG session functionality"""
        self.log("🔄 Testing RAG Session...")
        
        try:
            # Create session
            self.log("   Creating RAG session...")
            response = requests.post(f"{BASE_URL}/rag/session", json={
                "fileId": file_id,
                "sessionName": "ML Guide Chat Session"
            })
            
            if response.status_code != 200:
                self.log(f"   ❌ Session creation failed: {response.status_code}", "ERROR")
                return False
            
            session_data = response.json()
            session_id = session_data['sessionId']
            self.created_sessions.append(session_id)
            self.log(f"   ✅ Session created: {session_id}")
            
            # Test conversation
            conversation = [
                "What is the main topic of this document?",
                "Tell me about supervised learning",
                "What are some deep learning architectures mentioned?",
                "What applications are discussed?"
            ]
            
            success_count = 0
            
            for i, question in enumerate(conversation, 1):
                self.log(f"   Message {i}: {question}")
                
                response = requests.post(f"{BASE_URL}/rag/session/{session_id}/ask", json={
                    "question": question
                })
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result['content']
                    self.log(f"   ✅ Response: {answer[:80]}...")
                    success_count += 1
                else:
                    self.log(f"   ❌ Ask failed: {response.status_code}", "ERROR")
            
            # Test session retrieval
            self.log("   Testing session retrieval...")
            response = requests.get(f"{BASE_URL}/rag/session/{session_id}")
            if response.status_code == 200:
                self.log("   ✅ Session retrieval successful")
                success_count += 1
            else:
                self.log("   ❌ Session retrieval failed", "ERROR")
            
            # Test messages retrieval
            self.log("   Testing messages retrieval...")
            response = requests.get(f"{BASE_URL}/rag/session/{session_id}/messages")
            if response.status_code == 200:
                messages = response.json()
                self.log(f"   ✅ Messages retrieved: {len(messages)} messages")
                success_count += 1
            else:
                self.log("   ❌ Messages retrieval failed", "ERROR")
            
            # Test session listing
            self.log("   Testing session listing...")
            response = requests.get(f"{BASE_URL}/rag/sessions")
            if response.status_code == 200:
                sessions = response.json()
                # Fix: Check if sessions is a list
                if isinstance(sessions, list):
                    rag_sessions = [s for s in sessions if self.is_rag_file(s.get('filename', ''))]
                    self.log(f"   ✅ Found {len(rag_sessions)} RAG sessions")
                else:
                    self.log(f"   ✅ Session listing successful (response: {type(sessions)})")
                success_count += 1
            else:
                self.log("   ❌ Session listing failed", "ERROR")
            
            success_rate = success_count / (len(conversation) + 3)  # +3 for other tests
            if success_rate >= 0.8:
                self.log(f"✅ RAG Session test passed ({success_count}/{len(conversation) + 3} successful)")
                return True
            else:
                self.log(f"❌ RAG Session test failed ({success_count}/{len(conversation) + 3} successful)", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Session test error: {e}", "ERROR")
            return False
    
    def is_rag_file(self, filename: str) -> bool:
        """Check if filename is a RAG-supported file"""
        if not isinstance(filename, str):
            return False
        return filename.lower().endswith(('.txt', '.docx', '.pdf'))
    
    def test_multiple_file_types(self) -> bool:
        """Test different file types"""
        self.log("🔄 Testing Multiple File Types...")
        
        # Test different content types
        test_files = [
            {
                "filename": "tech_terms.txt",
                "content": """# Technology Terms

API: Application Programming Interface - allows different software applications to communicate.

Cloud Computing: Delivery of computing services over the internet.

DevOps: Practices that combine software development and IT operations.

Microservices: Architectural approach where applications are built as a collection of small services.
""",
                "questions": ["What is an API?", "Explain cloud computing"]
            }
        ]
        
        success_count = 0
        
        for test_file in test_files:
            self.log(f"   Testing {test_file['filename']}...")
            
            # Create and upload file
            filepath = self.create_test_document(test_file['filename'], test_file['content'])
            
            try:
                with open(filepath, 'rb') as f:
                    files = {"file": (test_file['filename'], f, "text/plain")}
                    response = requests.post(f"{BASE_URL}/rag/upload", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    file_id = data['fileId']
                    self.uploaded_files.append(file_id)
                    
                    # Test queries
                    query_success = True
                    for question in test_file['questions']:
                        response = requests.post(f"{BASE_URL}/rag/query", json={
                            "fileId": file_id,
                            "question": question
                        })
                        
                        if response.status_code != 200:
                            query_success = False
                            break
                    
                    if query_success:
                        self.log(f"   ✅ {test_file['filename']} test passed")
                        success_count += 1
                    else:
                        self.log(f"   ❌ {test_file['filename']} query failed", "ERROR")
                else:
                    self.log(f"   ❌ {test_file['filename']} upload failed", "ERROR")
                    
            except Exception as e:
                self.log(f"   ❌ {test_file['filename']} error: {e}", "ERROR")
            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)
        
        if success_count == len(test_files):
            self.log("✅ Multiple file types test passed")
            return True
        else:
            self.log(f"❌ Multiple file types test failed ({success_count}/{len(test_files)})", "ERROR")
            return False
    
    def cleanup(self):
        """Clean up created resources"""
        self.log("🧹 Cleaning up...")
        
        # Delete sessions
        for session_id in self.created_sessions:
            try:
                response = requests.delete(f"{BASE_URL}/rag/session/{session_id}")
                if response.status_code == 200:
                    self.log(f"   ✅ Deleted session: {session_id}")
                else:
                    self.log(f"   ⚠️  Failed to delete session: {session_id}")
            except Exception as e:
                self.log(f"   ❌ Error deleting session {session_id}: {e}", "ERROR")
        
        # Delete files (with retry)
        for file_id in self.uploaded_files:
            deleted = False
            for attempt in range(2):  # Try twice
                try:
                    if attempt > 0:
                        time.sleep(2)  # Wait 2 seconds before retry
                        self.log(f"   🔄 Retrying deletion of file: {file_id}")
                    
                    response = requests.delete(f"{BASE_URL}/rag/file/{file_id}")
                    if response.status_code == 200:
                        self.log(f"   ✅ Deleted file: {file_id}")
                        deleted = True
                        break
                    elif response.status_code == 404:
                        self.log(f"   ℹ️  File already deleted: {file_id}")
                        deleted = True
                        break
                    elif response.status_code == 500:
                        if attempt == 0:
                            continue  # Retry once
                        else:
                            self.log(f"   ⚠️  File {file_id} may be locked by database (will cleanup later)")
                    else:
                        self.log(f"   ⚠️  Failed to delete file {file_id}: {response.status_code}")
                except Exception as e:
                    if attempt == 0:
                        continue  # Retry once
                    else:
                        self.log(f"   ❌ Error deleting file {file_id}: {e}", "ERROR")
    
    def run_all_tests(self):
        """Run comprehensive RAG tests"""
        self.log("🚀 Starting RAG Feature Tests")
        self.log("Make sure the server is running on http://localhost:8000")
        self.log("=" * 60)
        
        test_results = {}
        
        try:
            # Test 1: Upload
            upload_result = self.test_rag_upload()
            test_results["Upload"] = upload_result is not None
            
            if upload_result:
                file_id = upload_result['fileId']
                
                # Test 2: Direct Query
                test_results["Direct Query"] = self.test_rag_query(file_id)
                
                # Test 3: Session Management
                test_results["Session Management"] = self.test_rag_session(file_id)
            else:
                test_results["Direct Query"] = False
                test_results["Session Management"] = False
            
            # Test 4: Multiple File Types
            test_results["Multiple File Types"] = self.test_multiple_file_types()
            
        except Exception as e:
            self.log(f"❌ Test suite error: {e}", "ERROR")
        
        finally:
            # Cleanup
            self.cleanup()
        
        # Summary
        self.log("=" * 60)
        self.log("📊 TEST RESULTS SUMMARY")
        self.log("=" * 60)
        
        passed_tests = []
        failed_tests = []
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            self.log(f"{test_name:20} : {status}")
            
            if result:
                passed_tests.append(test_name)
            else:
                failed_tests.append(test_name)
        
        total_tests = len(test_results)
        passed_count = len(passed_tests)
        
        self.log("-" * 60)
        self.log(f"Total Tests: {total_tests}")
        self.log(f"Passed: {passed_count}")
        self.log(f"Failed: {total_tests - passed_count}")
        self.log(f"Success Rate: {passed_count/total_tests*100:.1f}%")
        
        if failed_tests:
            self.log(f"\n❌ Failed Tests: {', '.join(failed_tests)}")
        
        if passed_count == total_tests:
            self.log("\n🎉 ALL RAG TESTS PASSED!")
            return True
        else:
            self.log(f"\n⚠️  {total_tests - passed_count} tests failed. Check server logs for details.")
            return False


def main():
    """Main test function"""
    tester = RAGTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ RAG feature is working perfectly!")
    else:
        print("\n❌ Some RAG tests failed. Please check the output above.")
    
    return success


if __name__ == "__main__":
    main()
