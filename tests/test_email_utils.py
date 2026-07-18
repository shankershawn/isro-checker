"""
Test cases for EmailUtils module.
"""
import pytest
from unittest.mock import patch, MagicMock, call, mock_open
from com.shankarsan.isro.util import EmailUtils


# PNG file signature (magic bytes)
PNG_BYTES = b'\x89PNG\r\n\x1a\n' + b'\x00' * 32


class TestEmailUtils:
    """Test class for EmailUtils functionality."""

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_send_mail_successfully(self, mock_file, mock_smtp):
        """Test successful email sending."""
        # Setup mock SMTP
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Test data
        verbiage = "Test mission data"
        subject = "ISRO Launch Update"
        from_addr = "test@gmail.com"
        from_pass = "password123"
        to_addr = "recipient@example.com"

        # Call the function
        EmailUtils.sendMail(verbiage, subject, from_addr, from_pass, to_addr)

        # Verify SMTP was called correctly
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(from_addr, from_pass)
        mock_server.sendmail.assert_called_once()

        # Verify the sendmail was called with correct parameters
        call_args = mock_server.sendmail.call_args
        assert call_args[0][0] == from_addr
        assert call_args[0][1] == to_addr
        assert "Test mission data" in call_args[0][2]

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_send_mail_includes_correct_subject(self, mock_file, mock_smtp):
        """Test that email includes correct subject."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        subject = "ISRO Mission Alert"
        EmailUtils.sendMail("data", subject, "from@test.com", "pass", "to@test.com")

        call_args = mock_server.sendmail.call_args
        email_message = call_args[0][2]
        assert subject in email_message

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_send_mail_includes_verbiage(self, mock_file, mock_smtp):
        """Test that email includes the provided verbiage."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        verbiage = "Chandrayaan-3 launch confirmed for December 2023"
        EmailUtils.sendMail(verbiage, "subject", "from@test.com", "pass", "to@test.com")

        call_args = mock_server.sendmail.call_args
        email_message = call_args[0][2]
        assert verbiage in email_message

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_send_mail_includes_image_reference(self, mock_file, mock_smtp):
        """Test that email includes image reference."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        EmailUtils.sendMail("data", "subject", "from@test.com", "pass", "to@test.com")

        call_args = mock_server.sendmail.call_args
        email_message = call_args[0][2]
        assert "cid:myImage" in email_message

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_send_mail_includes_registration_link(self, mock_file, mock_smtp):
        """Test that email includes registration link."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        EmailUtils.sendMail("data", "subject", "from@test.com", "pass", "to@test.com")

        call_args = mock_server.sendmail.call_args
        email_message = call_args[0][2]
        assert "https://lvg.shar.gov.in/VSCREGISTRATION/index.jsp" in email_message

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_send_mail_opens_image_file(self, mock_file, mock_smtp):
        """Test that email function opens the mission.png file."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        EmailUtils.sendMail("data", "subject", "from@test.com", "pass", "to@test.com")

        # Verify the file was opened
        mock_file.assert_called_once_with('mission.png', 'rb')

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_send_mail_with_special_characters_in_verbiage(self, mock_file, mock_smtp):
        """Test email with special characters in verbiage."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        verbiage = "Aditya-L1: <Special> & \"Quoted\" Characters"
        EmailUtils.sendMail(verbiage, "subject", "from@test.com", "pass", "to@test.com")

        mock_server.sendmail.assert_called_once()

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_send_mail_multipart_message_structure(self, mock_file, mock_smtp):
        """Test that email is sent as multipart/related."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        EmailUtils.sendMail("data", "subject", "from@test.com", "pass", "to@test.com")

        call_args = mock_server.sendmail.call_args
        email_message = call_args[0][2]
        # Multipart messages contain boundary markers
        assert "multipart/related" in email_message or "boundary=" in email_message

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_send_mail_smtp_connection_closed(self, mock_file, mock_smtp):
        """Test that SMTP connection is properly closed after sending."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        EmailUtils.sendMail("data", "subject", "from@test.com", "pass", "to@test.com")

        # The context manager should be called, ensuring the connection is closed
        mock_smtp.return_value.__exit__.assert_called_once()

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP', side_effect=Exception("SMTP Error"))
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_send_mail_smtp_error(self, mock_file, mock_smtp):
        """Test that SMTP errors are propagated."""
        with pytest.raises(Exception) as exc_info:
            EmailUtils.sendMail("data", "subject", "from@test.com", "pass", "to@test.com")

        assert "SMTP Error" in str(exc_info.value)

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', side_effect=FileNotFoundError("mission.png not found"))
    def test_send_mail_image_file_not_found(self, mock_file, mock_smtp):
        """Test that FileNotFoundError is raised when image is not found."""
        with pytest.raises(FileNotFoundError):
            EmailUtils.sendMail("data", "subject", "from@test.com", "pass", "to@test.com")

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_send_mail_from_and_to_addresses(self, mock_file, mock_smtp):
        """Test that from and to addresses are correctly set."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        from_addr = "sender@gmail.com"
        to_addr = "receiver@gmail.com"

        EmailUtils.sendMail("data", "subject", from_addr, "pass", to_addr)

        call_args = mock_server.sendmail.call_args
        assert call_args[0][0] == from_addr
        assert call_args[0][1] == to_addr

    @patch('com.shankarsan.isro.util.EmailUtils.smtplib.SMTP')
    @patch('com.shankarsan.isro.util.EmailUtils.open', new_callable=mock_open, read_data=PNG_BYTES)
    def test_send_mail_starttls_called(self, mock_file, mock_smtp):
        """Test that STARTTLS is called for secure connection."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        EmailUtils.sendMail("data", "subject", "from@test.com", "pass", "to@test.com")

        mock_server.starttls.assert_called_once()















