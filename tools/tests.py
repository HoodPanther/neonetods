from unittest import TestCase, main
from tax_resolve import tax_resolve
from get_mendeley_data import get_mendeley_data, citation


class TestTaxResolve(TestCase):
    def setUp(self):
        self.syn1 = {'applb': 'apple', 'applc': 'apple', 'bannnna': 'banana'}

        self.syn2 = {}
        data_file = open("../data/mosquito_synonyms.csv", 'r')
        data_file.readline()
        for line in data_file:
            wrong, right, spid, ref = line.split(',')
            self.syn2[wrong] = right


    def test_apple(self):
        for l, r in [('appleb', 'apple'), 
                     ('applb', 'apple'), 
                     ('apple', 'apple'), 
                     ('a', 'a'),
                     ('ap', 'ap'), 
                     ('appl', 'apple'), 
                     ('bionan', 'bionan'), 
                     ('banann', 'banana'), 
                     ('bannans', 'banana'),
                     ]:
            self.assertEqual(tax_resolve(l, self.syn1), r)
    
    def test_mosquitos(self):
        for to_test in ['Aedes clivis', 'Aedes clivid', 'Ochlerotatus clivis', 'Ochlerotatus clivid', 'Ochlarodadus clivus']:
            self.assertEqual(tax_resolve(to_test, self.syn2), 'Aedes clivis')


class TestMendeleyTags(TestCase):
    def setUp(self):
        self.url1 = "http://www.mendeley.com/research/niche-neutrality/"
        self.data_doc1 = get_mendeley_data(self.url1)
        self.citation1 = citation(self.url1)

        self.url2 = "http://www.mendeley.com/research/local-interactions-select-lower-pathogen-infectivity/"
        self.data_doc2 = get_mendeley_data(self.url2)
        self.citation2 = citation(self.url2)

        print '\n'.join((self.citation1, self.citation2))

    def test_adler(self):
        self.assertEqual(self.data_doc1['title'], 'A niche for neutrality')
        self.assertEqual(self.data_doc1['year'], 2007)
        self.assertEqual(self.data_doc1['published_in'], 'Ecology Letters')
        self.assertIn('Adler, P.', self.citation1)
        self.assertIn(self.data_doc1['title'], self.citation1)

    def test_boots(self):
        self.assertEqual(self.data_doc2['title'], 'Local interactions select for lower pathogen infectivity')
        self.assertEqual(self.data_doc2['year'], 2007)
        self.assertEqual(self.data_doc2['published_in'], 'Science')
        self.assertIn('Boots, M.', self.citation2)
        self.assertIn(self.data_doc2['title'], self.citation2)


if __name__ == '__main__':
    main()