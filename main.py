from pathlib import Path

from src.logger import SingletonLogger
from src.findtemplateimages import find_template_images
from src.templatematching import template_matching
import argparse
import os

if __name__ == "__main__":
    # TODO: check files and directories
    parser = argparse.ArgumentParser(description='Find paths in cross stitching patterns')
    parser.add_argument("-V", "--verbose", help="Output verbose logs",
                        action="store_true")
    parser.add_argument("-D", "--debug", help="Output debug logs",
                        action="store_true")
    # TODO: add / to end of dir name
    parser.add_argument("-d", "--directory", help="Directory location of pattern", default="examples/heart/",
                        action="store")
    parser.add_argument("-f", "--file", help="File name of pattern (default: img.png). "
                                             "The file must preferably have dimensions over 1500px", default="img.png",
                        action="store")
    parser.add_argument("-t", "--templates", help="Directory containing templates. Must only be defined if templates "
                                                  "are already created",
                        action="store")
    parser.add_argument("-o", "--output", help="Output directory, where paths will be stored",
                        action="store")

    args = parser.parse_args()
    logger = SingletonLogger(args.verbose, args.debug)
    directory = Path(args.directory)
    templates_directory = directory / "templates"

    if not os.path.isdir(args.directory):
        logger.log("Directory does not exist", "ERROR")
        exit(-1)

    if not os.path.isfile(directory / args.file):
        logger.log("File does not exist", "ERROR")
        exit(-1)
    # todo: set output directory
    output_directory = Path(directory / "paths")
    if args.output is None and not os.path.isdir(directory / "paths"):
        os.makedirs(directory / "paths")
    if args.output is not None:
        output_directory = Path(args.output)
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)
    # template_matching(args.directory, templates_directory, args.file)
    if args.templates is not None:
        templates_directory = args.templates
        template_matching(directory, templates_directory, args.file, output_directory)
    else:
        find_template_images(directory, args.file, output_directory)
    # TODO: pass outputs argument
