from bs4 import BeautifulSoup
import requests
import time
import concurrent.futures
import pandas as pd


page_num = 1


class DependentFinder:
    url_list = {}
    dup_checker = []
    repo_list_dict = []
    new_data_frame = pd.DataFrame()

    def __init__(self):
        print("working on request")

    def multiple_run(self, list_urls):
        '''
        will return the success of the process on each url.
        file will be updated once each process is completed.
        '''
        new_data_frame = pd.DataFrame()
        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(self.dependent_finder, url): url for url in list_urls}

            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                else:
                    print("Success")
                    repo_df = pd.DataFrame(DependentFinder.repo_list_dict)
                    new_data_frame = new_data_frame.append(repo_df)
                    uniq_df = new_data_frame.drop_duplicates()
                    uniq_df.to_csv("dependents.csv", index=False)
        return DependentFinder.repo_list_dict

    def dependent_finder(self, dep_url):
        '''
        will append to global variable. This function will not return anything.
        look for DependentFinder.repo_list_dict.
        '''
        group_repo = dep_url.split("/")
        dep_repo = f"{group_repo[3]}/{group_repo[4]}"
        print(dep_repo)

        print(f"working on {dep_url}")
        global page_num
        print(f"page number: {page_num}")
        print("GET " + dep_url)
        fail_count = 1

        while True:
            try:
                r = requests.get(dep_url)
                r.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
                DependentFinder.dup_checker.append(dep_repo)
                dict_info = {
                    "Repos": dep_repo,
                    "Dependent": err
                }
                DependentFinder.repo_list_dict.append(dict_info)
                break
            else:
                soup = BeautifulSoup(r.content, "html.parser")
                repo_count = '/{}/network/dependents?dependent_type=REPOSITORY'.format(dep_repo)

                repo_list = ["{}".format(
                    t.find('a', {"href": str(repo_count)}).text
                )
                    for t in soup.findAll("div", {"class": "table-list-header-toggle"})]

                # convert list to string and remove space
                repo_checker = " ".join(''.join(map(str, repo_list)).split())
                # check for repo count
                if "0 Repositories" in repo_checker:

                    print(f"Could not find Dependent for: {dep_repo}")
                    break
                else:
                    print("Scrapping Data *****")
                    data = [
                        "{}/{}".format(
                            t.find('a', {"data-repository-hovercards-enabled": ""}).text,
                            t.find('a', {"data-hovercard-type": "repository"}).text
                        )
                        for t in soup.findAll("div", {"class": "Box-row"})
                    ]

                    # this is to give some time delay for server to retrieve data
                    if len(data) < 1:
                        print(f"Retrying in: {fail_count} seconds")
                        time.sleep(fail_count)
                        fail_count += 1
                    else:
                        # create a single list of Dependents
                        for x in data:
                            # avoid circular dependents
                            if dep_repo != x:

                                DependentFinder.repo_list_dict.append({
                                    "Repos": dep_repo,
                                    "Dependent": x
                                })

                pagination_finder = soup.find("div", {"class": "paginate-container"}).find_all('a')

                if len(pagination_finder) > 1:
                    pagination_finder = pagination_finder[1]
                elif not pagination_finder:
                    break
                else:
                    pagination_finder = pagination_finder[0]

                url = pagination_finder["href"]

                if "dependents_before" in url:
                    break

                else:
                    page_num += 1
                    self.dependent_finder(url)
                break
