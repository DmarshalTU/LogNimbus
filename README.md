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

## Roadmap

# LogNimbus Roadmap

| Feature                          | Status       | Description                                                                                     |
|----------------------------------|--------------|-------------------------------------------------------------------------------------------------|
| Human-Readable Format            | Implemented  | YAML's indentation-based structure makes logs easy to read and write.                           |
| Structured Data                  | Implemented  | Supports hierarchical logging with nested structures.                                           |
| Tool Compatibility               | Implemented  | Seamlessly integrates with tools like Fluentd and Logstash.                                     |
| Unified Configuration            | Implemented  | Aligns with YAML-based configuration management tools like Kubernetes and Helm.                 |
| Extensible and Flexible          | Implemented  | Easily add custom fields and adapt log structures.                                              |
| Machine-Readable                 | Implemented  | Simplifies automated log analysis and processing due to its structured nature.                  |
| Error Reduction                  | Implemented  | Schema validation helps maintain consistent and error-free log entries.                         |
| Prometheus Monitoring            | Implemented  | Integrated Prometheus metrics to monitor logging activity.                                      |
| Contextual Logging               | Implemented  | Includes context in log messages for better traceability.                                       |
| Sensitive Data Masking           | Implemented  | Masks sensitive fields in the log data to protect sensitive information.                        |
| Dynamic Configuration Reloading  | Implemented  | Allows reloading configuration at runtime without restarting the application.                   |
| Integration with Logging Module  | Implemented  | Provides a handler to integrate with Python’s built-in logging module.                          |
| Error Notifications via Slack    | Implemented  | Sends error notifications to Slack using a webhook URL.                                         |
| Asynchronous Logging             | Implemented  | Implemented to avoid blocking operations.                                                       |
| Log Rotation and Retention       | Implemented  | Supports log rotation based on size and retention policies.                                     |
| Time-Based Log Rotation          | Planned      | Rotate logs based on time intervals (daily, weekly, monthly).                                   |
| Nested Contexts                  | Planned      | Support nested contexts for more granular contextual information.                               |
| Custom Retention Policies        | Planned      | Allow defining custom retention policies for old logs.                                          |
| Error Notifications via Email    | Planned      | Integrate with email notification systems.                                                      |
| Retry Mechanism for Logging      | Planned      | Implement a retry mechanism for logging failures.                                               |
| Advanced Log Filters             | Planned      | Allow users to define filters to include or exclude certain log messages.                       |
| Search and Query Interface       | Planned      | Provide an interface to search and query logs.                                                  |
| Custom Metrics                   | Planned      | Allow users to define custom Prometheus metrics related to their application.                   |
| Health Check Endpoint            | Planned      | Provide an endpoint to monitor the health of the logging system.                                |
| Encryption for Log Files         | Planned      | Encrypt log files to ensure data security.                                                      |
| Audit Logging                    | Planned      | Provide tamper-evident logging for audit purposes.                                              |
| Interactive Log Viewer           | Planned      | Develop a web-based or terminal-based interactive log viewer for exploring logs.                |
| Customizable Log Formats         | Planned      | Allow users to define custom log formats and templates.                                         |


## Installation

```bash
pip install lognimbus
```

## Usage

**Basic Usage**

You can start using LogNimbus with minimal configuration, which defaults to console logging only.

```python
from lognimbus import YamlLogger

# Initialize the logger with default settings (console logging only)
logger = YamlLogger()

# Log messages at different levels
logger.debug(msg="This is a debug message")
logger.info(msg="This is an info message")
logger.warning(msg="This is a warning message")
logger.error(msg="This is an error message")
logger.critical(msg="This is a critical message")

```

**Advanced Usage**

Override default settings and enable additional features as needed.
```python
from lognimbus import YamlLogger, LogContext

# Initialize the logger with custom settings
logger = YamlLogger(
    log_file='app_logs.yml',
    log_rotation_enabled=True,
    max_log_size=5242880,  # 5MB
    backup_count=3,
    prometheus_enabled=True,
    slack_webhook_url='https://hooks.slack.com/services/your/webhook/url'
)

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

## Integration with Python's Built-in Logging Module

You can integrate LogNimbus with Python's built-in logging module for seamless logging.

```python
from lognimbus import YamlLogger, LogNimbusHandler
import logging

# Initialize the logger
logger = YamlLogger()

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
```

## Configuratio

You can also configure LogNimbus using a YAML configuration file. Here is an example configuration file (lognimbus_config.yml):

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
  notifications:
    slack_webhook_url: "https://hooks.slack.com/services/your/webhook/url"  # Optional
```

To use the configuration file:

```python
from lognimbus import YamlLogger

# Initialize the logger from a configuration file
logger = YamlLogger(config_file='lognimbus_config.yml')

# Log messages as usual
logger.info(msg="Configured via YAML file")
```

## Why YAML-Based Logging?

YAML-based logging offers several advantages:
- Readability: Easy for humans to read and write.
- Structured Data: Captures complex data in a clear, hierarchical format.
- Compatibility: Works well with modern logging tools and container management systems.
- Flexibility: Easily extendable with custom fields.
- Consistency: Uniform format for both configuration and logs in cloud-native environments.

LogNimbus makes logging in YAML format simple and effective, enhancing both human readability and machine parsing capabilities, making it an excellent choice for modern development practices and cloud-native applications.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/100kw)
