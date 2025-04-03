from campo_minado import Campo_minado


class CampoMinadoFacil(Campo_minado):
    def __init__(self):
        super().__init__(linhas=4, colunas=4, minas=2)
    #     self.vidas = 2

    # def verificacao_da_casa(self, coordenadas, localizacao_minas):
    #     if coordenadas in localizacao_minas:
    #         self.vidas -= 1
    #         if not self.vidas:
    #             print("Booooooooooooooommmmm!!!!")
    #             return True
    #         else:
    #             print(f"Aqui tinha uma bomba! agora você só tem {self.vidas}")

    #     return False

    # if not self.vidas
    #     if  self.vidas == 0
    #     if  self.vidas == None
    #     if  self.vidas == False
