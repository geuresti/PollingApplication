# PollingApplication
This is a polling application that is being submitted to the 2022 IGN Code Foo Internship program. The prompt was to create a real-time polling application so I made a site that lets visitors create accounts in order to create and vote on each other's polls. The real-time component is on the live results page where a pie chart is displayed with the poll answer options as well as a visualization of the vote distribution.

## Tools
- I used Django, a python based web framework, to help make the application. I've worked with Django a few times before so I felt this was the best choice.
- I used AJAX to handle the real-time updates for the pie chart display.
- I used css to decorate the pages.

## Features 
- User authentication System
- User created polls
- Voting system
- Live poll updates

## How to Run
Clone it
`git clone git@github.com......`

Go to the project direction and run the command:
`python manage.py runserver`

Open `http://127.0.0.1:8000/livepoll/` in your web browser (preferably Google Chrome)
