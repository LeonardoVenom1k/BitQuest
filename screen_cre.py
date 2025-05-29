import pygame
import sys

def tela_creditos():
    pygame.init()
    tela = pygame.display.set_mode((1366, 768))
    pygame.display.set_caption("Créditos")

    # Usando a fonte Arial
    font = pygame.font.SysFont("Arial", 30)

    # Mensagens de créditos
    creditos = [
        "Desenvolvedores: Leonardo Davi, Luca Mol, Victor Leão",
        "Contribuidores: Ninguem",
        "Fontes e Referencias: João Tinti (Canal no Youtube)",
        "Agradecimentos Especiais: Eunice Gomes, Roberto Porto",
        "",
        "Pressione ESC para voltar ao menu principal."
    ]

    while True:
        tela.fill((0, 0, 0))  # Cor de fundo preta

        # Renderizar cada linha de créditos
        for i, linha in enumerate(creditos):
            texto = font.render(linha, True, (255, 255, 255))  # Texto branco
            # Centralizar a linha
            largura_texto = texto.get_width()
            pos_x = (1366 - largura_texto) // 2  # Calcular posição x centralizada
            tela.blit(texto, (pos_x, 100 + i * 50))  # Ajustar o espaçamento para 50

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    voltar_menu()
                    
def voltar_menu():
    from main_menu import menu_principal
    menu_principal()
