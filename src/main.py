from textnode import TextNode, TextType

def main():
    node = TextNode("some anchor text", TextType.LINK)
    print(node)

main()