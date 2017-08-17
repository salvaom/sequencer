import logging
import os
import sys

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv('SEQUENCER_LOG_LEVEL', 'WARNING'))

exec_name = os.path.split(sys.executable)[-1]

# Double logging!
if not any([x in exec_name for x in ['maya', 'mayapy']]):
    logging.basicConfig()
