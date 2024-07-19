import unittest

from block_services import markdown_to_blocks, block_to_block_type


class TestBlockServices(unittest.TestCase):
    def test_markdown_to_blocks(self):
        # Expected Nodes to be created below
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        return_text = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertEqual(markdown_to_blocks(text), return_text)

    def test_block_to_block_type_paragraph(self):
        text = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_block_to_block_type_heading(self):
        text = "# This is a heading"
        self.assertEqual(block_to_block_type(text), "heading")

    def test_block_to_block_type_code(self):
        text = "```\nThis is a code\n```"
        self.assertEqual(block_to_block_type(text), "code")

    def test_block_to_block_type_quote(self):
        text = ">This is a quote\n>This is another quote"
        self.assertEqual(block_to_block_type(text), "quote")

    def test_block_to_block_type_unordered_list(self):
        text = "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        self.assertEqual(block_to_block_type(text), "unordered_list")

    def test_block_to_block_type_ordered_list(self):
        text = "1. This is the first list item in a list block\n2. This is a list item\n3. This is another list item"
        self.assertEqual(block_to_block_type(text), "ordered_list")

if __name__ == "__main__":
    unittest.main()
