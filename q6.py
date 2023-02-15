import requests
import json
from datetime import datetime as date
from utils import headers, url


query = """
query issuesFechadas {
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        name
        issues(filterBy: {states: CLOSED}) {
          totalCount
        }
      }
    }
  }
}

query totalIssues {
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        name
        issues {
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
        pullRequests = repository[pullRequests]["totalCount"]
        print(f"repositório: {name} - Pull Resquests: {pullRequests}")