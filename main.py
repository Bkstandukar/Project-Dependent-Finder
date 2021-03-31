import argparse
from API_Dependents import get_token_key, get_test_data
from DependentFinder import DependentFinder
import csv
import time
import pandas as pd
import os

time_str_file = time.strftime("%m-%d-%Y_%H-%M-%S")


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


def get_file_name(file_name, directory_name=None):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    filename = f"{directory_name}\{file_name}_{time_str_file}.csv"
    return filename


if __name__ == "__main__":
    argp = argparse.ArgumentParser(description="Find direct dependents using Web Scraping")
    argp.add_argument('--filename', type=str, default="repos.csv", help='File name eg: repos.csv')
    args = argp.parse_args()
    print("working on getting Dependents")
    repos = read_csv(args.filename)
    url_list = convert_repo_to_url(repos)
    time.sleep(2)
    get_dependent = DependentFinder().multiple_run(url_list)
    # making list of dependents ready for API part
    uniq_df = get_dependent.drop_duplicates()
    print("pulling repo Information dor dependents...")

    dependent_list = [x for x in uniq_df["Dependent"] if x != "No Dependent"]

    data_table = get_test_data(get_token_key(), dependent_list)
    repo_dependencies_df = pd.json_normalize(data_table, max_level=500)
    file_to_save = get_file_name("all_dependents", directory_name="dependent_results")
    try:
        combined_df = repo_dependencies_df.merge(uniq_df, how="right", on="Dependent")
    except KeyError:
        print("There is not Dependent to work")
        uniq_df.to_csv(file_to_save, index=False)
    else:
        col_name = "Repos"
        first_col = combined_df.pop(col_name)
        combined_df.insert(0, col_name, first_col)
        combined_df.to_csv(file_to_save, index=False)

    print(f"file is saved as: {file_to_save}")