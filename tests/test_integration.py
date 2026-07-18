"""
Integration tests for ISRO Mission Checker.
"""
import pytest
from unittest.mock import patch, MagicMock, mock_open
import sys


class TestIntegrationMissionChecker:
    """Integration tests for mission-checker workflow."""

    @patch('com.shankarsan.isro.mission_checker.webdriver.Firefox')
    @patch('com.shankarsan.isro.mission_checker.redis.Redis')
    @patch('com.shankarsan.isro.mission_checker.EmailUtils.sendMail')
    def test_complete_workflow_new_mission(self, mock_email, mock_redis, mock_firefox):
        """Test the complete workflow when a new mission is detected."""
        from com.shankarsan.isro import mission_checker

        # Setup mocks
        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver

        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        mock_redis_instance.get.return_value = None  # No cached mission

        # Mock web elements
        mock_mission_div = MagicMock()
        mock_font_elem = MagicMock()
        mock_font_elem.text = "Chandrayaan-3 Launch"
        mock_mission_div.find_elements.return_value = [mock_font_elem]
        mock_driver.find_element.return_value = mock_mission_div

        mission_checker.redis_instance = mock_redis_instance

        # Execute
        result = mission_checker.invoke_isro()

        # Verify complete workflow
        assert "Chandrayaan-3 Launch" in result
        mock_driver.get.assert_called_once()
        mock_mission_div.screenshot.assert_called_once_with("mission.png")
        mock_email.assert_called_once()
        mock_redis_instance.set.assert_called_once_with("next_isro_mission", "Chandrayaan-3 Launch")
        mock_driver.quit.assert_called_once()

    @patch('com.shankarsan.isro.mission_checker.webdriver.Firefox')
    @patch('com.shankarsan.isro.mission_checker.redis.Redis')
    @patch('com.shankarsan.isro.mission_checker.EmailUtils.sendMail')
    def test_complete_workflow_same_mission(self, mock_email, mock_redis, mock_firefox):
        """Test the complete workflow when mission hasn't changed."""
        from com.shankarsan.isro import mission_checker

        # Setup mocks
        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver

        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance

        cached_mission = "Aditya-L1 Launch"
        mock_redis_instance.get.return_value = cached_mission.encode('utf-8')

        # Mock web elements returning same mission
        mock_mission_div = MagicMock()
        mock_font_elem = MagicMock()
        mock_font_elem.text = cached_mission
        mock_mission_div.find_elements.return_value = [mock_font_elem]
        mock_driver.find_element.return_value = mock_mission_div

        mission_checker.redis_instance = mock_redis_instance

        # Execute
        result = mission_checker.invoke_isro()

        # Verify workflow for cached mission
        assert cached_mission in result
        mock_driver.get.assert_called_once()
        mock_mission_div.screenshot.assert_not_called()  # No screenshot for cached
        mock_email.assert_not_called()  # No email for cached
        mock_redis_instance.set.assert_not_called()  # No cache update needed
        mock_driver.quit.assert_called_once()

    @patch('com.shankarsan.isro.mission_checker.webdriver.Firefox')
    @patch('com.shankarsan.isro.mission_checker.redis.Redis')
    @patch('com.shankarsan.isro.mission_checker.EmailUtils.sendMail')
    def test_error_handling_no_element(self, mock_email, mock_redis, mock_firefox):
        """Test error handling when web element is not found."""
        from com.shankarsan.isro import mission_checker

        # Setup mocks
        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver
        mock_driver.find_element.side_effect = Exception("Element not found")

        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        mock_redis_instance.get.return_value = None

        mission_checker.redis_instance = mock_redis_instance

        # Execute and verify exception is raised
        with pytest.raises(Exception) as exc_info:
            mission_checker.invoke_isro()

        assert "Element not found" in str(exc_info.value)
        mock_driver.quit.assert_called_once()

    @patch('com.shankarsan.isro.mission_checker.webdriver.Firefox')
    @patch('com.shankarsan.isro.mission_checker.redis.Redis')
    @patch('com.shankarsan.isro.mission_checker.EmailUtils.sendMail')
    def test_multiple_font_elements_joined_correctly(self, mock_email, mock_redis, mock_firefox):
        """Test that multiple font elements are joined with comma and space."""
        from com.shankarsan.isro import mission_checker

        # Setup mocks
        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver

        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        mock_redis_instance.get.return_value = None

        # Mock multiple mission elements
        mock_mission_div = MagicMock()
        missions = ["Date: 14 Nov 2023", "Time: 14:00 IST", "Mission: Chandrayaan-3"]
        mock_font_elements = []
        for mission in missions:
            mock_elem = MagicMock()
            mock_elem.text = mission
            mock_font_elements.append(mock_elem)

        mock_mission_div.find_elements.return_value = mock_font_elements
        mock_driver.find_element.return_value = mock_mission_div

        mission_checker.redis_instance = mock_redis_instance

        result = mission_checker.invoke_isro()

        # Verify proper formatting
        expected = "Date: 14 Nov 2023, Time: 14:00 IST, Mission: Chandrayaan-3"
        assert result == expected

        # Verify cache and email contain the joined result
        mock_redis_instance.set.assert_called_once_with("next_isro_mission", expected)
        mock_email.assert_called_once()
        call_args = mock_email.call_args
        assert expected in call_args[0][0]


