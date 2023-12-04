# grow-therapy-assignment

## Run

Works with python3, so make sure it is installed first.  Clone the code repository, install the requirements, and run the server.

Clone repo and change directory.

`$ git clone git@github.com:raackley/grow-therapy-assignment.git`

`$ cd grow-therapy-assignment`

Setup and use venv

`$ python3 -m venv venv`

`$ source venv/bin/activate`

`$ cd src`

Install python requirements.

`$ python -m pip install -r requirements.txt`

### Run for Development

`$ python main.py`

Connect

`$ curl http://127.0.0.1:5000/monthly_view_count/<article name>/<year NNNN>/<month NN>`

### Run for Production with gunicorn

`$ gunicorn -w 4 -b 0.0.0.0 main:app &`

Connect

`curl http://<IP Address>:8000/monthly_view_count/<article name>/<year NNNN>/<month NN>`
