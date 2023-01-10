from src.logger import SingletonLogger
from src.findtemplateimages import find_template_images
from src.templatematching import template_matching
import argparse

if __name__ == "__main__":
    # TODO: check files and directories
    parser = argparse.ArgumentParser(description='Find paths in cross stitching patterns')
    parser.add_argument("-V", "--verbose", help="Output verbose logs",
                        action="store_true")
    parser.add_argument("-D", "--debug", help="Output debug logs",
                        action="store_true")
    # TODO: add / to end of dir name
    parser.add_argument("-d", "--directory", help="Directory location of pattern", default="examples/et/",
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
    templates_directory = str(args.directory) + "templates/"
    if args.templates is not None:
        templates_directory = args.templates
    else:
        find_template_images(args.directory, args.file)
    # TODO: pass outputs argument
    template_matching(args.directory, templates_directory, args.file)
