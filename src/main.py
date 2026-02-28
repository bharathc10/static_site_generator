from textnode import TextNode, TextType
from copystatic import *

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")

    os.mkdir("public")
    copystatic("static", "public")

if __name__ == "__main__":
    main()