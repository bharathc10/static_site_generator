import os
import sys
import shutil
from copystatic import *
from gencontent import *

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    dir_path_content = "./content"
    template_path = "./template.html"
    dest_dir_path = "./docs"
    static_path = "./static"

    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)

    os.mkdir(dest_dir_path)
    copystatic(static_path, dest_dir_path)
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath)

if __name__ == "__main__":
    main()