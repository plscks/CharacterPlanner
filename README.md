# Nexus Clash Breath 5 Character Planner
Nexus Clash Breath 5 (2021) has many changes, lots of them mechanical in nature. And the legacy 
Nexus Clash Character Planner has become outdated throughout the years, being built on the planner that
was in use during Nexus War. This project attempts to completely rewrite the Planner.

I decided to write it in a language that I love and that I love to learn, Python 3. I decided to use Flask as the framework for it
mostly because I thought it would be fun to learn how Flask works, it was, and it continues to be.

The project however did not start with a web app in mind, instead it started with the [Character](https://repo.plscks.net/plscks/flaskNCPlanner/src/branch/main/testappPI/models/character.py) class which was followed by the [Skills](https://repo.plscks.net/plscks/flaskNCPlanner/src/branch/main/testappPI/models/skills.py) class.
These two classes were in themselves my adventure into writing a class, it has been a fun road so far!

Local Development Setup
---
So that it is recorded somewhere in case I need to reformat my SSD or something like that, here is a step-by-step guide to
getting at a minimum, a development environment set up for this project on Windows from scratch.

1. Download, install, and open [VSCode](https://code.visualstudio.com)
2. On the left click the `Source Control` icon, in the panel click where `install git` is highlighted
3. Download and install [git](https://git-scm.com) with all default settings
4. Restart VSCode
5. Press the explorer icon on the left (the top one)
6. Click `clone repository`
7. Paste the repository link in there and hit enter: `https://repo.plscks.net/plscks/flaskNCPlanner.git`
8. Find a good location to save the project (it will save it into a folder in the location you choose)
9. Click `Open Folder` or `File->Open Folder`
10. Choose the `flaskNCPlanner` folder in the location you saved it
11. Trust the authors (me)
12. Click the `Run and Debug` button on the left
13. Select `Python: Flask` from the dropdown at the top and then click the green arrow next to the dropdown menu (Start Debugging)
14. Python will not be recognized so click `Install python extension` which will bring the extension up
15. Click `Install`
16. It will attempt to install but not find Python and prompt you to install it
17. Click `Install Python` which will open the Microsoft Store, install it with the `Get` button
18. Head to the [VSCode flask tutorial](http:/code.visualstudio.com/docs/python/tutorial-flask) and read over the first part if you'd like, or skip down to `Create a project environment for the Flask Tutorial` we will follow this
19. In VSCode, click `Terminal->New Terminal` in the top menu bar
20. First be sure python is available, type `python` and press enter to load python's interactive interpreter. If there is an error try restarting your computer and trying again
21. Once into the python shell it should tell you that you are running python 3.9+ and give you a prompt, type `quit()` to exit for now
22. Back in terminal type `python -m venv env` and press enter, it will create a virtual environment for running our project
23. VSCode will pick up on this and ask if you want to add it to the workspace, click `Yes`
24. Back in the Flask tutorial setup proceed with step 4, open the command palette and begin to type `python: Select Interpreter` Click it, and then select the recommended one ('env': venv)
25. In the VSCode bottom bar where the terminal is, in the right sidebar click the little trash can icon by any terminals that are open, this will close them all
26. Next, in windows, click the search bar and search for `Powershell` either choose `Run as Administrator` or right click the icon and choose it from there
27. Once powershell is loaded, type `Set-ExecutionPolicy Unrestricted` and hit enter, this will allow us to enter into the python virtual environment we made earlier
28. Type `A` for Yes to All and hit enter, close powershell
29. Back in VSCode open a new terminal from the top menu bar `Terminal->New Terminal`
30. The terminal should open and load you into the virtual environment, noted by the `(env) PS C:\...` prompt
31. Type `python -m pip install -r requirements.txt` to install the required python modules
32. Next we need to install redis, head over  [here](https://github.com/microsoftarchive/redis/releases/tag/win-3.0.504)
33. Click on `Redis-x64-3.0.504.msi` to download it
34. Install it with the default settings
35. Next obtain the `.cfg` file from me and toss it into the main flaskNCPlanner folder. This is how we will pass secret keys to flask
36. Now open .cfg in VSCode by going back to our project and clicking the Explorer icon on the left, then click on `.cfg` which you copied into the folder last step
37. Be sure line 4 is `SESSION_REDIS=redis://127.0.0.1:6379` if it is not
37b. If you are on *nix operating system please consider [securing redis with a password](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04#step-4-%E2%80%94-configuring-a-redis-password) and by other means such as binding it specifically to localhost and forbidding outside access.
38. Now on the left, click the `Run and Debug` icon and then the green arrow (Start Debugging) at the top
39. Your terminal should open and load some things up before stalling at `* Running on http://127.0.0.1:5000/`
40. Go there (http://127.0.0.1:5000/) in the browser of your choice to load the page up
41. Click Planner at the right of the top menu bar to load the planner up (http://127.0.0.1:5000/planner)
42. Back in VSCode click the `Stop` button on the debugger overlay at the top middle of the screen to shut the debugging server down

How it Works
---
- [wsgi.py](wsgi.py) creates our app by calling create_app() from [__init__.py](testappPI/__init__.py) in the testappPI module
- create_app() sets up our Flask application first by pulling in our config settings from [config.py](config.py), things like out redis details, and SQlite database link
- create_app also pulls in other important things like our static files folder, routes, models, and services
- Once this is in motion our application should be online and ready for visitors
- When a user heaeds to the main planner(site/planner/), things kicks off by going through [routes.py](testappPI/routes.py#L69), executing at line 69
- Here we pick up some default values which will be our users selected classes, for now we set them to 'none'
- Our first order of business is to check if we have the character "dude" stored in our session data already and to check if the user has delibrately reset the dude
- If there is no "dude" or reset was triggered then we create a new Character object from the [Character class](testappPI/models/character.py)
- The Character class is the object this is our character that is being built, it holds all the information we care to see along with the functions that govern those things
   - All of our characters base stats
   - All possible class choices
   - Level up function
   - Skill buying functions
   - Skill removal functions
   - Class selection function
   - And lastly, a list of skills which is in fact a list of Skill objects as created from the [Skills class](testappPI/models/skills.py)
- Before the route is complete it pulls a master list of skill objects from the [SkillAttrib class](testappPI/services/skillDisplay.py) for the classes that have been chosen for the "dude" object
- Once our route runs it returns the [planner.html template](testappPI/templates/planner.html) with our "dude" object and our skill lists for the selected class_2 and class_3 of the "dude" object
- The planner template is the basis for our display, it is a jinja template that runs through all the information we gave it and displays it
- From here the user interacts with the page by clicking options which run different routes via AJAX requests which are defined in [planner.js](testappPI/static/js/planner.js)
- planner.js has a few JavaScript functions set up for updating our display and a couple event listeners that watch for the user's clicks on elements
- For instance when the user clicks on "Level Up" button we execute an AJAX request which runs our /levelup route which in turn runs the levelup() function of our "dude" object
- We then return our freshly leveled up "dude" object to the page as json data and run the JavaScript functions to update the page with our new information
- When the user clicks a checkbox to "purchase" a skill, a similar process happens which will run our /buyskill or /sellskill route
- Each skill that the user buys will add that skill as a [Skills class](testappPI/models/skills.py) object to the skills list in our "dude" object
   - The skills object holds all the data associated with that particular skill in regards to any stats that the particular skill affects
   - When a skill object is added to our "dude" the skill object is processed and any changes defined get executed on the attributes of our "dude"
- If the user chooses to reset, our "dude" object is removed and a fresh one is put in its place