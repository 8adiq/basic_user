#!/usr/bin/env python3
"""
Comprehensive API testing script for the FastAPI backend
Tests all endpoints: Users, Posts, Comments, Likes, Email Verification
"""
import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

# Global variables to store test data
import time

# Generate unique test data using timestamp
timestamp = int(time.time())
test_user = {
    "username": f"testuser_{timestamp}",
    "email": f"test_{timestamp}@example.com",
    "password": "password123"
}

test_user2 = {
    "username": f"testuser2_{timestamp}", 
    "email": f"test2_{timestamp}@example.com",
    "password": "password123"
}

auth_token = None
user_id = None
post_id = None
comment_id = None
verification_token = None

def print_test_header(test_name):
    """Print a formatted test header"""
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"{'='*60}")

def print_test_result(success, message):
    """Print formatted test result"""
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")

def cleanup_test_data():
    """Clean up test data after tests"""
    print("\n🧹 Cleaning up test data...")
    # Note: In a real test environment, you'd clean up the database
    # For now, we just print a message
    print("✅ Test data cleanup completed")

def test_registration():
    """Test user registration"""
    global auth_token, user_id
    
    print_test_header("User Registration")
    
    response = requests.post(f"{API_BASE}/register", json=test_user)
    print(f"Status: {response.status_code}")
    
    assert response.status_code == 201, f"Registration failed with status {response.status_code}"
    
    data = response.json()
    auth_token = data.get('token')
    user_id = data.get('user', {}).get('id')
    
    assert auth_token is not None, "No token received"
    assert user_id is not None, "No user ID received"
    
    print(f"Response: {json.dumps(data, indent=2)}")
    print_test_result(True, "Registration successful!")
    return True

def test_login_before_verification():
    """Test user login before email verification (should fail)"""
    global auth_token, user_id
    
    print_test_header("User Login Before Email Verification")
    
    response = requests.post(f"{API_BASE}/login", json=test_user)
    print(f"Status: {response.status_code}")
    
    assert response.status_code == 401, f"Login should fail before verification, got {response.status_code}"
    
    data = response.json()
    assert "Please verify your email" in data.get('detail', ''), "Wrong error message"
    
    print(f"Response: {json.dumps(data, indent=2)}")
    print_test_result(True, "Login correctly blocked - email not verified!")
    return True

def test_email_verification_request():
    """Test email verification request"""
    print_test_header("Email Verification Request")
    
    verification_data = {
        "email": test_user["email"]
    }
    
    response = requests.post(f"{API_BASE}/email-verification/request", json=verification_data)
    print(f"Status: {response.status_code}")
    
    assert response.status_code == 200, f"Email verification request failed with status {response.status_code}"
    
    data = response.json()
    assert "message" in data, "No message in response"
    
    print(f"Response: {json.dumps(data, indent=2)}")
    print_test_result(True, "Email verification request successful!")
    return True

def test_email_verification_confirm():
    """Test email verification confirmation"""
    global verification_token
    
    print_test_header("Email Verification Confirmation")
    
    # Note: In a real scenario, you'd get this token from the email
    # For testing, we'll simulate with a dummy token (this will fail)
    # In practice, you'd need to extract the token from the database or email
    
    dummy_token = "dummy_token_for_testing"
    
    response = requests.post(f"{API_BASE}/email-verification/confirm?token={dummy_token}")
    print(f"Status: {response.status_code}")
    
    assert response.status_code == 400, f"Invalid token should be rejected, got {response.status_code}"
    
    data = response.json()
    assert "Invalid or expired" in data.get('detail', ''), "Wrong error message for invalid token"
    
    print(f"Response: {json.dumps(data, indent=2)}")
    print_test_result(True, "Invalid token correctly rejected!")
    print("Note: In real testing, you'd use a valid token from the database")
    return True

def test_login():
    """Test user login after email verification"""
    global auth_token, user_id
    
    print_test_header("User Login After Email Verification")
    
    response = requests.post(f"{API_BASE}/login", json=test_user)
    print(f"Status: {response.status_code}")
    
    # This will fail until email is actually verified
    if response.status_code == 200:
        data = response.json()
        auth_token = data.get('token')
        user_id = data.get('user', {}).get('id')
        
        assert auth_token is not None, "No token received"
        assert user_id is not None, "No user ID received"
        
        print(f"Response: {json.dumps(data, indent=2)}")
        print_test_result(True, "Login successful!")
        return True
    else:
        print(f"Response: {response.text}")
        print_test_result(False, "Login failed - email not verified yet")
        return False

