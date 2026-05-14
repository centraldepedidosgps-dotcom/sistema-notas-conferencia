# ================= ESTILOS E CORES =================

import flet as ft
from config import CORES_CONFERENTES, CORES_SEPARADORES, MENU_COLOR, MENU_WIDTH


class Estilos:
    """Gerenciador de estilos da aplicação"""

    # Cores do menu
    MENU_BG = MENU_COLOR
    MENU_LARGURA = MENU_WIDTH

    # Cores dos rankings
    CORES_CONFERENTES = CORES_CONFERENTES
    CORES_SEPARADORES = CORES_SEPARADORES

    # Cores de status
    VERDE = "#15803D"
    VERMELHO = "#DC2626"
    AZUL = "#1D4ED8"
    CINZA = "#475569"

    # Cores de container
    CONTAINER_LIGHT = "#F1F5F9"
    CONTAINER_PAINEL = "#F8FAFC"
    CONTAINER_CONFERENTES = "#DBEAFE"
    CONTAINER_SEPARADORES = "#DCFCE7"


def criar_card_ranking(posicao, nome, total, cor):
    """
    Cria um card para exibir ranking
    """
    medalha = "🏅"

    if posicao == 1:
        medalha = "🥇"
    elif posicao == 2:
        medalha = "🥈"
    elif posicao == 3:
        medalha = "🥉"

    return ft.Container(
        padding=15,
        border_radius=15,
        bgcolor=cor,
        content=ft.Row([
            ft.Text(
                f"{medalha} {posicao}º",
                size=18,
                weight="bold"
            ),
            ft.Text(
                nome,
                expand=True,
                size=18,
                weight="bold"
            ),
            ft.Text(
                total,
                size=16,
                weight="bold"
            )
        ])
    )
