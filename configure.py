import sys
from pathlib import Path

import caseconverter
import click
from jinja2 import Environment, FileSystemLoader


@click.command()
@click.argument("name")
@click.option("--debug/--no-debug", is_flag=True, default=True, help="Enable debug mode.")
def main(name: str, debug: bool):
    """
    This is a script to configure the project.

    It's intended to be called by the `ato create` command.

    This script is intended to be run in the same environment
    as the ato CLI, so it's expecting to have access to the
    same packages and tools; Jinja, etc...
    """

    # Common variables
    repo_root = Path(__file__).parent
    extended_globals = {
        "name": name,
        "caseconverter": caseconverter,
        "repo_root": repo_root,
    }

    # Load templates
    env = Environment(loader=FileSystemLoader("."))

    for template_path in Path(".").glob("**/*.j2"):
        # Figure out the target path and variables and what not
        target_path = template_path.parent / template_path.name.replace(
            ".j2", ""
        ).replace("__name__", caseconverter.kebabcase(name))

        extended_globals["rel_path"] = target_path
        extended_globals["python_path"] = sys.executable

        template = env.get_template(str(template_path), globals=extended_globals)

        # Make the noise!
        with target_path.open("w") as f:
            for chunk in template.generate():
                f.write(chunk)

        # Remove the template
        if not debug:
            template_path.unlink()

    # Remove this script
    if not debug:
        Path(__file__).unlink()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
