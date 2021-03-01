from http import HTTPStatus

import requests


def test_healthcheck(healthcheck_url):
    response = requests.get(healthcheck_url)
    assert HTTPStatus.OK == response.status_code
