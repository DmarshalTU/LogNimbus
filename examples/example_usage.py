from lognimbus import YamlLogger, LogNimbusHandler, LogContext
import logging

# Initialize the logger with default settings (console logging only)
logger = YamlLogger()

# Optional: Override default settings through the constructor
logger_with_overrides = YamlLogger(
    log_file='custom_logs.yml',
    log_rotation_enabled=True,
    max_log_size=5242880,  # 5MB
    backup_count=3,
    prometheus_enabled=True,
    slack_webhook_url='https://hooks.slack.com/services/your/webhook/url'
)

# Integrate with Python's built-in logging module
log_handler = LogNimbusHandler(logger)
logging.basicConfig(level=logging.DEBUG, handlers=[log_handler])
python_logger = logging.getLogger(__name__)

# Log messages at different levels using the standard logging module
python_logger.debug("This is a debug message")
python_logger.info("This is an info message")
python_logger.warning("This is a warning message")
python_logger.error("This is an error message")
python_logger.critical("This is a critical message")

# Log a message with additional data using YamlLogger
additional_data = {
    'User': {'id': 12345, 'name': "John Doe"},
    'Operation': 'Data Processing'
}
logger.info(msg="Data processing completed", data=additional_data)

# Add contextual information and log messages with context using YamlLogger
with LogContext(request_id='12345', user_id='john_doe'):
    logger.info(msg="User login attempt")
    try:
        # Simulate a login operation
        raise ValueError("Invalid credentials")
    except Exception as e:
        logger.log_exception(e, msg="Login failed")

# Log a message with sensitive data using YamlLogger
sensitive_data = {
    'password': 'secret_password',
    'credit_card_number': '1234-5678-9876-5432'
}
logger.info(msg="User payment processing", data=sensitive_data)
