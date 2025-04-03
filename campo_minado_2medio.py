from campo_minado import Campo_minado


class CampoMinadoMedio(Campo_minado):
    def __init__(self):
        super().__init__(linhas=6, colunas=6, minas=4)
