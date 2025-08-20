import unittest
from markdown_blocks import markdown_to_blocks, bock_to_block_type, BlockType

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
    
    def test_block_to_block_type(self):
        heading = "### This is a heading"
        self.assertEqual(bock_to_block_type(heading), BlockType.HEADING)

        code = "``` This is code ```"
        self.assertEqual(bock_to_block_type(code), BlockType.CODE)

        quote = "> This is a quote"
        self.assertEqual(bock_to_block_type(quote), BlockType.QUOTE)

        unordered_list = "- this is unordered list"
        self.assertEqual(bock_to_block_type(unordered_list), BlockType.UNORDERED_LIST)

        ordered_list = "1. this is ordered list"
        self.assertEqual(bock_to_block_type(ordered_list), BlockType.ORDERED_LIST)

        paragraph = "This is a paragraph"
        self.assertEqual(bock_to_block_type(paragraph), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()