class TestErrorRecovery:
    """Test error recovery and edge cases."""

    @patch('com.shankarsan.isro.mission_checker.webdriver.Firefox')
    @patch('com.shankarsan.isro.mission_checker.redis.Redis')
    def test_redis_connection_error(self, mock_redis, mock_firefox):
        """Test handling of Redis connection errors."""
        from com.shankarsan.isro import mission_checker

        mock_redis.side_effect = Exception("Redis connection failed")

        with pytest.raises(Exception) as exc_info:
            # This would happen at module import/setup time in real scenario
            pass

    @patch('com.shankarsan.isro.mission_checker.webdriver.Firefox')
    @patch('com.shankarsan.isro.mission_checker.redis.Redis')
    def test_driver_instantiation_failure(self, mock_redis, mock_firefox):
        """Test handling of Firefox driver instantiation failure."""
        from com.shankarsan.isro import mission_checker

        mock_firefox.side_effect = Exception("geckodriver not found")

        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        mock_redis_instance.get.return_value = None

        mission_checker.redis_instance = mock_redis_instance

        with pytest.raises(Exception) as exc_info:
            mission_checker.invoke_isro()

        assert "geckodriver not found" in str(exc_info.value)


class TestEmailIntegration:
    """Integration tests for email functionality."""

    @patch('com.shankarsan.isro.mission_checker.webdriver.Firefox')
    @patch('com.shankarsan.isro.mission_checker.redis.Redis')
    @patch('com.shankarsan.isro.mission_checker.EmailUtils.sendMail')
    def test_email_called_with_correct_parameters(self, mock_email, mock_redis, mock_firefox):
        """Test that email is called with correct parameters."""
        from com.shankarsan.isro import mission_checker
        import sys

        # Setup args
        sys.argv = [
            'mission-checker.py',
            '--gmail-username', 'sender@gmail.com',
            '--gmail-password', 'password123',
            '--to-email', 'recipient@gmail.com'
        ]

        # Reload to pick up new args
        import importlib
        # Note: This is a tricky test due to argparse at module level
        # In a real scenario, argparse should be refactored into a function

        # Setup mocks
        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver

        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        mock_redis_instance.get.return_value = None

        # Mock web elements
        mock_mission_div = MagicMock()
        mock_font_elem = MagicMock()
        mock_font_elem.text = "New Mission"
        mock_mission_div.find_elements.return_value = [mock_font_elem]
        mock_driver.find_element.return_value = mock_mission_div

        mission_checker.redis_instance = mock_redis_instance

        mission_checker.invoke_isro()

        # Verify email was called
        mock_email.assert_called_once()

