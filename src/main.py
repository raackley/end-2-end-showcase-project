from flask import Flask, jsonify
from datetime import date
import requests


def get_monthly_pageview_count(article, year, month):
    try:
        query_start_date = '{0}{1}01'.format(year, month)
        query_end_date = '{0}{1}01'.format(year + 1, month)

        today = date.today()
        # formatted with "01" suffix to make it directly comparable
        today_formatted = today.strftime("%Y%m01")

        # validate user input
        # any string should be allowed as a potential article
        if not isinstance(article, str):
            return "error, article must be a string", 400
        if not isinstance(year, int):
            return "error, year must be an int", 400
        if int(month) < 1 or int(month) > 12:
            return "error, month must be an int between 1 and 12", 400
        if int(query_start_date) > int(today_formatted):
            return "error, queried date is in the future", 400

        # the full json data from wikipedia API
        data = query_wikipedia_api(article, query_start_date, query_end_date)

        # grab the view count for the month supplied
        # which will be the first item in the list
        views = data["items"][0]["views"]
    except Exception as error:
        print("Exception: ", error)
        return "error", 400

    return str(views), 200


def query_wikipedia_api(article, query_start_date, query_end_date):
    base_url = 'https://wikimedia.org/api/rest_v1/'
    api_query = 'metrics/pageviews/per-article/'
    static_options = 'en.wikipedia/all-access/all-agents/'
    user_options = '{0}/monthly/{1}/{2}'.format(article, query_start_date,
                                                query_end_date)

    # api-endpoint
    full_url = base_url + api_query + static_options + user_options

    # must set a user agent - https://meta.wikimedia.org/wiki/User-Agent_policy
    headers = {'User-Agent': 'GTAssignment/1.0'}

    # sending get request and saving the response as response object
    r = requests.get(full_url, headers=headers)

    return r.json()


# initialize our Flask application
app = Flask(__name__)


@app.route("/monthly_view_count/<string:article>/<int:year>/<int:month>",
           methods=["GET"])
def monthly_view_count(article, year, month):
    result, http_code = get_monthly_pageview_count(article, year,
                                                   str(month).zfill(2))
    return jsonify(result), http_code


@app.route("/health", methods=["GET"])
def health():
    return jsonify("healthy")


#  main thread of execution to start the server
if __name__ == '__main__':
    app.run()
