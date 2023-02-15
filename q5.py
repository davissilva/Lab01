import requests
import json
from utils import headers, url

query = """
query TotalReleases {
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        releases(orderBy: {field: CREATED_AT, direction: DESC}) {
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
        releases = repository["releases"]["totalCount"]
        print(f"Repositório: {name} - Releases: {releases}")
