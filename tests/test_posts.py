import pytest
from app.database import get_db
from sqlalchemy import text


@pytest.fixture(autouse=True)
def clean_db():
    """
    Fixture to clean the database after each test.
    The autouse=True parameter ensures this runs automatically for each test.
    """
    # The test runs here
    yield
    # After the test completes, clean up the database
    db = next(get_db())
    db.execute(text("DELETE FROM posts"))
    db.execute(text("DELETE FROM users"))
    db.commit()

def test_get_posts_empty(client):
    """
    Test retrieving posts when the user has no posts.
    Expected response: Empty list.
    """
    # First, sign up and log in to get a token
    user_response = client.post("/users/signup", json={"email": "test1@example.com", "password": "securepass"})

    assert user_response.status_code == 200
    token = user_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Make request to getposts endpoint
    response = client.get("/posts/getposts", headers=headers)
    
    assert response.status_code == 200
    assert response.json() == {"posts": []}  # User has no posts yet

def test_get_posts_with_data(client):
    """
    Test retrieving posts when the user has created posts.
    Expected response: List of created posts.
    """
    # First, sign up and log in to get a token
    user_response = client.post("/users/signup", json={"email": "test@example.com", "password": "securepass"})
    assert user_response.status_code == 200
    token = user_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create multiple posts
    client.post("/posts/addpost", json={"text": "First Post"}, headers=headers)
    client.post("/posts/addpost", json={"text": "Second Post"}, headers=headers)
    
    # Make request to getposts endpoint
    response = client.get("/posts/getposts", headers=headers)
    
    assert response.status_code == 200
    posts = response.json()["posts"]
    assert len(posts) == 2
    assert posts[0]["text"] == "First Post"
    assert posts[1]["text"] == "Second Post"

def test_get_posts_invalid_token(client):
    """
    Test retrieving posts with an invalid token.
    Expected response: 401 Unauthorized.
    """
    headers = {"Authorization": "Bearer invalidtoken"}
    
    response = client.get("/posts/getposts", headers=headers)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_get_posts_after_deleting_post(client):
    """
    Test retrieving posts after deleting one.
    Expected response: List with one less post.
    """
    # Sign up and log in
    user_response = client.post("/users/signup", json={"email": "test@example.com", "password": "securepass"})
    assert user_response.status_code == 200
    token = user_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create posts
    post1 = client.post("/posts/addpost", json={"text": "First Post"}, headers=headers)
    post2 = client.post("/posts/addpost", json={"text": "Second Post"}, headers=headers)
    
    post1_id = post1.json()["id"]
    
    # Delete one post
    delete_response = client.delete(f"/posts/deletepost/{post1_id}", headers=headers)
    assert delete_response.status_code == 200
    
    # Fetch posts again
    response = client.get("/posts/getposts", headers=headers)
    
    assert response.status_code == 200
    posts = response.json()["posts"]
    assert len(posts) == 1
    assert posts[0]["text"] == "Second Post"
