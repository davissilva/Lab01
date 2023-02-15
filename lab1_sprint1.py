import requests
import json
from datetime import datetime as date

url = "https://api.github.com/graphql"

headers = {"Authorization": "Token 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"}

today = date.utcnow()

# Queries
q1 = """
query IdadeRepositorio {
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        createdAt
      }
    }
  }
}
"""
q2 = """
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
q3 = """
query LinguagemPrimaria {
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        primaryLanguage {
          name
        }
        nameWithOwner
      }
    }
  }
}
"""
q4 = """
query ultimaAtualizacao {
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        updatedAt
      }
    }
  }
}
"""
q5 = """
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
q6 = """
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

print("RQ 01")
response = requests.post(url, headers=headers, json={"query": q1})
if response.status_code == 200:
    data = json.loads(response.text)
    repositories = data["data"]["search"]["nodes"]

    for repository in repositories:
        name = repository["nameWithOwner"]
        created_at = repository["createdAt"].rstrip("Z")
        created_at = date.fromisoformat(created_at)
        age = today - created_at
        print(f"Repositório: {name} - Criação: {created_at} - Idade: {age}")

print("RQ 02")
response = requests.post(url, headers=headers, json={"query": q2})
if response.status_code == 200:
    data = json.loads(response.text)
    repositories = data["data"]["search"]["nodes"]

    for repository in repositories:
        name = repository["nameWithOwner"]
        pull_requests = repository["pullRequests"]["totalCount"]
        print(f"Repositório: {name} - Pull Resquests aceitas: {pull_requests}")

print("RQ 03")
response = requests.post(url, headers=headers, json={"query": q3})
if response.status_code == 200:
    data = json.loads(response.text)
    repositories = data["data"]["search"]["nodes"]

    for repository in repositories:
        name = repository["nameWithOwner"]
        primary_language = repository["primaryLanguage"]
        language = primary_language[
            "name"] if primary_language is not None else "none"
        print(f"Repositório: {name} - Linguagem: {language}")

print("RQ 04")
response = requests.post(url, headers=headers, json={"query": q4})
if response.status_code == 200:
    data = json.loads(response.text)
    repositories = data["data"]["search"]["nodes"]

    for repository in repositories:
        name = repository["nameWithOwner"]
        updated_at = repository["updatedAt"].rstrip("Z")
        updated_at = date.fromisoformat(updated_at)
        age = today - updated_at
        print(
            f"Repositório: {name} - Última Atualização: {updated_at} - Tempo decorrido: {age}"
        )

print("RQ 05")
response = requests.post(url, headers=headers, json={"query": q5})
if response.status_code == 200:
    data = json.loads(response.text)
    repositories = data["data"]["search"]["nodes"]

    for repository in repositories:
        name = repository["nameWithOwner"]
        releases = repository["releases"]["totalCount"]
        print(f"Repositório: {name} - Releases: {releases}")

print("RQ 06")
response = requests.post(url, headers=headers, json={"query": q6})
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