from jinja2 import Environment, FileSystemLoader

def verify_auth_template(context):
    """Повертає html шаблон для верифікації реєстрації"""
    environment = Environment(loader=FileSystemLoader("src/email_template/"))
    template = environment.get_template("verify_account.html")
    return template.render(context)