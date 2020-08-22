import os
import coloredlogs, logging

# Create a logger object.
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


default_value: str = "xxxx"

http_response_500: str = "Internal Server Error"
http_response_200: str = "Successful Operation"
http_response_422: str = "Invalid Input"
http_response_400: str = "Bad Request"
http_response_403: str = "HTTP Connection Error"
