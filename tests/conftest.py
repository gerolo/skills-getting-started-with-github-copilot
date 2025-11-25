import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    from src import app as app_module
    
    # Store original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Team training, drills, and competitive matches",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
            "max_participants": 22,
            "participants": ["alex@mergington.edu", "maria@mergington.edu"]
        },
        "Basketball Team": {
            "description": "League play and skill development for basketball players",
            "schedule": "Tuesdays and Thursdays, 5:00 PM - 7:00 PM",
            "max_participants": 12,
            "participants": ["linda@mergington.edu", "kevin@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore drawing, painting, and mixed media projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["maya@mergington.edu", "chloe@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, stagecraft, and production rehearsals",
            "schedule": "Thursdays, 4:00 PM - 6:30 PM",
            "max_participants": 25,
            "participants": ["leo@mergington.edu", "isabella@mergington.edu"]
        },
        "Debate Team": {
            "description": "Practice argumentation, public speaking, and competitive debates",
            "schedule": "Mondays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["nina@mergington.edu", "ethan@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments, science projects, and guest lectures",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["oscar@mergington.edu", "zoe@mergington.edu"]
        }
    }
    
    # Replace app activities with fresh copy
    app_module.activities.clear()
    app_module.activities.update(original_activities)
    
    yield
    
    # Clean up after test
    app_module.activities.clear()
    app_module.activities.update(original_activities)
