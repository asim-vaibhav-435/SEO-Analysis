from bs4 import BeautifulSoup
import requests
import nltk
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')

def seo_analysis(soup):

    # create lists to store values
    bad = []
    good = []
    keywords = []

    # Grab the title
    title = soup.find('title').text
    if title:
        good.append(f"Title Exists: {title}")
    else:
        bad.append("No Title!")

    # grab the Meta description
    meta_d = soup.find("meta", attrs={"name":"description"})['content']
    if meta_d:
        good.append(f"Meta Description Exists: {meta_d}")
    else:
        bad.append("No Meta Description!")

    # grab the headings
    hs = ["h1","h2","h3"]
    h_tags = []
    for h in soup.find_all(hs):
        good.append(f"{h.name}-->{h.text.strip()}")
        h_tags.append(h.name)

    if "h1" not in h_tags:
        bad.append("No H1 found!")

    # grab the Images without Alt

    for i in soup.find_all('img',alt=''):
        bad.append(f"No Alt: {i}")

    # grab the keywords
    body = soup.find('body').text

    words = [i.lower() for i in word_tokenize(body)]

    sw = nltk.corpus.stopwords.words('english')

    new_words = []

    for i in words:
        if i not in sw and i.isalpha():
            new_words.append(i)

    freq = nltk.FreqDist(new_words)

    # Display Reslult
    print("Keywods:")
    print(freq.most_common(10))
    print("\nThe Good:")
    print(good)
    print("\nThe Bad: ")
    print(bad)

def main():

    url = "https://pythonology.eu/what-is-syntax-in-programming-and-linguistics/"

    # send requstse to get the url content 
    res = requests.get(url).text

    # parse the HTML of the url content using Beautifulsoup
    soup = BeautifulSoup(res, 'html.parser')

    seo_analysis(soup)

if __name__=="__main__":
    main()