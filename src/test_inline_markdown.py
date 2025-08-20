import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_images, split_nodes_links, text_to_text_nodes 

class TestNodeSpliter(unittest.TestCase):
    def test_split_text_with_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(3, len(new_nodes))

    def test_split_text_with_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(3, len(new_nodes))

    def test_split_text_with_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(3, len(new_nodes))

    def test_split_text_with_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )

        new_nodes = split_nodes_images([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes
        )

    def test_split_text_with_links(self):
        node = TextNode(
        "This is text with an [link](https://youtube.com) and another [link2](https://site2.com)",
        TextType.TEXT,
        )

        new_nodes = split_nodes_links([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://youtube.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "link2", TextType.LINK, "https://site2.com"
            ),
        ],
        new_nodes
        )

    def test_split_text_with_no_links(self):
        node = TextNode(
        "This is a text without any links",
        TextType.TEXT,
        )

        new_nodes = split_nodes_links([node])
        self.assertListEqual(
        [
            TextNode("This is a text without any links", TextType.TEXT),
        ],
        new_nodes
        )

    def test_split_text_with_no_images(self):
        node = TextNode(
        "This is a text without any images",
        TextType.TEXT,
        )

        new_nodes = split_nodes_images([node])
        self.assertListEqual(
        [
            TextNode("This is a text without any images", TextType.TEXT),
        ],
        new_nodes
        )
    
    def test_split_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_text_nodes(text)

        self.assertEqual(
            [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
        nodes
        )
    
    

    # extract from markdown

    def test_extract_markdown_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_multi_images(self):
        matches = extract_markdown_images(
            "This is text with two ![image1](https://i.imgur.com/image1.png) ![image2](https://i.imgur.com/image2.png)"
        )
        self.assertListEqual([("image1", "https://i.imgur.com/image1.png"), ("image2","https://i.imgur.com/image2.png" )], matches)

    def test_extract_markdown_no_images(self):
        matches = extract_markdown_images(
            "This is text with no images"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to youtube","https://www.youtube.com/@bootdotdev" )], matches)

    def test_extract_markdown_no_link(self):
        matches = extract_markdown_links(
            "This is a text without links"
        )
        self.assertListEqual([], matches)
