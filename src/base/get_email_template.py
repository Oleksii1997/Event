from jinja2 import Environment, FileSystemLoader


def get_email_template(context: dict, template_name: str):
    """Повертає html шаблон для надсилання електронного листа"""
    environment = Environment(loader=FileSystemLoader("src/email_template/"))
    template = environment.get_template(template_name)
    return template.render(context)
