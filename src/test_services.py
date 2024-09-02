import unittest

from textnode import TextNode
from services import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, extract_title


class TestServices(unittest.TestCase):
    def test_split_nodes_single_node(self):
        node = TextNode("This is a nested bold **text**.", "text")
        # Expected Nodes to be created below
        node1 = TextNode("This is a nested bold ", "text", None)
        node2 = TextNode("text", "bold", None)
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

    def test_split_images_single_node(self):
        node = TextNode("This is text with a![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "text")
        # Expected Nodes to be created below
        node1 = TextNode("This is text with a", "text", None)
        node2 = TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif")
        node3 = TextNode(" and ", "text", None)
        node4 = TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(split_nodes_image([node]), [node1, node2, node3, node4])

    def test_split_images_beginning(self):
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and ending sentence.", "text")
        # Expected Nodes to be created below
        node1 = TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif")
        node2 = TextNode(" and ", "text", None)
        node3 = TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg")
        node4 = TextNode(" and ending sentence.", "text", None)
        self.assertEqual(split_nodes_image([node]), [node1, node2, node3, node4])

    def test_split_no_images(self):
        node = TextNode("This is text with a [no image](https://i.imgur.com/fJRm4Vk.jpeg)", "text")
        res = TextNode("This is text with a [no image](https://i.imgur.com/fJRm4Vk.jpeg)", "text", None)
        self.assertEqual(split_nodes_image([node]), [res])

    def test_split_almost_match_images(self):
        node = TextNode("This is text with a ![rick roll] (https://i.imgur.com/aKaOqIh.gif) and ![obi wan]try to break it(https://i.imgur.com/fJRm4Vk.jpeg)", "text")
        res = TextNode("This is text with a ![rick roll] (https://i.imgur.com/aKaOqIh.gif) and ![obi wan]try to break it(https://i.imgur.com/fJRm4Vk.jpeg)", "text", None)
        self.assertEqual(split_nodes_image([node]), [res])

    def test_split_only_image(self):
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "text")
        # Expected Nodes to be created below
        node1 = TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif")
        node2 = TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(split_nodes_image([node]), [node1, node2])

    def test_split_links_single_node(self):
        node = TextNode("This is text with a[rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "text")
        # Expected Nodes to be created below
        node1 = TextNode("This is text with a", "text", None)
        node2 = TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif")
        node3 = TextNode(" and ", "text", None)
        node4 = TextNode("obi wan", "link", "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(split_nodes_link([node]), [node1, node2, node3, node4])

    def test_split_links_beginning(self):
        node = TextNode("[rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and ending sentence.", "text")
        # Expected Nodes to be created below
        node1 = TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif")
        node2 = TextNode(" and ", "text", None)
        node3 = TextNode("obi wan", "link", "https://i.imgur.com/fJRm4Vk.jpeg")
        node4 = TextNode(" and ending sentence.", "text", None)
        self.assertEqual(split_nodes_link([node]), [node1, node2, node3, node4])

    def test_split_no_links(self):
        node = TextNode("This is text with a ![no link](https://i.imgur.com/fJRm4Vk.jpeg)", "text")
        res = TextNode("This is text with a ![no link](https://i.imgur.com/fJRm4Vk.jpeg)", "text", None)
        self.assertEqual(split_nodes_link([node]), [res])

    def test_split_almost_match_links(self):
        node = TextNode("This is text with a [rick roll] (https://i.imgur.com/aKaOqIh.gif) and [obi wan]try to break it(https://i.imgur.com/fJRm4Vk.jpeg)", "text")
        res = TextNode("This is text with a [rick roll] (https://i.imgur.com/aKaOqIh.gif) and [obi wan]try to break it(https://i.imgur.com/fJRm4Vk.jpeg)", "text", None)
        self.assertEqual(split_nodes_link([node]), [res])

    def test_split_only_link(self):
        node = TextNode("[rick roll](https://i.imgur.com/aKaOqIh.gif)[obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "text")
        # Expected Nodes to be created below
        node1 = TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif")
        node2 = TextNode("obi wan", "link", "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(split_nodes_link([node]), [node1, node2])

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)!"
        node1 = TextNode("This is ", "text", None)
        node2 = TextNode("text", "bold", None)
        node3 = TextNode(" with an ", "text", None)
        node4 = TextNode("italic", "italic", None)
        node5 = TextNode(" word and a ", "text", None)
        node6 = TextNode("code block", "code", None)
        node7 = TextNode(" and an ", "text")
        node8 = TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg")
        node9 = TextNode(" and a ", "text", None)
        node10 = TextNode("link", "link", "https://boot.dev")
        node11 = TextNode("!", "text", None)
        self.assertEqual(
            text_to_textnodes(text), 
            [node1, node2, node3, node4, node5, node6, node7, node8, node9, node10, node11]
        )

    def test_extract_markdown_title(self):
        text = "# Nice    "
        res = "Nice" 
        self.assertEqual(extract_title(text), res)


if __name__ == "__main__":
    unittest.main()
