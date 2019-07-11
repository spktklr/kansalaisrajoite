#!/bin/sh
if [ "$DEVELOPMENT" = "false" ]; then
	LOG_LEVEL=info
else
	LOG_LEVEL=debug
fi

gunicorn -b 0.0.0.0:8000 -k gevent main:application --log-level=$LOG_LEVEL
