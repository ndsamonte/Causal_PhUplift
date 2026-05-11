import logging
import sys

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

# logger.py
def log_message(msg):
    print(f"[LOG]: {msg}")

# This part only runs if 'logger.py' is run, for testing purposes
if __name__ == "__main__":
    print("Testing logger...")
    log_message("This is a test message.")
    print("Test complete!")

