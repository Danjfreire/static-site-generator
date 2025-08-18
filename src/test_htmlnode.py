import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    #  Regular HTML Nodes
    def test_html_node_none(self):
        node = HTMLNode()
        self.assertEqual(node.props, None)
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)

    def test_html_node_with_tag(self):
        node = HTMLNode("p")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.props, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)

    def test_html_node_with_value(self):
        node = HTMLNode(None, "some text")
        self.assertEqual(node.tag, None)
        self.assertEqual(node.props, None)
        self.assertEqual(node.value, "some text")
        self.assertEqual(node.children, None)
    
    def test_node_with_single_prop(self):
        node = HTMLNode("a", "some link", None, {"href" : "https://somelink.com"})
        expected = ' href="https://somelink.com"'
        self.assertEqual(node.props_to_html(), expected)

    def test_node_with_multiple_props(self):
        node = HTMLNode("a", "some link", None, {"href" : "https://somelink.com", "aria": "something", "other": "other"})
        expected = ' href="https://somelink.com" aria="something" other="other"'
        self.assertEqual(node.props_to_html(), expected)

    #  Leaf Nodes

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    
    # Parent Nodes

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_parent_to_html_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", None)
            node.to_html()

    def test_parent_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, LeafNode("p", "some text"))
            node.to_html()



if __name__ == "__main__":
    unittest.main()
