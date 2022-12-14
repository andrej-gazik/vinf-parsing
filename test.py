import os
from unittest import TestCase
import unittest
from conf import (
    INDEX_DIR,
    OUTPUT_DIR,
    TYPE_REGEX,
    NAME_REGEX,
    ALIAS_REGEX,
    INPUT_FILE,
    PRESENT_PHRASE,
    PRESENT_WORD,
)
import argparse
from whoosh import scoring
from whoosh import index
from search import search

# class TestHelloWorld(TestCase):
#     def (self):
#         self.assertEqual("Hello World", "Hello World", "incorrect")


class TestRegexExpressions(TestCase):

    # Type regex

    # Alias regex

    def test_name_regex(self):
        test_str = '<http://rdf.freebase.com/ns/m.11b822qb2c>	<http://rdf.freebase.com/ns/type.object.name>	"Seven Names"@en	.'

        self.assertRegex(test_str, NAME_REGEX)

    def test_type_regex(self):
        test_str = "<http://rdf.freebase.com/ns/m.11b822qb2v>	<http://rdf.freebase.com/ns/type.object.type>	<http://rdf.freebase.com/ns/base.type_ontology.abstract>	."

        self.assertRegex(test_str, TYPE_REGEX, "xd")

    def test_alt_regex(self):
        test_str = '<http://rdf.freebase.com/ns/m.11b8c59_m9>	<http://rdf.freebase.com/ns/common.topic.alias>	"13.1.14.4.18.1.7.15.181.1100"@en	.'
        self.assertRegex(test_str, ALIAS_REGEX)


class TestParsingResults(TestCase):
    def test_output_dir_existence(self):
        self.assertTrue(os.path.exists(OUTPUT_DIR))

    def test_output_files_creation(self):
        self.assertGreater(len(os.listdir(OUTPUT_DIR)), 0)

    def test_input_data_existence(self):
        self.assertTrue(os.path.exists(INPUT_FILE))


class TestIndexingResults(TestCase):
    def test_index_creation(self):
        self.assertTrue(os.path.exists(INDEX_DIR))
        self.assertGreater(len(os.listdir(INDEX_DIR)), 0)


class TestSearchingResults(TestCase):
    def test_finding_word(self):
        ix = index.open_dir(INDEX_DIR)
        s = ix.searcher(weighting=scoring.TF_IDF())
        self.assertGreater(
            len(search(PRESENT_WORD, ix, s)), 0, "Word not found in index"
        )

    def test_finding_words(self):
        ix = index.open_dir(INDEX_DIR)
        s = ix.searcher(weighting=scoring.TF_IDF())
        self.assertGreater(
            len(search('"' + PRESENT_PHRASE + '"', ix, s)), 0, "Word not found in index"
        )


def regex_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestRegexExpressions("test_name_regex"))
    suite.addTest(TestRegexExpressions("test_type_regex"))
    suite.addTest(TestRegexExpressions("test_alt_regex"))
    return suite


def parsing_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestParsingResults("test_output_dir_existence"))
    suite.addTest(TestParsingResults("test_output_files_creation"))
    suite.addTest(TestParsingResults("test_input_data_existence"))
    return suite


def index_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestIndexingResults("test_index_creation"))
    return suite


def search_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestSearchingResults("test_finding_word"))
    suite.addTest(TestSearchingResults("test_finding_words"))
    return suite


if __name__ == "__main__":
    # Argument parsing
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        "-t", "--test", help="Test to run (regex | parsing | index | search | runall)"
    )

    args = argParser.parse_args()

    runner = unittest.TextTestRunner(verbosity=2)

    # Running test logic
    if args.test is not None:
        if args.test == "regex":
            runner.run(regex_suite())

        if args.test == "parsing":
            runner.run(parsing_suite())

        if args.test == "index":
            runner.run(index_suite())

        if args.test == "search":
            runner.run(search_suite())

        if args.test == "runall":
            runner.run(regex_suite())
            runner.run(parsing_suite())
            runner.run(index_suite())
            runner.run(search_suite())
