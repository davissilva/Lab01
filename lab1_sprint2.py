import json
from python_graphql_client import GraphqlClient
from datetime import datetime as date

url = "https://api.github.com/graphql"

headers = {"Authorization": "Token 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"}

today = date.utcnow()

variables = {
    "query": "stars :> 100",
    "type": "REPOSITORY",
    "fist": 20,
    "after": None,
}

query = """
query ($query: String!, $type: SearchType!, $first: Int!, $after: String) {
  search(query: $query, type: $type, first: $first, after: $after) {
    pageInfo{
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        nameWithOwner
        createdAt
        pullRequests(states: MERGED) {
          totalCount
        }
        primaryLanguage {
          name
        }
        updatedAt
        releases(orderBy: {field: CREATED_AT, direction: DESC}) {
          totalCount
        }
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
client = GraphqlClient(endpoint = url, headers = headers)


response = client.execute(query=query, variables=variables)
print(response)