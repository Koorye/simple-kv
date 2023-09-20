import logging


class Logger(object):
    def __init__(self, root):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        handler = logging.FileHandler(root, mode='w')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def debug(self, x):
        self.logger.debug(x)
            
    def info(self, x):
        self.logger.info(x)
        
    def warn(self, x):
        self.logger.warn(x)
        
    def error(self, x):
        self.logger.error(x)
