from jinja2 import Environment, FileSystemLoader
from Telegram.config import template_folder as template_folder_config


class MyJinja:
    def __init__(self, template_folder: str = None, template_file: str = 'course_registration.html'):
        if template_folder is None:
            self.template_folder = template_folder_config
        self.environment = Environment(auto_reload=True, loader=FileSystemLoader(self.template_folder))
        self.template_file = self.environment.get_template(template_file)

    def render_document(self, user) -> str:
        return self.template_file.render(user=user)
