import requests
import json
from datetime import datetime as date
from utils import headers, url

query = """
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

response = requests.post(url, headers=headers, json={"query": query})

if response.status_code == 200:
    data = json.loads(response.text)
    repositories = data["data"]["search"]["nodes"]

    for repository in repositories:
        name = repository["nameWithOwner"]
        createdAt = repository["createdAt"].rstrip("Z")
        createdAt = date.fromisoformat(createdAt)
        hoje = date.now()
        idade = hoje - createdAt
        print(f"repositório: {name} - criação: {createdAt} - idade: {idade}")
