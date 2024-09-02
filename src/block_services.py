from parentnode import ParentNode
from leafnode import LeafNode
from services import text_to_textnodes, text_node_to_html_node


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
                children.append(ParentNode("p", convert_nested_text(block)))
            case "heading":
                h_count = block[:7].count("#")
                children.append(
                    ParentNode(f"h{h_count}", convert_nested_text(block.strip("# ")))
                )
            case "code":
                c_content = block.strip("```")
                children.append(ParentNode("pre", [LeafNode("code", c_content)]))
            case "quote":
                q_content = block.replace(">", "").strip()
                children.append(
                    ParentNode("blockquote", convert_nested_text(q_content))
                )
            case "unordered_list":
                c_li = [
                    ParentNode("li", convert_nested_text(x.strip("* ").rstrip()))
                    for x in block.split("* ") if x
                ]
                children.append(ParentNode("ul", c_li))
            case "ordered_list":
                c_li = [
                    ParentNode("li", convert_nested_text(x.strip("1234567890. ")))
                    for x in block.split("\n")
                ]
                children.append(ParentNode("ol", c_li))
    return ParentNode("div", children, None)


def convert_nested_text(text):
    textnodes = text_to_textnodes(text)
    converted_html = []
    for node in textnodes:
        converted_html.append(text_node_to_html_node(node))
    return converted_html
