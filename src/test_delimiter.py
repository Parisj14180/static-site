import unittest
from textnode import TextNode
from textnode import TextType
from node_delimiter import split_nodes_delimiter
from node_delimiter import extract_markdown_images
from node_delimiter import extract_markdown_links

class TestDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "Visit [Google](https://google.com) today!"
        )
        self.assertListEqual([("Google", "https://google.com")], matches)
        

if __name__ == "__main__":
    unittest.main()