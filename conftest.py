"""Global pytest configuration."""
from framework.base.base_test import config, page, browser_name
from framework.utils.logger import setup_logger

# Setup logging
setup_logger()

# Re-export fixtures for global access
__all__ = ["config", "page", "browser_name"]
