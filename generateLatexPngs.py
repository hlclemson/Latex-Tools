import os
import logging
import subprocess
import numpy as np


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="genPNG.log",  # Log file name
    filemode="w",  # Overwrite the log file each time
)


def latexTemplate(equation):
    fname = "temp.tex"
    with open(fname, "w+") as o:
        o.write(
            "\\documentclass[convert={density=500}, border=2pt, varwidth=8in]{standalone}\n"
        )
        o.write("\\usepackage{amsmath}\n")
        o.write("\\usepackage{amssymb}\n")
        o.write("\\usepackage{bm}\n")
        o.write("\\begin{document}\n")
        o.write("\\begin{align*}\n")
        # o.write("_{256}P_{8} = \\frac{256!}{(256 - 8)!} = 1.65 \\times 10^{19}\n")
        o.write(f"{equation}\n")
        o.write("\\end{align*}\n")
        o.write("\\end{document}\n")


def latex2png():
    fname = "temp"
    try:
        # Compile LaTeX to PDF
        logging.info("Compiling LaTeX to PDF...")
        result = subprocess.run(
            ["pdflatex", "--shell-escape", f"{fname}.tex"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        logging.info(result.stdout)
        if result.stderr:
            logging.info(result.stderr)
        # Convert PDF to PNG and trim borders
        logging.info("Converting PDF to PNG and trimming borders...")
        result = subprocess.run(
            [
                "magick",
                "-density",
                "800",
                "-units",
                "PixelsPerInch",
                f"{fname}.pdf",
                "-quality",
                "90",
                "-trim",
                "+repage",
                f"{fname}.png",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        logging.info(result.stdout)
        if result.stderr:
            logging.info(result.stderr)

        # Clean up auxiliary files
        logging.info("Cleaning up auxiliary files...")
        subprocess.run(
            ["rm", f"{fname}.pdf", f"{fname}.aux", f"{fname}.log", f"{fname}.tex"],
            check=True,
        )
        logging.info("Process completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred: {e}")


def genPNGfromEquation(eq: str):
    # create temporary tex file
    latexTemplate(eq)
    # compile the temp tex file
    latex2png()
    # change the temp file name
    imgNum = 1
    # prevent overwritting existing equation image files
    outputDir = "png"
    while True:
        if os.path.exists(f"{outputDir}/eq{imgNum}.png"):
            imgNum += 1
        else:
            if os.path.exists("temp.png"):
                os.rename("temp.png", f"{outputDir}/eq{imgNum}.png")
                break
            else:
                exit("Error: filed to generate a temporary png file.")
                break


def main():
    equations = []
    with open("equations.txt", "r") as out:
        for line in out:
            line = line.strip()
            equations.append(line)
    # remove empty strings in the list
    equations = [x for x in equations if x]
    # generate png equation files
    for eq in equations:
        genPNGfromEquation(eq)


if __name__ == "__main__":
    main()
