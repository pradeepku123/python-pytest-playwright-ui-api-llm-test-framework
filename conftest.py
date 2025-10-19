"""Global pytest configuration."""
from framework.base.base_test import config, page

# Re-export fixtures for global access
__all__ = ['config', 'page']
