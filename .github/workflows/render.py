from typing import Optional

import os
from shutil import copyfile
from subprocess import Popen, PIPE

TMP_FOLDER = "rendertmp"


def renderSvg(path_in: str, path_out: str, width: Optional[int] = None, height: Optional[int] = None, colored: bool = False) -> tuple:
    '''Converts SVG file (path_int) to PNG file (path_out) with a specified width OR height.
       Returns command line response'''

    if os.path.splitext(path_in)[1] != ".svg":
        raise ValueError("Input file must have the \".svg\" extension.")

    if os.path.splitext(path_out)[1] != ".png":
        raise ValueError("Output file must have the \".png\" extension.")

    if not (width is None) ^ (height is None):
        raise ValueError("One of the parameters \"width\" or \"height\" must be an integer > 0, the other has to be None.")

    filename = os.path.splitext(os.path.split(path_in)[1])[0]
    fin = os.path.join(TMP_FOLDER, filename + ".svg")
    fout = os.path.join(TMP_FOLDER, filename + ".png")

    # Copy file to tmp folder
    copyfile(path_in, fin)

    command = "convert-svg-to-png {size} \"{fin}\"".format(
        fin=fin,
        size="--width " + str(width) if width is not None else "--height " + str(height)
    )
    s = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()

    # Remove tmp file
    os.remove(fin)

    # Move result to path_out
    if os.path.exists(path_out):
        os.remove(path_out)
    os.rename(fout, path_out)

    return s


# print(renderSvg("../../SVG/Codeforces/Codeforces.svg", "output.png", width=300, colored=True))  # Test
