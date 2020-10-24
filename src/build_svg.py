from typing import List

from json import load as jsonLoad, loads as jsonLoads
import os
from bs4 import BeautifulSoup
from PIL import Image
import re
from ast import literal_eval
from requests import post as req_post
from time import sleep

import svg_render
svg_render.TMP_FOLDER = "rendertmp"


XML_HEADER = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
XML_HEADER_SIZE = 40  # Size of "<?xml version="1.0" encoding="utf-8"?>\n"
VERSION_HEADER = "version=\"1.1\""


def makePath(*paths: List[str]) -> str:
    '''Combines paths and normalizes the result'''
    return os.path.normpath(os.path.join(*paths))


def minify(code: str) -> str:
    r = req_post("https://htmlcompressor.com/compress", data={
        "code_type": "html",
        "output_format": "text",
        "code": code,

        "html_level": 3,
        "html_single_line": True,
        "html_keep_quotes": True,
        "minimize_style": True,
        "keep_comments": False,
        "minimize_css": True,
    }).text

    sleep(request_sleep_time)

    try:
        r = jsonLoads(r)
        print("\nWarning! Can not handle result from htmlcompressor.com\n")
    except Exception:
        pass

    return r


def prettifySize(value: int) -> str:
    if value < 1024:
        return str(round(value, 0)) + " B"
    value /= 1024
    if value < 1024:
        return str(round(value, 2)) + " kB"
    value /= 1024
    if value < 1024:
        return str(round(value, 2)) + " MB"
    value /= 1024
    if value < 1024:
        return str(round(value, 2)) + " GB"
    return str(round(value / 1024, 2)) + " TB"


def makeUrl(string: str) -> str:
    return string.replace(" ", "%20")


def checkGithubPages(image: str) -> bool:
    '''Checks whether to create a page for an image'''
    if not os.path.exists(makePath(root_path, "SVG", image, "src/conf.json")):
        return False
    with open(makePath(root_path, "SVG", image, "src/conf.json"), 'r', encoding="utf-8") as conf_file:
        conf_data = jsonLoad(conf_file, encoding="utf-8")
    if ("github_pages" not in conf_data or
        not isinstance(conf_data["github_pages"], dict) or
        "status" not in conf_data["github_pages"] or
            not isinstance(conf_data["github_pages"]["status"], bool)):

        print("Warning! Can not handle due to invalid parameters: \"" + image + "\"")
        return False

    return conf_data["github_pages"]["status"]


