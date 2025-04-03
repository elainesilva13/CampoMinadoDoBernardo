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
from construtor_campo_minado import ConstrutorCampoMinado
 
VERMELHO = (1, 0, 0, 1)
VERDE_ESCURO = (0, 0.5, 0, 1)
CINZA = (0.5, 0.5, 0.5, 1)
COR_BOTOES = CINZA
 
 
class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.construtor = ConstrutorCampoMinado()
 
        # Adicionar título
        self.layout.add_widget(
            Label(text="Bem-vindo ao Campo Minado!", font_size=32, size_hint=(1, 0.1)))
 
        # Adicionar botoes de seleção de dificuldade
        dificuldades = list(self.construtor.dificuldades.keys())
 
        for dificuldade in dificuldades:
            botao = Button(text=dificuldade, size_hint=(1, None), height=50)
            botao.bind(on_press=self.seleciona_dificuldade)
            self.layout.add_widget(botao)
 
        self.add_widget(self.layout)
 
    def seleciona_dificuldade(self, botao_dificuldade: Button):
        campo = self.construtor.dificuldades[botao_dificuldade.text]()
 
        # Passar o objeto de dificuldade para a próxima tela
        self.manager.current = "campo_minado"
        self.manager.get_screen("campo_minado").iniciar_jogo(campo)
 
 
class TelaDeJogo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='horizontal')
 
        side_bar = BoxLayout(orientation='vertical', size_hint=(
            # Largura fixa da barra lateral
            0.15, 1), padding=[10, 10, 10, 10])
        self.desistir_botao = Button(
            text="Desistir", size_hint=(1, 0.5))  # Ocupa 50% da altura da tela
        self.desistir_botao.bind(on_press=self.voltar_ou_desistir)
 
        toggle_botao = Button(text="Marcar\nBombas",
                              # Ocupa 50% da altura da tela
                              size_hint=(1, 0.5))
        toggle_botao.bind(on_press=self.alternar_modos)
 
        side_bar.add_widget(self.desistir_botao)
        side_bar.add_widget(toggle_botao)
 
        # Layout principal do campo minado
        self.game_area = BoxLayout(
            # Vai ocupar 100% da altura e largura disponível
            orientation='horizontal', size_hint=(1, 1), padding=[10, 10, 10, 10])
        self.game_area.add_widget(
            # Placeholder
            Label(text="Campo Minado", size_hint=(1, None), height=40))
 
        # Adicionando a barra lateral e a área do jogo
        self.layout.add_widget(side_bar)
        self.layout.add_widget(self.game_area)
 
        self.add_widget(self.layout)
 
        self.abrindo_bombas = True
        self.jogo = None
        self.botoes = {}
 
    def iniciar_jogo(self, campo: Campo_minado):
        self.perdeu = False
        self.jogo = campo
        self.game_area.clear_widgets()  # Limpar campo existente
        self.game_area.cols = self.jogo.colunas  # Ajuste dinâmico das colunas do campo
 
        self.minas = self.jogo.prepara_lista_de_minas()
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
                botao = Button(size_hint=(None, None), width=w, height=h)
                botao.bind(on_press=self.revelar_mina)
                botao.background_color = COR_BOTOES
                botao.background_normal = ''
                grid.add_widget(botao)
                self.botoes[botao] = [linha, coluna]
 
        self.game_area.add_widget(grid)
 
    def bandeira(self, botao_mina: Button):
        if botao_mina.background_normal == '':
            botao_mina.background_normal = r'imagens/bandeirinha.png'
            return
        botao_mina.background_normal = ''
 
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
            self.mostrar_minas()  # Exibe as minas em vermelho
            self.desistir_botao.text = "Voltar"  # Altera o texto do botão para "Voltar"
        else:
            bombas_vizinhas = self.jogo.pega_vizinhos(
                coordenadas[0], coordenadas[1], self.minas)
            botao_mina.text = str(bombas_vizinhas)
            self.jogo.lista_de_coordenadas.append(coordenadas)
 
        if len(self.jogo.lista_de_coordenadas) == (self.jogo.linhas * self.jogo.colunas - self.jogo.minas):
            self.show_popup("Parabéns, você venceu!")
 
    def alternar_modos(self, instance):
        self.abrindo_bombas = not self.abrindo_bombas
        instance.text = "Abrir\nCampos" if not self.abrindo_bombas else "Marcar\nBombas"
 
    def mostrar_minas(self):
        """Alterar a cor dos botões que possuem minas para vermelho."""
        for botao, coordenadas in self.botoes.items():
            if coordenadas in self.minas:
                botao.background_color = VERMELHO
 
    def voltar_ou_desistir(self, _):
        """Alterar comportamento do botão 'Desistir' para 'Voltar'."""
        if self.desistir_botao.text == "Desistir":
            self.show_popup("Você desistiu do jogo!", True)
        else:
            # Navegar para a tela inicial quando "Voltar" for pressionado
            self.manager.current = "tela_inicial"  # Voltar para a tela inicial
 
    def show_popup(self, mensagem, voltar=False):
        popup = Popup(title="Fim de Jogo", content=Label(
            text=mensagem), size_hint=(None, None), size=(400, 400))
 
        if voltar:
            popup.bind(on_dismiss=self.voltar_para_tela_inicial)
 
        popup.open()
 
    def voltar_para_tela_inicial(self, instance):
        """Esta função será chamada quando o Popup for fechado."""
        self.manager.current = 'tela_inicial'  # Retorna para a tela inicial
 
 
class CampoMinadoApp(App):
    def build(self):
        self.title = "Campo Minado"
        Window.size = (Window.width, Window.height)
 
        sm = ScreenManager()
 
        sm.add_widget(TelaInicial(name="tela_inicial"))
        sm.add_widget(TelaDeJogo(name="campo_minado"))
 
        return sm
 
 
if __name__ == '__main__':
    CampoMinadoApp().run()
 
tem menu de contexto

