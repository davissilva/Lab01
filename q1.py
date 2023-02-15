import requests
import json
from datetime import datetime as date
from utils import headers, url

today = date.utcnow()

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
        created_at = repository["createdAt"].rstrip("Z")
        created_at = date.fromisoformat(created_at)
        age = today - created_at
        print(f"Repositório: {name} - Criação: {created_at} - Idade: {age}")
