import logging
import time
 
class Log(object):    
    def __init__(self, name, out_path=""):    
        self.logger = logging.getLogger(name)    
        self.logger.setLevel(logging.INFO)
        if out_path:
            self.out_to_file(out_path)
        else:
            self.out_to_terminal()

    def out_to_terminal(self):
        self.ch = logging.StreamHandler()    
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s[line:%(lineno)d] - %(message)s')    
        self.ch.setFormatter(formatter)    
        self.logger.addHandler(self.ch) 
    
    def out_to_file(self, out_path):
        rq = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.filename = out_path + rq + '.log'
        self.fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 10)    
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s -   %(name)s[line:%(lineno)d] - %(message)s')
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)
        
if __name__ == "__main__":
    log = Log("tete")
    log.logger.info("adfadfa")
