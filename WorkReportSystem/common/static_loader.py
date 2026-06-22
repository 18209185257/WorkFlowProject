# common/static_loader.py

import os


def load_js_files():

    js_dir = os.path.join(
        "static",
        "js"
    )

    scripts = []

    for file in os.listdir(js_dir):

        if file.endswith(".js"):

            file_path = os.path.join(
                js_dir,
                file
            )

            print("加载JS:", file_path)

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:

                scripts.append(
                    f.read()
                )

    return "\n".join(scripts)