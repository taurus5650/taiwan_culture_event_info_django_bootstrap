import contextvars
import logging
import uuid
from datetime import datetime, timezone, timedelta
from functools import wraps
from logging.handlers import TimedRotatingFileHandler
from typing import Optional, Callable, Any, List, Type


class Logger:
    LOG_FORMAT = '%(asctime)s | %(levelname)s | %(request_id)s | %(message)s'

    def __init__(self):
        # ContextVar: pass a variable along the chain of calls so that they
        # share the same context.
        self.uuid_var = contextvars.ContextVar('request_id', default=None)
        self._logger = logging.getLogger('')
        self._setup_logger()

    def _create_context_filter(self):
        class ContextFilter(logging.Filter):
            def __init__(self, uuid_var):
                super().__init__()
                self.uuid_var = uuid_var

            def filter(self, record):
                record.request_id = self.uuid_var.get() or "-"
                return True

        return ContextFilter(self.uuid_var)

    def _create_handlers(self) -> List[logging.Handler]:
        # Console log
        console_handler = logging.StreamHandler()

        # Document log
        try:
            log_filename = f"app_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = TimedRotatingFileHandler(
                filename=log_filename,
                when='midnight',  # Rotate at midnight
                interval=1,  # Rotate every day
                backupCount=7,  # Keep 7 backup files
                encoding='UTF-8'
            )
        except Exception as e:
            self._logger.warning(f"Failed to create file handler: {e}")
            file_handler = None

        # Log timer converter
        def converter(timestamp):
            conv_datetime = datetime.fromtimestamp(
                timestamp, tz=timezone(timedelta(hours=8)))
            return conv_datetime.timetuple()

        # Set log format
        formatter = logging.Formatter(self.LOG_FORMAT)
        formatter.converter = converter

        console_handler.setFormatter(formatter)
        handlers = [console_handler]

        if file_handler:
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)

        return handlers

    def _setup_logger(self) -> None:
        if self.uuid_var.get() is None:
            self.set_request_id()

        context_filter = self._create_context_filter()
        handlers = self._create_handlers()

        root_logger = logging.getLogger()
        if not root_logger.handlers:
            for handler in handlers:
                root_logger.addHandler(handler)
            root_logger.setLevel(logging.INFO)

        root_logger.addFilter(context_filter)
        logging.setLogRecordFactory(self._record_factory_with_request_id())

    def _record_factory_with_request_id(self):
        factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs):
            record = factory(*args, **kwargs)
            record.request_id = self.uuid_var.get() or "-"
            return record

        return record_factory

    def set_request_id(self, request_id: Optional[str] = None) -> None:
        """ Set req id for request. """
        self.uuid_var.set(request_id or str(uuid.uuid4()))

    def get_request_id(self) -> Optional[str]:
        """ Get req id after request. """
        return self.uuid_var.get()

    def _log_decorator(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            request_id_existed = self.uuid_var.get() is not None
            if not request_id_existed:
                self.set_request_id()

            func_name = func.__name__
            self.info(f"○ Func start: {func_name}")

            try:
                result = func(*args, **kwargs)
                self.info(f"● Func end: {func_name}")
                return result
            except Exception as e:
                self.error(f"✘ Func ERROR: '{func_name}': {e}")
                raise
            finally:
                if not request_id_existed:
                    self.uuid_var.set(None)

        return wrapper

    def log_class(self, func: Callable) -> Callable:
        return self._log_decorator(func)

    def log_func(self, func: Callable) -> Callable:
        return self._log_decorator(func)

    def logger_class(self, cls: Type) -> Type:
        for attr_name in dir(cls):
            if not attr_name.startswith("__"):
                attr = getattr(cls, attr_name)
                if callable(attr):
                    setattr(cls, attr_name, self._log_decorator(attr))
        return cls

    def __getattr__(self, name: str) -> Any:
        if name in ("info", "error", "warning", "debug", "critical"):
            return getattr(self._logger, name)
        raise AttributeError(f"'Logger' object has no attribute '{name}'")


logger = Logger()
log_class = logger.log_class
log_func = logger.log_func
set_request_id = logger.set_request_id
get_request_id = logger.get_request_id
