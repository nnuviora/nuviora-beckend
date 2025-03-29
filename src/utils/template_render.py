from jinja2 import Environment, FileSystemLoader


async def get_template(template_name: str, context: dict) -> str:
    env = Environment(loader=FileSystemLoader("utils/templates"))
    template = env.get_template(template_name)

    return template.render(context)