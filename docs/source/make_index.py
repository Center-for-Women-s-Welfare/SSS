# -*- mode: python; coding: utf-8 -*-

"""
Format the readme.md file into the sphinx index.rst file.
"""
import os
import inspect

import pypandoc
import time


def write_index_rst(readme_file=None, write_file=None):
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
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
    # readme_text = readme_text.replace(
    #     "<docs/",
    #     "<https://github.com/RadioAstronomySoftwareGroup/pyradiosky/tree/main/docs/",
    # )

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
        "   developer_docs\n"
    )

    out.replace("\u2018", "'").replace("\u2019", "'").replace("\xa0", " ")

    if write_file is None:
        write_path = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
        write_file = os.path.join(write_path, "index.rst")
    F = open(write_file, "w")
    F.write(out)
    print("wrote " + write_file)