# PollingApplication
This is a polling application that is being submitted to the 2022 IGN Code Foo Internship program. The prompt was to create a real-time polling application so I made a site that lets visitors create accounts in order to create and vote on each other's polls. The real-time component is on the live results page where a pie chart is displayed with the poll answer options as well as a visualization of the vote distribution. I used Django, a python based web framework, to help make the application. I've worked with Django a few times before so I felt this was the best choice.

## Features 
- User authentication System
- User created polls
- Voting system
- Live poll updates

## How to Run
Download python version 3.8.5 or higher

Install the latest version of pip

Open your command line

Clone the repository
`git clone https://github.com/geuresti/PollingApplication.git`

Go to the project directory on your command line and type the command:

`pip install -r requirements.txt` 

then enter the cf22 directory and type:

`python manage.py runserver`

Open `http://127.0.0.1:8000/livepoll/` in your web browser (preferably Google Chrome)

Play around with the website!

To close the server, go to your command line and type ctrl+C

## Testing the Site
I created a couple of dummy accounts, some example polls, as well as an admin account in order to show off some features without requiring you to create and bunch of accounts and polls on your own. For example, if you log on the admin account (username: Gio, password: cfintern22), you can vote on any poll as many times as you want (polls are normally one vote per user). This will allow you to have the polling results in one window while you open up a second window and navigate to the voting page so you can try out the real-time updating pie chart without having to log into a different account to vote on a poll again. 
