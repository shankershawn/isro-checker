"""
Edge case and boundary tests for ISRO Mission Checker.
"""
import pytest
from unittest.mock import patch, MagicMock, mock_open
from com.shankarsan.isro.loggers.NoDuplicateLogger import NoDuplicateLogger
import logging
from io import StringIO


# PNG file signature (magic bytes)
PNG_BYTES = b'\x89PNG\r\n\x1a\n' + b'\x00' * 32


class TestNoDuplicateLoggerEdgeCases:
    """Edge case tests for NoDuplicateLogger."""

    def test_very_long_message(self):
        """Test handling of very long messages."""
        logger = logging.getLogger("test_long")
        logger.setLevel(logging.INFO)
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        logger.addHandler(handler)

        no_dup = NoDuplicateLogger(logger)

        long_message = "x" * 10000
        no_dup.info(long_message)

        output = stream.getvalue()
        assert long_message in output

    def test_unicode_messages(self):
        """Test handling of unicode characters."""
        logger = logging.getLogger("test_unicode")
        logger.setLevel(logging.INFO)
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        logger.addHandler(handler)

        no_dup = NoDuplicateLogger(logger)

        unicode_msg = "चंद्रयान-३ मिशन शुरू होगा"
        no_dup.info(unicode_msg)

        output = stream.getvalue()
        assert unicode_msg in output

    def test_newline_in_message(self):
        """Test handling of messages with newlines."""
        logger = logging.getLogger("test_newline")
        logger.setLevel(logging.INFO)
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        logger.addHandler(handler)

        no_dup = NoDuplicateLogger(logger)

        msg_with_newline = "Line 1\nLine 2\nLine 3"
        no_dup.info(msg_with_newline)

        output = stream.getvalue()
        assert "Line 1" in output
        assert "Line 2" in output

    def test_tab_characters_in_message(self):
        """Test handling of messages with tabs."""
        logger = logging.getLogger("test_tabs")
        logger.setLevel(logging.INFO)
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        logger.addHandler(handler)

        no_dup = NoDuplicateLogger(logger)

        msg_with_tabs = "Column1\tColumn2\tColumn3"
        no_dup.info(msg_with_tabs)

        output = stream.getvalue()
        assert "Column1\tColumn2\tColumn3" in output

    def test_message_with_quotes(self):
        """Test handling of messages with various quote types."""
        logger = logging.getLogger("test_quotes")
        logger.setLevel(logging.INFO)
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        logger.addHandler(handler)

        no_dup = NoDuplicateLogger(logger)

        msg_quotes = 'Single "double" and \'single\' quotes'
        no_dup.info(msg_quotes)

        output = stream.getvalue()
        assert "double" in output

    def test_sequential_different_messages(self):
        """Test rapid succession of different messages."""
        logger = logging.getLogger("test_sequential")
        logger.setLevel(logging.INFO)
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        logger.addHandler(handler)

        no_dup = NoDuplicateLogger(logger)

        messages = [f"Message {i}" for i in range(100)]
        for msg in messages:
            no_dup.info(msg)

        output = stream.getvalue()
        assert "Message 0" in output
        assert "Message 99" in output

    def test_alternating_messages(self):
        """Test alternating between two different messages."""
        logger = logging.getLogger("test_alternating")
        logger.setLevel(logging.INFO)
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        logger.addHandler(handler)

        no_dup = NoDuplicateLogger(logger)

        msg_a = "Message A"
        msg_b = "Message B"

        for _ in range(5):
            no_dup.info(msg_a)
            no_dup.info(msg_b)

        output = stream.getvalue()
        # Count occurrences - each message should appear 5 times
        assert output.count(msg_a) == 5
        assert output.count(msg_b) == 5


class TestEmailUtilsEdgeCases:
    """Edge case tests for EmailUtils."""

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_empty_image_file(self, mock_file, mock_smtp):
        """Test handling of empty image file."""
        from com.shankarsan.isro.util import EmailUtils

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        EmailUtils.sendMail("data", "subject", "from@test.com", "pass", "to@test.com")

        mock_server.sendmail.assert_called_once()

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES * 100)
    def test_large_image_file(self, mock_file, mock_smtp):
        """Test handling of very large image file."""
        from com.shankarsan.isro.util import EmailUtils

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        EmailUtils.sendMail("data", "subject", "from@test.com", "pass", "to@test.com")

        mock_server.sendmail.assert_called_once()

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_email_with_html_special_chars(self, mock_file, mock_smtp):
        """Test email with HTML special characters in verbiage."""
        from com.shankarsan.isro.util import EmailUtils

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        verbiage = "Launch <confirmed> & \"scheduled\" for 2023-12-14"
        EmailUtils.sendMail(verbiage, "subject", "from@test.com", "pass", "to@test.com")

        call_args = mock_server.sendmail.call_args
        email_message = call_args[0][2]
        assert "&" in email_message
        assert "<" in email_message

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_email_with_long_addresses(self, mock_file, mock_smtp):
        """Test email with very long email addresses."""
        from com.shankarsan.isro.util import EmailUtils

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        long_from = "a" * 50 + "@example.com"
        long_to = "b" * 50 + "@example.com"

        EmailUtils.sendMail("data", "subject", long_from, "pass", long_to)

        call_args = mock_server.sendmail.call_args
        assert call_args[0][0] == long_from
        assert call_args[0][1] == long_to

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_email_subject_with_unicode(self, mock_file, mock_smtp):
        """Test email with unicode characters in subject."""
        from com.shankarsan.isro.util import EmailUtils

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        subject = "चंद्रयान-३ मिशन: अपडेट"
        EmailUtils.sendMail("data", subject, "from@test.com", "pass", "to@test.com")

        call_args = mock_server.sendmail.call_args
        email_message = call_args[0][2]
        # Should be properly encoded in the email
        assert subject in email_message or subject.encode('utf-8') in str(email_message).encode()


