from jinja2 import FileSystemLoader
from jinja2.environment import Environment

class TemplateRender:
    """
    Create, find and render templates for html page.
    :param folder: папка с шаблонами
    """

    def __init__(self, folder='templates'):
        self.folder = folder

    def render(self, template_name, **kwargs):
        """
        Рендер шаблонов из папки
        :param template_name: имя шаблона
        :param kwargs: параметры для передачи в шаблон
        :return:
        """

        env = Environment()
        env.loader = FileSystemLoader(self.folder)
        template = env.get_template(template_name)
        return template.render(**kwargs)
