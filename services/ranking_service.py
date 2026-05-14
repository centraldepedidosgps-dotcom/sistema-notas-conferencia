# ================= RANKING SERVICE =================

from datetime import datetime, timedelta
from firebase_manager import FirebaseManager


class RankingService:
    """Serviço para calcular rankings de produtividade"""

    def __init__(self):
        self.firebase = FirebaseManager()

    # ================= PERÍODO SEMANA =================
    def obter_periodo_semana(self):
        agora = datetime.now()

        inicio_semana = agora - timedelta(days=agora.weekday())
        inicio_semana = inicio_semana.replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        fim_semana = inicio_semana + timedelta(days=4)
        fim_semana = fim_semana.replace(
            hour=23, minute=59, second=59
        )

        return inicio_semana, fim_semana

    # ================= CONFERENTES =================
    def calcular_ranking_conferentes(self):
        inicio, fim = self.obter_periodo_semana()
        registros = self.firebase.carregar_registros_semana(inicio, fim)

        conf = {}
        for r in registros:
            nome = r.get("conferente", "Sem Nome")
            conf[nome] = conf.get(nome, 0) + 1

        ranking = sorted(
            conf.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        return ranking, inicio, fim

    # ================= SEPARADORES (GERAL) =================
    def calcular_ranking_separadores(self):
        inicio, fim = self.obter_periodo_semana()
        separacoes = self.firebase.carregar_separacoes(inicio, fim)

        sep = {}
        for r in separacoes:
            nome = r.get("separador", "Sem Nome")
            sep[nome] = sep.get(nome, 0) + 1

        ranking = sorted(
            sep.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        return ranking, inicio, fim

    # ================= SEPARADORES POR ANDAR =================
    def calcular_ranking_separadores_por_andar(self):
        """
        Retorna ranking dos separadores separados por andar (1, 2, 3)
        """
        inicio, fim = self.obter_periodo_semana()
        separacoes = self.firebase.carregar_separacoes(inicio, fim)

        # Dicionário com chave = andar
        dados = {"1": {}, "2": {}, "3": {}}

        for r in separacoes:
            nome = r.get("separador", "Sem Nome")
            andar = str(r.get("andar", "1"))  # Default para 1 se não tiver
            if andar not in dados:
                dados[andar] = {}
            dados[andar][nome] = dados[andar].get(nome, 0) + 1

        # Ordena cada andar e pega top 3
        ranking_por_andar = {}
        for andar, sep in dados.items():
            ranking_por_andar[andar] = sorted(
                sep.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]

        return ranking_por_andar, inicio, fim

    # ================= NOTAS POR SEPARADOR =================
    def calcular_notas_por_separador(self):
        """
        Ranking baseado na quantidade de notas processadas
        """
        inicio, fim = self.obter_periodo_semana()
        separacoes = self.firebase.carregar_separacoes(inicio, fim)

        dados = {}
        for r in separacoes:
            nome = r.get("separador", "Sem Nome")
            dados[nome] = dados.get(nome, 0) + 1

        ranking = sorted(
            dados.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return ranking, inicio, fim