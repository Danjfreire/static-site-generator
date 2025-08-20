import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType ):
    final_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_nodes.append(node)
            continue

        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        final_nodes.extend(split_nodes)

    return final_nodes
            
def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    
    return matches 

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    
    return matches 

def split_nodes_images(old_nodes: list[TextNode]):
    final_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_nodes.append(node)
            continue
    
        text = node.text
        image_matches = extract_markdown_images(text)
        rest_of_text = text

        for i in range(len(image_matches)):
            image_alt, image_link = image_matches[i]
            splits = rest_of_text.split(f"![{image_alt}]({image_link})")

            if len(splits) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if splits[0] != "":
                final_nodes.append(TextNode(splits[0], TextType.TEXT))
            final_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            rest_of_text = splits[1]
        
        if len(rest_of_text) != 0:
            final_nodes.append(TextNode(rest_of_text, TextType.TEXT))
        
    return final_nodes


def split_nodes_links(old_nodes):
    final_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_nodes.append(node)
            continue
    
        text = node.text
        link_matches = extract_markdown_links(text)
        rest_of_text = text

        for i in range(len(link_matches)):
            link_alt, link = link_matches[i]
            splits = rest_of_text.split(f"[{link_alt}]({link})")

            if len(splits) != 2:
                raise ValueError("invalid markdown, link section not closed")

            if splits[0] != "":
                final_nodes.append(TextNode(splits[0], TextType.TEXT))
            final_nodes.append(TextNode(link_alt, TextType.LINK, link))

            rest_of_text = splits[1]
        
        if len(rest_of_text) != 0:
            final_nodes.append(TextNode(rest_of_text, TextType.TEXT))
        
    return final_nodes

def text_to_text_nodes(text):
    final_nodes = []
    node = TextNode(text, TextType.TEXT)

    final_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    final_nodes = split_nodes_delimiter(final_nodes, "_", TextType.ITALIC)
    final_nodes = split_nodes_delimiter(final_nodes, "`", TextType.CODE)
    final_nodes = split_nodes_images(final_nodes)
    final_nodes = split_nodes_links(final_nodes)

    return final_nodes
