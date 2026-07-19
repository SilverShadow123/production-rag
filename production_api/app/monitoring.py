import logging
import json
import time
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
        }

        if hasattr(record, 'extra_data'):
            log_obj.update(record.extra_data)
        return json.dumps(log_obj)


def get_logger(name: str = 'production-api') -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


class MetricsCollector:
    def __init__(self):
        self._request_total = 0
        self._error_total = 0
        self._latency_sum = 0
        self._latency_count = 0
        self._tokens_input = 0
        self._tokens_output = 0
        self._cache_hits = 0
        self._cache_misses = 0

    def record_request(self,
                       latency_ms: float,
                       input_tokens: int = 0,
                       output_tokens: int = 0,
                       error: bool = False,
                       cache_hit: bool = False
                       ):
        self._request_total += 1
        self._latency_sum += latency_ms
        self._latency_count += 1
        self._tokens_input += input_tokens
        self._tokens_output += output_tokens

        if error:
            self._error_total += 1

        if cache_hit:
            self._cache_hits += 1
        else:
            self._cache_misses += 1

    def get_summary(self) -> dict:
        avg_latency = (
            self._latency_sum / self._latency_count
            if self._latency_count > 0
            else 0
        )
        error_rate = (
            self._error_total / self._request_total
            if self._request_total > 0
            else 0
        )
        cache_hit_rate = (
            self._cache_hits
            / (self._cache_hits + self._cache_misses)
            if (self._cache_hits + self._cache_misses) > 0
            else 0
        )

        return {
            "total_requests": self._request_total,
            "total_errors": self._error_total,
            "error_rate": f"{error_rate:.2%}",
            "avg_latency_ms": round(avg_latency, 2),
            "total_input_tokens": self._tokens_input,
            "total_output_tokens": self._tokens_output,
            "cache_hit_rate": f"{cache_hit_rate:.2%}",
        }


class RequestTimer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.elapsed_ms = (time.time() - self.start) * 1000
