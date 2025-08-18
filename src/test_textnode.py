import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_dif(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a italic node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.someurl.com")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.someurl.com)", repr(node)
        )

    def test_repr_url(self):
        node = TextNode("This is a link node", TextType.LINK, "https://someurl.com")
        self.assertEqual("TextNode(This is a link node, link, https://someurl.com)", repr(node))


class TestTextNodeToHtmlNode(unittest.TestCase):
   def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node") 

   def test_bold(self):
    node = TextNode("This is a bold node", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "This is a bold node") 

   def test_italic(self):
    node = TextNode("This is an italic node", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "This is an italic node") 

   def test_code(self):
    node = TextNode("This is a code node", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "This is a code node") 

   def test_link(self):
    node = TextNode("This is a link node", TextType.LINK, "https://someurl.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "This is a link node") 
    self.assertEqual(html_node.props["href"], "https://someurl.com") 

   def test_image(self):
    node = TextNode("This is an image node", TextType.IMAGE, "https://someimage.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, "") 
    self.assertEqual(html_node.props["src"], "https://someimage.com") 
    self.assertEqual(html_node.props["alt"], "This is an image node") 


if __name__ == "__main__":
    unittest.main()