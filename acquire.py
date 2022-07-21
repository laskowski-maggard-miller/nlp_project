"""
A module for obtaining repo readme and language data from the github API.
Before using this module, read through it, and follow the instructions marked
TODO.
After doing so, run it like this:
    python acquire.py
To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List, Optional, Union, cast
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

from env import github_token, github_username

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token: https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

# Created repo_list Function below to pull in repos
def repo_list():
    '''
    This pulls all of the repos in from a csv file making this clearer than having a giant list for REPO
    '''
    df = pd.read_csv('repo_list.csv')
    repo_list = df['0'].values.tolist()

    return repo_list

repo_list = repo_list()
print(repo_list[:10])
REPOS = repo_list[:10]

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )


def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        if "language" not in repo_info:
            raise Exception(
                "'language' key not round in response\n{}".format(json.dumps(repo_info))
            )
        return repo_info["language"]
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme_download_url = get_readme_download_url(contents)
    if readme_download_url == "":
        readme_contents = ""
    else:
        readme_contents = requests.get(readme_download_url).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    #REPO = repo_list()
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)






## ----------++----------++----------++----------++----------

# def repo_list(start_page, end_page, repo_list = []):
#     '''
#     This function generates a list of repositories to then be acquired via the functions above    
#     '''
#     for page in range((start_page-1),end_page):
#         url = f'https://github.com/search?p={1+page}&q=cats&type=Repositories'
#         print(f'Procuring {url}')
#         r = requests.get(url)
#         soup = bs(r.content, 'html.parser')
        
#         repo = soup.find('ul', class_ = "repo-list")

#         try:
#             repos = repo.find_all('a', class_ = 'v-align-middle')
#         except:
#             print(f'>>>Failed to procure {url}')
#             repo_list(page,end_page,repo_list=repo_list)
#         for thing in repos:
#             repo_url = thing.text
#             repo_list.append(repo_url)
#         sleep(2)

# def repo_list():
#     '''
#     This pulls all of the repos in from a csv file making this clearer than having a giant list for REPO
#     '''
#     df = pd.read_csv('repo_list.csv')
#     repo_list = df['0'].values.tolist()

#     return repo_list