import os
import shutil
from block_services import markdown_to_html_node 
from pathlib import Path
from services import extract_title 

def main():
    cleanup()
    generate()
    generate_pages_recursive()


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


def generate_pages_recursive(dir_path_content="./content", template_path="./template.html", dest_dir_path="./public"):
    contents = os.listdir(dir_path_content)

    if not contents:
        return

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for item in contents:
        item_src = os.path.join(dir_path_content, item)
        item_dst = os.path.join(dest_dir_path, item)
        print(item_dst)
        if os.path.isfile(item_src):
            f = open(item_src)
            from_content = f.read()
            f.close()
    
            t = open(template_path)
            template_content = t.read()
            t.close()

            content = markdown_to_html_node(from_content).to_html()
            title = extract_title(from_content)
            new = template_content.replace("{{ Title }}", title)
            new = new.replace("{{ Content }}", content)
            
            new_file = Path(os.path.join(dest_dir_path, item)).with_suffix(".html")

            n = open(new_file, "w")
            n.write(new)
            n.close()
        else:
            generate_pages_recursive(item_src, template_path, item_dst)



main()
