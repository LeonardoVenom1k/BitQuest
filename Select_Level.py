import pygame
import sys

def desenhar_botao_redondo(tela, texto, posicao, tamanho, cor_normal, fonte):
    # Desenha a sombra do botão (efeito 3D)
    sombra_rect = pygame.Rect(posicao[0] + 5, posicao[1] + 5, tamanho[0], tamanho[1])
    pygame.draw.rect(tela, (0, 0, 0, 128), sombra_rect, border_radius=20)  # Sombra em preto semi-transparente

    # Desenha o botão arredondado
    rect = pygame.Rect(posicao, tamanho)
    pygame.draw.rect(tela, cor_normal, rect, border_radius=20)  # 20 é o raio das bordas

    # Renderiza o texto do botão com contorno
    contorno_texto = fonte.render(texto, True, (0, 0, 0))  # Contorno em preto
    texto_renderizado = fonte.render(texto, True, (255, 255, 255))  # Texto em branco

    texto_rect = texto_renderizado.get_rect(center=rect.center)  # Centraliza o texto

    # Desenha o contorno em preto
    for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        tela.blit(contorno_texto, texto_rect.move(dx, dy))

    # Desenha o texto em branco sobre o contorno
    tela.blit(texto_renderizado, texto_rect)

def selecionar():
    pygame.init()
    tela = pygame.display.set_mode((1366, 768))
    pygame.display.set_caption("Selecionar Nível")

    # Carregar a imagem de fundo
    imagem_fundo = pygame.image.load('assets/images/backgroundgame.jpg')  # Altere para o caminho da sua imagem
    imagem_fundo = pygame.transform.scale(imagem_fundo, (1366, 768))  # Redimensiona para o tamanho da tela

    # Ajustando a posição dos botões
    botoes = {
        'Nível 1': pygame.Rect(150, 100, 200, 50),
        'Nível 2': pygame.Rect(550, 100, 200, 50),
        'Nível 3': pygame.Rect(1000, 100, 200, 50),
        'Nível 4': pygame.Rect(150, 300, 200, 50),
        'Nível 5': pygame.Rect(550, 300, 200, 50),
        'Nível 6': pygame.Rect(1000, 300, 200, 50),
        'Voltar': pygame.Rect(550, 500, 200, 50),  # Centralizado na parte inferior
    }

    # Definindo as cores dos botões
    cores_botao = {
        'Nível 1': (0, 128, 0),      # Verde escuro
        'Nível 2': (85, 107, 47),    # Verde oliva
        'Nível 3': (255, 215, 0),    # Amarelo dourado
        'Nível 4': (255, 140, 0),    # Laranja escuro
        'Nível 5': (139, 0, 0),      # Vermelho escuro
        'Nível 6': (128, 0, 128),    # Vinho
        'Voltar': (50, 50, 50),      # Cinza escuro para o botão Voltar
    }

    # Tente carregar a fonte desejada
    try:
        fonte = pygame.font.Font('assets/fonts/PropolishRufftu-BLLyd.ttf', 40)  # Aumente o tamanho da fonte
    except FileNotFoundError:
        print("Fonte não encontrada, usando fonte padrão.")
        fonte = pygame.font.SysFont('arial', 40)  # Usar fonte padrão caso a personalizada não seja encontrada

    while True:
        # Desenha a imagem de fundo
        tela.blit(imagem_fundo, (0, 0))

        # Desenha os botões
        for texto, rect in botoes.items():
            # Verifica se o mouse está sobre o botão
            if rect.collidepoint(pygame.mouse.get_pos()):
                # Mudar a cor ao passar o mouse
                cor_normal = (min(255, cores_botao[texto][0] + 100), 
                              min(255, cores_botao[texto][1] + 100), 
                              min(255, cores_botao[texto][2] + 100))  # Aumenta a luminosidade da cor
            else:
                cor_normal = cores_botao[texto]
            
            desenhar_botao_redondo(
                tela,
                texto,
                rect.topleft,
                rect.size,
                cor_normal=cor_normal,
                fonte=fonte
            )

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Verifica se é o clique esquerdo
                    if botoes['Nível 1'].collidepoint(evento.pos):
                        Nivel1()
                    elif botoes['Nível 2'].collidepoint(evento.pos):
                        Nivel2()
                    elif botoes['Nível 3'].collidepoint(evento.pos):
                        Nivel3()
                    elif botoes['Nível 4'].collidepoint(evento.pos):
                        Nivel4()
                    elif botoes['Nível 5'].collidepoint(evento.pos):
                        Nivel5()
                    elif botoes['Nível 6'].collidepoint(evento.pos):
                        Nivel6()
                    elif botoes['Voltar'].collidepoint(evento.pos):
                        voltar_menu()

# Funções para carregar os níveis
def Nivel1():
    from Level1 import nivel1
    nivel1()

def Nivel2():
    from Level2 import nivel2
    nivel2()

def Nivel3():
    from Level3 import nivel3
    nivel3()

def Nivel4():
    from Level4 import nivel4
    nivel4()

def Nivel5():
    from Level5 import nivel5
    nivel5()

def Nivel6():
    from Level6 import nivel6
    nivel6()

def voltar_menu():
    from main_menu import menu_principal
    menu_principal()

selecionar()
