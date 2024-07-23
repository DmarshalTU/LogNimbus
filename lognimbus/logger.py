import yaml
import os
from rich.console import Console
from rich.text import Text
from datetime import datetime
from logging.handlers import RotatingFileHandler
from prometheus_client import Counter, start_http_server

from .config import Config
from .context import LogContext

class YamlLogger:
    LEVELS = {
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold red'
    }

    # Prometheus metrics
    log_counter = Counter('log_messages_total', 'Total number of log messages', ['level'])

    def __init__(self, config_file=None):
        self.config = Config(config_file)
        self.console_logging = self.config.get('lognimbus.console_logging', True)
        self.log_file = self.config.get('lognimbus.log_file', 'logs.yml')
        self.additional_log_file = self.config.get('lognimbus.additional_log_file')
        self.log_level = self.config.get('lognimbus.log_level', 'INFO').upper()
        self.sensitive_fields = self.config.get('lognimbus.sensitive_data_masking.fields', [])

        # Log rotation settings
        self.log_rotation_enabled = self.config.get('lognimbus.log_rotation.enabled', False)
        self.max_log_size = self.config.get('lognimbus.log_rotation.max_size', 10485760)  # 10MB default
        self.backup_count = self.config.get('lognimbus.log_rotation.backup_count', 5)

        self.console = Console()  # Create a Console instance for rich formatting

        # Setup log rotation handler if enabled
        if self.log_rotation_enabled:
            self.handler = RotatingFileHandler(
                self.log_file, maxBytes=self.max_log_size, backupCount=self.backup_count)
        else:
            self.handler = None

        # Start Prometheus server for metrics
        prometheus_port = self.config.get('lognimbus.prometheus_port', 8000)
        start_http_server(prometheus_port)

    def _mask_sensitive_data(self, data):
        for field in self.sensitive_fields:
            if field in data:
                data[field] = '***'
        return data

    def _log_to_file(self, file_path, data):
        if self.handler:
            log_file = self.handler.stream.name
        else:
            log_file = file_path

        with open(log_file, 'a') as file:
            console = Console(file=file)
            console.rule(f"Report Generated {datetime.now().ctime()}")
            yaml.dump(data, file, default_flow_style=False)

    def _get_colored_level(self, level):
        color = self.LEVELS.get(level, 'white')
        return color

    def _log(self, level, msg=None, data=None, ex='None'):
        # Skip logging if the log level is lower than the configured log level
        if list(self.LEVELS.keys()).index(level) < list(self.LEVELS.keys()).index(self.log_level):
            return

        # Update Prometheus counter
        self.log_counter.labels(level=level).inc()

        log_data = {
            'Timestamp': datetime.now().ctime(),
            'Level': level,
            'Exception': ex
        }

        context = LogContext.get_context()
        if context:
            log_data['Context'] = context

        if msg:
            log_data['Message'] = msg

        if data:
            log_data['Data'] = self._mask_sensitive_data(data)

        # Log to the primary file
        self._log_to_file(self.log_file, log_data)

        # Log to the additional file if specified
        if self.additional_log_file:
            self._log_to_file(self.additional_log_file, log_data)

        # Log to console if enabled
        if self.console_logging:
            color = self._get_colored_level(level)
            colored_level = Text(level, style=color)
            self.console.print(colored_level, end=" ")
            self.console.print(f"Report Generated {datetime.now().ctime()}")
            self.console.print(yaml.dump(log_data, default_flow_style=False))

    def debug(self, msg=None, data=None):
        self._log('DEBUG', msg, data)

    def info(self, msg=None, data=None):
        self._log('INFO', msg, data)

    def warning(self, msg=None, data=None):
        self._log('WARNING', msg, data)

    def error(self, msg=None, data=None):
        self._log('ERROR', msg, data)

    def critical(self, msg=None, data=None):
        self._log('CRITICAL', msg, data)

    def log_exception(self, ex, msg=None, data=None):
        log_data = {
            'Timestamp': datetime.now().ctime(),
            'Level': 'ERROR',
            'Exception': {
                'Type': type(ex).__name__,
                'Message': str(ex),
                'Args': ex.args
            }
        }

        if msg:
            log_data['Message'] = msg

        if data:
            log_data['Data'] = self._mask_sensitive_data(data)

        # Log to the primary file
        self._log_to_file(self.log_file, log_data)

        # Log to the additional file if specified
        if self.additional_log_file:
            self._log_to_file(self.additional_log_file, log_data)

        # Log to console if enabled
        if self.console_logging:
            color = self._get_colored_level('ERROR')
            colored_level = Text('ERROR', style=color)
            self.console.print(colored_level, end=" ")
            self.console.print(f"Exception Occurred at {datetime.now().ctime()}")
            self.console.print(yaml.dump(log_data, default_flow_style=False))
