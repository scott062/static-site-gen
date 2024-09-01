from textnode import TextNode
import os
import shutil

def main():
    cleanup()
    generate()

def cleanup():
    if os.path.exists("./public"):
            shutil.rmtree("./public")
    os.mkdir("./public")

def generate(src="./static", dst="./public"):
    contents = os.listdir(src)

    if not contents:
        return

    if not os.path.exists(dst):
        os.mkdir(dst)

    for item in contents:
        item_src = os.path.join(src, item)
        item_dst = os.path.join(dst, item)
        if os.path.isfile(item_src):
            shutil.copy(item_src, item_dst)
        else:
            generate(item_src, item_dst)






main()
