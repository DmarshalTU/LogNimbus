# LogNimbus
![lognimbus](lognimbus.png)

LogNimbus is a YAML-based logging library with rich formatting for container and Kubernetes environments.

## Features

- **Human-Readable Format**: YAML's indentation-based structure makes logs easy to read and write, facilitating quick understanding.
- **Structured Data**: Supports hierarchical logging with nested structures, allowing for detailed and organized logs.
- **Tool Compatibility**: Seamlessly integrates with modern logging and monitoring tools like Fluentd and Logstash, which efficiently parse YAML.
- **Unified Configuration**: Aligns with YAML-based configuration management tools (e.g., Kubernetes, Helm), ensuring consistency across your stack.
- **Extensible and Flexible**: Easily add custom fields and adapt log structures to evolving application requirements.
- **Machine-Readable**: Simplifies automated log analysis and processing due to its structured nature.
- **Error Reduction**: Schema validation helps maintain consistent and error-free log entries.
- **Prometheus Monitoring**: Integrated Prometheus metrics to monitor logging activity.
- **Contextual Logging**: Includes context in log messages for better traceability.
- **Sensitive Data Masking**: Masks sensitive fields in the log data to protect sensitive information.

## Installation

```bash
pip install lognimbus
```

## Usage

```python
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


```

## Configuratio

```yaml
lognimbus:
  log_file: "app_logs.yml"
  additional_log_file: "backup_logs.yml"
  console_logging: true
  log_level: "INFO"
  log_rotation:
    enabled: true
    max_size: 10485760  # 10MB
    backup_count: 5
  prometheus_port: 8000
  sensitive_data_masking:
    enabled: true
    fields:
      - "password"
      - "credit_card_number"

```

## Why YAML-Based Logging?

YAML-based logging offers several advantages:
- Readability: Easy for humans to read and write.
- Structured Data: Captures complex data in a clear, hierarchical format.
- Compatibility: Works well with modern logging tools and container management systems.
- Flexibility: Easily extendable with custom fields.
- Consistency: Uniform format for both configuration and logs in cloud-native environments.

LogNimbus makes logging in YAML format simple and effective, enhancing both human readability and machine parsing capabilities, making it an excellent choice for modern development practices and cloud-native applications.
