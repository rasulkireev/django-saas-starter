from logging import LogRecord

from sentry_sdk.integrations.logging import LoggingIntegration

_IGNORED_LOGGERS = {"ask_hn_digest"}

class CustomLoggingIntegration(LoggingIntegration):
    def _handle_record(self, record: LogRecord) -> None:
        # This match upper logger names, e.g. "celery" will match "celery.worker"
        # or "celery.worker.job"
        if record.name in _IGNORED_LOGGERS or record.name.split(".")[0] in _IGNORED_LOGGERS:
            return
        super()._handle_record(record)


def before_send(event, hint):
    if "exc_info" in hint:
        exc_type, exc_value, tb = hint["exc_info"]

        if isinstance(exc_value, SystemExit):  # group all SystemExits together
            event["fingerprint"] = ["system-exit"]
    return event
