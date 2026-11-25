import logging

logging.basicConfig(level=logging.DEBUG)

logging.debug("This is a debugging message")
logging.info("Application started")
logging.warning("API response is taking longer than expected")
logging.error("Unable to connect to database")
logging.critical("Application cannot continue")