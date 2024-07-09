from enum import Enum
from leafnode import LeafNode


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_text_node):
        return (
            self.text == other_text_node.text
            and
            self.text_type == other_text_node.text_type
            and
            self.url == other_text_node.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})" 



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
    if text_type not in allowed_types:
        return old_nodes
    if delimiter is None or delimiter not in allowed_types.values():
        raise ValueError(f"{delimiter} is not a valid md delimiter")
    return_nodes = []
    for node in old_nodes:
        return_nodes.append(LeafNode())
        
        
