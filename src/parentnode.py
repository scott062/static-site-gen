from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Must pass tag to ParentNode")
        if self.children is None:
            raise ValueError("Must pass children to ParentNode")
        concat_html = ""
        for n in self.children:
            concat_html += n.to_html()
        return f"<{self.tag}{self.props_to_html()}>{concat_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

   
