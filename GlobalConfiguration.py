import os
import sys

__author__ = 'daan'

project_root = os.path.dirname(__file__)

import logging.config
logging.config.fileConfig(os.path.join(project_root, 'logging.conf'))

log = logging.getLogger(__name__)
log.info("logging set up.")
log.info("project root at %s", project_root)

sunburnt_path = os.path.join(project_root, "sunburnt")
sys.path.append(sunburnt_path)
log.debug("sunburnt submodule added to python path.")
