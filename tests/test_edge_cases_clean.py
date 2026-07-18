"""
Edge case and boundary tests for EmailUtils and NoDuplicateLogger modules.
Note: MissionChecker tests are in test_mission_checker.py
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

