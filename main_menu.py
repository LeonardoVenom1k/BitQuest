import pygame
import sys
from screens import desenhar_botao

# Função para carregar o estado da música de um arquivo
def carregar_estado_musica():
    try:
        with open("saves/volume/estado_musica.txt", "r") as arquivo:
            estado = arquivo.read().strip()
            return estado == "1"
    except FileNotFoundError:
        return True  # Música ativa por padrão se o arquivo não for encontrado

# Função para carregar o estado do volume de um arquivo
def carregar_volume():
    try:
        with open("saves/volume/estado_volume.txt", "r") as arquivo:
            volume = float(arquivo.read())
            return volume
    except FileNotFoundError:
        return 0.5  # Volume padrão se o arquivo não for encontrado

# Variável global para o estado da música
musica_tocando = True  # Assume que a música deve tocar por padrão

def menu_principal():
    global musica_tocando  # Acesse a variável global

    pygame.init()
    pygame.mixer.init()
    tela = pygame.display.set_mode((1366, 768))  # Dimensões da tela
    pygame.display.set_caption("Menu Principal")

    # Carrega o volume e o estado da música
    volume_atual = carregar_volume()
    musica_tocando = carregar_estado_musica()

    # Configura o volume da música
    pygame.mixer.music.set_volume(volume_atual)

    # Verifique se a música não está tocando e se deve tocar
    if musica_tocando and not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('assets/sounds/musicgame.mp3')
        pygame.mixer.music.play(-1)
    elif not musica_tocando:  # Se música está desligada
        pygame.mixer.music.stop()

    font_titulo = pygame.font.Font("assets/fonts/PropolishRufftu-BLLyd.ttf", 150)
    font_botoes = pygame.font.Font("assets/fonts/PropolishRufftu-BLLyd.ttf", 50)
    
    # Defina as cores
    cor_titulo = (0, 0, 0)  # Cor preta para o título
    cor_sombra = (100, 100, 100)  # Cor para a sombra (tom de cinza)
    cor_botao = (255, 215, 0)  # Amarelo claro (cor dos botões)

    # Renderize o texto do título com efeito 3D (sombra)
    texto_titulo = font_titulo.render("BITQUEST", True, cor_titulo)
    sombra_titulo = font_titulo.render("BITQUEST", True, cor_sombra)

    # Defina os textos dos botões
    botoes_textos = ['ESCOLHER NIVEIS', 'EXIBIR RANKINGS', 'CONFIGURAÇÕES', 'SAIR']

    # Carregar e redimensionar a imagem de fundo
    imagem_fundo = pygame.image.load('assets/images/backgroundgame.jpg')  # Caminho atualizado
    imagem_fundo = pygame.transform.scale(imagem_fundo, (1366, 768))  # Redimensiona a imagem para o tamanho da tela

    # Carregar a imagem do botão de informações
    imagem_info = pygame.image.load('assets/images/information_button.png')
    imagem_info = pygame.transform.scale(imagem_info, (50, 50))

    # Definir a posição do botão de informações no canto inferior direito
    largura_tela, altura_tela = tela.get_size()
    largura_info, altura_info = imagem_info.get_size()
    pos_info = (largura_tela - largura_info - 150, altura_tela - altura_info - 200)  # Margem de 150 e 200 megapixels

    while True:
        # Desenhar a imagem de fundo redimensionada
        tela.blit(imagem_fundo, (0, 0))

        # Centralizar o título com efeito 3D e desenhá-lo
        x_centro_titulo = 1366 / 2 - texto_titulo.get_width() / 2
        y_titulo = 100

        # Desenhar a sombra primeiro, deslocada levemente
        tela.blit(sombra_titulo, (x_centro_titulo + 5, y_titulo + 5))

        # Desenhar o texto do título acima da sombra
        tela.blit(texto_titulo, (x_centro_titulo, y_titulo))

        # Centralizar e desenhar os botões
        mouse_pos = pygame.mouse.get_pos()
        espacamento = 55  # Espaçamento entre os botões
        y_inicial = 300  # Posição Y inicial para o primeiro botão

        for i, texto in enumerate(botoes_textos):
            # Renderizar o texto do botão
            texto_botao = font_botoes.render(texto, True, cor_botao)
            texto_botao_pos = (1366 / 2 - texto_botao.get_width() / 2, y_inicial + i * espacamento)
            
            # Expanda a área de clique dos botões
            area_botao = pygame.Rect(texto_botao_pos[0] - 10, texto_botao_pos[1] - 10, 
                                     texto_botao.get_width() + 120, texto_botao.get_height() + 20)

            # Verificar se o mouse está sobre o botão
            if area_botao.collidepoint(mouse_pos):
                cor_hover = (255, 255, 255)  # Cor do texto ao passar o mouse (branca)
                texto_botao_hover = font_botoes.render(texto, True, cor_hover)
                texto_botao_hover.set_alpha(150)  # Reduzir a opacidade no hover
                tela.blit(texto_botao_hover, texto_botao_pos)
            else:
                # Desenhar o botão normalmente
                tela.blit(texto_botao, texto_botao_pos)

        # Verificar se o mouse está sobre o botão de informações
        if pygame.Rect(pos_info, imagem_info.get_size()).collidepoint(mouse_pos):
            imagem_info.set_alpha(150)  # Define a opacidade reduzida
        else:
            imagem_info.set_alpha(255)  # Opacidade normal

        # Desenhar o botão de informações no canto inferior direito
        tela.blit(imagem_info, pos_info)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botão esquerdo do mouse
                    for i in range(len(botoes_textos)):
                        area_botao = pygame.Rect((1366 / 2 - texto_botao.get_width() / 2) - 105, 
                                                  y_inicial + i * espacamento - 10, 
                                                  texto_botao.get_width() + 215, 
                                                  texto_botao.get_height() + 20)
                        if area_botao.collidepoint(evento.pos):
                            if i == 0:
                                escolher()
                            elif i == 1:
                                Rankings()
                            elif i == 2:
                                configuracoes_de_tela()
                            elif i == 3:
                                pygame.quit()
                                sys.exit()
                    if pygame.Rect(pos_info, imagem_info.get_size()).collidepoint(evento.pos):
                        mostrar_informacoes()

def Rankings():
    from Rankings import exibir_ranking_nivel1
    exibir_ranking_nivel1()

def escolher():
    from Select_Level import selecionar
    selecionar()

def configuracoes_de_tela():
    from config_screen import tela_configuracoes
    global musica_tocando  # Acesse a variável global para atualizá-la
    tela_configuracoes()  # Chama a tela de configurações
    # Atualiza a variável musica_tocando com base no estado da música
    musica_tocando = pygame.mixer.music.get_busy()  # Se a música estiver tocando, mantém True, caso contrário, False

def mostrar_informacoes():
    from screen_cre import tela_creditos
    tela_creditos()

menu_principal()
