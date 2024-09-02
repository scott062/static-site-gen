import os
import shutil
from block_services import markdown_to_html_node 
from services import extract_title 

def main():
    cleanup()
    generate()
    generate_page("content/index.md", "template.html", "public/index.html")

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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    from_content = f.read()
    f.close()
    t = open(template_path)
    template_content = t.read()
    t.close()

    content = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)
    new = template_content.replace("{{ Title }}", title)
    new = new.replace("{{ Content }}", content)

    n = open(dest_path, "w")
    n.write(new)
    n.close()

main()
