import unittest

from textnode import TextNode, split_nodes_delimiter


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

    def test_split_nodes_single_node(self):
        node = TextNode("This is a nested bold **text node**.", "text")
        # Expected Nodes to be created below
        node1 = TextNode("This is a nested bold ", "text", None)
        node2 = TextNode("text node", "bold", None)
        node3 = TextNode(".", "text", None)
        self.assertEqual(split_nodes_delimiter([node], "**", "bold"), [node1, node2, node3])

    def test_split_nodes_multi_node(self):
        node = TextNode("**This is a nested bold** text node.", "text")
        another_node = TextNode("Time for more bold **text node**!", "text")
        # Expected Nodes to be created below
        node1 = TextNode("This is a nested bold", "bold", None)
        node2 = TextNode(" text node.", "text", None)
        node3 = TextNode("Time for more bold ", "text", None)
        node4 = TextNode("text node", "bold", None)
        node5 = TextNode("!", "text", None)
        self.assertEqual(
            split_nodes_delimiter([node, another_node], "**", "bold")
            , [node1, node2, node3, node4, node5]
        )

    def test_split_nodes_non_text(self):
        node = TextNode("**This is a not text we would split.**", "bold")
        another_node = TextNode("*Skip this*", "italic")
        self.assertEqual(
            split_nodes_delimiter([node, another_node], "**", "bold")
            , [node, another_node]
        )

    def test_split_nodes_bad_delimiter(self):
        node = TextNode("This is a nested bold **text node**.", "text")
        self.assertRaises(ValueError, lambda: split_nodes_delimiter([node], "***", "bold"))

    def test_split_nodes_mismatch_type_delimiter(self):
        node = TextNode("This is a nested bold **text node**.", "text")
        self.assertRaises(ValueError, lambda: split_nodes_delimiter([node], "**", "italic"))


if __name__ == "__main__":
    unittest.main()
