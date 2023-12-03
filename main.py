from flask import Flask
import requests

def get_monthly_pageview_count(article, year, month):
    start_date = '{0}{1}01'.format(year, month)
    end_date = '{0}{1}01'.format(year + 1, month)

    # the full json data from wikipedia API
    data = query_wikipedia_api(article, start_date, end_date)

    # grab the view count for the month supplied, which will be the first item in the list
    views = data["items"][0]["views"]

    return str(views)

def query_wikipedia_api(article, start_date, end_date):
    # api-endpoint
    wikipedia_url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{0}/monthly/{1}/{2}'.format(article, start_date, end_date)

    # we must set a user agent - https://meta.wikimedia.org/wiki/User-Agent_policy
    headers = {'User-Agent': 'GTAssignment/1.0'}

    # sending get request and saving the response as response object
    r = requests.get(wikipedia_url, headers=headers)

    return r.json()

# initialize our Flask application
app = Flask(__name__)

@app.route("/monthly_view_count/<string:article>/<int:year>/<int:month>", methods=["GET"])
def monthly_view_count(article, year, month):
    return get_monthly_pageview_count(article, year, str(month).zfill(2))

#  main thread of execution to start the server
if __name__ == '__main__':
    app.run()
