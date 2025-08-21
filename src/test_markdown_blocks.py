import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node, extract_markdown_title

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
        self.assertEqual(block_to_block_type(heading), BlockType.HEADING)

        code = "``` This is code ```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

        quote = "> This is a quote"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

        unordered_list = "- this is unordered list"
        self.assertEqual(block_to_block_type(unordered_list), BlockType.UNORDERED_LIST)

        ordered_list = "1. this is ordered list"
        self.assertEqual(block_to_block_type(ordered_list), BlockType.ORDERED_LIST)

        paragraph = "This is a paragraph"
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)

    # markdown to html nodes tests

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
### This is a header 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a header 3</h3></div>",
        )

    def test_ul(self):
        md = """
- this is the first item
- this is the second item
- this is the third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this is the first item</li><li>this is the second item</li><li>this is the third item</li></ul></div>",
        )

    def test_ol(self):
        md = """
1. this is the first item
2. this is the second item
3. this is the third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>this is the first item</li><li>this is the second item</li><li>this is the third item</li></ol></div>",
        )

    def test_quote(self):
        md = """
> this is a quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is a quote</blockquote></div>",
        )
    
    def test_extract_markdown_title(self):
        markdown = """
# This is a header

this is some text
""" 
        header = extract_markdown_title(markdown)
        self.assertEqual(header, "This is a header")


if __name__ == "__main__":
    unittest.main()