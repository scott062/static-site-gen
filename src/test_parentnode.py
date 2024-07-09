import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_repr(self):
        node = ParentNode(
            "p",
            [LeafNode("b", "Bold text")]
        )
        self.assertEqual(repr(node), "ParentNode(p, [LeafNode(b, Bold text, None)], None)")

    def test_flat_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "BOLDLY"),
                LeafNode(None, "beam me up"),
                LeafNode("i", "italic scotty"),
                LeafNode(None, "!"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>BOLDLY</b>beam me up<i>italic scotty</i>!</p>")

    def test_missing_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_missing_tag(self):
        node = ParentNode(None, LeafNode("b", "BOLDLY"))
        self.assertRaises(ValueError, node.to_html)

    def test_nested_parent(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "Kirk is in charge"),
                LeafNode(None, "on the"),
                LeafNode("i", "outside"),
                LeafNode(None, "!"),
                ParentNode(
                    "div",
                    [
                        LeafNode("h1", "but scotty keeps things running on the inside"),
                        LeafNode("h2", "!"),
                    ],
                )
            ],
            {"onClick": "doTheThing"} 
        )
        check = '<div onClick="doTheThing"><p>Kirk is in charge</p>on the<i>outside</i>!<div><h1>but scotty keeps things running on the inside</h1><h2>!</h2></div></div>'
        self.assertEqual(node.to_html(), check)



if __name__ == "__main__":
    unittest.main()
