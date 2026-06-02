import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import markdown

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.smtp_from = os.getenv("SMTP_FROM", self.smtp_user)
        logger.info("EmailService initialized")

    def send_markdown_email(
        self,
        recipients: list,
        subject: str,
        markdown_content: str
    ) -> bool:
        if not all([self.smtp_host, self.smtp_user, self.smtp_password]):
            logger.warning("SMTP configuration incomplete. Logging email instead of sending.")
            self._log_email(recipients, subject, markdown_content)
            return True

        try:
            html_content = markdown.markdown(
                markdown_content,
                extensions=['tables', 'fenced_code']
            )

            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_from
            msg['To'] = ", ".join(recipients)
            msg['Subject'] = subject

            text_part = MIMEText(markdown_content, 'plain', 'utf-8')
            html_part = MIMEText(html_content, 'html', 'utf-8')

            msg.attach(text_part)
            msg.attach(html_part)

            filename = f"碳交易策略会纪要_{datetime.now().strftime('%Y%m%d')}.md"
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(markdown_content.encode('utf-8'))
            encoders.encode_base64(attachment)
            attachment.add_header(
                'Content-Disposition',
                f'attachment; filename="{filename}"'
            )
            msg.attach(attachment)

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_from, recipients, msg.as_string())

            logger.info(f"Email sent successfully to {len(recipients)} recipients")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    def _log_email(self, recipients: list, subject: str, content: str):
        log_file = f"email_log_{datetime.now().strftime('%Y%m%d')}.txt"
        log_path = os.path.join(os.path.dirname(__file__), '..', 'logs', log_file)
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"收件人: {', '.join(recipients)}\n")
            f.write(f"主题: {subject}\n")
            f.write(f"内容:\n{content}\n")
            f.write(f"{'='*80}\n")

        logger.info(f"Email logged to {log_path}")
