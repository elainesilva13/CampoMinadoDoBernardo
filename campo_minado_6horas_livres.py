from campo_minado import Campo_minado


class CampoMinadoHorasLivres(Campo_minado):
    def __init__(self):
        super().__init__(linhas=17, colunas=17, minas=20)
