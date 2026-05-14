# ================= NOTAS SEPARAÇÃO SERVICE =================
from datetime import datetime, timedelta
from firebase_manager import FirebaseManager

class NotasSeparacaoService:
    """Serviço para obter quantidade de notas separadas por cada separador"""

    def __init__(self):
        self.firebase = FirebaseManager()

    def obter_notas_por_separador(self):
        """
        Retorna uma lista de tuplas [(separador, total_notas), ...] 
        ordenada pelo total de notas, e também o início e fim da semana atual.
        """
        agora = datetime.now()
        inicio_semana = agora - timedelta(days=agora.weekday())
        inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
        fim_semana = inicio_semana + timedelta(days=4)
        fim_semana = fim_semana.replace(hour=23, minute=59, second=59)

        separacoes = self.firebase.carregar_separacoes(inicio_semana, fim_semana)

        dados = {}
        for r in separacoes:
            nome = r.get("separador", "Sem Nome")
            dados[nome] = dados.get(nome, 0) + 1

        # Ordena por total de notas decrescente
        ranking = sorted(dados.items(), key=lambda x: x[1], reverse=True)
        return ranking, inicio_semana, fim_semana