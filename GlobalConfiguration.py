import os
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
    'http://reddit.com/',
    'http://en.wikipedia.org/wiki/Special:Random',
    # 'http://www.fotopedia.com/reporter/home/popular',
)
log.info("default Solr url: %s", DEFAULT_URL_SEEDS)

sunburnt_path = os.path.join(project_root, "sunburnt")
sys.path.append(sunburnt_path)
log.debug("sunburnt submodule added to python path.")
