from query_data import query_string
import requests
import time
import json

parent_flag = True

level = []  # to count depth
data_table = []  # save output
time_str_file = time.strftime("%m-%d-%Y_%H-%M-%S")
seen = []


def get_token_key():
    # read token from cred.json file
    with open("cred.json", "r") as cred:
        token_json = json.load(cred)
        token_map = token_json["token_key"]
        return token_map


def get_test_data(token, dependency):
    for single_dependency in dependency:
        print(f"getting info for repo --> {single_dependency}")
        repo_splitter = single_dependency.split('/')
        repo_owner = repo_splitter[0]
        repo_name = repo_splitter[1]
        data = query_string(f"{repo_owner}", f"{repo_name}")
        url = "https://api.github.com/graphql"
        headers = {
            "Authorization": f"Bearer {token}",  # github personal token for authentication
        }

        get_info = requests.post(url=url, json={'query': data}, headers=headers, verify=True)

        if get_info.status_code == 200:
            query_result = get_info.json()
            # error after successful HTTP response
            if 'errors' in query_result and len(query_result['errors']) > 0:
                # failure due to GitHub trying to populate data
                fail_data = {'Dependent': single_dependency,
                             'hasDependencies': False,
                             'status': 'timeout',
                             'repository': {'databaseId': None,
                                            'name': repo_name,
                                            'owner': {'login': repo_owner},
                                            }
                             }
                data_table.append(fail_data)
            else:
                query_result["Dependent"] = single_dependency
                data_table.append(query_result)

        else:
            # other error than error code 200
            fail_data = {'Dependent': single_dependency,
                         'hasDependencies': False,
                         'status': get_info.status_code,
                         'repository': {'databaseId': None,
                                        'name': repo_name,
                                        'owner': {'login': repo_owner},
                                        }
                         }
            data_table.append(fail_data)
    return data_table