from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
 
from campo_minado import Campo_minado
from campo_minado_1facil import CampoMinadoFacil
from construtor_campo_minado import ConstrutorCampoMinado

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
        self.botao_de_alternar= Button(text="Marcar bombas", size_hint=(1, 0.50)) 
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
# tem menu de contexto


    # def revelar_mina(self, botao_do_campo):
    #     if botao_do_campo.text!="":
    #         return
        
    #     coordenadas=self.botoes[botao_do_campo]
    #     tem_bomba= self.jogo.verificacao_da_casa(coordenadas, self.minas)
        
        
    #     if tem_bomba == True:
    #         #funcao para pintar de vermelho
    #         perdeu=Popup(title="Voce perdeu", content=Label(text="Você perdeu!"), size_hint=(0.50, 0.25))
    #         perdeu.bind(on_dismiss=self.voltar_para_tela_inicial)
    #         perdeu.open()
    #         return
        

    #     contagem=self.jogo.pega_vizinhos(x=coordenadas[0], y=coordenadas[1], lista_minas=self.minas)
    #     botao_do_campo.text=str(contagem)
    #     self.lista_de_coordenadas.append(coordenadas)
    #     casas_a_percorrer = self.jogo.linhas * self.jogo.colunas - self.jogo.minas
    #     if len(self.lista_de_coordenadas) == casas_a_percorrer:
    #         ganhou=Popup(title="Voce ganhou!", content=Label(text="Parabéns! Você ganhou!"), size_hint=(0.50, 0.25))
    #         ganhou.bind(on_dismiss=self.voltar_para_tela_inicial)
    #         ganhou.open()




CampoMinadoAndroid().run()