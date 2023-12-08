# grow-therapy-assignment

## Assignment

This is the take home assignment for Grow Therapy, for Ryan Ackley.  The minimum requirements were to:

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

Above and beyond:

- [x] Add CI/CD tests and container builds for GitHub Pull Requests
- [x] Build images from Pull Request branches and `master` branch commits to Docker Hub
- [x] Include Helm chart for easy Kubernetes deployments
- [x] Use and enforce Python style standards with the `flake8` tool
- [x] Actually run it "in production" on Kubernetes with High Availability, SSL, CDN, DDoS protection on a domain!

The following sections will document this application generally, but also point out specifically how it meets all the given requirements.

## Overview

This project contains a Python Flask web application.  It exposes 3 endpoints.

The first endpoint that is exposed is `/monthly_view_count/` which will return the page view count of a given Wikipedia article for a given month.  It takes 3 parameters, first is the article name, second is the year, and the third is the month in digit format (e.g. using 02 for February).  The parameters are supplied as part of the path in this format `/monthly_view_count/<article name>/<year NNNN>/<month NN>`.  This meets the primary goal of the assignment.

The second endpoint is `/health`.  This is a basic healthcheck that just returns http 200 and "healthy".  This can be used as part of a deployment to a Kubernetes cluster as a liveness or readiness probe.  Included in this project is a Helm chart that does make use of the endpoint in this way.  This enables high availability (production concern) by providing a mechanism for a Pod to fail in a cluster, in which Kubernetes would automatically reschedule a new replacement Pod.  That combined with running at least 2 replicas on the cluster will ensure that there is zero downtime in the even of a Pod failure, a node failure, or even a regular deploy of new code.

The third endpoint is `/apidocs`.  This endpoint exposes the API documentation with Swagger.  This meets the requirement of documenting the endpoint.

## Run Locally

The app requires python3, so make sure it is installed first.  Clone the code repository, install the requirements, and run the server.  Running in this way is the easiest and the faster for a developer to iterate on code changes, which meets the requirement for easy build and running for the team.

Clone repo and change directory.

```
git clone git@github.com:raackley/grow-therapy-assignment.git
```

```
cd grow-therapy-assignment
```

Setup and use venv

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Install python requirements.

```
pip install -r src/requirements.txt
```

### Run for Development

```
python src/main.py
```

Connect

```
curl http://127.0.0.1:5000/monthly_view_count/<article name>/<year NNNN>/<month NN>
```

### Run production-like with gunicorn

For running locally in a more production-like way, use gunicorn like so.

```
gunicorn -w 4 -b 0.0.0.0 main:app &
```

Connect

```
curl http://127.0.0.1:8000/monthly_view_count/<article name>/<year NNNN>/<month NN>
```

## Build and run Docker Image

### Build local

The project includes a Dockerfile to build an image and then to run a container with Docker, meeting the containerization requirement.  The Dockerfile copies the minimum amount of files to the image to be able to function.  For example, the tests, Helm, Readme and other files that would be unnecessary to include in the image are not included, just the source files and the requirements file are copied.  The base image is also using an appropriately slimmed image for the purpose, which is the official `python` image with the up to date and automatically patched `3.12` tag.  This addresses some Docker best practices, as well as some performance and security concerns as well.

To build and run a Docker image locally, run the following from the root repo directory.

```
docker build -t grow-therapy-assignment .
```

Then run it locally like so.

```
docker run -p 8000:8000 grow-therapy-assignment
```

Connect via localhost.

```
curl http://127.0.0.1:8000/monthly_view_count/<article name>/<year NNNN>/<month NN>
```

### Build from CI

This repo builds an image for each Pull Request, and it also builds an image for each merge to the `master` branch.  Each of these are pushed to `raackley/gt-assignment` on [Docker Hub](https://hub.docker.com/repository/docker/raackley/gt-assignment).  Each `master` branch will update the `latest` tag, and each Pull Request will update the tag named `pr-<pr number>` where "pr-number" is your Pull Request number.

For example, if your Pull Request number is `3`, then you can run the latest build of your branch like so.

```
docker run -p 8000:8000 raackley/gt-assignment:pr-3
```

Similarly, if you want to run the latest version of the `master` branch, run the following.

```
docker run -p 8000:8000 raackley/gt-assignment:latest
```

## Deploy to a Kubernetes cluster with Helm

You can easily deploy the latest version of this application using the included Helm chart.  To deploy with Helm, make sure you have Helm 3 installed, and that your kubeconfig is configured for your desired cluster.

To install with default values, you can install it with the following command.

```
helm -n <namespace> upgrade -i gt-assignment helm/grow-therapy-assignment --create-namespace
```

To override any of the variables in the `values.yaml`, you can install/upgrade like the following.  This example enables and configures the Ingress resource.

```
helm -n gt-assignment upgrade -i gt-assignment helm/grow-therapy-assignment --create-namespace --set ingress.enabled=true,ingress.hosts[0].host=gta.ryanackley.com,ingress.hosts[0].paths[0].path=/,ingress.hosts[0].paths[0].pathType=ImplementationSpecific
```

## Running in Production

The app is running in "Production" using the CI build in GitHub, and the Helm chart to deploy to a Kubernetes cluster.  The "production" app can be found at `https://gta.ryanackley.com/`.  It is deployed in a High Availability configuration, with SSL, and behind a CDN with DDoS protection.  These features address some of the concerns around preformance, security, and reliability in the requirements.  It can be used simlarly to the local version, like so.

```
curl https://gta.ryanackley.com/monthly_view_count/<article name>/<year NNNN>/<month NN>
```

## Swagger API Documentation

The API is documented with Swagger.  To view the Swagger API documentation, connect to the `/apidocs` endpoint.

Example for dev: [http://127.0.0.1:5000/apidocs/](http://127.0.0.1:5000/apidocs/)

Production: [https://gta.ryanackley.com/apidocs/](https://gta.ryanackley.com/apidocs/)

## API tests with pytest

There are API tests for the project in `tests/`, meeting the testing requirement.  The tests test some normal use cases, and test many corner cases and invalid requests as well, meeting that requirement.  These tests run automatically in GitHub for each Pull Request.  To run them locally, perform the following in your venv as setup above.

From the root directory.

```
pip install -r tests/requirements.txt
```

```
pytest
```

## CI/CD and GitHub Pull Requests

For each Pull Request on GitHub, you get 3 checks using GitHub Actions.

1)  Flake8 Python style check test.  This will fail if your branch's code fails the style enforcement test.
2)  The `pytest` tests are run.  This will fail if your branch's code fails any of the API tests.
3)  A Docker image is built and uploaded to Docker Hub.  The tag used for the image sent to Docker Hub will be `pr-<your PR number`.  This will fail if the Dockerfile fails to build, or if the image can't be sent to Docker Hub.

If any of those checks fails, your Pull Request will not allow you to merge it.  In that case, fix whatever problem has been caught, and push a new commit until all checks pass.

For each commit and merge to the `master` branch, the following happens.

1)  A Docker image is built and uploaded to Docker Hub.  The tag used for the image sent to Docker Hub will be `latest`.  This means that the `latest` tag is always the latest image build specifically from the `master` branch, no other branch builds will override this one.
