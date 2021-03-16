# Project-Dependent-Finder
This project lists all the direct dependents of a GitHub repository using Web Scraper and exports the list to a csv file.

Edit the repos.csv file and add the name of repository you want to search dependent for. You can add one or more than one repository in the csv file. 
Make sure you put one repository per line. The repository should be in the format: repo_owner/repo_name. For example: facebook/react

Then, run the project with:

python main.py

or if you want to run your own csv file, then run the project with:

python main.py --filename yourcsvfile.csv

But make sure that the csv file is in the same folder as this project.
