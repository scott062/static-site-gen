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


Texttype = Enum("Texttype", ["text", "bold", "italic", "code", "link", "image"])

def text_node_to_html_node(text_node):
    content = text_node.value
    match (text_node.text_type):
        case (Texttype.text):
            return LeafNode(None, content)
        case (Texttype.bold):
            return LeafNode("b", content)
        case (Texttype.italic):
            return LeafNode("i", content)
        case (Texttype.code):
            return LeafNode("code", content)
        case (Texttype.link):
            return LeafNode("a", content, {"href": text_node.url})
        case (Texttype.image):
            return LeafNode("img", "", {"src": text_node.url, "alt": content})
        case _:
            raise Exception("Not a valid text type")

