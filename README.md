# Amazon Nike Shoes Web Scraper

## Description
This project is a Python-based web scraping project that extracts Nike Shoes data from Amazon's multiple pages and processes it with Pandas. 

The top 5 shoes are then selected based on their price, rating, and reviews. Finally, the data is sent as text through the Pushover Notification Service's api. 

## Automation

The Python script runs on AWS Lambda, and a CloudWatch Event Trigger is set up to automate the process to run at 7AM and 7PM every day.

I have created a CloudWatch Event Trigger which invokes the Lambda Function "Nike Scraper". 
The `lambda_handler` is the Handler Method and it's also invoked by AWS Lambda. 

The Cron Expression for the Trigger is `30,30 1,13 * * ? *`

Here's a screenshot of the Function Overview

<img width="694" alt="Screenshot 2023-04-01 at 7 25 48 PM" src="https://user-images.githubusercontent.com/100070155/229293415-1bfd2b6b-4f2a-462b-8d99-d5fff0bbce73.png">




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
