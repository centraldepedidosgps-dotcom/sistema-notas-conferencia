# ================= main.py =================

import flet as ft
from ui.views import (
    CadastroView,
    SeparacaoView,
    ConsultaView,
    PainelView,
    AdminView,
    NotasSeparacaoView,
)
from services.cache_service import CacheService


def main(page: ft.Page):

    # ================= CONFIGURAÇÃO DA PÁGINA =================
    page.title = "Sistema de Notas"
    page.window_width = 1200
    page.window_height = 750
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#F1F5F9"
    page.scroll = None

    # ================= CACHE + FIREBASE =================
    cache_service = CacheService()

    # 🔥 IMPORTANTE: carregar dados antes de criar as views
    cache_service.carregar_conferentes()
    cache_service.carregar_boxes()
    cache_service.carregar_separadores()
    cache_service.carregar_registros()

    # ================= INSTÂNCIA DAS VIEWS =================
    cadastro_view = CadastroView(page, cache_service)
    separacao_view = SeparacaoView(page, cache_service)
    consulta_view = ConsultaView(page, cache_service)
    painel_view = PainelView(page)
    admin_view = AdminView(page, cache_service)
    notas_view = NotasSeparacaoView(page, cache_service)

    # ================= ÁREA PRINCIPAL =================
    main_area = ft.Container(
        expand=True,
        bgcolor="#F8FAFC",
        padding=40
    )

    # ================= CONTROLE BOTÃO ATIVO =================
    botoes_menu = []

    def ativar_botao(botao):
        for b in botoes_menu:
            b.style = ft.ButtonStyle(
                padding=15,
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor=None
            )

        botao.style = ft.ButtonStyle(
            padding=15,
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor="#334155"
        )

        page.update()

    # ================= TROCA DE VIEW =================
    def mostrar_view(view):

        main_area.content = ft.Container(
            content=view.obter_view(),
            expand=True,
            bgcolor="white",
            padding=30,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color="black12"
            )
        )

        page.update()

    # ================= CRIAR BOTÃO DO MENU =================
    def criar_botao(texto, icone, view):

        btn = ft.TextButton(
            content=ft.Row(
                [
                    ft.Icon(icone, color="white"),
                    ft.Text(texto, color="white"),
                ],
                spacing=10,
            ),
            on_click=lambda e: (
                ativar_botao(btn),
                mostrar_view(view)
            ),
            style=ft.ButtonStyle(
                padding=15,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )

        botoes_menu.append(btn)
        return btn

    # ================= SIDEBAR =================
    sidebar = ft.Container(
        width=180,
        bgcolor="#1E293B",
        padding=20,
        content=ft.Column(
            [
                ft.Text("Sistema", size=20, weight="bold", color="white"),
                ft.Divider(color="white24"),

                criar_botao("Cadastro", ft.Icons.PERSON_ADD, cadastro_view),
                criar_botao("Separação", ft.Icons.INVENTORY, separacao_view),
                criar_botao("Consulta", ft.Icons.SEARCH, consulta_view),
                criar_botao("Painel", ft.Icons.DASHBOARD, painel_view),
                criar_botao("Admin", ft.Icons.ADMIN_PANEL_SETTINGS, admin_view),
                criar_botao("Notas", ft.Icons.RECEIPT_LONG, notas_view),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        ),
    )

    # ================= LAYOUT PRINCIPAL =================
    layout = ft.Row(
        [
            sidebar,
            main_area
        ],
        expand=True
    )

    page.add(layout)

    # ================= VIEW INICIAL =================
    ativar_botao(botoes_menu[0])
    mostrar_view(cadastro_view)


ft.app(target=main)