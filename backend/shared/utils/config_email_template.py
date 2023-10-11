from fastapi.templating import Jinja2Templates


def generate_email_template(url: str) -> str:
    template = Jinja2Templates(directory="/backend/shared/email_templates/")
    html = template.get_template("reset_password.html").render({"url": url})

    return html
