import requests
import json
from utils import headers, url

query = """
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


response = requests.post(url, headers=headers, json={"query": query})

if response.status_code == 200:
    data = json.loads(response.text)
    repositories = data["data"]["search"]["nodes"]

    for repository in repositories:
        name = repository["nameWithOwner"]
        primaryLanguage = repository["primaryLanguage"]
        language = primaryLanguage["name"] if primaryLanguage is not None else "none"
        print(f"repositório: {name} - linguagem: {language}")
