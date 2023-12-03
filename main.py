from flask import Flask

# initialize our Flask application
app = Flask(__name__)

@app.route("/monthly_view_count/<string:article>/<int:year>/<int:month>", methods=["GET"])
def monthly_view_count(article, year, month):
    return 'Article: {0}\nYear: {1}\nMonth {2}\n'.format(article, year, month)

#  main thread of execution to start the server
if __name__ == '__main__':
    app.run()
