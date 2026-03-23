"""
Tests for signup endpoint following AAA (Arrange-Act-Assert) pattern
"""

import pytest


class TestSignupSuccess:
    """Tests for successful signup scenarios"""
    
    def test_signup_success(self, client, sample_activities, test_email):
        """
        Test successful signup for an activity
        
        Arrange: User not yet signed up, activity exists with available slots
        Act: Call POST /activities/{activity_name}/signup with email
        Assert: Response status 200, user added to participants list
        """
        # Arrange
        activity_name = "Programming Class"
        email = test_email["new_user"]
        # Programming Class has 0 participants, max_participants=3
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in sample_activities[activity_name]["participants"]
    
    def test_signup_multiple_users_same_activity(self, client, sample_activities, test_email):
        """
        Test multiple users can sign up for the same activity
        
        Arrange: Two different users, activity with available slots
        Act: Call POST signup for first user, then second user
        Assert: Both users added to participants list
        """
        # Arrange
        activity_name = "Programming Class"
        user1 = "user1@mergington.edu"
        user2 = "user2@mergington.edu"
        
        # Act
        response1 = client.post(f"/activities/{activity_name}/signup?email={user1}")
        response2 = client.post(f"/activities/{activity_name}/signup?email={user2}")
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert user1 in sample_activities[activity_name]["participants"]
        assert user2 in sample_activities[activity_name]["participants"]


class TestSignupErrors:
    """Tests for signup error scenarios"""
    
    def test_signup_activity_not_found(self, client, sample_activities, test_email):
        """
        Test signup fails when activity doesn't exist
        
        Arrange: Activity name that doesn't exist
        Act: Call POST /activities/{nonexistent_activity}/signup
        Assert: Response status 404 and error message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = test_email["new_user"]
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_already_registered(self, client, sample_activities, test_email):
        """
        Test signup fails if user is already registered for activity
        
        Arrange: User already in participants list
        Act: Call POST /activities/{activity_name}/signup with existing participant
        Assert: Response status 400 and error message
        """
        # Arrange
        activity_name = "Chess Club"
        email = test_email["existing_user_1"]  # alice@mergington.edu is already in Chess Club
        # Verify user is already signed up
        assert email in sample_activities[activity_name]["participants"]
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_allowed_even_at_max_capacity(self, client, sample_activities, test_email):
        """
        Test that signup is allowed even when activity is at max participants
        
        Note: Current app.py doesn't enforce max_participants limit
        
        Arrange: Activity with all slots filled
        Act: Call POST /activities/{full_activity}/signup
        Assert: Response status 200 (signup succeeds despite max capacity)
        """
        # Arrange
        activity_name = "Gym Class"
        email = test_email["new_user"]
        # Gym Class has max_participants=2 and participants=[bob, charlie]
        assert len(sample_activities[activity_name]["participants"]) == sample_activities[activity_name]["max_participants"]
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert - Current implementation allows signup even at max capacity
        assert response.status_code == 200
        assert email in sample_activities[activity_name]["participants"]
    
    def test_signup_missing_email_parameter(self, client, sample_activities):
        """
        Test signup fails when email parameter is missing
        
        Arrange: No email query parameter provided
        Act: Call POST /activities/{activity_name}/signup without email
        Assert: Response status 422 (validation error)
        """
        # Arrange
        activity_name = "Programming Class"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup")
        
        # Assert
        assert response.status_code == 422
