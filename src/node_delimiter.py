from textnode import TextNode
from textnode import TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Invalid markdown: unmatched delimiter")
            for idx, part in enumerate(parts):
                if idx % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes
    
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        remaining_text_to_process = node.text
        image = extract_markdown_images(node.text)
        for alt_text, url in image:
            image_markdown_string = f"![{alt_text}]({url})"
            parts = remaining_text_to_process.split(image_markdown_string, 1)
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            remaining_text_to_process = parts[1]
        if remaining_text_to_process != "":
             new_nodes.append(TextNode(remaining_text_to_process, TextType.TEXT))    
    return new_nodes
        
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        remaining_text_to_process = node.text
        link = extract_markdown_links(node.text)
        for alt_text, url in link:
            link_markdown_string = f"[{alt_text}]({url})"
            parts = remaining_text_to_process.split(link_markdown_string, 1)
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            remaining_text_to_process = parts[1]
        if remaining_text_to_process != "":
             new_nodes.append(TextNode(remaining_text_to_process, TextType.TEXT)) 
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes