from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import sys


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger.info(f'\033[95mRequest: {request.method} {request.url}\033[0m')
        response = await call_next(request)
        logger.info(f'\033[95mResponse: {response.status_code}\033[0m')
        return response


logger.add(
    sys.stderr,
    level='INFO',
    colorize=True,
    format=(
        '<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <green>{level}</green>'
    )
)


if __name__ == '__main__':
    pass
