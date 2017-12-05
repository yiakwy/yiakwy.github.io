'''
Created on 14 Jul, 2016

@author: wangyi
'''
import logging
from logging.config import dictConfig

class NotConfigured(Exception):pass

class LoggerAdaptor(logging.LoggerAdapter):

    def __init__(self, prefix, logger):
        # super(self, App_LoggerAdaptor).__init__(logger, {})
        logging.LoggerAdapter.__init__(self, logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        return "%s %s" % (self.prefix, msg), kwargs
    
def configure_loggings(config):
    if config:
        dictConfig(config)
    else:
        raise NotConfigured(details="passing null config!")

