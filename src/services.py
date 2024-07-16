import re
from textnode import TextNode
from leafnode import LeafNode


def text_node_to_html_node(text_node):
    content = text_node.value
    match (text_node.text_type):
        case ("text"):
            return LeafNode(None, content)
        case ("bold"):
            return LeafNode("b", content)
        case ("italic"):
            return LeafNode("i", content)
        case ("code"):
            return LeafNode("code", content)
        case ("link"):
            return LeafNode("a", content, {"href": text_node.url})
        case ("image"):
            return LeafNode("img", "", {"src": text_node.url, "alt": content})
        case _:
            raise Exception("Not a valid text type")


allowed_types = {"text": None, "bold": "**", "italic": "*", "code": "`", "link": None, "image": None}


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # Redundant checks for different cases
    # TO-DO: Determine if extra checks are helpful interface
    if text_type not in allowed_types:
        raise ValueError(f"{text_type} is not a supported type")
    if not delimiter or delimiter not in allowed_types.values():
        raise ValueError(f"{delimiter} is not a valid Markdown delimiter")
    if delimiter != allowed_types.get(text_type):
        raise ValueError(f"Markdown delimiter {delimiter} does not match type {text_type}")

    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            len_content = len(split_text)
            if len_content % 2 == 0:
                raise Exception("Invalid Markdown syntax") 
            for x in range(len_content): 
                # When Markdown delimiter is at the beginning of a line, it will
                # split into ['', ..., ...]. This skips any empty '' so we do
                # not create unnecessary nodes
                if not split_text[x]:
                    continue
                if x % 2 == 0:
                    new_nodes.append(TextNode(split_text[x], "text"))
                else:
                    new_nodes.append(TextNode(split_text[x], text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
        else:
            # To be modified on each loop to track remaining text 
            node_text = node.text
            for image in images:
                split_text = node_text.split(f"![{image[0]}]({image[1]})", 1)
                if len(split_text[0]):
                    new_nodes.append(TextNode(split_text[0], "text"))
                new_nodes.append(TextNode(image[0], "image", image[1]))
                node_text = split_text[1] 
            # Remaing text, if any, after removing all images
            if len(node_text):
                new_nodes.append(TextNode(node_text, "text"))
    return new_nodes
    

def split_nodes_link(old_nodes):       
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        # node_text to be modified on each loop to track remaining text 
        node_text = node.text
        for link in links:
            split_text = node_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(split_text[0]):
                new_nodes.append(TextNode(split_text[0], "text"))
            new_nodes.append(TextNode(link[0], "link", link[1]))
            node_text = split_text[1] 
        # Remaing text, if any, after removing all links
        if len(node_text):
            new_nodes.append(TextNode(node_text, "text"))
    return new_nodes


def extract_markdown_images(text):
    # regex pattern: "![ group1 ]( group2 )"
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text) 


def extract_markdown_links(text):
    # regex pattern: "[ group1 ]( group2 )"
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text) 


def text_to_textnodes(text):
    boldified = split_nodes_delimiter([TextNode(text, "text")], "**", "bold")
    italicized = split_nodes_delimiter(boldified, "*", "italic")
    codified = split_nodes_delimiter(italicized, "`", "code")
    linkified = split_nodes_link(codified)
    imagified = split_nodes_image(linkified)
    return imagified


