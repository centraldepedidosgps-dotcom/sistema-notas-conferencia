# ================= ui/views.py =================

import flet as ft
from ui.components import AutocompleteFiled, ContainerRegistro
from ui.styles import Estilos, criar_card_ranking
from config import SENHA_PAINEL, SENHA_ADMIN
from services.cache_service import CacheService
from services.registro_service import RegistroService
from services.separacao_service import SeparacaoService
from services.ranking_service import RankingService
from services.notas_separacao_service import NotasSeparacaoService
from firebase_manager import FirebaseManager

# ================= CADASTRO VIEW =================
class CadastroView:
    def __init__(self, page, cache_service: CacheService):
        self.page = page
        self.cache = cache_service
        self.registro_service = RegistroService(cache_service)
        self.firebase = FirebaseManager()

        self.cad_controle = ft.TextField(label="Controle")
        self.cad_cliente = ft.TextField(label="Cliente")
        self.cad_conferente_field = AutocompleteFiled("Conferente", self.cache.conferentes, self._select_conferente)
        self.cad_box_field = AutocompleteFiled("Box", self.cache.boxes, self._select_box)
        self.cad_volume = ft.TextField(label="Volume")
        self.msg_cadastro = ft.Text()

    def _select_conferente(self, valor):
        self.page.update()

    def _select_box(self, valor):
        self.page.update()

    def _salvar(self, e):
        sucesso, msg = self.registro_service.salvar_registro(
            self.cad_controle.value,
            self.cad_cliente.value,
            self.cad_conferente_field.obter_valor(),
            self.cad_box_field.obter_valor(),
            self.cad_volume.value
        )
        self.msg_cadastro.value = msg
        self.msg_cadastro.color = "green" if sucesso else "red"
        if sucesso:
            self.cad_controle.value = ""
            self.cad_cliente.value = ""
            self.cad_volume.value = ""
            self.cad_conferente_field.limpar()
            self.cad_box_field.limpar()
            self.cache.carregar_registros()
        self.page.update()

    def obter_view(self):
        return ft.Column([
            ft.Text("Cadastro", size=22, weight="bold"),
            self.cad_controle,
            self.cad_cliente,
            self.cad_conferente_field.obter_container(),
            self.cad_box_field.obter_container(),
            self.cad_volume,
            ft.ElevatedButton("Salvar", on_click=self._salvar),
            self.msg_cadastro
        ])

# ================= SEPARACAO VIEW =================
class SeparacaoView:
    def __init__(self, page, cache_service: CacheService):
        self.page = page
        self.cache = cache_service
        self.separacao_service = SeparacaoService(cache_service)

        self.sep_separador_field = AutocompleteFiled("Separador", self.cache.separadores, self._select_separador)
        self.sep_notas = ft.TextField(label="Notas", keyboard_type=ft.KeyboardType.NUMBER)
        self.sep_andar = ft.Dropdown(
            label="Andar",
            options=[ft.dropdown.Option("1"), ft.dropdown.Option("2"), ft.dropdown.Option("3")],
            value="1"
        )
        self.msg_sep = ft.Text()

    def _select_separador(self, valor):
        self.page.update()

    def _salvar(self, e):
        separador = self.sep_separador_field.obter_valor()
        nota = self.sep_notas.value
        andar = self.sep_andar.value

        sucesso, msg = self.separacao_service.salvar_separacao(separador, nota, andar)
        self.msg_sep.value = msg
        self.msg_sep.color = "green" if sucesso else "red"
        if sucesso:
            self.sep_separador_field.limpar()
            self.sep_notas.value = ""
            self.sep_andar.value = "1"
        self.page.update()

    def obter_view(self):
        return ft.Column([
            ft.Text("Separação", size=22, weight="bold"),
            self.sep_separador_field.obter_container(),
            self.sep_notas,
            self.sep_andar,
            ft.ElevatedButton("Salvar Separação", on_click=self._salvar),
            self.msg_sep
        ])

