from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self=None, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result
    
    def __repr__(self):
        return f"HTMLNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
           raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
           return self.value
        else:
            props_str = self.props_to_html()
            return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'
        

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("no tag found")
        if self.children is None or self.children == []:
            raise ValueError("children missing")
        
        result = ""
        for child in self.children:
            result += child.to_html()
        return f"<{self.tag}>{result}</{self.tag}>"
    
def text_node_to_html_node(text_node):
    if text_node.text_type != TextType.TEXT and text_node.text_type != TextType.BOLD and text_node.text_type != TextType.ITALIC and text_node.text_type != TextType.CODE and text_node.text_type != TextType.LINK and text_node.text_type != TextType.IMAGE:
        raise Exception("invalid")
    elif text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a[href]", text_node.text)
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img","", "src", "alt", text_node.text)
    
