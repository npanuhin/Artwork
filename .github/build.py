from typing import List

from json import loads
import os
from bs4 import BeautifulSoup
from PIL import Image
import re
from ast import literal_eval

import render
render.TMP_FOLDER = "rendertmp"


def make_path(*paths: List[str]) -> str:
    '''Combines paths and normalizes the result'''
    return os.path.normpath(os.path.join(*paths))


def checkGithubPages(image: str) -> bool:
    if not os.path.exists(make_path(root_path, "SVG", image, "src/conf.json")):
        return False
    with open(make_path(root_path, "SVG", image, "src/conf.json"), 'r', encoding="utf-8") as conf_file:
        conf_data = loads(conf_file.read(), encoding="utf-8")
    if "github_pages" not in conf_data or not isinstance(conf_data["github_pages"], dict):
        print("Warning! Can not handle due to invalid parameters: \"" + image + "\"")
        return False
    if "status" not in conf_data["github_pages"] or not isinstance(conf_data["github_pages"]["status"], bool):
        print("Warning! Can not handle due to invalid parameters: \"" + image + "\"")
        return False
    if not conf_data["github_pages"]["status"]:
        return False
    return True


def githubPages() -> None:
    '''Updates Github Pages'''
    print("Updating Github Pages...")
    rp = root_path

    # ---SVG---
    with open(make_path(rp, ".github/templates/SVG.md"), 'r', encoding='utf-8') as file:
        svg_md = file.read().strip()

    images = []

    for image in os.listdir(make_path(rp, "SVG")):
        if not checkGithubPages(image):
            continue
        images.append("-   [{name}](./{url} \"See {name} SGV image\")".format(name=image, url=image.replace(' ', '%20')))

    svg_md += "\n\n" + "\n".join(images)

    # Save
    with open(make_path(rp, "SVG/README.md"), 'w', encoding='utf-8') as file:
        file.write(svg_md)

    print("Created README.md with list of SVG images")

    # ---Images---
    with open(make_path(rp, ".github/templates/image.md"), 'r', encoding='utf-8') as file:
        image_md_template = file.read()
    with open(make_path(rp, ".github/templates/not_colored_image.md"), 'r', encoding="utf-8") as file:
        image_not_colored_template = file.read().strip()
    with open(make_path(rp, ".github/templates/colored_image.md"), 'r', encoding="utf-8") as file:
        image_colored_template = file.read().strip()

    for image in os.listdir(make_path(rp, "SVG")):
        # Many checks
        if not checkGithubPages(image):
            continue
        with open(make_path(rp, "SVG", image, "src/conf.json"), 'r', encoding="utf-8") as conf_file:
            conf_data = loads(conf_file.read(), encoding="utf-8")['github_pages']

        if "name" not in conf_data or not isinstance(conf_data["name"], str):
            print("Warning! Can not handle due to invalid parameters: \"" + image + "\"")
            continue

        has_not_colored_version = (image + ".svg" in os.listdir(make_path(rp, "SVG", image)))
        has_colored_version = (image + ".colored.svg" in os.listdir(make_path(rp, "SVG", image)))

        if has_not_colored_version and "name" not in conf_data or not isinstance(conf_data["name"], str):
            print("Warning! Can not handle due to invalid parameters: \"" + image + "\"")
            continue
        if has_colored_version and "colored_name" not in conf_data or not isinstance(conf_data["colored_name"], str):
            print("Warning! Can not handle due to invalid parameters: \"" + image + "\"")
            continue

        if not os.path.exists(make_path(rp, "SVG", image, "src/template.md")) or not os.path.exists(make_path(rp, "SVG", image, "src/description.md")):
            print("Warning! Can not handle \"" + image + "\". No such file or directory.")
            continue

        with open(make_path(rp, "SVG", image, "src/template.md"), 'r', encoding="utf-8") as file:
            image_template = file.read()
        if image_template:
            image_template = "\n" + image_template + "\n"
        with open(make_path(rp, "SVG", image, "src/description.md"), 'r', encoding="utf-8") as file:
            image_description = file.read()
        if image_description:
            image_description = "\n" + image_description + "\n"

        image_md = image_md_template

        image_colored_template_loc = image_colored_template
        if has_colored_version and has_not_colored_version:
            image_colored_template_loc += "\n"

        for _ in range(2):
            image_md = image_md.format(
                image_name=conf_data["name"] if has_not_colored_version else "",
                image_colored_name=conf_data["colored_name"] if has_colored_version else "",
                image_path=image + ".svg",
                image_colored_path=image + ".colored.svg",
                description_text=image_description,
                template_text=image_template,
                not_colored_image=image_not_colored_template if has_not_colored_version else "",
                colored_image=image_colored_template_loc if has_colored_version else ""
            )

        # Save
        with open(make_path(rp, "SVG", image, "README.md"), 'w', encoding='utf-8') as file:
            file.write(image_md.strip())

        print("Created README.md for {name}".format(name=image))


