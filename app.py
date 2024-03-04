import streamlit as st
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pandas as pd
import logging
import ssl
from urllib.parse import quote  # Import the quote function for URL encoding

# Bypass SSL connection
ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(filename="scrapper.log", level=logging.INFO)

@st.cache_data(ttl=600)  # Set the time-to-live (ttl) to 600 seconds (10 minutes)
def scrape_data(search_string):
    try:
        # URL encode the search string
        encoded_search_string = quote(search_string)
        flipkart_url = f"https://www.flipkart.com/search?q={encoded_search_string}"
        
        url_client = uReq(flipkart_url)
        flipkart_page = url_client.read()
        url_client.close()
        flipkart_html = bs(flipkart_page, "html.parser")
        bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
        del bigboxes[0:3]
        box = bigboxes[0]
        product_link = "https://www.flipkart.com" + box.div.div.div.a['href']
        product_req = requests.get(product_link)
        product_req.encoding = 'utf-8'
        prod_html = bs(product_req.text, "html.parser")
        comment_box = prod_html.find_all('div', {'class': "_16PBlm"})

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
                comment_head = i.div.div.div.p.text
            except:
                comment_head = 'No Comment Heading'
                logging.info(comment_head)

            try:
                com_tag = i.div.div.find_all('div', {'class': ''})
                cust_comment = com_tag[0].div.text
            except Exception as e:
                logging.info(e)

            my_dict = {"Product": search_string, "Name": name, "Rating": rating, "CommentHead": comment_head,
                      "Comment": cust_comment}
            reviews.append(my_dict)

        return reviews
    except Exception as e:
        logging.error(f"Error during scraping: {e}")
        return []

def main():
    st.title("Flipkart Review Scraper")

    search_string = st.text_input("Enter the product name:")
    if st.button("Scrape Reviews"):
        if search_string:
            reviews = scrape_data(search_string)
            if reviews:
                st.write(pd.DataFrame(reviews))
            else:
                st.warning("No reviews found or an error occurred during scraping.")
        else:
            st.warning("Please enter a product name.")

if __name__ == "__main__":
    main()
=======
import streamlit as st
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pandas as pd
import logging
import ssl
from urllib.parse import quote  # Import the quote function for URL encoding

# Bypass SSL connection
ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(filename="scrapper.log", level=logging.INFO)

@st.cache_data(ttl=600)  # Set the time-to-live (ttl) to 600 seconds (10 minutes)
def scrape_data(search_string):
    try:
        # URL encode the search string
        encoded_search_string = quote(search_string)
        flipkart_url = f"https://www.flipkart.com/search?q={encoded_search_string}"
        
        url_client = uReq(flipkart_url)
        flipkart_page = url_client.read()
        url_client.close()
        flipkart_html = bs(flipkart_page, "html.parser")
        bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
        del bigboxes[0:3]
        box = bigboxes[0]
        product_link = "https://www.flipkart.com" + box.div.div.div.a['href']
        product_req = requests.get(product_link)
        product_req.encoding = 'utf-8'
        prod_html = bs(product_req.text, "html.parser")
        comment_box = prod_html.find_all('div', {'class': "_16PBlm"})

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
                comment_head = i.div.div.div.p.text
            except:
                comment_head = 'No Comment Heading'
                logging.info(comment_head)

            try:
                com_tag = i.div.div.find_all('div', {'class': ''})
                cust_comment = com_tag[0].div.text
            except Exception as e:
                logging.info(e)

            my_dict = {"Product": search_string, "Name": name, "Rating": rating, "CommentHead": comment_head,
                      "Comment": cust_comment}
            reviews.append(my_dict)

        return reviews
    except Exception as e:
        logging.error(f"Error during scraping: {e}")
        return []

def main():
    st.title("Flipkart Review Scraper")

    search_string = st.text_input("Enter the product name:")
    if st.button("Scrape Reviews"):
        if search_string:
            reviews = scrape_data(search_string)
            if reviews:
                st.write(pd.DataFrame(reviews))
            else:
                st.warning("No reviews found or an error occurred during scraping.")
        else:
            st.warning("Please enter a product name.")

if __name__ == "__main__":
    main()
>>>>>>> 6f1c7462dd3f0c18270d80f5bf8d4674b26f286a
