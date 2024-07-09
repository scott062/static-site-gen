import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_empty_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        node = HTMLNode(None, None, None, { "htmlProp": "first", "htmlPropAgain": "second" })
        self.assertEqual(node.props_to_html(), ' htmlProp="first" htmlPropAgain="second"')

    def test_repr(self):
        node = HTMLNode("p", "gigi", None, { "htmlProp": "first", "htmlPropAgain": "second" })
        self.assertEqual(repr(node), "HTMLNode(p, gigi, None, {'htmlProp': 'first', 'htmlPropAgain': 'second'})")



if __name__ == "__main__":
    unittest.main()
