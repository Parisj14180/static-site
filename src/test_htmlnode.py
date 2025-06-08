import unittest
from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        actual_output = node.props_to_html()
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(actual_output, expected_output)

    def test_empty_props_to_html(self):
        node = HTMLNode(props={})
        actual_output = node.props_to_html()
        expected_output = ""
        self.assertEqual(actual_output, expected_output)

    def test_single_property_props_to_html(self):
        node = HTMLNode(props={"id": "my-element"})
        actual_output = node.props_to_html()
        expected_output = ' id="my-element"'
        self.assertEqual(actual_output, expected_output)

if __name__ == "__main__":
    unittest.main()