def renderAll() -> None:
    '''Renders all SVG files'''
    print("Rendering files...")
    rp = root_path
    re_find = re.compile(r"^\d+\)[A-Za-zА-Яа-я0-9 \/\\\t\-\+=\*\)\(\.<>\?\,\%\$\#\@\!\^\;\"\'\`\~]+\((\d+)x(\d+)\)\.png$")
    re_find_colored = re.compile(r"^\d+\)[A-Za-zА-Яа-я0-9 \/\\\t\-\+=\*\)\(\.<>\?\,\%\$\#\@\!\^\;\"\'\`\~]+\((\d+)x(\d+)\)\.colored\.png$")

    for image in os.listdir(make_path(rp, "SVG")):
        if not os.path.exists(make_path(rp, "SVG", image, "src/conf.json")):
            continue

        with open(make_path(rp, "SVG", image, "src/conf.json"), 'r', encoding="utf-8") as conf_file:
            conf_data = loads(conf_file.read(), encoding="utf-8")

        if "render_sizes" not in conf_data:
            continue

        sizes = conf_data["render_sizes"]

        render_path = make_path(rp, "SVG", image, "render")

        if not os.path.exists(render_path):
            os.mkdir(render_path)

        if update_old_files:
            for file in os.listdir(render_path):
                os.remove(make_path(render_path, file))

        for svg_filename in os.listdir(make_path(rp, "SVG", image)):
            if os.path.splitext(svg_filename)[1] != ".svg":
                continue

            svg_basename = os.path.splitext(svg_filename)[0]
            svg_path = make_path(rp, "SVG", image, svg_filename)
            output_path = make_path(render_path, svg_basename + ".png")

            # List of sizes, that are already rendered
            not_render = []
            if not update_old_files:
                if svg_basename.endswith(".colored"):
                    for filename in os.listdir(render_path):
                        matches = re_find_colored.match(filename)
                        if matches:
                            not_render.append([int(matches.group(1)), int(matches.group(2))])
                else:
                    for filename in os.listdir(render_path):
                        matches = re_find.match(filename)
                        if matches:
                            not_render.append([int(matches.group(1)), int(matches.group(2))])

            if svg_basename.endswith(".colored"):
                output_name = "{i}) {name} ({rw}x{rh}).colored.png"
                svg_basename = svg_basename[:-8]
            else:
                output_name = "{i}) {name} ({rw}x{rh}).png"

            # SVG sizes
            with open(svg_path, 'r', encoding='utf-8') as svg_file_data:
                svg_data = svg_file_data.read()
            image_sizes = BeautifulSoup(svg_data, "lxml").find("svg").get('viewbox').split()
            width = int(image_sizes[2]) - int(image_sizes[0])
            height = int(image_sizes[3]) - int(image_sizes[1])

            index_length = len(str(len(sizes)))
            index = 0
            for x, y in sizes.values():
                index += 1
                if not (isinstance(x, str) ^ isinstance(y, str) and (x is None) ^ (y is None)):
                    print("Warning! Can not handle due to invalid parameters: \"" + svg_path + "\"")
                    continue

                if y is None:
                    x = literal_eval(x.format(w=width, h=height))
                else:
                    y = literal_eval(y.format(w=width, h=height))

                flag = False
                for test_x, test_y in not_render:
                    if (y is None and test_x == x) or (x is None and test_y == y):
                        flag = True
                        break
                if flag:
                    continue

                if y is None:
                    # Render using width
                    render.renderSvg(svg_path, output_path, width=x)
                else:
                    # Render using height
                    render.renderSvg(svg_path, output_path, height=y)

                # Result image sizes
                result_width, result_height = Image.open(output_path).size

                # Save with correct name
                os.rename(output_path, make_path(render_path, output_name.format(
                    i=str(index).zfill(index_length), name=svg_basename, rw=result_width, rh=result_height
                )))

                print("{name} (width: {w}, height: {h}) rendered as png image (width: {rw}, height: {rh})".format(
                    name=svg_filename,
                    w=width, h=height,
                    rw=result_width, rh=result_height
                ))


def main() -> None:
    print("Starting build...")

    renderAll()
    githubPages()

    print("Build complete.")


# ---SETTINGS--- #

# Update all old rendered files
update_old_files = False

# Path to the root of repository
root_path = "..\\"

# ---SETTINGS--- #


if __name__ == "__main__":
    main()
