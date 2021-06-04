from logging import basicConfig, getLogger, INFO

basicConfig(level=INFO, datefmt='%b-%d-%Y %H:%M:%S', format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger('tracker.py')
