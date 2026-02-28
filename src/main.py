import os
import shutil
from copystatic import *
from gencontent import *

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")

    os.mkdir("public")
    copystatic("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()