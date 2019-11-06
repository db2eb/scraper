from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as ureq

myurl = "https://www.tripadvisor.com/Hotel_Review-g55197-d105191-Reviews-or5-Rodeway_Inn_Memphis_American_Way-Memphis_Tennessee.html#REVIEWS"
uClient = ureq(myurl)
html = uClient.read()
#uClient.close() #dont close

#html parsing
pagesoup = soup(html, "html.parser")

# get reviews from here
review = pagesoup.findAll("div",{"class":"hotels-community-tab-common-Card__card--ihfZB hotels-community-tab-common-Card__section--4r93H"})


titleandlink = review[0].findAll("div",{"class":"hotels-review-list-parts-ReviewTitle__reviewTitle--2Fauz"})

# 1 show user review link. link to the review in its own page
reviewLink = titleandlink[0].a['href'] 
newlink = "https://www.tripadvisor.com"+reviewLink
# 2 name of hotel
locName = pagesoup.h1.text
# 3 part after the slash, from the given excel
parsedUrl = myurl[27:] # TODO remove 'https://www.tripadvisor.com'
# 4, title of review
reviewTitle = titleandlink[0].a.text


# 8, overall rating???
# rtemp = review[0].findAll("div",{"class":"hotels-review-list-parts-RatingLine__bubbles--1oCI4"})
# rating = rtemp[0].span['class'][1][7]
rtemp = review[0].findAll("div",{"class":"hotels-review-list-parts-RatingLine__bubbles--1oCI4"})[0].span['class'][1][7]
# bubble_10 1 stars, bubble_20 2 stars, bubble_30 3 stars, bubble_40 4 stars, bubble_50 5 stars

uClient2 = ureq(newlink)
html2 = uClient2.read()
uClient.close()

#html parsing
pagesoup2 = soup(html2, "html.parser")
review2 = pagesoup2.findAll("div",{"class":"featured-review-container"})

# 5, username of review
username = review2[0].findAll("div",{"class":"info_text"})[0].div.text
# username = review[0].findAll("div",{"class":"social-member-event-MemberEventOnObjectBlock__event_type--3njyv"})
# username[0].text # this one doesnt parse

# 6, date of review, might have to get from the reviewer link
date = review2[0].findAll("span",{"class":"ratingDate"})[0]['title']

# 7, review itself, get from reviewer link
fullReview = review2[0].findAll("span",{"class":"fullText"})[0].text


# 9, reviews of other things, from reviewerlink
moreratings = review2[0].findAll("ul",{"class":"recommend"})[0]
minireviews = moreratings.findAll("li",{"class":"recommend-answer"})
finalans = ""
for minireview in minireviews:
	category = minireview.findAll("div",{"class":"recommend-description"})[0].text #name of category
	minirating = minireview.div["class"][1][7] #rating
	if(len(finalans)>0):
		finalans+="$$$$"+category+"||||"+minirating
	else:
		finalans+=category+"||||"+minirating
# Rooms||||5$$$$Cleanliness||||5$$$$Service||||5

print(newlink,locName,parsedUrl,reviewTitle,username,date,fullReview,rtemp,finalans)


#NOTes
#clean .text with .strip()





