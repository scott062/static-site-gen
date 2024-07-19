from parentnode import ParentNode
from textnode import TextNode
from leafnode import LeafNode
from htmlnode import HTMLNode


def markdown_to_blocks(markdown):
    return [x.strip() for x in markdown.split("\n\n") if x]


def block_to_block_type(block):
    lines = block.split("\n")
    if lines[0] == "```" and lines[-1] == "```":
        return "code"
    if lines[0][:7].startswith("#") and "# " in lines[0][:7]:
        return "heading"

    is_quote = True
    is_unordered_list = True
    is_ordered_list = True

    for line in lines:
        if not line.startswith(">"): 
            is_quote = False
        if not (line[:2].startswith("* ") or line.startswith("- ")): 
            is_unordered_list = False
        if not (line[0].isnumeric() and ". " in line):
            is_ordered_list = False
    if is_quote:
        return "quote"
    elif is_unordered_list:
        return "unordered_list"
    elif is_ordered_list:
        return "ordered_list"
    return "paragraph"
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)     
    children = []
    for block in blocks:
        t = block_to_block_type(block)
    match t:
        case "paragraph":
            children.append(HTMLNode("p", block))
        case "heading":
            h_count = block[:7].count("#")
            children.append(HTMLNode(f"h{h_count}", block.strip("#")))
        case "code":
            c_content = block.strip("```")
            children.append(ParentNode("pre",[LeafNode("code", c_content)]))
        case "quote":
            q_content = block.replace(">", "").strip()
            children.append(HTMLNode("blockquote", q_content))
        case "unordered_list":
            c_li = [LeafNode("li", x.strip()) for x in block.split("*")]
            children.append(ParentNode("ul", c_li))
        case "ordered_list":
            # To Do: Determine best wild card matching?
            c_li = [LeafNode("li", x.strip()) for x in block.split("*")]
            children.append(ParentNode("ol", c_li))
            children.append()
    return ParentNode("div", children)

