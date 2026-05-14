# ================= REGISTRO SERVICE =================

from firebase_manager import FirebaseManager
from services.cache_service import CacheService


class RegistroService:
    """Serviço para gerenciar registros de conferência"""

    def __init__(self, cache_service: CacheService):
        self.firebase = FirebaseManager()
        self.cache = cache_service

    def salvar_registro(self, controle, cliente, conferente, box, volume):
        """
        Salva novo registro de conferência
        """
        try:
            sucesso = self.firebase.salvar_registro({
                "controle": controle,
                "cliente": cliente,
                "conferente": conferente,
                "box": box,
                "volume": volume
            })

            if sucesso:
                self.cache.carregar_registros()
                return True, "Registro salvo!"
            else:
                return False, "Erro ao salvar registro"

        except Exception as e:
            return False, f"Erro: {str(e)}"

    def obter_registros(self):
        """Retorna todos os registros do cache"""
        return self.cache.registros

    def obter_registros_filtrados(self, termo):
        """Retorna registros filtrados"""
        return self.cache.filtrar_registros(termo)
