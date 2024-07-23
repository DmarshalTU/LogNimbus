import unittest
from lognimbus import YamlLogger, LogContext
from datetime import datetime
import os

class TestYamlLogger(unittest.TestCase):
    def setUp(self):
        self.logger = YamlLogger(config_file='test_lognimbus_config.yml')

    def test_debug_log(self):
        self.logger.debug(msg="This is a debug message")
        # Check the log file or structure to ensure the message was logged

    def test_info_log(self):
        self.logger.info(msg="This is an info message")
        # Check the log file or structure to ensure the message was logged

    def test_warning_log(self):
        self.logger.warning(msg="This is a warning message")
        # Check the log file or structure to ensure the message was logged

    def test_error_log(self):
        self.logger.error(msg="This is an error message")
        # Check the log file or structure to ensure the message was logged

    def test_critical_log(self):
        self.logger.critical(msg="This is a critical message")
        # Check the log file or structure to ensure the message was logged

    def test_log_exception(self):
        try:
            raise ValueError("This is a test exception")
        except Exception as e:
            self.logger.log_exception(e, msg="Exception occurred during processing")
        # Check the log file or structure to ensure the exception was logged

    def test_contextual_logging(self):
        with LogContext(request_id='12345', user_id='john_doe'):
            self.logger.info(msg="User login attempt with context")
            try:
                raise ValueError("Invalid credentials")
            except Exception as e:
                self.logger.log_exception(e, msg="Login failed")
        # Check the log file or structure to ensure the context was logged

    def test_sensitive_data_masking(self):
        sensitive_data = {'password': 'secret', 'credit_card_number': '1234-5678-9876-5432'}
        self.logger.info(msg="Logging with sensitive data", data=sensitive_data)
        # Check the log file or structure to ensure sensitive data is masked

if __name__ == '__main__':
        unittest.main()