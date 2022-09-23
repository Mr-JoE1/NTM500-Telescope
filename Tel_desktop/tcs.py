import logging
import sys
import os 

absFilePath = os.path.abspath(__file__)
fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)-2s - %(name)-5s - %(levelname)s: %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=fileDir+'/history.log',
                    filemode='a')

maher = logging.getLogger('Cigar')

#logging.debug('This is a debug message')
#logging.info('This is an info message')
#logging.warning('This is a warning message')
#logging.error('This is an error message')
#logging.critical('This is a critical message')