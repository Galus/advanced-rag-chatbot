import logging
import pprint
import sys
from typing import Any
import os

class PrettyPrintFormatter(logging.Formatter):
    """A custom formatter that uses pprint for the log message content."""
    
    # Define a special attribute key to flag if pretty-printing should be used
    PP_KEY = "pretty_print"

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log message. If record has the PP_KEY attribute set to True,
        it uses pprint.pformat() on the message content.
        """
        
        # Check if the log record has the pretty_print flag set
        if getattr(record, self.PP_KEY, False):
            # Use pprint.pformat() to pretty-print the message content
            # We assume the message is a complex object (like a dict or list)
            try:
                # The message content is accessed via record.args when using extra
                # For simplicity, we just format the msg attribute itself here.
                # If the log call was `logger.info("Data:", extra={"pprint_data": my_dict})` 
                # you might use `pprint.pformat(record.__dict__.get("pprint_data"))`
                
                # In this setup, we assume the dict/list is passed as the main message.
                pp_content = pprint.pformat(record.msg)
                
                # Replace the original message with the pretty-printed content
                record.msg = pp_content
                
                # Clear the args so the default formatter doesn't try to interpolate
                record.args = ()
            except Exception:
                # Fallback if the message isn't a complex object
                pass

        # Use the base class to handle the rest of the formatting (timestamp, level name, etc.)
        return super().format(record)


def setup_pprint_logger(name: str = 'my_pp_logger', level: int = logging.INFO) -> logging.Logger:
    """Sets up a logger with the PrettyPrintFormatter."""
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent propagation to the root logger, which might double-print
    logger.propagate = False 

    # Create a stream handler to output logs to the console
    handler = logging.StreamHandler(sys.stdout)
    
    # Define the format for the rest of the log line
    # (asctime, levelname, and the final pretty-printed message)
    log_format = '%(asctime)s - %(levelname)s - %(name)s: %(message)s'
    
    # Instantiate the custom formatter
    formatter = PrettyPrintFormatter(fmt=log_format)
    
    # Attach the formatter to the handler
    handler.setFormatter(formatter)
    
    # Attach the handler to the logger
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

def configure_root_pprint_logger():
    """
    Configures the root logger to use the PrettyPrintFormatter.
    This sets the default behavior for ALL loggers unless explicitly overridden.
    """
    
    log_level_name = os.environ.get('LOG_LEVEL', 'INFO').upper()
    try:
        log_level = logging.getLevelName(log_level_name)
    except ValueError:
        print(f"Warning: Invalid LOG_LEVEL '{log_level_name}'. Defaulting to INFO.")
        log_level = logging.INFO

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Create a handler (e.g., StreamHandler for console output)
    handler = logging.StreamHandler(sys.stdout)
    
    # Define the base log format
    log_format = '%(asctime)s - %(levelname)s - %(name)s: %(message)s'
    
    # Instantiate and set the custom formatter
    formatter = PrettyPrintFormatter(fmt=log_format)
    handler.setFormatter(formatter)
    
    # Clear any existing handlers to prevent duplicate output, 
    # which is common when frameworks set up their own logging.
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    # Add the custom handler to the root logger
    root_logger.addHandler(handler)

    silence_third_party_loggers(max_level=logging.INFO)

    print(f"\n--- Logging initialized ---")
    print(f"Root/App level set to: {logging.getLevelName(root_logger.level)}")
    print("--- ------------------- ---\n")

def silence_third_party_loggers(max_level: int = logging.INFO):
    # These will get set to max_level
    noisy_loggers = [
        'anthropic',
        'urllib3',
        'uvicorn.access',
        'langchain.retrievers'
    ]

    for logger_name in noisy_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(max_level)
        print(f"Silenced logger '{logger_name}' to level: {logging.getLevelName(max_level)}")

    # These will get set to CRITICAL
    blacklisted_loggers = [
        'httpx',
        'httpcore',
        'asyncio',
    ]

    CRITICAL_LEVEL = logging.CRITICAL
    for logger_name in blacklisted_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(CRITICAL_LEVEL)
        print(f"Silenced logger '{logger_name}' to level: {logging.getLevelName(CRITICAL_LEVEL)}")

