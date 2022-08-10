STOCK = "TSLA"
COMPANY_NAME = "Tesla"
AV_API_KEY="GHPCDJZOHPRKN8F0"
NEWS_API_KEY="54cdab37123a4c468d35264969772b1d"
TWILIO_SID="AC3daf1c86599283ef1fee08b3ce87a525"
TWILIO_AUTH="d238060029fa99686d15234d72d09b2e"
TWILIO_NUM="+19065694801"
MAX_CHANGE=5
import requests
import itertools
from twilio.rest import Client

parameters_av={
	"function":"TIME_SERIES_DAILY",
	"symbol":STOCK,
	"apikey":AV_API_KEY
}
av_response=requests.get(url="https://www.alphavantage.co/query",params=parameters_av)
av_data=av_response.json()
req_av_data=av_data["Time Series (Daily)"]
fin_av_data=list(itertools.islice(req_av_data.items(),2))
av_close_y=float(fin_av_data[0][1].get("4. close"))
av_close_dby=float(fin_av_data[1][1].get("4. close"))
perc_change_av=round((av_close_y-av_close_dby)/(av_close_dby)*100,2)
print(perc_change_av)														#PERCENTAGE CHANGE

if perc_change_av>=MAX_CHANGE or perc_change_av<=-1*MAX_CHANGE:
	news_response=requests.get(f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from=2022-08-10&sortBy=popularity&apiKey=54cdab37123a4c468d35264969772b1d")
	news_all=news_response.json().get('articles')
	dict_news={}
	dict_news[news_all[0].get("title")]=news_all[0].get("description")				##Got three top news articles
	dict_news[news_all[1].get("title")]=news_all[1].get("description")
	dict_news[news_all[2].get("title")]=news_all[2].get("description")

	client = Client(TWILIO_SID, TWILIO_AUTH)
	temp=""
	if perc_change_av>=MAX_CHANGE:
		temp="🔺"
	else:
		temp="🔻"
	for i in dict_news:
		message = client.messages \
          	      .create(
            	         body=f"{STOCK}: {temp}{perc_change_av}%\nHeadline: {i}\nBrief: {dict_news[i]}",
            	         from_=TWILIO_NUM,
            	         to='+916238766496'
            	     )

		print(message.status)

