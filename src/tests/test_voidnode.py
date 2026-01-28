import unittest
from multiprocessing.sharedctypes import Value

from html_tags import HTMLTags
from html_void_node import VoidNode
from tests.utils import expected_error


class TestVoidNode(unittest.TestCase):

    def test_happy_init(self):
        node = VoidNode(HTMLTags.META.value, None)
        self.assertIsInstance(node, VoidNode)

    def test_raises_with_no_tag_at_init(self):
        node = lambda: VoidNode(None, None)  # type: ignore
        _ = expected_error(self, node, ValueError)

    def test_raises_with_no_tag_to_html(self):
        node = VoidNode(HTMLTags.META.value, None)
        node.tag = None
        _ = expected_error(self, lambda: node.to_html(), ValueError)

    def test_generates_good_meta_html(self):
        node = VoidNode(
            HTMLTags.META.value,
            {"charset": "UTF-8", "name": "description", "content": "some content"},
        )
        html = '<meta charset="UTF-8" name="description" content="some content">'
        self.assertEqual(node.to_html(), html)


if __name__ == "__main__":
    unittest.main()
