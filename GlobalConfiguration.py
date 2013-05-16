import os
import re
import sys

__author__ = 'daan'

project_root = os.path.dirname(__file__)

import logging.config
logging.config.fileConfig(os.path.join(project_root, 'logging.conf'))

log = logging.getLogger(__name__)
log.info("logging set up.")
log.info("project root at %s", project_root)

DEFAULT_SOLR_URL = 'http://130.229.171.104:8080/solr/test3'
# DEFAULT_SOLR_URL = 'http://localhost:8080/solr/test3'
log.info("default Solr url: %s", DEFAULT_SOLR_URL)

DEFAULT_URL_SEEDS = (
    'http://www.aljazeera.com/',
    'http://svd.se',
    'http://www.cnn.com',
    # 'http://www.coolthings.com/',
    'http://www.dn.se/',
    'http://edition.cnn.com/',
    'http://slashdot.org/',
    'http://www.thewebcomiclist.com/latest/',


    #'http://en.wikipedia.org/wiki/Special:Random',
)
log.info("default Solr url: %s", DEFAULT_URL_SEEDS)

sunburnt_path = os.path.join(project_root, "sunburnt")
sys.path.append(sunburnt_path)
log.debug("sunburnt submodule added to python path.")


image_block_regexs = (
    re.compile('.*\\.gif.*', re.IGNORECASE),
    re.compile('.*ad\\..*', re.IGNORECASE),
    re.compile('.*logo.*', re.IGNORECASE),
    re.compile('.*banner.*', re.IGNORECASE),
    re.compile('.*icon.*', re.IGNORECASE),
    re.compile('.*menu.*', re.IGNORECASE),
)

page_block_regexs = (
    re.compile('.*contact.*', re.IGNORECASE),
    re.compile('.*login.*', re.IGNORECASE),
    re.compile('.*\\.ad.*', re.IGNORECASE),
    re.compile('.*help.*', re.IGNORECASE),
    re.compile('.*\\.gif.*', re.IGNORECASE),
    re.compile('.*\\.jpg.*', re.IGNORECASE),
    re.compile('.*\\.png.*', re.IGNORECASE),
    re.compile('.*\\.bmp.*', re.IGNORECASE),
)
