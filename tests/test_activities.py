import pytest
from fastapi.testclient import TestClient
from src.app import app


def test_get_activities(client):
    """Test GET /activities endpoint returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert len(data) == 9


def test_get_activities_structure(client):
    """Test activity structure is correct"""
    response = client.get("/activities")
    data = response.json()
    activity = data["Chess Club"]
    
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_signup_success(client):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    
    # Verify participant was added
    activities = client.get("/activities").json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate(client):
    """Test duplicate signup is rejected"""
    # Try to signup someone already registered
    response = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity(client):
    """Test signup to non-existent activity returns 404"""
    response = client.post(
        "/activities/Nonexistent%20Activity/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_unregister_success(client):
    """Test successful unregister from an activity"""
    response = client.delete(
        "/activities/Chess%20Club/participants?email=michael@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    
    # Verify participant was removed
    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_not_registered(client):
    """Test unregister for non-registered student returns 400"""
    response = client.delete(
        "/activities/Chess%20Club/participants?email=notregistered@mergington.edu"
    )
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"].lower()


def test_unregister_nonexistent_activity(client):
    """Test unregister from non-existent activity returns 404"""
    response = client.delete(
        "/activities/Nonexistent%20Activity/participants?email=test@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_then_unregister_workflow(client):
    """Test complete workflow: signup then unregister"""
    test_email = "workflow@mergington.edu"
    activity = "Programming Class"
    
    # Signup
    signup_response = client.post(
        f"/activities/{activity}/signup?email={test_email}"
    )
    assert signup_response.status_code == 200
    
    # Verify signup worked
    activities = client.get("/activities").json()
    assert test_email in activities[activity]["participants"]
    
    # Unregister
    unregister_response = client.delete(
        f"/activities/{activity}/participants?email={test_email}"
    )
    assert unregister_response.status_code == 200
    
    # Verify unregister worked
    activities = client.get("/activities").json()
    assert test_email not in activities[activity]["participants"]


def test_activity_max_participants_not_enforced(client):
    """Test that signup doesn't check max_participants limit"""
    # Chess Club has max 12, let's try adding many students
    for i in range(5):
        response = client.post(
            f"/activities/Chess%20Club/signup?email=student{i}@mergington.edu"
        )
        assert response.status_code == 200
    
    # All should be added (no max limit enforcement in current implementation)
    activities = client.get("/activities").json()
    assert len(activities["Chess Club"]["participants"]) >= 7  # 2 original + 5 new


def test_multiple_activities_independent(client):
    """Test that participants in different activities are independent"""
    test_email = "multiactivity@mergington.edu"
    
    # Signup for two activities
    client.post(f"/activities/Chess%20Club/signup?email={test_email}")
    client.post(f"/activities/Programming%20Class/signup?email={test_email}")
    
    # Verify in both
    activities = client.get("/activities").json()
    assert test_email in activities["Chess Club"]["participants"]
    assert test_email in activities["Programming Class"]["participants"]
    
    # Unregister from one
    client.delete(f"/activities/Chess%20Club/participants?email={test_email}")
    
    # Verify removed from Chess Club but still in Programming Class
    activities = client.get("/activities").json()
    assert test_email not in activities["Chess Club"]["participants"]
    assert test_email in activities["Programming Class"]["participants"]
