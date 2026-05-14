# ================= COMPONENTES REUTILIZÁVEIS =================

import flet as ft
from firebase_manager import FirebaseManager
from ui.styles import Estilos, criar_card_ranking


class AutocompleteFiled:
    """Campo com autocompletar"""

    def __init__(self, label, lista_base, callback_select):
        self.label = label
        self.lista_base = lista_base
        self.callback_select = callback_select

        self.campo = ft.TextField(label=label)
        self.sugestoes = ft.Column(spacing=2)

        self.campo.on_change = self._on_change

    def _on_change(self, e):
        """Atualiza sugestões ao digitar"""
        texto = (e.control.value or "").strip().lower()
        self.sugestoes.controls.clear()

        if len(texto) < 2:
            return

        encontrados = [item for item in self.lista_base if texto in item.lower()][:5]

        for valor in encontrados:
            self.sugestoes.controls.append(
                ft.Container(
                    content=ft.Text(valor),
                    padding=10,
                    bgcolor="#E5E7EB",
                    border_radius=8,
                    on_click=lambda ev, v=valor: self._select(v)
                )
            )

    def _select(self, valor):
        """Seleciona item das sugestões"""
        self.campo.value = valor
        self.sugestoes.controls.clear()
        self.callback_select(valor)

    def obter_container(self):
        """Retorna container com campo e sugestões"""
        return ft.Column([
            self.campo,
            self.sugestoes
        ])

    def obter_valor(self):
        """Retorna valor digitado"""
        return self.campo.value

    def limpar(self):
        """Limpa o campo"""
        self.campo.value = ""
        self.sugestoes.controls.clear()


class ContainerRegistro:
    """Container para exibir um registro"""

    @staticmethod
    def criar(registro, firebase_manager):
        """
        Cria container com dados do registro
        """
        data_formatada = firebase_manager.formatar_data(
            registro.get("data_hora")
        )

        return ft.Container(
            padding=12,
            border_radius=12,
            bgcolor=Estilos.CONTAINER_LIGHT,
            content=ft.Column([
                ft.Text(
                    f"Cliente: {registro.get('cliente')}",
                    weight="bold"
                ),
                ft.Text(
                    f"Controle: {registro.get('controle')}"
                ),
                ft.Text(
                    f"Conferente: {registro.get('conferente')}"
                ),
                ft.Text(
                    f"Box: {registro.get('box')}"
                ),
                ft.Text(
                    f"Volume: {registro.get('volume')}"
                ),
                ft.Text(
                    f"📅 {data_formatada}",
                    color="blue"
                )
            ])
        )


class RankingWidget:
    """Widget para exibir ranking"""

    @staticmethod
    def criar_conferentes(ranking, cores, inicio, fim):
        """
        Cria widget de ranking dos conferentes
        """
        coluna = ft.Column()

        coluna.controls.append(
            ft.Container(
                padding=20,
                border_radius=15,
                bgcolor=Estilos.CONTAINER_CONFERENTES,
                content=ft.Column([
                    ft.Text(
                        "🏆 TOP 3 Conferentes",
                        size=24,
                        weight="bold",
                        color=Estilos.AZUL
                    ),
                    ft.Text(
                        f"Semana: {inicio.strftime('%d/%m/%Y')} até {fim.strftime('%d/%m/%Y')}",
                        color=Estilos.CINZA
                    )
                ])
            )
        )

        coluna.controls.append(ft.Container(height=10))

        if ranking:
            for i, (nome, total) in enumerate(ranking, start=1):
                coluna.controls.append(
                    criar_card_ranking(
                        i,
                        nome,
                        f"{total} registros",
                        cores[i - 1]
                    )
                )

        return coluna

    @staticmethod
    def criar_separadores(ranking, cores, inicio, fim):
        """
        Cria widget de ranking dos separadores
        """
        coluna = ft.Column()

        coluna.controls.append(
            ft.Container(
                padding=20,
                border_radius=15,
                bgcolor=Estilos.CONTAINER_SEPARADORES,
                content=ft.Column([
                    ft.Text(
                        "📦 TOP 3 Separadores",
                        size=24,
                        weight="bold",
                        color=Estilos.VERDE
                    ),
                    ft.Text(
                        f"Semana: {inicio.strftime('%d/%m/%Y')} até {fim.strftime('%d/%m/%Y')}",
                        color=Estilos.CINZA
                    )
                ])
            )
        )

        coluna.controls.append(ft.Container(height=10))

        if ranking:
            for i, (nome, total) in enumerate(ranking, start=1):
                coluna.controls.append(
                    criar_card_ranking(
                        i,
                        nome,
                        f"{total} itens",
                        cores[i - 1]
                    )
                )

        return coluna
