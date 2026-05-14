# ================= FIREBASE =================

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta, timezone
from config import FIREBASE_CREDENTIALS


class FirebaseManager:
    """Gerenciador centralizado de operações Firebase"""

    _instance = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa conexão com Firebase"""
        try:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            self._db = firestore.client()
        except Exception as e:
            print(f"Erro ao inicializar Firebase: {e}")

    @property
    def db(self):
        """Retorna instância do Firestore"""
        return self._db

    # ================= DATAS =================
    @staticmethod
    def formatar_data(data):
        """
        Formata data Firestore para formato legível
        """
        try:
            # Timestamp Firestore
            if hasattr(data, "to_datetime"):
                data = data.to_datetime()

            # Converter UTC -> Brasil
            data_local = data.astimezone(
                timezone(timedelta(hours=-3))
            )

            return data_local.strftime("%d/%m/%Y %H:%M")

        except:
            return "Sem data"

    # ================= CONFERENTES =================
    def carregar_conferentes(self):
        """Carrega lista de conferentes"""
        try:
            return [
                d.to_dict().get("nome")
                for d in self.db.collection("conferentes").stream()
                if d.to_dict().get("nome")
            ]
        except Exception as e:
            print(f"Erro ao carregar conferentes: {e}")
            return []

    def salvar_conferente(self, nome):
        """Salva novo conferente"""
        try:
            self.db.collection("conferentes").document(
                nome.lower()
            ).set({"nome": nome})
            return True
        except Exception as e:
            print(f"Erro ao salvar conferente: {e}")
            return False

    # ================= BOXES =================
    def carregar_boxes(self):
        """Carrega lista de boxes"""
        try:
            return [
                d.to_dict().get("nome")
                for d in self.db.collection("boxes").stream()
                if d.to_dict().get("nome")
            ]
        except Exception as e:
            print(f"Erro ao carregar boxes: {e}")
            return []

    def salvar_box(self, nome):
        """Salva novo box"""
        try:
            self.db.collection("boxes").document(
                nome.lower()
            ).set({"nome": nome})
            return True
        except Exception as e:
            print(f"Erro ao salvar box: {e}")
            return False

    # ================= SEPARADORES =================
    def carregar_separadores(self):
        """Carrega lista de separadores"""
        try:
            return [
                d.to_dict().get("nome")
                for d in self.db.collection("separadores").stream()
                if d.to_dict().get("nome")
            ]
        except Exception as e:
            print(f"Erro ao carregar separadores: {e}")
            return []

    def salvar_separador(self, nome):
        """Salva novo separador"""
        try:
            self.db.collection("separadores").document(
                nome.lower()
            ).set({"nome": nome})
            return True
        except Exception as e:
            print(f"Erro ao salvar separador: {e}")
            return False

    # ================= REGISTROS =================
    def salvar_registro(self, dados):
        """Salva novo registro de conferência"""
        try:
            self.db.collection("registros").add({
                **dados,
                "data_hora": firestore.SERVER_TIMESTAMP
            })
            return True
        except Exception as e:
            print(f"Erro ao salvar registro: {e}")
            return False

    def carregar_registros(self):
        """Carrega todos os registros ordenados por data"""
        try:
            return [
                d.to_dict()
                for d in self.db.collection("registros")
                .order_by(
                    "data_hora",
                    direction=firestore.Query.DESCENDING
                )
                .stream()
            ]
        except Exception as e:
            print(f"Erro ao carregar registros: {e}")
            return []

    # ================= SEPARAÇÃO =================
    def salvar_separacao(self, dados):
        """Salva novo registro de separação"""
        try:
            self.db.collection("separacao").add({
                **dados,
                "data_hora": firestore.SERVER_TIMESTAMP
            })
            return True
        except Exception as e:
            print(f"Erro ao salvar separação: {e}")
            return False

    def carregar_separacoes(self, inicio, fim):
        """Carrega separações em um período específico"""
        try:
            return [
                r.to_dict()
                for r in self.db.collection("separacao")
                .where("data_hora", ">=", inicio)
                .where("data_hora", "<=", fim)
                .stream()
            ]
        except Exception as e:
            print(f"Erro ao carregar separações: {e}")
            return []

    # ================= RANKING =================
    def carregar_registros_semana(self, inicio, fim):
        """Carrega registros da semana para ranking"""
        try:
            return [
                r.to_dict()
                for r in self.db.collection("registros")
                .where("data_hora", ">=", inicio)
                .where("data_hora", "<=", fim)
                .stream()
            ]
        except Exception as e:
            print(f"Erro ao carregar registros da semana: {e}")
            return []
