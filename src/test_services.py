import unittest

from textnode import TextNode
from services import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestServices(unittest.TestCase):
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

    def test_extract_markdown_images(self):
        text = "This is text with a![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        res = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), res)

    def test_extract_beginning_markdown_images(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        res = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), res)

    def test_extract_no_markdown_images(self):
        text = "This is text with a [no image](https://i.imgur.com/fJRm4Vk.jpeg)"
        res = []
        self.assertEqual(extract_markdown_images(text), res)

    def test_extract_almost_match_markdown_images(self):
        text = "This is text with a ![rick roll] (https://i.imgur.com/aKaOqIh.gif) and ![obi wan]try to break it(https://i.imgur.com/fJRm4Vk.jpeg)"
        res = []
        self.assertEqual(extract_markdown_images(text), res)

    def test_extract_empty_string_markdown_images(self):
        text = ""
        res = []
        self.assertEqual(extract_markdown_images(text), res)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and[to youtube](https://www.youtube.com/@bootdotdev)"
        res = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), res)

    def test_extract_beginning_markdown_links(self):
        text = "[to boot dev](https://www.boot.dev) and[to youtube](https://www.youtube.com/@bootdotdev)"
        res = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), res)

    def test_extract_no_markdown_links(self):
        text = "This is text with no links"
        res = []
        self.assertEqual(extract_markdown_links(text), res)

    def test_extract_almost_match_markdown_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        res = []
        self.assertEqual(extract_markdown_links(text), res)

    def test_extract_empty_string_markdown_links(self):
        text = ""
        res = []
        self.assertEqual(extract_markdown_links(text), res)

if __name__ == "__main__":
    unittest.main()
