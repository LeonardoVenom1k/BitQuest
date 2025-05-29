import pygame
import sys

# Variável global para o estado da música
musica_ativa = True

# Função para salvar o estado da música em um arquivo
def salvar_estado_musica(estado_musica):
    with open("saves/volume/estado_musica.txt", "w") as arquivo:
        arquivo.write("1" if estado_musica else "0")

# Função para carregar o estado da música de um arquivo
def carregar_estado_musica():
    try:
        with open("saves/volume/estado_musica.txt", "r") as arquivo:
            estado = arquivo.read().strip()
            return estado == "1"
    except FileNotFoundError:
        return True  # Música ativa por padrão se o arquivo não for encontrado

# Função para salvar o estado do volume em um arquivo
def salvar_volume(volume):
    with open("saves/volume/estado_volume.txt", "w") as arquivo:
        arquivo.write(str(volume))

# Função para carregar o estado do volume de um arquivo
def carregar_volume():
    try:
        with open("saves/volume/estado_volume.txt", "r") as arquivo:
            volume = float(arquivo.read())
            return volume
    except FileNotFoundError:
        return 0.5  # Volume padrão se o arquivo não for encontrado

def tela_configuracoes():
    global musica_ativa  # Referencia a variável global musica_ativa
    pygame.init()
    pygame.mixer.init()

    # Inicializa a tela no modo janela
    largura_tela, altura_tela = 1366, 768
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Configurações")

    # Carrega a imagem de fundo
    imagem_fundo = pygame.image.load('assets/images/backgroundgame.jpg')
    imagem_fundo = pygame.transform.scale(imagem_fundo, (largura_tela, altura_tela))

    # Carrega a fonte personalizada
    fonte = pygame.font.Font('assets/fonts/PropolishRufftu-BLLyd.ttf', 50)

    # Carrega o volume e o estado da música salvos
    volume_atual = carregar_volume()
    pygame.mixer.music.set_volume(volume_atual)
    musica_ativa = carregar_estado_musica()

    # Se a música não estiver ativa, pare a reprodução
    if not musica_ativa:
        pygame.mixer.music.stop()

    # Definição do slider de volume
    slider_rect = pygame.Rect(533, 350, 300, 10)
    cursor_pos = (533 + volume_atual * 300, 340)
    cursor_radius = 20  # Raio do cursor aumentado

    arrastando_cursor = False

    # Função auxiliar para desenhar textos
    def desenhar_texto(texto, y):
        texto_renderizado = fonte.render(texto, True, (255, 255, 0))
        rect_texto = texto_renderizado.get_rect(center=(largura_tela / 2, y))

        # Detecta se o mouse está sobre o botão
        mouse_pos = pygame.mouse.get_pos()
        if rect_texto.collidepoint(mouse_pos):
            texto_renderizado.set_alpha(150)  # Reduz opacidade no hover
        else:
            texto_renderizado.set_alpha(255)  # Opacidade normal

        # Desenha o texto com a opacidade ajustada
        tela.blit(texto_renderizado, rect_texto.topleft)
        return rect_texto  # Retorna o rect do texto para detecção de clique

    while True:
        # Desenha a imagem de fundo
        tela.blit(imagem_fundo, (0, 0))

        # Atualiza o texto da música conforme o estado
        texto_musica = 'Desligar Música' if musica_ativa else 'Ligar Música'

        # Desenha os textos e obtém os rects
        rect_musica = desenhar_texto(texto_musica, 200)
        rect_voltar = desenhar_texto('Voltar', 500)

        # Desenha a barra de volume com bordas arredondadas
        pygame.draw.rect(tela, (255, 255, 255), slider_rect, border_radius=5)  # Barra de volume com bordas arredondadas
        pygame.draw.circle(tela, (255, 255, 0), (int(cursor_pos[0]), int(cursor_pos[1] + 15)), cursor_radius)  # Cursor amarelo

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    # Verifica se o botão de música foi clicado
                    if rect_musica.collidepoint(pygame.mouse.get_pos()):
                        if musica_ativa:
                            pygame.mixer.music.stop()
                        else:
                            pygame.mixer.music.load('assets/sounds/musicgame.mp3')
                            pygame.mixer.music.play(-1)
                        musica_ativa = not musica_ativa

                    # Verifica se o botão "Voltar" foi clicado
                    if rect_voltar.collidepoint(pygame.mouse.get_pos()):
                        salvar_volume(volume_atual)  # Salva o estado do volume ao sair
                        salvar_estado_musica(musica_ativa)  # Salva o estado da música ao sair
                        return  # Volta para o menu principal

                    # Detecta se clicou no cursor do volume
                    cursor_rect = pygame.Rect(cursor_pos[0] - cursor_radius, cursor_pos[1] - cursor_radius, cursor_radius * 2, cursor_radius * 2)
                    if cursor_rect.collidepoint(evento.pos):
                        arrastando_cursor = True

            if evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    arrastando_cursor = False

            if evento.type == pygame.MOUSEMOTION:
                if arrastando_cursor:
                    # Atualiza a posição do cursor e o volume
                    cursor_pos = (min(max(evento.pos[0], slider_rect.x), slider_rect.x + slider_rect.width), 340)
                    volume_atual = (cursor_pos[0] - slider_rect.x) / slider_rect.width
                    pygame.mixer.music.set_volume(volume_atual)

        # Atualiza a posição do cursor
        cursor_pos = (533 + volume_atual * 300, 340)  # Mantém a posição atual do cursor
