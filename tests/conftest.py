"""
Pytest configuration and fixtures for FastAPI tests
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a FastAPI TestClient instance for testing endpoints
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Reset and provide clean activity state for each test.
    This ensures test isolation by resetting the global activities dict
    to its default state before each test.
    """
    # Save original state
    original_activities = activities.copy()
    
    # Reset activities to default state
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 2,
            "participants": ["alice@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 3,
            "participants": []
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 2,
            "participants": ["bob@mergington.edu", "charlie@mergington.edu"]
        }
    })
    
    yield activities
    
    # Restore original state after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def test_email():
    """
    Provide consistent test email addresses
    """
    return {
        "new_user": "newuser@mergington.edu",
        "existing_user_1": "alice@mergington.edu",
        "existing_user_2": "bob@mergington.edu"
    }
