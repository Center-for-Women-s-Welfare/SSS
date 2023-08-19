# -*- mode: python; coding: utf-8 -*-

"""
Format the readme.md file into the sphinx index.rst file.
"""
import os
import inspect

import pypandoc
import time

md_files_to_convert = [
    "computer_setup.md",
    "developer_documentation.md",
    "user_documentation.md",
]


def write_rst_files(input_files=None, write_files=None):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    if input_files is None:
        main_path = os.path.dirname(
            os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
        )
        input_files = [
            os.path.join(main_path, "docs", fname) for fname in md_files_to_convert
        ]

    fname_bases = [
        os.path.splitext(os.path.basename(fname))[0] for fname in input_files
    ]

    if write_files is None:
        write_path = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
        write_files = [os.path.join(write_path, fb + ".rst") for fb in fname_bases]

    for f_ind, fname in enumerate(input_files):
        out = (
            f".. SSS documentation {fname_bases[f_ind]} file, created by\n"
            f"   make_computer_setup.py on {time_str}\n\n"
        )

        input_text = ".. _" + fname_bases[f_ind] + ":\n\n"
        input_text += pypandoc.convert_file(fname, "rst")

        out += input_text

        out.replace("\u2018", "'").replace("\u2019", "'").replace("\xa0", " ")

        F = open(write_files[f_ind], "w")
        F.write(out)
        print("wrote " + write_files[f_ind])
