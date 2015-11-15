from crawler import crawler
import unittest

class TestCrawlerInvertedIndex(unittest.TestCase):
    def setUp(self):
        mock_doc_index = {
            1: (1, 2, 3),
            2: (2, 3, 4, 5),
            3: (3, 4, 5, 1)
        }

        mock_word_cache = {
            'hello': 1,
            'world': 2,
            'jelly': 3,
            'beans': 4,
            'green': 5
        }

        mock_doc_cache = {
            'http://example.com': 1,
            'http://example.com/123': 2,
            'http://someotherexample.com': 3
        }

        self.bot = crawler(None, '')
        self.bot._doc_id_cache = mock_doc_cache
        self.bot._word_id_cache = mock_word_cache
        self.bot._doc_index = mock_doc_index

    def test_add_words_to_document(self):
        self.bot._doc_index = {}

        self.bot._curr_words = [(1, 5), (2, 6), (3, 7)]
        self.bot._curr_doc_id = 1
        self.bot._add_words_to_document()

        self.bot._curr_words = [(2, 7), (3, 3), (4, 1)]
        self.bot._curr_doc_id = 2
        self.bot._add_words_to_document()

        expected = {
            1: (1, 2, 3),
            2: (2, 3, 4)
        }

        self.assertEqual(self.bot._doc_index, expected)

    def test_get_inverted_index(self):
        expected = {
            1: set([1, 3]),
            2: set([1, 2]),
            3: set([1, 2, 3]),
            4: set([2, 3]),
            5: set([2, 3])
        }

        self.assertEqual(self.bot.get_inverted_index(), expected)

    def test_get_resolved_inverted_index(self):
        expected = {
            'hello': set(['http://example.com', 'http://someotherexample.com']),
            'world': set(['http://example.com', 'http://example.com/123']),
            'jelly': set(['http://example.com', 'http://example.com/123', 'http://someotherexample.com']),
            'beans': set(['http://example.com/123', 'http://someotherexample.com']),
            'green': set(['http://example.com/123', 'http://someotherexample.com'])
        }

        self.assertEqual(self.bot.get_resolved_inverted_index(), expected)

    def test_db_persistence_and_page_rank(self):
        # mock url_pairs for page rank
        self.bot.add_link(1, 2)
        self.bot.add_link(2, 4)
        self.bot.add_link(3, 2)
        self.bot.persist_to_db(db_name="test_db")
        # normalize database results into dictionary
        rank = { doc['doc_id']: doc['score'] for doc in self.bot.db.page_rank.find() }
        self.assertEqual(rank[1], rank[3])
        self.assertGreater(rank[2], rank[1])
        self.assertGreater(rank[2], rank[3])


if __name__ == '__main__':
    unittest.main()
