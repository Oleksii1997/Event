from src.base import email

def send_new_account_email():
    email.send_email("oleksiygr@i.ua", subject_template="<p>Hi</p>", html_template="<p> Hello </p>",
                     environment={})