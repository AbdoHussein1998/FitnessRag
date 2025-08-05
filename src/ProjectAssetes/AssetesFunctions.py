import logging

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)  # Change name as needed
    logger.setLevel(logging.DEBUG)  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

# Create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    return logger

