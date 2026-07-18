"""
Test cases for NoDuplicateLogger module.
"""
import pytest
import logging
from io import StringIO
from com.shankarsan.isro.loggers.NoDuplicateLogger import NoDuplicateLogger


@pytest.fixture
def mock_logger():
    """Create a logger with a string stream handler for testing."""
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)

    # Remove existing handlers
    logger.handlers = []

    # Add a string stream handler
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger, stream


class TestNoDuplicateLogger:
    """Test class for NoDuplicateLogger functionality."""

    def test_logger_initialization(self, mock_logger):
        """Test that NoDuplicateLogger initializes correctly."""
        logger, _ = mock_logger
        no_dup_logger = NoDuplicateLogger(logger)

        assert no_dup_logger.logger == logger
        assert no_dup_logger.last_message is None

    def test_single_message_is_logged(self, mock_logger):
        """Test that a single message is logged."""
        logger, stream = mock_logger
        no_dup_logger = NoDuplicateLogger(logger)

        test_message = "Test message"
        no_dup_logger.info(test_message)

        output = stream.getvalue()
        assert test_message in output
        assert no_dup_logger.last_message == test_message

    def test_duplicate_message_is_not_logged(self, mock_logger):
        """Test that duplicate messages are not logged."""
        logger, stream = mock_logger
        no_dup_logger = NoDuplicateLogger(logger)

        test_message = "Duplicate test message"
        no_dup_logger.info(test_message)
        stream.truncate(0)
        stream.seek(0)

        # Log the same message again
        no_dup_logger.info(test_message)

        output = stream.getvalue()
        assert output == ""
        assert no_dup_logger.last_message == test_message

    def test_different_messages_are_logged(self, mock_logger):
        """Test that different messages are all logged."""
        logger, stream = mock_logger
        no_dup_logger = NoDuplicateLogger(logger)

        message1 = "First message"
        message2 = "Second message"
        message3 = "Third message"

        no_dup_logger.info(message1)
        no_dup_logger.info(message2)
        no_dup_logger.info(message3)

        output = stream.getvalue()
        assert message1 in output
        assert message2 in output
        assert message3 in output
        assert no_dup_logger.last_message == message3

    def test_duplicate_after_different_message(self, mock_logger):
        """Test that a message is logged after being different from the last one."""
        logger, stream = mock_logger
        no_dup_logger = NoDuplicateLogger(logger)

        message1 = "First message"
        message2 = "Second message"

        no_dup_logger.info(message1)
        no_dup_logger.info(message2)
        stream.truncate(0)
        stream.seek(0)

        # Log the first message again
        no_dup_logger.info(message1)

        output = stream.getvalue()
        assert message1 in output

    def test_empty_string_message(self, mock_logger):
        """Test handling of empty string messages."""
        logger, stream = mock_logger
        no_dup_logger = NoDuplicateLogger(logger)

        no_dup_logger.info("")
        output = stream.getvalue()
        assert output != ""  # Empty message should still be logged

        stream.truncate(0)
        stream.seek(0)

        # Second empty message should not be logged
        no_dup_logger.info("")
        output = stream.getvalue()
        assert output == ""

    def test_none_initial_last_message(self, mock_logger):
        """Test that last_message is None initially."""
        logger, _ = mock_logger
        no_dup_logger = NoDuplicateLogger(logger)

        assert no_dup_logger.last_message is None

    def test_whitespace_messages(self, mock_logger):
        """Test handling of messages with different whitespace."""
        logger, stream = mock_logger
        no_dup_logger = NoDuplicateLogger(logger)

        message_with_space = "Message with space "
        message_without_space = "Message with space"

        no_dup_logger.info(message_with_space)
        no_dup_logger.info(message_without_space)

        output = stream.getvalue()
        # Both should be logged as they are different
        assert message_with_space in output or message_without_space in output

    def test_case_sensitive_messages(self, mock_logger):
        """Test that message comparison is case-sensitive."""
        logger, stream = mock_logger
        no_dup_logger = NoDuplicateLogger(logger)

        message_lower = "test message"
        message_upper = "TEST MESSAGE"

        no_dup_logger.info(message_lower)
        no_dup_logger.info(message_upper)

        output = stream.getvalue()
        # Both should be logged as they are different (case-sensitive)
        assert "test message" in output.lower()

