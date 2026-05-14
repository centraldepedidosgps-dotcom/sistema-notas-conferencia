# ================= CACHE SERVICE =================

from firebase_manager import FirebaseManager


class CacheService:
    """Serviço de cache para dados do aplicativo"""

    def __init__(self):
        self.firebase = FirebaseManager()
        self.conferentes = []
        self.boxes = []
        self.separadores = []
        self.registros = []

    def carregar_tudo(self):
        """Carrega todos os caches"""
        self.carregar_conferentes()
        self.carregar_boxes()
        self.carregar_separadores()
        self.carregar_registros()

    def carregar_conferentes(self):
        """Carrega conferentes em cache"""
        self.conferentes = self.firebase.carregar_conferentes()

    def carregar_boxes(self):
        """Carrega boxes em cache"""
        self.boxes = self.firebase.carregar_boxes()

    def carregar_separadores(self):
        """Carrega separadores em cache"""
        self.separadores = self.firebase.carregar_separadores()

    def carregar_registros(self):
        """Carrega registros em cache"""
        self.registros = self.firebase.carregar_registros()

    def filtrar_registros(self, termo=""):
        """Filtra registros por termo de busca"""
        if not termo:
            return self.registros

        termo = termo.lower()
        return [
            r for r in self.registros
            if termo in str(r).lower()
        ]