def githubPages() -> None:
    '''Updates Github Pages'''
    print("Updating Github Pages...")
    rp = root_path

    total_svg_size = 0
    total_compressed_svg_size = 0
    svg_files_count = 0

    # ---SVG list---
    with open(makePath(rp, "src/templates/svg_list.md"), 'r', encoding='utf-8') as file:
        svg_md = file.read().strip()

    images = []

    for image in os.listdir(makePath(rp, "SVG")):
        if checkGithubPages(image):
            images.append("-   [{name}](./{url} \"See {name} SVG image\")".format(name=image, url=makeUrl(image)))

    with open(makePath(rp, "SVG/README.md"), 'w', encoding='utf-8') as file:
        file.write(svg_md + "\n\n" + "\n".join(images))

    print("Created README.md with list of SVG images")

    # ---Images---
    with open(makePath(rp, "src/templates/image.md"), 'r', encoding='utf-8') as image_template_file, \
            open(makePath(rp, "src/templates/not_colored_image.md"), 'r', encoding="utf-8") as image_not_colored_template_file, \
            open(makePath(rp, "src/templates/colored_image.md"), 'r', encoding="utf-8") as image_colored_template_file:
        image_md_template = image_template_file.read()
        image_not_colored_template = image_not_colored_template_file.read().strip()
        image_colored_template = image_colored_template_file.read().strip()

    for image in os.listdir(makePath(rp, "SVG")):
        if not checkGithubPages(image):
            continue

        if os.path.exists(makePath(rp, "SVG", image, "README.md")):
            os.remove(makePath(rp, "SVG", image, "README.md"))

        with open(makePath(rp, "SVG", image, "src/conf.json"), 'r', encoding="utf-8") as conf_file:
            conf_data = jsonLoad(conf_file, encoding="utf-8")['github_pages']

        has_not_colored_version = (image + ".svg" in os.listdir(makePath(rp, "SVG", image)))
        has_colored_version = (image + ".colored.svg" in os.listdir(makePath(rp, "SVG", image)))

        # Getting image template
        if os.path.exists(makePath(rp, "SVG", image, "src/template.md")):
            with open(makePath(rp, "SVG", image, "src/template.md"), 'r', encoding="utf-8") as file:
                image_template = file.read().strip()
                if image_template:
                    image_template = image_template + "\n"
        else:
            image_template = ""

        # Getting image description
        if os.path.exists(makePath(rp, "SVG", image, "src/description.md")):
            with open(makePath(rp, "SVG", image, "src/description.md"), 'r', encoding="utf-8") as file:
                image_description = file.read().strip()
                if image_description:
                    image_description = image_description + "\n"
        else:
            image_description = ""

        image_md = image_md_template
        image_colored_template_loc = image_colored_template

        if has_colored_version and has_not_colored_version:
            image_colored_template_loc += "\n"

        image_size, image_compressed_size = "", ""
        image_colored_size, image_colored_compressed_size = "", ""

        if has_not_colored_version:
            with open(makePath(rp, "SVG", image, image + ".svg"), 'r', encoding="utf-8") as svg_file:
                svg_file_data = svg_file.read().strip()

            with open(makePath(rp, "SVG", image, image + ".svg"), 'w', encoding="utf-8") as svg_file, \
                    open(makePath(rp, "SVG", image, "src", image + ".min.svg"), 'w', encoding="utf-8") as compressed_svg_file:
                svg_file.write(svg_file_data + "\n")

                compressed_svg_file.write(minify(
                    svg_file_data.replace(XML_HEADER, "").replace(VERSION_HEADER, "")
                ).strip())

            image_size = os.path.getsize(
                makePath(rp, "SVG", image, image + ".svg")
            ) - XML_HEADER_SIZE

            total_svg_size += image_size
            svg_files_count += 1
            image_size = prettifySize(image_size)

            compressed_svg_size = os.path.getsize(makePath(rp, "SVG", image, "src", image + ".min.svg"))

            total_compressed_svg_size += compressed_svg_size
            image_compressed_size = prettifySize(compressed_svg_size)

        if has_colored_version:
            with open(makePath(rp, "SVG", image, image + ".colored.svg"), 'r', encoding="utf-8") as svg_file:
                svg_file_data = svg_file.read().strip()

            with open(makePath(rp, "SVG", image, image + ".colored.svg"), 'w', encoding="utf-8") as svg_file, \
                    open(makePath(rp, "SVG", image, "src", image + ".colored.min.svg"), 'w', encoding="utf-8") as compressed_svg_file:
                svg_file.write(svg_file_data + "\n")

                compressed_svg_file.write(minify(
                    svg_file_data.replace(XML_HEADER, "").replace(VERSION_HEADER, "")
                ).strip())

            image_colored_size = os.path.getsize(
                makePath(rp, "SVG", image, image + ".colored.svg")
            ) - XML_HEADER_SIZE

            total_svg_size += image_colored_size
            svg_files_count += 1
            image_colored_size = prettifySize(image_colored_size)

            compressed_svg_size = os.path.getsize(makePath(rp, "SVG", image, "src", image + ".colored.min.svg"))

            total_compressed_svg_size += compressed_svg_size
            image_colored_compressed_size = prettifySize(compressed_svg_size)

        for _ in range(3):
            image_md = image_md.format(
                image=image,
                image_url=makeUrl(image),

                image_colored=image + ".colored",
                image_colored_url=makeUrl(image + ".colored"),

                image_name=conf_data["name"],
                image_name_url=makeUrl(conf_data["name"]),

                image_colored_name=conf_data["colored_name"] if has_colored_version else "",
                image_colored_name_url=makeUrl(conf_data["colored_name"] if has_colored_version else ""),

                image_path=image + ".svg",
                image_path_url=makeUrl(image + ".svg"),

                image_compressed_path=image + ".min.svg",
                image_compressed_path_url=makeUrl(image + ".min.svg"),

                image_colored_path=image + ".colored.svg",
                image_colored_path_url=makeUrl(image + ".colored.svg"),

                image_colored_compressed_path=image + ".colored.min.svg",
                image_colored_compressed_path_url=makeUrl(image + ".colored.min.svg"),

                not_colored_template=image_not_colored_template if has_not_colored_version else "",
                colored_template=image_colored_template_loc if has_colored_version else "",

                template_text=image_template,
                description_text=image_description,

                image_size=image_size,
                image_size_url=makeUrl(image_size),

                image_compressed_size=image_compressed_size,
                image_compressed_size_url=makeUrl(image_compressed_size),

                image_colored_size=image_colored_size,
                image_colored_size_url=makeUrl(image_colored_size),

                image_colored_compressed_size=image_colored_compressed_size,
                image_colored_compressed_size_url=makeUrl(image_colored_compressed_size),

                not_colored_image_shown=" shown" if has_not_colored_version and not has_colored_version else "",

                beautified_pure="-   [Beautified black-and-white version]({} \"Download beautified black-and-white SVG\")\n".format(
                    makeUrl(image + ".svg")
                ) if has_not_colored_version else "",
                compressed_pure="-   [Compressed black-and-white version]({} \"Download compressed black-and-white SVG\")\n".format(
                    makeUrl("./src/" + image + ".min.svg")
                ) if has_not_colored_version else "",
                beautified_colored="-   [Beautified colored version]({} \"Download beautified colored SVG\")\n".format(
                    makeUrl(image + ".colored.svg")
                ) if has_colored_version else "",
                compressed_colored="-   [Compressed colored version]({} \"Download compressed colored SVG\")\n".format(
                    makeUrl("./src/" + image + ".colored.min.svg")
                ) if has_colored_version else "",
                ai_pure="-   [*Adobe Illustrator* source file]({} \"Download Adobe Illustrator (.ai) source file\")\n".format(
                    makeUrl("./src/" + image + ".ai")
                ) if has_not_colored_version else "",
                ai_colored="-   [*Adobe Illustrator* source file with colors]({} \"Download Adobe Illustrator (.ai) source file with colors\")\n".format(
                    makeUrl("./src/" + image + ".colored.ai")
                ) if has_colored_version else ""
            )

        # Save
        with open(makePath(rp, "SVG", image, "README.md"), 'w', encoding='utf-8') as file:
            file.write(image_md.strip())

        print("Created README.md for {name}".format(name=image))

    # ---Main README---
    # with open(makePath(rp, "src/templates/MAIN.md"), 'r', encoding='utf-8') as file:
    #     readme_data = file.read().strip()

    # average_svg_size = prettifySize(total_svg_size / svg_files_count)
    # average_compressed_svg_size = prettifySize(total_compressed_svg_size / svg_files_count)

    # readme_data = readme_data.format(
    #     average_svg_size=average_svg_size,
    #     average_svg_size_url=makeUrl(average_svg_size),
    #     average_compressed_svg_size=average_compressed_svg_size,
    #     average_compressed_svg_size_url=makeUrl(average_compressed_svg_size)
    # )

    # with open(makePath(rp, "README.md"), 'w', encoding='utf-8') as file:
    #     file.write(readme_data.strip())

    # print("Created README.md for repository")


