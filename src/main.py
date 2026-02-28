import os
import shutil
from copystatic import *
from gencontent import *

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")

    os.mkdir("public")
    copystatic("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()