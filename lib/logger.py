from logging import INFO, basicConfig, getLogger

basicConfig(level=INFO, datefmt='%b-%d-%Y %H:%M:%S', format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger('tracker.py')
