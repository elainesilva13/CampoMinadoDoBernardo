from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
 
import random

class Campo_minado:  # instanciando a classe = criando a classe e colocando na prateleirinha
    "Esta classe serve como um molde para as outras classes campo minado, ou seja é a classe INTERFACE."

    "configurar campo"
    "configurar posição das minas"
    "verificar se pisou em mina"

    "exibir quantas minas estão no perimetro do local clicado"
    "desenhar o campo"

    def __init__(self, linhas, colunas, minas):
        self.linhas = linhas
        self.colunas = colunas
        self.minas = minas

    def jogo(self):
        "Função principal responsável pela execução de toda a lógica do jogo"
        # config = self.configuracoes()
        localizacao_das_minas = self.prepara_lista_de_minas()

        # print(localizacao_das_minas)
        explodiu = False
        lista_de_coordenadas = []
        casas_a_percorrer = self.linhas * self.colunas - self.minas
        while explodiu == False:
            self.campo(self.linhas, self.colunas, lista_de_coordenadas,
                       localizacao_das_minas)

            #  linhas, colunas, lista_de_coordenadas: list[list], lista_de_minas, fim_de_jogo=False)
            coordenadas_do_usuario = self.coordenadas()
            print(coordenadas_do_usuario)
            explodiu = self.verificacao_da_casa(
                coordenadas_do_usuario, localizacao_das_minas)
            if coordenadas_do_usuario not in lista_de_coordenadas:
                lista_de_coordenadas.append(coordenadas_do_usuario)
            else:
                print("Coordenada já foi digitada. Tente outra!")
            if len(lista_de_coordenadas) == casas_a_percorrer:
                print("Parabéns, você venceu!")
                break
        # self.campo(linhas, colunas, lista_de_coordenadas: list[list], lista_de_minas, fim_de_jogo=False)

    # def configuracoes(self):
    #     raise Exception("Definir a dificuldade")

    def prepara_lista_de_minas(self):
        lista_de_minas = []
        qtdminas = self.minas
        while qtdminas:

            linhas = self.linhas
            sorteia_linha = int(random.uniform(0, linhas))
            colunas = self.colunas
            sorteia_coluna = int(random.uniform(0, colunas))
            localizacao_da_mina = [sorteia_linha, sorteia_coluna]
            if localizacao_da_mina not in lista_de_minas:
                lista_de_minas .append(localizacao_da_mina)
                qtdminas -= 1
        return lista_de_minas

    def campo(self, linhas, colunas, lista_de_coordenadas: list[list], lista_de_minas, fim_de_jogo=False):
        print('\n ', end='   ')
        numeros = 0
        numeros2 = 0
        for numero in range(colunas):
            print(f"{numeros2:2}", end=" ")
            numeros2 += 1
        print("\n")
        for linha in range(linhas):
            for coluna in range(-1, colunas):
                if coluna == -1:
                    print(f"{numeros:2}", end="  ")

                    numeros += 1
                    continue
                if [linha, coluna] in lista_de_coordenadas and not fim_de_jogo:
                    bombas_vizinhas = self.pega_vizinhos(
                        x=linha, y=coluna, lista_minas=lista_de_minas)
                    print(bombas_vizinhas, end=" ")
                elif [linha, coluna] in lista_de_minas and fim_de_jogo:
                    print(" X", end=" ")
                else:
                    print(" .", end=" ")
            print("\n")

    def coordenadas(self):

        while True:
            coordenadas_das_linhas = input("Qual linha você deseja ir?    ")
            if not coordenadas_das_linhas.isnumeric():

                print("A sua coordenada não é válida. Digite novamente.")
                continue
            coordenadas_das_linhas = int(coordenadas_das_linhas)

            if coordenadas_das_linhas >= self.linhas:
                print(f"""A sua coordenada não é válida. Digite de 0 á {
                    self.linhas-1}.""")
                continue
            break

        while True:
            coordenadas_das_colunas = input("Qual coluna você deseja ir?    ")

            if not coordenadas_das_colunas.isnumeric():
                print("A sua coordenada não é válida. Digite novamente.")
                continue
            coordenadas_das_colunas = int(coordenadas_das_colunas)
            if coordenadas_das_colunas >= self.colunas:
                print(f"""A sua coordenada não é válida. Digite de 0 á {
                    self.colunas-1}.""")
                continue

            break
        return [coordenadas_das_linhas, coordenadas_das_colunas]

    def verificacao_da_casa(self, coordenadas, localizacao_minas):
        if coordenadas in localizacao_minas:
            print("Booooooooooooooommmmm!!!!")
            return True

        return False

    def pega_vizinhos(self, x, y, lista_minas) -> str:
        bombas_proximas = 0

        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Cima, Baixo, Esquerda, Direita
                    (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonais

        for dx, dy in direcoes:
            viz_x, viz_y = x + dx, y + dy

            if [viz_x, viz_y] in lista_minas:
                bombas_proximas += 1

        return f"{bombas_proximas:2}"


class CampoMinadoFacil(Campo_minado):
    def __init__(self):
        super().__init__(linhas=4, colunas=4, minas=2)


class CampoMinadoMedio(Campo_minado):
    def __init__(self):
        super().__init__(linhas=6, colunas=6, minas=4)


class CampoMinadoDificil(Campo_minado):
    def __init__(self):
        super().__init__(linhas=9, colunas=9, minas=8)


class CampoMinadoComplicado(Campo_minado):
    def __init__(self):
        super().__init__(linhas=13, colunas=13, minas=15)


class CampoMinadoEntediado(Campo_minado):
    def __init__(self):
        super().__init__(linhas=15, colunas=15, minas=18)


class CampoMinadoHorasLivres(Campo_minado):
    def __init__(self):
        super().__init__(linhas=17, colunas=17, minas=20)



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

        
class CampoMinadoAndroid(App):
    "A classe App (biblioteca kivy) trará para a class CampoMinadoAndroid as configurações necessárias para sua conversão em arquivo .apk (para publicação na loja andoid)"

    def build(self):
        self.title= "Campo Minado"

        Window.size = (Window.width , Window.height)
        # define o tamanho de tela que o jogo vai ocupar
        
        sm=ScreenManager()
        sm.add_widget(TelaInicial(name="tela_inicial"))
        sm.add_widget(TelaDeJogo(name="campo_minado"))
        return sm

class TelaInicial(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout= BoxLayout(orientation="vertical")
        self.construtor=ConstrutorCampoMinado() 
        self.layout.add_widget(
            Label( # caixa de texto
                text="Bem-vindo ao campo minado!",
                font_size=32,
                size_hint=(1,0.1)

            )
        )

        dificuldades=list(self.construtor.dificuldades.keys())

       
        for dificuldade in dificuldades:
            botao = Button(text=dificuldade, size_hint=(1, None), height=50)
            botao.bind(on_press=self.seleciona_dificuldade)
            self.layout.add_widget(botao)
        # self.layout.add_widget(Button(text=dificuldades[0], size_hint=(1, None), height=50))

        # self.layout.add_widget(Button(text=dificuldades[1], size_hint=(1, None), height=50))

        # self.layout.add_widget(Button(text=dificuldades[2], size_hint=(1, None), height=50))

        # self.layout.add_widget(Button(text=dificuldades[3], size_hint=(1, None), height=50))
        
        # self.layout.add_widget(Button(text=dificuldades[4], size_hint=(1, None), height=50))

        # self.layout.add_widget(Button(text=dificuldades[5], size_hint=(1, None), height=50))



      

        # botao = Button(text=dificuldade, size_hint=(1, None), height=50)

        self.add_widget(self.layout)
        

    def seleciona_dificuldade(self, botao:Button):
        nome_dificuldade=botao.text
        dicionario_dificuldaes=self.construtor.dificuldades
        campo_desligado= dicionario_dificuldaes[nome_dificuldade]
        campo_ligado=campo_desligado()
        self.manager.current="campo_minado"
        self.manager.get_screen("campo_minado").iniciar_jogo(campo_ligado)



class TelaDeJogo(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.lista_de_coordenadas=[]
        self.layout=BoxLayout(orientation="horizontal")
        barra_lateral=BoxLayout(orientation="vertical",size_hint=(0.15, 1),padding=[10,10,10,10])
        self.botao_de_desistir= Button(text="Desistir",size_hint=(1, 0.50))
        self.botao_de_desistir.bind(on_press=self.desistir_voltar)
        self.botao_de_alternar= Button(text="Marcar\nbombas", size_hint=(1, 0.50)) 
        barra_lateral.add_widget(self.botao_de_desistir)
        barra_lateral.add_widget(self.botao_de_alternar)
        self.layout.add_widget(barra_lateral)
        self.area_do_jogo=BoxLayout(orientation="horizontal",size_hint=(1, 1), padding=[10, 10, 10, 10])
        self.texto_da_area_do_jogo=Label(text="Campo minado", size_hint=(1, 0.5))
        self.area_do_jogo.add_widget(self.texto_da_area_do_jogo)
        self.layout.add_widget(self.area_do_jogo)
        self.add_widget(self.layout)
        self.abrindo_bombas=True
        self.jogo=None
        self.botoes={}

        
    def desistir_voltar(self,_):
        self.show_popup("Você desistiu do jogo!")

    def show_popup(self, mensagem):
        tela_de_desistiu=Popup(title="Fim de jogo", content=Label(text=mensagem), size_hint=(0.50, 0.25))
        tela_de_desistiu.bind(on_dismiss=self.voltar_para_tela_inicial)
        tela_de_desistiu.open()
        

    def voltar_para_tela_inicial(self, _):
        """Esta função será chamada quando o Popup for fechado."""
        self.manager.current = 'tela_inicial'  # Retorna para a tela inicial
 
    def iniciar_jogo(self, campo_ligado:Campo_minado): 

        self.perdeu= False
        self.jogo:Campo_minado=campo_ligado #campo_minado
        self.area_do_jogo.clear_widgets()
        self.area_do_jogo.cols=self.jogo.colunas

        self.minas=self.jogo.prepara_lista_de_minas()
        self.setup_botoes()

    def setup_botoes(self):
        # Adicionando botões do campo minado
        largura_do_grid = Window.width - 100  # Subtrai a largura da barra lateral
        altura_do_grid = Window.height  # O grid deve ocupar 100% da altura da tela

        w = largura_do_grid / self.jogo.colunas - 10  # Ajusta a largura dos botões
        h = altura_do_grid / self.jogo.linhas - 10  # Ajusta a altura dos botões

        grid = GridLayout(cols=self.jogo.colunas, padding=10, spacing=5)
        


            
        for linha in range(self.jogo.linhas):
            for coluna in range(self.jogo.colunas):
                botao_do_campo=Button(size_hint=(None, None), width=w, height=h)
                botao_do_campo.bind(on_press=self.revelar_mina)
                botao_do_campo.background_color=(0, 0.5, 0,1)
                botao_do_campo.background_normal=""
                grid.add_widget(botao_do_campo)
                self.botoes[botao_do_campo]=[linha, coluna]
        self.area_do_jogo.add_widget(grid)     
    def revelar_mina(self, botao_mina: Button):
        if self.perdeu:
            return
 
        if not self.abrindo_bombas:
            self.bandeira(botao_mina)
            return
 
        if botao_mina.background_normal != '':
            return
 
        if botao_mina.text != '':
            return
 
        coordenadas = self.botoes[botao_mina]
 
        if self.jogo.verificacao_da_casa(coordenadas, self.minas):
            self.show_popup("Boooooooooooooooooom! Você perdeu!")
            self.perdeu = True
            # self.mostrar_minas()  # Exibe as minas em vermelho
            self.botao_de_desistir.text = "Voltar"  # Altera o texto do botão para "Voltar"
        else:
            bombas_vizinhas = self.jogo.pega_vizinhos(
                coordenadas[0], coordenadas[1], self.minas)
            botao_mina.text = str(bombas_vizinhas)
            self.lista_de_coordenadas.append(coordenadas)
 
        if len(self.lista_de_coordenadas) == (self.jogo.linhas * self.jogo.colunas - self.jogo.minas):
            self.show_popup("Parabéns, você venceu!")


CampoMinadoAndroid().run()
