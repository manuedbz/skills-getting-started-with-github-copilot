"""
Tests for unregister endpoint following AAA (Arrange-Act-Assert) pattern
"""

import pytest


class TestUnregisterSuccess:
    """Tests for successful unregister scenarios"""
    
    def test_unregister_success(self, client, sample_activities, test_email):
        """
        Test successful unregister from an activity
        
        Arrange: User is registered for activity
        Act: Call POST /activities/{activity_name}/unregister
        Assert: Response status 200, user removed from participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email = test_email["existing_user_1"]  # alice@mergington.edu is in Chess Club
        assert email in sample_activities[activity_name]["participants"]
        
        # Act
        response = client.post(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email not in sample_activities[activity_name]["participants"]
    
    def test_unregister_frees_up_activity_slot(self, client, sample_activities, test_email):
        """
        Test that unregister frees up a slot for new signups
        
        Arrange: User registered, activity at capacity
        Act: Unregister user, then signup a different user
        Assert: New user can successfully signup after unregister
        """
        # Arrange
        activity_name = "Gym Class"
        existing_user = test_email["existing_user_2"]
        new_user = test_email["new_user"]
        # Gym Class at capacity (2 participants, max 2)
        assert len(sample_activities[activity_name]["participants"]) == 2
        
        # Act - Unregister existing user
        response1 = client.post(f"/activities/{activity_name}/unregister?email={existing_user}")
        
        # Then signup new user
        response2 = client.post(f"/activities/{activity_name}/signup?email={new_user}")
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert existing_user not in sample_activities[activity_name]["participants"]
        assert new_user in sample_activities[activity_name]["participants"]


class TestUnregisterErrors:
    """Tests for unregister error scenarios"""
    
    def test_unregister_activity_not_found(self, client, sample_activities, test_email):
        """
        Test unregister fails when activity doesn't exist
        
        Arrange: Activity name that doesn't exist
        Act: Call POST /activities/{nonexistent_activity}/unregister
        Assert: Response status 404 and error message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = test_email["existing_user_1"]
        
        # Act
        response = client.post(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_user_not_registered(self, client, sample_activities, test_email):
        """
        Test unregister fails if user is not registered for activity
        
        Arrange: User not in participants list
        Act: Call POST /activities/{activity_name}/unregister with unregistered user
        Assert: Response status 400 and error message
        """
        # Arrange
        activity_name = "Programming Class"
        email = test_email["new_user"]
        # Verify user is not in Programming Class
        assert email not in sample_activities[activity_name]["participants"]
        
        # Act
        response = client.post(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_unregister_missing_email_parameter(self, client, sample_activities):
        """
        Test unregister fails when email parameter is missing
        
        Arrange: No email query parameter provided
        Act: Call POST /activities/{activity_name}/unregister without email
        Assert: Response status 422 (validation error)
        """
        # Arrange
        activity_name = "Chess Club"
        
        # Act
        response = client.post(f"/activities/{activity_name}/unregister")
        
        # Assert
        assert response.status_code == 422