# ================= CONSULTA VIEW =================
class ConsultaView:
    def __init__(self, page, cache_service: CacheService):
        self.page = page
        self.cache = cache_service
        self.firebase = FirebaseManager()
        self.busca = ft.TextField(label="Buscar")
        self.lista = ft.Column(scroll="auto")
        self.busca.on_change = self._filtrar
        self._atualizar_lista()

    def _filtrar(self, e=None):
        termo = (self.busca.value or "").lower()
        self._atualizar_lista(termo)

    def _atualizar_lista(self, termo=""):
        self.lista.controls.clear()
        registros = self.cache.filtrar_registros(termo)
        for d in registros:
            self.lista.controls.append(ContainerRegistro.criar(d, self.firebase))
        self.page.update()

    def obter_view(self):
        return ft.Column([
            ft.Text("Consulta", size=22, weight="bold"),
            self.busca,
            self.lista
        ])

# ================= PAINEL VIEW =================
class PainelView:
    def __init__(self, page):
        self.page = page
        self.ranking_service = RankingService()
        self.senha = ft.TextField(label="Senha Painel", password=True)
        self.cadeado = ft.Text("🔒 Painel Trancado", color="red", size=18, weight="bold")
        self.ranking_conf = ft.Column()
        self.ranking_sep = ft.Column()
        self.painel = ft.Container(visible=False)
        self._construir_painel()

    def _construir_painel(self):
        self.painel.content = ft.Column([
            ft.Text("📊 Painel de Produtividade", size=24, weight="bold"),
            ft.Divider(),
            self.ranking_conf,
            ft.Divider(),
            self.ranking_sep,
            ft.Divider(),
            ft.ElevatedButton("🔒 Trancar Painel", bgcolor="red", color="white", on_click=self._trancar)
        ])

    def _trancar(self, e=None):
        self.painel.visible = False
        self.cadeado.visible = True
        self.senha.value = ""
        self.page.update()

    def _abrir(self, e):
        if self.senha.value == SENHA_PAINEL:
            ranking_conf, _, _ = self.ranking_service.calcular_ranking_conferentes()
            self.ranking_conf.controls.clear()
            for i, (nome, total) in enumerate(ranking_conf, start=1):
                self.ranking_conf.controls.append(
                    criar_card_ranking(i, nome, f"{total} registros", Estilos.CORES_CONFERENTES[i-1])
                )
            ranking_por_andar, _, _ = self.ranking_service.calcular_ranking_separadores_por_andar()
            self.ranking_sep.controls.clear()
            for andar in ["1", "2", "3"]:
                self.ranking_sep.controls.append(ft.Text(f"Andar {andar}", size=18, weight="bold"))
                for i, (nome, total) in enumerate(ranking_por_andar.get(andar, []), start=1):
                    self.ranking_sep.controls.append(
                        criar_card_ranking(i, nome, f"{total} notas", Estilos.CORES_SEPARADORES[i-1])
                    )
                self.ranking_sep.controls.append(ft.Container(height=10))
            self.painel.visible = True
            self.cadeado.visible = False
        else:
            self._trancar()
        self.page.update()

    def obter_view(self):
        return ft.Column([
            self.senha,
            ft.ElevatedButton("Abrir Painel", on_click=self._abrir),
            self.cadeado,
            self.painel
        ])

