from campo_minado_1facil import CampoMinadoFacil
from campo_minado_2medio import CampoMinadoMedio
from campo_minado_3dificil import CampoMinadoDificil
from campo_minado_4complicado import CampoMinadoComplicado
from campo_minado_5entediado import CampoMinadoEntediado
from campo_minado_6horas_livres import CampoMinadoHorasLivres


class ConstrutorCampoMinado:
    def __init__(self):
        self.dificuldades = {
            'Fácil': CampoMinadoFacil,
            'Médio': CampoMinadoMedio,
            'Difícil': CampoMinadoDificil,
            'Complicado': CampoMinadoComplicado,
            'Entediado': CampoMinadoEntediado,
            'Horas Livres': CampoMinadoHorasLivres,
        }

    def escolhe_campo(self):
        "Aqui serão exibidas as dificuldades e retornar-se-á um objeto do tipo Campo_minado de acordo com a escolha do usuário"
        while True:
            dificuldade = (input("""seja bem vindo(a) ao campo minado! Agora me diga, qual o nivel de dificuldade que voce gostaria de jogar?
                fácil
                        
                médio
                        
                dificil
                        
                complicado
                        
                entediado

                horas livres
                            
                            """).lower())

            if dificuldade == "facil":
                return CampoMinadoFacil()

            if dificuldade == "medio":
                return CampoMinadoMedio()

            if dificuldade == "dificil":
                return CampoMinadoDificil()

            if dificuldade == "complicado":

                return CampoMinadoComplicado()

            if dificuldade == "entediado":
                return CampoMinadoEntediado()

            if dificuldade == "horas livres":
                return CampoMinadoHorasLivres()
