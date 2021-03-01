# Face Detection Service

A service providing REST API for face detection.

## Rationale

I created two endpoints:

* REST endpoint for "production" usage
* Web interface for easy result checking

The application uses Flask, OpenCV and Tensorflow. Detection is based on
the [MTCNN face detector](https://github.com/ipazc/mtcnn).

There is a dockerfile available that allows to build and run the application easily. The container deployment uses
gunicorn as a server.

## Installation

To build and run the application using docker-compose run:
`docker-compose -f docker-compose.yml up face_service`

By default the application listens on the 8000 port.

## Usage

### Web interface

Assuming that you have started the app locally, visit the: [http://localhost:8000](http://localhost:8000). You should
see following interface:
![web interface](images/screen.png)
Detection is applied immediately after uploading an image. Image itself is lightened a bit to make boxes more visible.

### REST API

```bash
curl --location --request POST 'localhost:8000/api/detect' \
--header 'Content-Type: image/jpeg' \
--data-binary '@examples/1.jpeg'
```

#### Example response

The service returns a JSON containing list of objects in a following form:

```[
    {
        "box": [
            1820,
            352,
            29,
            41
        ],
        "confidence": 0.7826327085494995,
        "keypoints": {
            "left_eye": [
                1832,
                368
            ],
            "right_eye": [
                1844,
                366
            ],
            "nose": [
                1840,
                375
            ],
            "mouth_left": [
                1834,
                384
            ],
            "mouth_right": [
                1843,
                383
            ]
        }
    }
]
```

Box format: [x, y, width, height]

Features format: [x, y]

## Tests

### Unit tests

`docker-compose -f docker-compose.yml up unit_tests`

### Integration tests

`docker-compose -f docker-compose.yml up integration_tests`