# ================= ADMIN VIEW =================
class AdminView:
    def __init__(self, page, cache_service: CacheService):
        self.page = page
        self.cache = cache_service
        self.firebase = FirebaseManager()

        self.admin_senha = ft.TextField(label="Senha Admin", password=True)
        self.admin_msg = ft.Text()
        self.adm_conf = ft.TextField(label="Novo Conferente")
        self.adm_box = ft.TextField(label="Novo Box")
        self.adm_sep = ft.TextField(label="Novo Separador")
        self.admin_area = ft.Container(visible=False)
        self._construir_area_admin()

    def _construir_area_admin(self):
        self.admin_area.content = ft.Column([
            ft.Text("🔐 Área Administrativa", size=22, weight="bold"),
            self.adm_conf,
            ft.ElevatedButton("Salvar Conferente", on_click=self._salvar_conf),
            self.adm_box,
            ft.ElevatedButton("Salvar Box", on_click=self._salvar_box),
            self.adm_sep,
            ft.ElevatedButton("Salvar Separador", on_click =self._salvar_sep),
            ft.Divider(),
            ft.ElevatedButton("🔒 Trancar Admin", bgcolor="#374151", color="white", on_click=self._trancar),
            self.admin_msg
        ])

    def _salvar_conf(self, e):
        """Salva novo conferente"""
        if self.adm_conf.value:
            if self.firebase.salvar_conferente(self.adm_conf.value):
                self.adm_conf.value = ""
                self.cache.carregar_conferentes()
                self.admin_msg.value = "Conferente salvo!"
                self.admin_msg.color = "green"
            else:
                self.admin_msg.value = "Erro ao salvar conferente"
                self.admin_msg.color = "red"
        self.page.update()

    def _salvar_box(self, e):
        """Salva novo box"""
        if self.adm_box.value:
            if self.firebase.salvar_box(self.adm_box.value):
                self.adm_box.value = ""
                self.cache.carregar_boxes()
                self.admin_msg.value = "Box salvo!"
                self.admin_msg.color = "green"
            else:
                self.admin_msg.value = "Erro ao salvar box"
                self.admin_msg.color = "red"
        self.page.update()

    def _salvar_sep(self, e):
        """Salva novo separador"""
        if self.adm_sep.value:
            if self.firebase.salvar_separador(self.adm_sep.value):
                self.adm_sep.value = ""
                self.cache.carregar_separadores()
                self.admin_msg.value = "Separador salvo!"
                self.admin_msg.color = "green"
            else:
                self.admin_msg.value = "Erro ao salvar separador"
                self.admin_msg.color = "red"
        self.page.update()

    def _entrar(self, e):
        """Valida senha e abre área admin"""
        if self.admin_senha.value == SENHA_ADMIN:
            self.admin_area.visible = True
            self.admin_msg.value = "Admin liberado!"
            self.admin_msg.color = "green"
        else:
            self.admin_area.visible = False
            self.admin_msg.value = "Senha incorreta!"
            self.admin_msg.color = "red"
        self.page.update()

    def _trancar(self, e=None):
        """Tranca a área admin"""
        self.admin_area.visible = False
        self.admin_senha.value = ""
        self.admin_msg.value = "Admin trancado!"
        self.admin_msg.color = "red"
        self.page.update()

    def obter_view(self):
        """Retorna a view completa da área administrativa"""
        return ft.Column([
            ft.Text("Admin", size=22, weight="bold"),
            self.admin_senha,
            ft.ElevatedButton("Entrar", on_click=self._entrar),
            self.admin_area,
            self.admin_msg
        ])
    
    # ================= LAYOUT PADRÃO =================
def layout_padrao(titulo, conteudo):

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    titulo,
                    size=24,
                    weight="bold"
                ),
                ft.Divider(),
                conteudo
            ],
            spacing=20,
            expand=True,
            scroll="auto"
        ),
        padding=30,
        expand=True
    )
# ================= NOTAS SEPARAÇÃO VIEW =================
class NotasSeparacaoView:

    def __init__(self, page, cache_service: CacheService):
        self.page = page
        self.cache = cache_service
        self.service = NotasSeparacaoService()

        self.senha = ft.TextField(label="Senha Admin", password=True)
        self.msg = ft.Text()
        self.relatorio = ft.Column(visible=False, scroll="auto")

    def _abrir(self, e):

        if self.senha.value == SENHA_ADMIN:

            self.relatorio.controls.clear()

            ranking, inicio, fim = self.service.obter_notas_por_separador()

            self.relatorio.controls.append(
                ft.Text(
                    f"Período: {inicio.strftime('%d/%m/%Y')} - {fim.strftime('%d/%m/%Y')}",
                    weight="bold"
                )
            )

            self.relatorio.controls.append(ft.Divider())

            if ranking:
                for i, (nome, total) in enumerate(ranking, start=1):
                    self.relatorio.controls.append(
                        ft.Text(
                            f"{i}. {nome} - {total} notas",
                            size=16
                        )
                    )
            else:
                self.relatorio.controls.append(
                    ft.Text("Nenhuma nota encontrada.", color="red")
                )

            self.relatorio.visible = True
            self.msg.value = ""

        else:
            self.relatorio.visible = False
            self.msg.value = "Senha incorreta"
            self.msg.color = "red"

        self.page.update()

    def _trancar(self, e):
        self.relatorio.visible = False
        self.senha.value = ""
        self.page.update()

    def obter_view(self):

        conteudo = ft.Column([
            self.senha,
            ft.Row([
                ft.ElevatedButton("Abrir Relatório", on_click=self._abrir),
                ft.ElevatedButton(
                    "Trancar",
                    bgcolor="red",
                    color="white",
                    on_click=self._trancar
                )
            ]),
            self.msg,
            self.relatorio
        ])

        return layout_padrao("Notas Separação", conteudo)