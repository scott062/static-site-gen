import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_empty_value(self):
        node = LeafNode("a", None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_repr(self):
        node = LeafNode("a", "b", {"c": "d"})
        self.assertEqual(repr(node), "LeafNode(a, b, {'c': 'd'})")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "b", {"c": "d"})
        self.assertEqual(node.to_html(), "b")

    def test_to_html(self):
        node = LeafNode("a", "b", {"c": "d"})
        self.assertEqual(node.to_html(), '<a c="d">b</a>')





if __name__ == "__main__":
    unittest.main()
