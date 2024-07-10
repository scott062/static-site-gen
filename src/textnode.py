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
        
        
