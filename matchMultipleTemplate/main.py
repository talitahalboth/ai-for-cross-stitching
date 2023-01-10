from src.logger import SingletonLogger
from src.findtemplateimages import find_template_images
from src.templatematching import template_matching
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find paths in cross stitching patterns')
    parser.add_argument("-V", "--verbose", help="output verbose logs",
                        action="store_true")
    parser.add_argument("-D", "--debug", help="output debug logs",
                        action="store_true")
    parser.add_argument("-d", "--directory", help="directory location of pattern", default="et/",
                        action="store")
    parser.add_argument("-f", "--file", help="file name of pattern (default: img.png). "
                                             "The file must preferably have dimensions over 1500px", default="img.png",
                        action="store")

    args = parser.parse_args()
    logger = SingletonLogger(args.verbose, args.debug)
    find_template_images(args.directory, args.file)
    template_matching(args.directory, args.file)
