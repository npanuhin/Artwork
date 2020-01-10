from typing import List

from json import loads
import os
from bs4 import BeautifulSoup
from PIL import Image

import render
render.TMP_FOLDER = "rendertmp"


def make_path(*paths: List[str]) -> str:
    '''Combines paths and normalizes the result'''
    return os.path.normpath(os.path.join(*paths))


# def githubPages():
#     '''Updates Github Pages'''
#     print("Updating Github Pages...")


def renderAll() -> None:
    '''Renders all SVG files'''
    print("Rendering files...")
    rp = root_path

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

        if remove_old_files:
            for file in os.listdir(render_path):
                os.remove(make_path(render_path, file))

        for svg_filename in os.listdir(make_path(rp, "SVG", image)):
            if os.path.splitext(svg_filename)[1] != ".svg":
                continue

            svg_basename = os.path.splitext(svg_filename)[0]
            svg_path = make_path(rp, "SVG", image, svg_filename)
            output_path = make_path(render_path, svg_basename + ".png")

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
            index = 1
            for name, (x, y) in sizes.items():
                if not ((type(x) is str) ^ (type(y) is str) and (x is None) ^ (y is None)):
                    print("Warning! Can not handle due to invalid parameters: \"" + svg_path + "\"")
                    continue

                if type(x) is str:
                    # Render using width
                    render.renderSvg(svg_path, output_path, width=eval(x.format(w=width, h=height)))
                else:
                    # Render using height
                    render.renderSvg(svg_path, output_path, height=eval(y.format(w=width, h=height)))

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

                index += 1


def main() -> None:
    print("Starting build...")

    renderAll()

    print("Build complete.")


# ---SETTINGS--- #

# Delete old rendered files
remove_old_files = True

# Path to the root of repository
root_path = "..\\..\\"

# ---SETTINGS--- #


if __name__ == "__main__":
    main()
