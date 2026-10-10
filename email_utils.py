from pydantic import functional_serializers
from email.message import EmailMessage
import aiosmtplib
from fastapi.templating import Jinja2Templates
from config import settings

templates = Jinja2Templates(directory="templates")


async def send_email(
    subject: str,
    to_email: str,
    plain_text:str ,
    html_content: str | None = None
)-> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.mail_from
    msg["To"] = to_email

    msg.set_content(plain_text)

    if html_content:
        msg.add_alternative(html_content, subtype="html")

    await aiosmtplib.send(
        msg,
        hostname=settings.mail_server,
        port = settings.mail_port,
        username=settings.mail_username if settings.mail_username else None,
        password = settings.mail_password.get_secret_value() if settings.mail_password else None,
        start_tls = settings.mail_use_tls,
    )

async def send_password_reset_email(to_email:str, username:str, token:str)->None:
    reset_url = f"{settings.frontend_url}/reset-password?token={token}"
    try:
        template = templates.env.get_template("email/password_reset.html")
        html_content = template.render(reset_url=reset_url, username=username)
    except Exception:
        html_content = None

    plain_text = f"""Hi {username},
 You requested to reset your password. Click the link below to set a new password:
 {reset_url}

This link will expire in 1 hour.

If you did'nt request this, you can safely ignore this email.

Best regards,
The FastApi Blog Team
"""

    try:
        await send_email(
            to_email=to_email,
            subject="Reset Your Password - FastAPI Blog",
            plain_text=plain_text,
            html_content=html_content,
        )
    except Exception:
        return


    
    
    
    
