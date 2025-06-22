from enum import Enum
from htmlnode import HTMLNode, ParentNode, text_node_to_html_node
from node_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

def markdown_to_blocks(markdown):
    blocks = []
    MD_list = markdown.split('\n\n')
    for i in MD_list:
        stripped_block = i.strip()
        if stripped_block != "":
            blocks.append(stripped_block)
    return blocks

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

def block_to_block_type(block):
    count = 0
    for i in block:
        if i == '#':
            count += 1
        else:
            break
    if 1 <= count <= 6 and len(block) > count and block[count] == " ":  
        return BlockType.heading
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.code
    
    elif block.startswith(">"):
        lines = block.split('\n')
        is_quote = True
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.quote
        
    elif block.startswith("- "):
        lines = block.split('\n')
        is_unordered_list = True
        for line in lines:
            if not line.startswith("- "):
                is_unordered_list = False
                break
        if is_unordered_list:
            return BlockType.unordered_list
        
    elif block.startswith("1. "):
        lines = block.split('\n')
        is_ordered_list = True
        for i in range(len(lines)):
            expected_start = f"{i + 1}. "
            if not lines[i].startswith(expected_start):
                is_ordered_list = False
                break
        if is_ordered_list:
            return BlockType.ordered_list
        
    else:
        return BlockType.paragraph
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    node_list = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.paragraph:
            normalized_text = ' '.join(block.split())
            children = text_to_children(normalized_text)
            node = ParentNode(tag="p", children=children, props=None)
            node_list.append(node)

        elif block_type == BlockType.heading:
            count = 0
            for i in block:
                if i == '#':
                    count += 1
                else:
                    break
            tag = "h" + str(count)
            heading_text = block[count + 1:]
            children = text_to_children(heading_text)
            node = ParentNode(tag=tag, children=children, props=None)
            node_list.append(node)

        elif block_type == BlockType.code:
            lines = block.split('\n')
            stripped_lines = [line.strip() for line in lines[1:-1]]
            code_content = '\n'.join(stripped_lines) + '\n'
            code_text_node = TextNode(code_content, TextType.TEXT)
            code_leaf_node = text_node_to_html_node(code_text_node)
            code_html_node = ParentNode(tag="code", children=[code_leaf_node], props=None)
            
            node = ParentNode(tag="pre", children=[code_html_node], props=None)
            node_list.append(node)

        elif block_type == BlockType.quote:
            lines = block.split('\n')
            cleaned_lines = []
            for line in lines:
                cleaned_line = line.lstrip("> ")
                cleaned_lines.append(cleaned_line)
            quote_text = '\n'.join(cleaned_lines)
            children = text_to_children(quote_text)
            node = ParentNode(tag="blockquote", children=children, props=None)
            node_list.append(node)

        elif block_type == BlockType.unordered_list:
            lines = block.split('\n')
            list_items = []
            for line in lines:
                cleaned_line = line.lstrip("- ")
                li_children = text_to_children(cleaned_line)
                li_node = ParentNode(tag="li", children=li_children, props=None)
                list_items.append(li_node)

            node = ParentNode(tag="ul", children=list_items, props=None)
            node_list.append(node)

        elif block_type == BlockType.ordered_list:
            lines = block.split('\n')
            list_items = []
            for line in lines:
                space_index = line.find(" ")
                cleaned_line = line[space_index + 1:]
                li_children = text_to_children(cleaned_line)
                li_node = ParentNode(tag="li", children=li_children, props=None)
                list_items.append(li_node)

            node = ParentNode(tag="ol", children=list_items, props=None)  # <ol> contains all <li>s
            node_list.append(node)


    parent_node = ParentNode(tag="div", children=node_list, props=None)
    return parent_node

def text_to_children(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes