"""
Format the readme.md file into the sphinx index.rst file.
"""

import inspect
import os
import time

import pypandoc


def write_index_rst(readme_file=None, write_file=None):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    out = (
        ".. SSS documentation index file, created by\n"
        f"   make_index.py on {time_str}\n\n"
    )

    if readme_file is None:
        main_path = os.path.dirname(
            os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
        )
        readme_file = os.path.join(main_path, "README.md")

    readme_text = pypandoc.convert_file(readme_file, "rst")

    # convert relative links in readme to explicit links
    readme_text = readme_text.replace(
        "`here <docs/computer_setup.md>`__", ":ref:`here <computer_setup>`"
    )

    readme_text = readme_text.replace(
        "`here <docs/developer_documentation.md>`__",
        ":ref:`here <developer_documentation>`",
    )

    readme_text = readme_text.replace(
        "`here <docs/user_documentation.md>`__", ":ref:`here <user_documentation>`"
    )

    # readme_text = readme_text.replace(
    #     "<.github/",
    #     "<https://github.com/RadioAstronomySoftwareGroup/pyradiosky/tree/main/.github/",
    # )

    out += readme_text
    out += (
        "\n\nFurther Documentation\n====================================\n"
        ".. toctree::\n"
        "   :maxdepth: 1\n\n"
        "   computer_setup\n"
        "   user_documentation\n"
        "   developer_documentation\n"
        "   table_definitions\n"
        "   functions\n"
    )

    out.replace("\u2018", "'").replace("\u2019", "'").replace("\xa0", " ")

    if write_file is None:
        write_path = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
        write_file = os.path.join(write_path, "index.rst")
    with open(write_file, "w") as file:
        file.write(out)
    print("wrote " + write_file)
