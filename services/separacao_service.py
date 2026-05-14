# ================= SEPARAÇÃO SERVICE =================

from firebase_manager import FirebaseManager
from services.cache_service import CacheService
from collections import defaultdict


class SeparacaoService:
    """Serviço para gerenciar separações baseado em nota e andar"""

    def __init__(self, cache_service: CacheService):
        self.firebase = FirebaseManager()
        self.cache = cache_service

    def salvar_separacao(self, separador, nota, andar):
        """
        Salva uma nova separação

        Args:
            separador (str): nome do usuário
            nota (str/int): número da nota
            andar (int): 1, 2 ou 3
        """
        try:
            if not separador:
                return False, "Separador inválido"

            if not nota:
                return False, "Nota inválida"

            if int(andar) not in [1, 2, 3]:
                return False, "Andar inválido (use 1, 2 ou 3)"

            dados = {
                "separador": str(separador).strip(),
                "nota": str(nota).strip(),
                "andar": int(andar)
            }

            sucesso = self.firebase.salvar_separacao(dados)

            if sucesso:
                self._atualizar_cache(dados)
                return True, "Separação salva com sucesso!"

            return False, "Erro ao salvar separação no Firebase"

        except ValueError:
            return False, "Andar deve ser um número (1, 2 ou 3)"

        except Exception as e:
            return False, f"Erro inesperado: {str(e)}"

    def listar_separacoes(self):
        """
        Lista separações (com cache se disponível)
        """
        try:
            cache_key = "separacoes"
            cached = self.cache.get(cache_key)
            if cached:
                return cached

            dados = self.firebase.listar_separacoes()
            self.cache.set(cache_key, dados)
            return dados

        except Exception as e:
            print(f"Erro ao listar separações: {str(e)}")
            return []

    def filtrar_por_andar(self, andar):
        """
        Filtra separações por andar (1, 2 ou 3)
        """
        try:
            todas = self.listar_separacoes()
            return [s for s in todas if s.get("andar") == int(andar)]
        except Exception as e:
            print(f"Erro ao filtrar por andar: {str(e)}")
            return []

    def contar_por_nota(self, andar=None):
        """
        Conta separações agrupadas por nota.
        Se 'andar' for fornecido, filtra antes.
        """
        try:
            separacoes = self.listar_separacoes()
            if andar:
                separacoes = [s for s in separacoes if s.get("andar") == int(andar)]

            contagem = defaultdict(int)
            for s in separacoes:
                contagem[s["nota"]] += 1

            # retorna como lista de dicionários (ou pode ser dict puro)
            return [{"nota": nota, "quantidade": qtd} for nota, qtd in contagem.items()]

        except Exception as e:
            print(f"Erro ao contar separações por nota: {str(e)}")
            return []

    def _atualizar_cache(self, nova_separacao):
        """
        Atualiza cache de últimas separações
        """
        try:
            cache_key = "ultimas_separacoes"
            ultimas = self.cache.get(cache_key) or []
            ultimas.insert(0, nova_separacao)
            ultimas = ultimas[:20]
            self.cache.set(cache_key, ultimas)
        except Exception as e:
            print(f"Erro ao atualizar cache: {str(e)}")