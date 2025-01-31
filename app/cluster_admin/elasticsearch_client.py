from elasticsearch import Elasticsearch

class ElasticsearchClient:
    def __init__(self, session):
        """
        Inicializa o cliente Elasticsearch com as informações da sessão.

        :param session: Objeto de sessão do Django contendo as credenciais do Elasticsearch.
        """
        es_config = session.get("elasticsearch")
        if not es_config:
            raise ValueError("Informações de conexão com o Elasticsearch não encontradas na sessão.")

        self.host = es_config.get("host")
        self.username = es_config.get("username")
        self.password = es_config.get("password")

        try:
            self.client = Elasticsearch(
                hosts=[self.host],
                basic_auth=(self.username, self.password)
            )
        except Exception as e:
            raise ConnectionError(f"Erro ao conectar ao Elasticsearch: {e}")

    def get_cluster_health(self):
        try:
            response = self.client.cluster.health()
            return response
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar informações de saúde do cluster: {e}")


    def get_cluster_stats(self):
        try:
            response = self.client.cluster.stats()
            return response
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar estatísticas do cluster: {e}")

    def get_cluster_settings(self):
        try:
            response = self.client.cluster.get_settings(include_defaults=True)
            return response
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar settings do cluster: {e}")