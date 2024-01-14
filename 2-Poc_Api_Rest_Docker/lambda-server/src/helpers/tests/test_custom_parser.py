import unittest
from custom_parser import CustomHTMLParser

class TestCustomHTMLParser(unittest.TestCase):
    def setUp(self):
        # Configuração inicial comum para os testes
        self.html_parser = CustomHTMLParser(123)

    def test_handle_starttag(self):
        # Testa o método handle_starttag
        test_html = '<body><div><a href="http://example.com">Link</a></div></body>'
        expected_links = [('None', 'None', 'http://example.com')]
        
        self.html_parser.feed(test_html)
        self.assertEqual(self.html_parser.get_links(), expected_links)

    def test_handle_endtag(self):
        # Testa o método handle_endtag
        test_html = '<head></head><body></body><div></div>'
        expected_links = []

        self.html_parser.feed(test_html)
        self.assertEqual(self.html_parser.get_links(), expected_links)

    def test_handle_data(self):
        # Testa o método handle_data
        test_html = '<head>title_code</head><div>title_file</div>'
        expected_links = []

        self.html_parser.feed(test_html)
        self.assertEqual(self.html_parser.get_links(), expected_links)

if __name__ == '__main__':
    unittest.main()
