import numpy as np
import os


def latexTemplate(equation):
    fname = "temp.tex"
    with open(fname, "w+") as o:
        o.write(
            "\\documentclass[convert={density=500}, border=2pt, varwidth=8in]{standalone}\n"
        )
        o.write("\\usepackage{amsmath}\n")
        o.write("\\usepackage{amssymb}\n")
        o.write("\\begin{document}\n")
        o.write("\\begin{align*}\n")
        # o.write("_{256}P_{8} = \\frac{256!}{(256 - 8)!} = 1.65 \\times 10^{19}\n")
        o.write(f"{equation}\n")
        o.write("\\end{align*}\n")
        o.write("\\end{document}\n")


def latex2png():
    fname = "temp"
    # Compile LaTeX to PDF
    os.system(f"pdflatex --shell-escape {fname}.tex > /dev/null")
    # Convert PDF to PNG and trim borders
    os.system(
        f"magick -density 800 -units PixelsPerInch {fname}.pdf -quality 90 -trim +repage {fname}.png > /dev/null"
    )
    # Clean up auxiliary files
    os.system(f"rm {fname}.pdf {fname}.aux {fname}.log {fname}.tex > /dev/null")


def genPNGfromEquation(eq: str):
    # create temporary tex file
    latexTemplate(eq)
    # compile the temp tex file
    latex2png()
    # change the temp file name
    imgNum = 1
    while True:
        if os.path.exists(f"eq{imgNum}.png"):
            imgNum += 1
        else:
            if os.path.exists("temp.png"):
                os.rename("temp.png", f"eq{imgNum}.png")
                break
            else:
                print("Error: temp.png not found.")
                break


def main():
    genPNGfromEquation("x^2 + y^2 = z^2")
    genPNGfromEquation("x^3 + y^2 = z^2")


if __name__ == "__main__":
    main()
