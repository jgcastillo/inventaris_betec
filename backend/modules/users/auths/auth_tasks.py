from pathlib import Path

from loguru import logger
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from shared.core.config import (
    DESCRIPTION,
    NO_RESPOND_EMAIL_ADDRESS,
    PROJECT_NAME,
    SENDGRID_API_KEY,
    URL_CHANGE_PSW,
)
from shared.utils.config_email_template import generate_email_template


def send_reset_psw_email_task(email_to: str, token: str):
    url = f"{URL_CHANGE_PSW}{token}"
    template = generate_email_template(url=url)

    subject = f"{DESCRIPTION}-{PROJECT_NAME} Recuperación de clave de acceso"
    message = Mail(
        from_email=NO_RESPOND_EMAIL_ADDRESS,
        to_emails=email_to,
        subject=subject,
        html_content=template,
    )

    try:
        sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
        response = sendgrid_client.send(message)
        logger.debug(f"status_code: {response.status_code}")
        logger.debug(f"response body: {response.body}")
        logger.debug(f"response Headers: {response.headers}")
    except Exception as e:
        logger.error(e)
