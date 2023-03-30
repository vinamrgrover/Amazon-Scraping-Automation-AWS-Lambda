# Amazon Nike Shoes Web Scraper

## Description
This is a personal portfolio project that showcases my skills in web scraping and data processing using Python. This project scrapes Nike Shoes products from Amazon's multiple pages, processes the data using pandas, selects the top 5 shoes by price, rating, and reviews, and sends the data as a text message through the Pushover Notification Service. The process is automated to run at 7AM and 7PM every day on replit.com.

## Automation
Added the schedule.yaml to the root folder of repl. This would automate the process to run the script on 7AM and 7PM everyday. The cron syntax is as follows:
`0 7,19 * * *`

## Notification

The script uses Pushover Notification Service to send the top 5 shoes information as a text message to my mobile device. This is done by utilizing the Pushover API. 

The notification includes the following information for each of the top 5 shoes:

+ Product Name
+ Price
+ Rating
+ Number of Reviews

Here is a screenshot of the notification:

<img width="808" alt="Screenshot 2023-03-31 at 12 18 42 AM" src="https://user-images.githubusercontent.com/100070155/228935144-bd4bfb04-f606-498e-a237-e5716554204a.png">



I find this feature very useful as it allows me to quickly check the top 5 shoes from Amazon without having to manually search for them.
