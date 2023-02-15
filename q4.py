import requests
import json
from datetime import datetime as date
from utils import headers, url

today = date.utcnow()

query = """
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

response = requests.post(url, headers=headers, json={"query": query})

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