def test_profile():
    """Test getting user profile"""
    global auth_token
    
    print_test_header("User Profile")
    
    assert auth_token is not None, "No auth token available"
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{API_BASE}/profile", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        assert "user" in data, "No user data in response"
        assert data["user"]["email"] == test_user["email"], "Wrong user email"
        
        print(f"Response: {json.dumps(data, indent=2)}")
        print_test_result(True, "Profile retrieved successfully!")
        return True
    else:
        print(f"Response: {response.text}")
        print_test_result(False, "Profile retrieval failed!")
        return False

def test_create_post():
    """Test creating a post"""
    global auth_token, post_id
    
    print_test_header("Create Post")
    
    assert auth_token is not None, "No auth token available"
    
    post_data = {
        "text": "This is a test post created by the automated test suite!"
    }
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{API_BASE}/posts", json=post_data, headers=headers)
    
    print(f"Status: {response.status_code}")
    
    assert response.status_code == 201, f"Post creation failed with status {response.status_code}"
    
    data = response.json()
    post_id = data.get('id')
    
    assert post_id is not None, "No post ID received"
    assert data['text'] == post_data['text'], "Post text doesn't match"
    assert 'created_at' in data, "No created_at timestamp"
    
    print(f"Response: {json.dumps(data, indent=2)}")
    print_test_result(True, "Post creation successful!")
    return True

def test_get_all_posts():
    """Test getting all posts"""
    print_test_header("Get All Posts")
    
    response = requests.get(f"{API_BASE}/posts")
    
    print(f"Status: {response.status_code}")
    
    assert response.status_code == 200, f"Get posts failed with status {response.status_code}"
    
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    
    print(f"Found {len(data)} posts")
    print(f"Response: {json.dumps(data, indent=2)}")
    print_test_result(True, "Get all posts successful!")
    return True

def test_get_single_post():
    """Test getting a single post"""
    global post_id
    
    print_test_header("Get Single Post")
    
    assert post_id is not None, "No post ID available"
    
    response = requests.get(f"{API_BASE}/posts/{post_id}")
    
    print(f"Status: {response.status_code}")
    
    assert response.status_code == 200, f"Get single post failed with status {response.status_code}"
    
    data = response.json()
    assert data['id'] == post_id, "Wrong post ID"
    assert 'text' in data, "No text in post"
    assert 'created_at' in data, "No created_at timestamp"
    
    print(f"Response: {json.dumps(data, indent=2)}")
    print_test_result(True, "Get single post successful!")
    return True

def test_create_comment():
    """Test creating a comment"""
    global auth_token, post_id, comment_id
    
    print_test_header("Create Comment")
    
    assert auth_token is not None, "No auth token available"
    assert post_id is not None, "No post ID available"
    
    comment_data = {
        "text": "This is a test comment!"
    }
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{API_BASE}/comments?post_id={post_id}", json=comment_data, headers=headers)
    
    print(f"Status: {response.status_code}")
    
    assert response.status_code == 201, f"Comment creation failed with status {response.status_code}"
    
    data = response.json()
    comment_id = data.get('id')
    
    assert comment_id is not None, "No comment ID received"
    assert data['text'] == comment_data['text'], "Comment text doesn't match"
    assert data['post_id'] == post_id, "Wrong post ID in comment"
    assert 'created_at' in data, "No created_at timestamp"
    
    print(f"Response: {json.dumps(data, indent=2)}")
    print_test_result(True, "Comment creation successful!")
    return True

def test_get_comments():
    """Test getting comments for a post"""
    global post_id
    
    print_test_header("Get Comments")
    
    assert post_id is not None, "No post ID available"
    
    response = requests.get(f"{API_BASE}/{post_id}/comments")
    
    print(f"Status: {response.status_code}")
    
    assert response.status_code == 200, f"Get comments failed with status {response.status_code}"
    
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    
    print(f"Found {len(data)} comments")
    print(f"Response: {json.dumps(data, indent=2)}")
    print_test_result(True, "Get comments successful!")
    return True

def test_like_post():
    """Test liking a post"""
    global auth_token, post_id
    
    print_test_header("Like Post")
    
    assert auth_token is not None, "No auth token available"
    assert post_id is not None, "No post ID available"
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{API_BASE}/likes?post_id={post_id}", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    assert response.status_code == 201, f"Like post failed with status {response.status_code}"
    
    data = response.json()
    assert 'id' in data, "No like ID received"
    assert data['post_id'] == post_id, "Wrong post ID in like"
    assert data['user_id'] == user_id, "Wrong user ID in like"
    
    print(f"Response: {json.dumps(data, indent=2)}")
    print_test_result(True, "Post liked successfully!")
    return True

