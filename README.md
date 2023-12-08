# grow-therapy-assignment

## Overview

This is the take home assignment for Grow Therapy.  The minimum requirements were to:

- [x] Create backend web application that exposes an endpoint to return a given Wikipedia article's page views for a given month.
- [x] App containerized with Docker

Extended requirements:

- [x] Add README
- [x] Document API endpoint
- [x] Write tests for the application
- [x] Make it easy for the team to build and run locally
- [x] Utilize best practices for containerization and Docker
- [x] Handle corner cases
- [x] Handle performance, security, and reliability concerns for production

## Run

Works with python3, so make sure it is installed first.  Clone the code repository, install the requirements, and run the server.

Clone repo and change directory.

```
$ git clone git@github.com:raackley/grow-therapy-assignment.git
```

```
$ cd grow-therapy-assignment
```

Setup and use venv

```$ python3 -m venv venv```

```$ source venv/bin/activate```

```$ cd src```

Install python requirements.

```$ python -m pip install -r requirements.txt```

### Run for Development

```$ python main.py```

Connect

```$ curl http://127.0.0.1:5000/monthly_view_count/<article name>/<year NNNN>/<month NN>```

### Run for Production with gunicorn

```$ gunicorn -w 4 -b 0.0.0.0 main:app &```

Connect

```$ curl http://<IP Address>:8000/monthly_view_count/<article name>/<year NNNN>/<month NN>```

## Build and run Docker Image

### Build local

To build a docker image locally, run the following from the root repo directory.

```$ docker build -t grow-therapy-assignment .```

Then run it locally like so.

```$ docker run -p 8000:8000 grow-therapy-assignment```

Connect via localhost.

```$ curl http://<IP Address>:8000/monthly_view_count/<article name>/<year NNNN>/<month NN>```

### Build from CI

This repo builds an image for each Pull Request, and it also builds an image for each merge to the `master` branch.  Each of these are pushed to `raackley/gt-assignment` on [Docker Hub](https://hub.docker.com/repository/docker/raackley/gt-assignment).  Each `master` branch will update the `latest` tag, and each Pull Request will update the tag named `pr-<pr number>` where "pr-number" is your Pull Request number.

For example, if your Pull Request number is `3`, then you can run the latest build of your branch like so.

```$ docker run -p 8000:8000 raackley/gt-assignment:pr-3```

Similarly, if you want to run the latest version of the `master` branch, run the following.

```$ docker run -p 8000:8000 raackley/gt-assignment:latest```

## Deploy to a Kubernetes cluster with Helm

You can easily deploy the latest version of this application using the included Helm chart.  To deploy with Helm, make sure you have Helm 3 installed, and that your kubeconfig is configured for your desired cluster.

To install with default values, you can install it with the following command.

```$ helm -n <namespace> upgrade -i gt-assignment helm/grow-therapy-assignment --create-namespace```

To override any of the variables in the `values.yaml`, you can install/upgrade like the following.  This example enables and configures the Ingress resource.

```$ helm -n gt-assignment upgrade -i gt-assignment helm/grow-therapy-assignment --create-namespace --set ingress.enabled=true,ingress.hosts[0].host=gta.ryanackley.com,ingress.hosts[0].paths[0].path=/,ingress.hosts[0].paths[0].pathType=ImplementationSpecific```

## Running in Production

The app is running in "Production" using the CI build in GitHub, and the Helm chart to deploy to a Kubernetes cluster.  The "production" app can be found at `https://gta.ryanackley.com/`.  It is deployed in a High Availability configuration, with SSL, and behind a CDN with DDoS protection.  It can be used simlarly to the local version, like so.

```$ curl https://gta.ryanackley.com/monthly_view_count/<article name>/<year NNNN>/<month NN>```

## Swagger API Documentation

To view the Swagger API documentation, connect to the `/apidocs` endpoint.

Example for dev: [http://127.0.0.1:5000/apidocs/](http://127.0.0.1:5000/apidocs/)

Production: [https://gta.ryanackley.com/apidocs/](https://gta.ryanackley.com/apidocs/)

## API tests with pytest

There are API tests for the project in `tests/`.  These tests run automatically in GitHub for each Pull Request.  To run them locally, perform the following in your venv as setup above.

From the root directory.

```$ pip install -r tests/requirements.txt```

```$ pytest```
