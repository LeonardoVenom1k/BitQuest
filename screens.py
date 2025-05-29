import pygame
import textwrap

def quebrar_texto(texto, largura):
    return textwrap.fill(texto, width=largura).splitlines()


# Função para desenhar texto com suporte a quebra de linha com '\n' e centralizado
def desenhar_texto(surface, texto, cor, x, y, fonte_size=50):
    fonte = pygame.font.Font(None, fonte_size)
    linhas = texto.split('\n')  # Divide o texto em linhas com base no '\n'
    
    # Calcula a altura total do texto para centralizar
    altura_total = sum([fonte.size(linha)[1] for linha in linhas])
    y -= altura_total // 2  # Ajusta para centralizar verticalmente

    for linha in linhas:
        texto_surf = fonte.render(linha, True, cor)
        texto_rect = texto_surf.get_rect(midtop=(x, y))
        surface.blit(texto_surf, texto_rect)
        y += texto_surf.get_height()  # Move a posição Y para a próxima linha

# Função para desenhar o botão
def desenhar_botao(surface, texto, pos, tamanho, cor_normal, cor_hover, cor_click, opacidade=255, fonte_size=50):
    x, y = pos
    largura, altura = tamanho

    # Criação do botão
    botao = pygame.Surface((largura, altura))
    botao.set_alpha(opacidade)
    
    # Determinar a cor do botão
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    
    if pygame.Rect(x, y, largura, altura).collidepoint(mouse_pos):
        if mouse_click[0]:  # Botão esquerdo do mouse
            cor_atual = cor_click
        else:
            cor_atual = cor_hover
    else:
        cor_atual = cor_normal
    
    botao.fill(cor_atual)
    surface.blit(botao, (x, y))
    
    # Centraliza o texto dentro do botão
    desenhar_texto(surface, texto, (255, 255, 255), x + largura // 2, y + altura // 2, fonte_size)

# Função para desenhar o botão 'Voltar'
def desenhar_botao_voltar(surface, x, y, largura, altura):
    desenhar_botao(
        surface,
        "Voltar",
        (x, y),
        (largura, altura),
        cor_normal=(150, 150, 150),
        cor_hover=(200, 200, 200),
        cor_click=(100, 100, 100)
    )

    pygame.display.flip()

    pygame.quit()