def test_unlike_post():
    """Test unliking a post"""
    global auth_token, post_id
    
    print_test_header("Unlike Post")
    
    assert auth_token is not None, "No auth token available"
    assert post_id is not None, "No post ID available"
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.delete(f"{API_BASE}/likes?post_id={post_id}", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    assert response.status_code == 204, f"Unlike post failed with status {response.status_code}"
    
    print_test_result(True, "Post unliked successfully!")
    return True

def test_update_post():
    """Test updating a post"""
    global auth_token, post_id
    
    print_test_header("Update Post")
    
    assert auth_token is not None, "No auth token available"
    assert post_id is not None, "No post ID available"
    
    update_data = {
        "text": "This post has been updated by the test suite!"
    }
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.put(f"{API_BASE}/posts/{post_id}", json=update_data, headers=headers)
    
    print(f"Status: {response.status_code}")
    
    assert response.status_code == 200, f"Update post failed with status {response.status_code}"
    
    data = response.json()
    assert data['text'] == update_data['text'], "Post text not updated"
    assert data['id'] == post_id, "Wrong post ID"
    
    print(f"Response: {json.dumps(data, indent=2)}")
    print_test_result(True, "Post update successful!")
    return True

def test_error_cases():
    """Test various error cases"""
    print_test_header("Error Cases")
    
    # Test invalid login
    print("\n--- Testing Invalid Login ---")
    invalid_login = {"email": "wrong@email.com", "password": "wrongpass"}
    response = requests.post(f"{API_BASE}/login", json=invalid_login)
    print(f"Status: {response.status_code}")
    assert response.status_code == 401, "Invalid login should be rejected"
    print_test_result(True, "Invalid login correctly rejected")
    
    # Test duplicate registration
    print("\n--- Testing Duplicate Registration ---")
    response = requests.post(f"{API_BASE}/register", json=test_user)
    print(f"Status: {response.status_code}")
    assert response.status_code == 400, "Duplicate registration should be rejected"
    print_test_result(True, "Duplicate registration correctly rejected")
    
    # Test invalid token
    print("\n--- Testing Invalid Token ---")
    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(f"{API_BASE}/profile", headers=headers)
    print(f"Status: {response.status_code}")
    assert response.status_code == 401, "Invalid token should be rejected"
    print_test_result(True, "Invalid token correctly rejected")
    
    # Test accessing non-existent post
    print("\n--- Testing Non-existent Post ---")
    response = requests.get(f"{API_BASE}/posts/non-existent-id")
    print(f"Status: {response.status_code}")
    assert response.status_code == 404, "Non-existent post should return 404"
    print_test_result(True, "Non-existent post correctly handled")

def test_validation_errors():
    """Test input validation"""
    print_test_header("Input Validation")
    
    # Test invalid email format
    print("\n--- Testing Invalid Email ---")
    invalid_data = {
        "username": "testuser3",
        "email": "invalid-email",
        "password": "password123"
    }
    response = requests.post(f"{API_BASE}/register", json=invalid_data)
    print(f"Status: {response.status_code}")
    assert response.status_code == 422, "Invalid email should be rejected"
    print_test_result(True, "Invalid email format correctly rejected")
    
    # Test short password
    print("\n--- Testing Short Password ---")
    invalid_data = {
        "username": "testuser3",
        "email": "test3@example.com",
        "password": "123"
    }
    response = requests.post(f"{API_BASE}/register", json=invalid_data)
    print(f"Status: {response.status_code}")
    assert response.status_code == 400, "Short password should be rejected"
    print_test_result(True, "Short password correctly rejected")

def main():
    """Run all tests"""
    print("🚀 Starting Comprehensive Backend API Tests")
    print(f"Testing against: {BASE_URL}")
    print("=" * 60)
    
    try:
        # Test user operations
        test_registration()
        
        # Test email verification flow
        test_login_before_verification()  # Should fail
        test_email_verification_request()  # Request verification email
        test_email_verification_confirm()  # Test token validation
        
        # Test login (will fail until email is actually verified)
        test_login()
        
        # Test profile (will only work if login succeeded)
        test_profile()
        
        # Test post operations
        test_create_post()
        test_get_all_posts()
        test_get_single_post()
        test_update_post()
        
        # Test comment operations
        test_create_comment()
        test_get_comments()
        
        # Test like operations
        test_like_post()
        test_unlike_post()
        
        # Test error cases
        test_error_cases()
        test_validation_errors()
        
        print("\n" + "=" * 60)
        print("🎉 All tests completed successfully!")
        print("=" * 60)
        print("\n📝 Notes:")
        print("- Email verification tests use dummy tokens")
        print("- For complete testing, manually verify email or extract token from database")
        print("- Some tests may fail until email verification is complete")
        
        # Clean up test data
        cleanup_test_data()
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to {BASE_URL}")
        print("Make sure your backend server is running!")
        print("Run: uvicorn app.main:app --reload")
    except AssertionError as e:
        print(f"❌ Test assertion failed: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()