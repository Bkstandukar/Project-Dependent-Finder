import argparse
from DependentFinder import DependentFinder
import csv
import time


def read_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        # convert nested loop to single array
        repo_list_from_csv = [item for sublist in reader for item in sublist]
    return repo_list_from_csv


def convert_repo_to_url(repo_list):
    # repo argument is converted to github url
    new_url_list = [f"https://github.com/{x}/network/dependents" for x in repo_list]
    return new_url_list


if __name__ == "__main__":
    argp = argparse.ArgumentParser(description="Find direct dependents using Web Scraping")
    argp.add_argument('--filename', type=str, default="repos.csv", help='File name eg: repos.csv')
    args = argp.parse_args()
    print("working on getting Dependents")
    repos = read_csv(args.filename)
    url_list = convert_repo_to_url(repos)
    time.sleep(2)
    DependentFinder().multiple_run(url_list)


