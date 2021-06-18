# BBSim
---
BBSim is a simulator of the TV show Big Brother. In this show, there are 14-16 contestants that live in a house, and week by week, 1 by 1, someone is voted out of the house. During this process, a large amount of strategy, relationship building, and manipulation is involved. The purpose of this application is to replicate that behavior as closely as possible.

# Technologies Used
---
* Backend: Django, Postgres, Python
* Frontend: React

# How to Use
---
BBSim is hosted on Heroku at https://bigbrothersim.herokuapp.com/, but can also be run locally by following the steps below
 
1. [Clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository)
2. Setup the frontend
    * Make sure you have the latest version of node installed
    * Run `$ cd client` to switch to the frontend directory and run `$ npm install` to install the required packages
    * Once finished, run `npm start` to start the development server
3. Setup the backend
    * Make sure you have the latest version of Django installed
    * Install from the Pipfile using `$ pipenv install`
    * Activate the environment using `$pipenv shell`
    * Start the backend server using `$python manage.py runserver`
4. With both of these servers running, you should be able to access the application in your browser at `http://localhost:3000/`
