
from findTemplateImages import  find_template_images
from template_matching import templateMatching
if __name__ == "__main__":
    directory = "flower"
    find_template_images(directory, True)
    templateMatching(directory, True)

