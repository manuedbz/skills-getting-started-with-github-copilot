"""
Tests for basic FastAPI endpoints following AAA (Arrange-Act-Assert) pattern
"""

import pytest


class TestRootEndpoint:
    """Tests for GET / endpoint"""
    
    def test_get_root_redirect(self, client):
        """
        Test that GET / redirects to /static/index.html
        
        Arrange: Prepare the client
        Act: Call GET /
        Assert: Verify 307 redirect status and location header
        """
        # Arrange
        # Client is provided by fixture
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestActivitiesEndpoint:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client, sample_activities):
        """
        Test that GET /activities returns all activities with correct structure
        
        Arrange: Set up sample activities via fixture
        Act: Call GET /activities
        Assert: Verify response contains all activities and correct structure
        """
        # Arrange
        # Activities provided by sample_activities fixture
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        assert len(data) == 3
    
    def test_get_activities_has_correct_structure(self, client, sample_activities):
        """
        Test that each activity has the required fields
        
        Arrange: Set up sample activities via fixture
        Act: Call GET /activities
        Assert: Verify each activity has description, schedule, max_participants, participants
        """
        # Arrange
        # Activities provided by sample_activities fixture
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity in data.items():
            assert "description" in activity
            assert "schedule" in activity
            assert "max_participants" in activity
            assert "participants" in activity
            assert isinstance(activity["participants"], list)
    
    def test_get_activities_returns_participant_data(self, client, sample_activities):
        """
        Test that GET /activities includes current participant information
        
        Arrange: Set up sample activities with participants
        Act: Call GET /activities
        Assert: Verify participant lists are returned correctly
        """
        # Arrange
        # Activities with participants provided by sample_activities fixture
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        # Chess Club has 1 participant
        assert len(data["Chess Club"]["participants"]) == 1
        assert "alice@mergington.edu" in data["Chess Club"]["participants"]
        
        # Programming Class has 0 participants
        assert len(data["Programming Class"]["participants"]) == 0
        
        # Gym Class has 2 participants
        assert len(data["Gym Class"]["participants"]) == 2
