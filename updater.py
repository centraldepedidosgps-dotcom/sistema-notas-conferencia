import requests
from config import APP_VERSION, GITHUB_USER, GITHUB_REPO


def verificar_atualizacao():
    """
    Verifica versão no GitHub Releases
    """
    try:
        url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
        response = requests.get(url)

        if response.status_code != 200:
            print("Erro ao verificar atualização")
            return

        data = response.json()
        versao_github = data["tag_name"].replace("v", "")

        print("Versão atual:", APP_VERSION)
        print("Versão GitHub:", versao_github)

        if versao_github != APP_VERSION:
            print("Nova versão disponível!")
        else:
            print("Sistema atualizado.")

    except Exception as e:
        print("Erro no updater:", e)