def renderAll() -> None:
    '''Renders all SVG files'''
    print("Rendering files...")
    rp = root_path
    re_find_not_colored = re.compile(r"^\d+\)[\w \-\d]+\((\d+)x(\d+)\)\.png$")
    re_find_colored = re.compile(r"^\d+\)[\w \-\d]+\((\d+)x(\d+)\)\.colored\.png$")

    for image in os.listdir(makePath(rp, "SVG")):
        if not os.path.exists(makePath(rp, "SVG", image, "src/conf.json")):
            continue

        with open(makePath(rp, "SVG", image, "src/conf.json"), 'r', encoding="utf-8") as conf_file:
            conf_data = jsonLoad(conf_file, encoding="utf-8")
            if "render_sizes" not in conf_data:
                continue
            sizes = conf_data["render_sizes"]

        render_path = makePath(rp, "SVG", image, "render")

        # Create render directory if it does not exist
        if not os.path.exists(render_path):
            os.mkdir(render_path)

        # Delete all files if "update_old_files" set to True
        if update_old_files:
            for file in os.listdir(render_path):
                os.remove(makePath(render_path, file))

        for svg_filename in os.listdir(makePath(rp, "SVG", image)):
            if os.path.splitext(svg_filename)[1] != ".svg":  # Finding SVG files
                continue

            svg_basename = os.path.splitext(svg_filename)[0]
            svg_path = makePath(rp, "SVG", image, svg_filename)
            output_path = makePath(render_path, svg_basename + ".png")

            # List of sizes, that are already rendered
            rendered = []
            if not update_old_files:
                for filename in os.listdir(render_path):
                    if svg_basename.endswith(".colored"):
                        matches = re_find_colored.match(filename)
                    else:
                        matches = re_find_not_colored.match(filename)

                    if matches:
                        rendered.append([None, int(matches.group(2))])
                        rendered.append([int(matches.group(1)), None])

            if svg_basename.endswith(".colored"):
                output_name = "{i}) {name} ({rw}x{rh}).colored.png"
                svg_basename = svg_basename[:-8]
            else:
                output_name = "{i}) {name} ({rw}x{rh}).png"

            # SVG sizes
            with open(svg_path, 'r', encoding='utf-8') as svg_data_file:
                svg_data = svg_data_file.read()
            image_sizes = list(map(int, BeautifulSoup(svg_data, "lxml").find("svg").get('viewbox').split()))
            width = image_sizes[2] - image_sizes[0]
            height = image_sizes[3] - image_sizes[1]

            total_count = len(str(len(sizes)))
            count = 0
            for x, y in sizes.values():
                count += 1
                if not (isinstance(x, str) ^ isinstance(y, str) and (x is None) ^ (y is None)):
                    print("Warning! Can not handle due to invalid parameters: \"" + svg_path + "\"")
                    continue

                if x is None:
                    y = literal_eval(y.format(w=width, h=height))
                else:
                    x = literal_eval(x.format(w=width, h=height))

                if [x, y] in rendered:
                    continue

                if x is None:
                    # Render using height
                    svg_render.renderSvg(svg_path, output_path, height=y)
                else:
                    # Render using width
                    svg_render.renderSvg(svg_path, output_path, width=x)

                # Result image sizes
                result_width, result_height = Image.open(output_path).size

                # Save with correct name
                os.rename(output_path, makePath(render_path, output_name.format(
                    i=str(count).zfill(total_count), name=svg_basename, rw=result_width, rh=result_height
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

# Time for sleep between requests
request_sleep_time = 0.5

# ---SETTINGS--- #


if __name__ == "__main__":
    main()
