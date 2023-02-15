import requests
import json
from utils import headers, url

query = """
query razaoIssues {
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        closedIssues: issues(filterBy: {states: CLOSED}) {
          totalCount
        }
        totalIssues: issues{
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
        closed_issues = repository["closedIssues"]["totalCount"]
        total_issues = repository["totalIssues"]["totalCount"]
        issues_ratio = closed_issues / total_issues if total_issues > 0 else 0
        print(
            f"Repositório: {name} - Issues fechadas: {closed_issues} - Issues total: {total_issues} - Razão de issues: {issues_ratio}"
        )
