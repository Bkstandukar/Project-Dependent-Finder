# **Project-Dependent-Finder**
This project finds all the direct dependents of a GitHub repository using Web Scraping method and exports the list along with its information to a csv file.
Web scraping is done with help of BeautifulSoup4 library and the repository information is extracted from GitHub Graph API.
The code can be run iteratively if you wish to find transitive dependents too. Just re-run the code with extracted list of dependents. Unfortunately, you have to do it manually.



# **How to run:**

Edit the repos.csv file and add the name of repository you want to search dependent for. You can add one or more than one repository in the csv file. 
Make sure you put one repository per line. The repository should be in the format: repo_owner/repo_name. For example: facebook/react

Then, run the project with:

python main.py

or if you want to run your own csv file, then run the project with:

python main.py --filename yourcsvfile.csv

But make sure that the csv file is in the same folder as this project.

The output file will be saved in dependent_results folder within the project folder. 
