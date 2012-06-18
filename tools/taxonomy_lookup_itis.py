import sys
reload(sys)
sys.setdefaultencoding('utf8')
import spynner
import re
from pyquery import PyQuery as p
try:
    from itis_cache import itis_cache
except:
    itis_cache = {}


ITIS_URL = 'http://www.itis.gov/'

browser = spynner.Browser()

def itis_lookup(name):
    success = browser.load(ITIS_URL)
    if not success: raise Exception('ITIS failed to load.')

    # fill in search box and submit form
    browser.fill('input#search', name)
    browser.runjs('doSubmit();')

    # wait for results to load
    while not 'results of' in browser.html.lower():
        browser.wait(1)

    # parse results to pull out unique species
    html = browser.html
    results = [s.tail for s in p(html)('td.body a')]
    species = sum([re.findall('Species: [A-Z][a-z ]*', result) for result in results], [])
    species = [s.split(':')[1].strip() for s in species]
    
    if species and len(species) == 1:
        itis_cache[name] = result
        open('itis_cache.py', 'w').write('itis_cache = %s' % tnrs_cache)
        return species

    return False

if __name__=='__main__':
    print itis_lookup('sparrowhawk')
