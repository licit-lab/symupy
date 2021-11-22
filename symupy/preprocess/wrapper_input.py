
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("ensemble", "templates"),
    autoescape=select_autoescape(
        [
            "xml",
        ]
    ),
)

def transform_data(TEST):
    VEHICLES = [dict(zip(KEYS, v)) for v in TEST]
    template = env.get_template("restitution.xml")
    return bytes(template.render(vehicles=VEHICLES), encoding="UTF8")
