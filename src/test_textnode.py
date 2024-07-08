import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
     
    def test_eq_all_fields(self):
        node = TextNode("This is a text node", "bold", "www.fakeurl.com")
        node2 = TextNode("This is a text node", "bold", "www.fakeurl.com")
        self.assertEqual(node, node2)

    def test_eq_none_fields(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node, node2)

    def test_neq_all_fields(self):
        node = TextNode("This is a text node", "bold", "www.fakeurl.com")
        node2 = TextNode("This is a different text node", "italic", "www.morefakeurl.com")
        self.assertNotEqual(node, node2)

    def test_neq_none_fields(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", "www.fakeurl.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("One", "Two", "Three")
        node_repr = "TextNode(One, Two, Three)"
        self.assertEqual(repr(node), node_repr)

    def test_none_repr(self):
        node = TextNode("One", "Two")
        node_repr = "TextNode(One, Two, None)"
        self.assertEqual(repr(node), node_repr)


if __name__ == "__main__":
    unittest.main()
