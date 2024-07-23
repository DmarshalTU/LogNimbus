from lognimbus import YamlLogger, LogContext

# Initialize the logger from a configuration file
logger = YamlLogger(config_file='lognimbus_config.yml')  # Adjust path as needed

# Log messages at different levels
logger.debug(msg="This is a debug message")
logger.info(msg="This is an info message")
logger.warning(msg="This is a warning message")
logger.error(msg="This is an error message")
logger.critical(msg="This is a critical message")

# Log a message with additional data
additional_data = {
    'User': {'id': 12345, 'name': "John Doe"},
    'Operation': 'Data Processing'
}
logger.info(msg="Data processing completed", data=additional_data)

# Add contextual information and log messages with context
with LogContext(request_id='12345', user_id='john_doe'):
    logger.info(msg="User login attempt")
    try:
        # Simulate a login operation
        raise ValueError("Invalid credentials")
    except Exception as e:
        logger.log_exception(e, msg="Login failed")

# Log a message with sensitive data
sensitive_data = {
    'password': 'secret_password',
    'credit_card_number': '1234-5678-9876-5432'
}
logger.info(msg="User payment processing", data=sensitive_data)
