import logging
import os
from time import sleep
from urllib.parse import urljoin

import httpx
import pytest
from requests import ReadTimeout
from urllib3.exceptions import NewConnectionError

logging.basicConfig(level="DEBUG")
logger = logging.getLogger()


@pytest.fixture(scope="session")
def service_endpoint():
    return os.environ.get("SERVICE_ENDPOINT", "http://localhost:8000").strip("/")


@pytest.fixture(scope="session")
def healthcheck_url(service_endpoint):
    return urljoin(service_endpoint, "healthcheck")


@pytest.fixture(scope="session", autouse=True)
def wait_for_service(service_endpoint):
    """Waits for service to respond to GET request on SERVICE_ENDPOINT (env)

    The following environemnt variables can be used to adjust delays / retries:
    INTEGRATION_INIT_RETRIES - how many retries - by default it's 10
    INTEGRATION_INIT_DELAY - delay time in seconds between retries - by default it's 5.0
    Args:
        service_endpoint:

    Returns:

    """
    retries = int(os.environ.get("INTEGRATION_INIT_RETRIES", "10"))
    delay = float(os.environ.get("INTEGRATION_INIT_DELAY", "5.0"))
    for i in range(retries):
        logger.info(
            f"Waiting for {service_endpoint} to be reachable... [{i + 1}/{retries}]"
        )
        try:
            httpx.get(service_endpoint)
            logger.info(f"Connected to {service_endpoint}")
            break
        except (
            httpx._exceptions.NetworkError,
            ConnectionRefusedError,
            NewConnectionError,
            ReadTimeout,
        ):
            logger.warning(
                f"Could not connect to endpoint, waiting {delay}s before next retry"
            )
            sleep(delay)
    else:
        logger.error(f"Cannot connect to the service {service_endpoint}")
