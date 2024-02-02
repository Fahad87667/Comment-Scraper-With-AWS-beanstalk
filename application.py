from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
import csv
import os
import pandas as pd

logging.basicConfig(filename="scrapper.log", level=logging.INFO)

import ssl  # bypassing ssl connection
ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(filename="scrapper.log", level=logging.INFO)

application = Flask(__name__)
app = application

@app.route("/", methods=['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            url_client = uReq(flipkart_url)
            flipkartPage = url_client.read()
            url_client.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            product_link = "https://www.flipkart.com" + box.div.div.div.a['href']
            product_req = requests.get(product_link)
            product_req.encoding = 'utf-8'
            prod_html = bs(product_req.text, "html.parser")
            print(prod_html)
            comment_box = prod_html.find_all('div', {'class': "_16PBlm"})

            filename = searchString + ".csv"
            header = ["Product", "Customer Name", "Rating", "Heading", "Comment"]

            df = pd.DataFrame(columns=header)

            reviews = []
            for i in comment_box:
                try:
                    name = i.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                except:
                    logging.info("name")

                try:
                    rating = i.div.div.div.div.text
                except:
                    rating = 'No Rating'
                    logging.info("rating")

                try:
                    commentHead = i.div.div.div.p.text
                except:
                    commentHead = 'No Comment Heading'
                    logging.info(commentHead)

                try:
                    comtag = i.div.div.find_all('div', {'class': ''})
                    custComment = comtag[0].div.text
                except Exception as e:
                    logging.info(e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)

            df = pd.DataFrame(reviews)
            df.to_csv(filename, index=False)

            logging.info("log my final result {}".format(reviews))
            return render_template('result.html', reviews=reviews[0:(len(reviews) - 1)])
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=8501)