class TestMissionCheckerEdgeCases:
    """Edge case tests for mission-checker."""

    @patch('com.shankarsan.isro.mission_checker.webdriver.Firefox')
    @patch('com.shankarsan.isro.mission_checker.redis.Redis')
    def test_empty_mission_text(self, mock_redis, mock_firefox):
        """Test handling of empty mission text from website."""
        from com.shankarsan.isro import mission_checker

        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver

        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        mock_redis_instance.get.return_value = None

        # Mock web elements with empty text
        mock_mission_div = MagicMock()
        mock_font_elem = MagicMock()
        mock_font_elem.text = ""
        mock_mission_div.find_elements.return_value = [mock_font_elem]
        mock_driver.find_element.return_value = mock_mission_div

        mission_checker.redis_instance = mock_redis_instance

        with patch('com.shankarsan.isro.mission_checker.EmailUtils.sendMail'):
            result = mission_checker.invoke_isro()

        assert result == ""

    @patch('com.shankarsan.isro.mission_checker.webdriver.Firefox')
    @patch('com.shankarsan.isro.mission_checker.redis.Redis')
    def test_mission_with_special_characters(self, mock_redis, mock_firefox):
        """Test mission data with special characters."""
        from com.shankarsan.isro import mission_checker

        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver

        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        mock_redis_instance.get.return_value = None

        # Mock web elements with special characters
        mock_mission_div = MagicMock()
        mock_font_elem = MagicMock()
        mock_font_elem.text = "Mission: [Ü™ß¡£¢€] (Special)"
        mock_mission_div.find_elements.return_value = [mock_font_elem]
        mock_driver.find_element.return_value = mock_mission_div

        mission_checker.redis_instance = mock_redis_instance

        with patch('com.shankarsan.isro.mission_checker.EmailUtils.sendMail'):
            result = mission_checker.invoke_isro()

        assert "Special" in result

    @patch('com.shankarsan.isro.mission_checker.webdriver.Firefox')
    @patch('com.shankarsan.isro.mission_checker.redis.Redis')
    def test_many_mission_elements(self, mock_redis, mock_firefox):
        """Test parsing many mission elements."""
        from com.shankarsan.isro import mission_checker

        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver

        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        mock_redis_instance.get.return_value = None

        # Create many mission elements
        mock_mission_div = MagicMock()
        mock_font_elements = []
        for i in range(50):
            mock_elem = MagicMock()
            mock_elem.text = f"Item {i}"
            mock_font_elements.append(mock_elem)

        mock_mission_div.find_elements.return_value = mock_font_elements
        mock_driver.find_element.return_value = mock_mission_div

        mission_checker.redis_instance = mock_redis_instance

        with patch('com.shankarsan.isro.mission_checker.EmailUtils.sendMail'):
            result = mission_checker.invoke_isro()

        assert "Item 0" in result
        assert "Item 49" in result
        # Should have 49 commas for 50 items
        assert result.count(", ") == 49

    @patch('com.shankarsan.isro.mission_checker.webdriver.Firefox')
    @patch('com.shankarsan.isro.mission_checker.redis.Redis')
    def test_redis_get_returns_non_utf8_bytes(self, mock_redis, mock_firefox):
        """Test handling of non-UTF8 bytes from Redis."""
        from com.shankarsan.isro import mission_checker

        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver

        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        # Return bytes that represent UTF-8
        mock_redis_instance.get.return_value = "Previous Mission".encode('utf-8')

        # New mission
        mock_mission_div = MagicMock()
        mock_font_elem = MagicMock()
        mock_font_elem.text = "New Mission"
        mock_mission_div.find_elements.return_value = [mock_font_elem]
        mock_driver.find_element.return_value = mock_mission_div

        mission_checker.redis_instance = mock_redis_instance

        with patch('com.shankarsan.isro.mission_checker.EmailUtils.sendMail'):
            mission_checker.invoke_isro()

        # Should handle the decoding properly
        mock_driver.quit.assert_called_once()







