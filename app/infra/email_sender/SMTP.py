import smtplib
from dataclasses import dataclass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@dataclass
class SMTPEmailSender:
    _host: str
    _port: int
    _company_email: str
    _password: str
    _server: smtplib.SMTP = None  # Initialize with None by default

    @classmethod
    def create(cls, host: str, port: int, username: str, password: str):
        # Initialize the class and create the SMTP connection
        smtp_email_sender: SMTPEmailSender = cls(
            _host=host,
            _port=port,
            _company_email=username,
            _password=password
        )
        smtp_email_sender._connect_to_smtp_server()  # Establish connection during initialization
        return smtp_email_sender

    def _connect_to_smtp_server(self) -> None:
        try:
            # Create the SMTP server connection and login
            self._server = smtplib.SMTP(self._host, self._port)
            self._server.starttls()  # Secure the connection
            self._server.login(self._company_email, self._password)
            print("SMTP connection established.")
        except Exception as e:
            print(f"Failed to connect to SMTP server: {e}")
            self._server = None

    def send_email(self, to_email: str, subject: str, copyright_txt: str, certificate_key: str) -> None:
        if not self._server:
            self._connect_to_smtp_server()

            if not self._server:
                print("No SMTP connection available.")
                return

        # Create a multipart email
        msg = MIMEMultipart()

        msg['From'] = self._company_email
        msg['To'] = to_email
        msg['Subject'] = subject

        txt_to_send: str = copyright_txt.format(certificate_key)

        # Attach the email body
        msg.attach(MIMEText(txt_to_send, 'plain'))

        try:
            # Send the email using the existing SMTP server connection
            self._server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def close(self) -> None:
        """Close the SMTP server connection when done."""
        if self._server:
            self._server.quit()
            print("SMTP connection closed.")
        else:
            print("No active SMTP connection to close.")
