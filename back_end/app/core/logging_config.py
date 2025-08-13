import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logging():
    """Configure logging for the application"""
    
    # Create logs directory
    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Create log filename with date
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"server_{today}.log"
    
    # Configure logging format
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            # File handler - all logs
            logging.FileHandler(log_file, encoding='utf-8'),
            # Console handler - INFO and above
            logging.StreamHandler()
        ]
    )
    
    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    # Set our app loggers to DEBUG for detailed tracking
    logging.getLogger("app").setLevel(logging.DEBUG)
    logging.getLogger("app.api").setLevel(logging.DEBUG)
    logging.getLogger("app.services").setLevel(logging.DEBUG)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured. Log file: {log_file}")
    logger.info("=" * 80)
    logger.info("SERVER STARTED")
    logger.info("=" * 80)
    
    return logger
