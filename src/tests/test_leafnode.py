import unittest

from html_leafnode import LeafNode


class TestLeafeNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_p_with_class(self):
        node = LeafNode("p", "Read me!", {"class": "some_text_class"})
        self.assertEqual(node.to_html(), '<p class="some_text_class">Read me!</p>')


if __name__ == "__main__":
    unittest.main()
