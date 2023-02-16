from graphqlclient import GraphQLClient
from datetime import datetime as date
import json
import csv

url = "https://api.github.com/graphql"
token = "Token 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"
today = date.utcnow()
variables = {"after": None}

query = """
query ($after: String) {
  search(query: "stars:>100", type: REPOSITORY, first: 20, after: $after) {
    pageInfo{ endCursor }
    nodes {
      ... on Repository {
        nameWithOwner
        createdAt
        pullRequests(first: 1,states: MERGED) { totalCount }
        primaryLanguage { name }
        updatedAt
        releases(first: 1, orderBy: {field: CREATED_AT, direction: ASC}) { totalCount }
        closedIssues: issues(first: 1,states: CLOSED) { totalCount }
        totalIssues: issues(first: 1){ totalCount }
      }
    }
  }
}
"""
client = GraphQLClient(url)
client.inject_token(token=token)

with open("dadosRepositorios1.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "repository",
        "createdAt",
        "age",
        "pullRequests",
        "releases",
        "updatedAt",
        "daysSinceUpdate",
        "primaryLanguage",
        "closedIssues",
        "totalIssues",
        "issuesRatio",
    ])

    for i in range(5):
        data = json.loads(client.execute(query=query, variables=variables))
        results = data["data"]["search"]
        end_cursor = results["pageInfo"]["endCursor"]

        variables["after"] = end_cursor
        repositories = results["nodes"]

        for repo in repositories:
            name = repo["nameWithOwner"]
            created_at = date.strptime(repo["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
            age = (today - created_at).days
            pull_requests = repo["pullRequests"]["totalCount"]
            language = repo["primaryLanguage"]["name"] if repo[
                "primaryLanguage"] is not None else "none"
            updated_at = date.strptime(repo["updatedAt"], "%Y-%m-%dT%H:%M:%SZ")
            days_since_update = today - updated_at
            releases = repo["releases"]["totalCount"]
            closed_issues = repo["closedIssues"]["totalCount"]
            total_issues = repo["totalIssues"]["totalCount"]
            issues_ratio = closed_issues / total_issues if total_issues > 0 else 0

            writer.writerow([
                name,
                created_at,
                age,
                pull_requests,
                releases,
                updated_at,
                days_since_update,
                language,
                closed_issues,
                total_issues,
                issues_ratio,
            ])

print("fim")
