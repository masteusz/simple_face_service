from io import BytesIO

import pytest

from utils import check_image

EXAMPLE_LIST = [
    ('examples/1.jpeg', True),
    ('examples/2.jpeg', True),
    ('examples/3.png', True),
    ('examples/empty.bmp', False),
]


@pytest.mark.parametrize("imgpath,expected", EXAMPLE_LIST)
def test_examples(imgpath, expected, app):
    with open(imgpath, "rb") as f:
        s = BytesIO(f.read())
        with app.app_context():
            res = check_image(s)
        assert res == expected
