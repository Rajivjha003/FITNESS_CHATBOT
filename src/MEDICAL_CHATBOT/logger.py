import logging
import os
from datetime import datetime

LOG_file= f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"  #it create log_file in dir using .log in the current date format
log_path= os.path.join(os.getcwd(), "logs", LOG_file)           # it will fetch current work directory and make log file
os.makedirs(log_path, exist_ok=True)    # make dir called log_path

LOG_FILE_PATH =os.path.join(log_path, LOG_file)

logging.basicConfig(  # message for the logs 
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)