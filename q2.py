import requests
import json
from datetime import datetime as date
from utils import headers, url


query = """
query totalPullRequestsAceitas {
  search(type: REPOSITORY, first: 100, query: "stars:>100") {
    nodes {
      ... on Repository {
        nameWithOwner
        pullRequests(states: MERGED) {
          totalCount
        }
      }
    }
  }
}
"""


response = requests.post(url, headers=headers, json={"query": query})

if response.status_code == 200:
    data = json.loads(response.text)
    repositories = data["data"]["search"]["nodes"]

    for repository in repositories:
        name = repository["nameWithOwner"]
        pullRequests = repository["pullRequests"]["totalCount"]
        print(f"Repositório: {name} - Pull Resquests aceitas: {pullRequests}")