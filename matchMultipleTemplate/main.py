from src.logger import SingletonLogger
from src.findTemplateImages import find_template_images
from src.template_matching import templateMatching

if __name__ == "__main__":
    directory = "et"
    logger = SingletonLogger(True, True)
    find_template_images(directory, True)
    templateMatching(directory, True)

