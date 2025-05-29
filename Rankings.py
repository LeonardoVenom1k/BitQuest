import pygame
import sys
import json

# Função para desenhar um botão 3D com bordas arredondadas
def desenhar_botao_3d(tela, texto, posicao, tamanho, cor_normal, cor_hover):
    x, y = posicao
    largura, altura = tamanho

    # Define o raio para as bordas arredondadas
    raio = 15

    # Cria um retângulo para o botão
    rect_inferior = pygame.Rect(x, y, largura, altura)
    rect_superior = pygame.Rect(x + 5, y + 5, largura, altura)

    # Desenha o botão 3D
    pygame.draw.rect(tela, cor_hover, rect_superior, border_radius=raio)  # Efeito de sombra
    pygame.draw.rect(tela, cor_normal, rect_inferior, border_radius=raio)  # Botão normal

    # Renderiza o texto
    font = pygame.font.SysFont("Arial", 30)
    texto_renderizado = font.render(texto, True, (255, 255, 255))  # Cor do texto
    texto_rect = texto_renderizado.get_rect(center=(x + largura // 2, y + altura // 2))
    tela.blit(texto_renderizado, texto_rect)

# Função para exibir o ranking do Nível 1 com botões de navegação
def exibir_ranking_nivel1():
    exibir_ranking("saves/points/ranking.json", "Ranking - Nível 1", exibir_ranking_nivel2, None)

# Função para exibir o ranking do Nível 2
def exibir_ranking_nivel2():
    exibir_ranking("saves/points/ranking2.json", "Ranking - Nível 2", exibir_ranking_nivel3, exibir_ranking_nivel1)

# Função para exibir o ranking do Nível 3
def exibir_ranking_nivel3():
    exibir_ranking("saves/points/ranking3.json", "Ranking - Nível 3", exibir_ranking_nivel4, exibir_ranking_nivel2)

# Função para exibir o ranking do Nível 4
def exibir_ranking_nivel4():
    exibir_ranking("saves/points/ranking4.json", "Ranking - Nível 4", exibir_ranking_nivel5, exibir_ranking_nivel3)

# Função para exibir o ranking do Nível 5
def exibir_ranking_nivel5():
    exibir_ranking("saves/points/ranking5.json", "Ranking - Nível 5", exibir_ranking_nivel6, exibir_ranking_nivel4)

# Função para exibir o ranking do Nível 6
def exibir_ranking_nivel6():
    exibir_ranking("saves/points/ranking6.json", "Ranking - Nível 6", None, exibir_ranking_nivel5)

# Função genérica para exibir o ranking
# Função genérica para exibir o ranking
def exibir_ranking(arquivo_ranking, titulo_texto, proxima_funcao, voltar_funcao):
    pygame.init()
    tela = pygame.display.set_mode((1366, 768))
    pygame.display.set_caption(titulo_texto)

    font_titulo = pygame.font.Font("assets/fonts/PropolishRufftu-BLLyd.ttf", 70)
    font = pygame.font.SysFont("Arial", 40)

    # Carrega o ranking do arquivo JSON
    try:
        with open(arquivo_ranking, 'r') as f:
            ranking = json.load(f)
    except FileNotFoundError:
        ranking = []

    # Carrega e redimensiona a imagem de fundo
    imagem_fundo = pygame.image.load('assets/images/backgroundgame.jpg')
    imagem_fundo = pygame.transform.scale(imagem_fundo, (1366, 768))

    # Desenha a imagem de fundo na tela
    tela.blit(imagem_fundo, (0, 0))

    # Exibe o título em 3D
    sombra_titulo = font_titulo.render(titulo_texto, True, (50, 50, 50))
    titulo_x = (1366 - sombra_titulo.get_width()) // 2
    tela.blit(sombra_titulo, (titulo_x + 5, 95))  # Deslocado

    # Título principal em amarelo
    texto_titulo = font_titulo.render(titulo_texto, True, (255, 255, 0))
    tela.blit(texto_titulo, (titulo_x, 95))

    # Exibe o ranking
    y_offset = 200
    if ranking:
        for i, recorde in enumerate(ranking[:5]):
            text = font.render(f"{i + 1}. {recorde['nome']} - {recorde['pontos']} pontos", True, (0, 0, 0))
            tela.blit(text, (200, y_offset))
            y_offset += 50
    else:
        text = font.render("Nenhum recorde registrado", True, (0, 0, 0))
        tela.blit(text, (200, y_offset))

    # Desenha os botões
    botoes = {
        'Sair': pygame.Rect(435, 500, 200, 50),
        'Resetar': pygame.Rect(720, 500, 200, 50)  # Botão Resetar
    }

    if titulo_texto != "Ranking - Nível 1":
        botoes['Voltar'] = pygame.Rect(155, 500, 200, 50)

    if titulo_texto != "Ranking - Nível 6":
        botoes['Avançar'] = pygame.Rect(1000, 500, 200, 50)

    # Detecta a posição do mouse para aplicar o efeito hover
    mouse_pos = pygame.mouse.get_pos()

    for texto, rect in botoes.items():
        cor_normal = (50, 50, 50)
        cor_hover = (100, 100, 100)

        # Se o mouse estiver sobre o botão, mude a cor normal para um tom mais claro
        if rect.collidepoint(mouse_pos):
            cor_normal = (150, 150, 150)  # Cor do botão ao passar o mouse
            cor_hover = (200, 200, 200)  # Cor do hover para um efeito mais claro

        desenhar_botao_3d(tela, texto, rect.topleft, rect.size, cor_normal, cor_hover)

    pygame.display.flip()

    # Espera até que o usuário clique em um botão ou feche a tela
    esperar_interacao_ranking(botoes, tela, proxima_funcao, voltar_funcao, arquivo_ranking)

# Função para interagir com os botões do ranking
def esperar_interacao_ranking(botoes, tela, proxima_funcao, voltar_funcao, arquivo_ranking):
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Verifica se houve clique
                    if 'Voltar' in botoes and botoes['Voltar'].collidepoint(evento.pos):
                        if voltar_funcao:
                            voltar_funcao()
                    elif 'Avançar' in botoes and botoes['Avançar'].collidepoint(evento.pos):
                        if proxima_funcao:  # Verifica se proxima_funcao não é None
                            proxima_funcao()  # Avança para o próximo ranking
                    elif botoes['Sair'].collidepoint(evento.pos):
                        voltar_menu()
                    elif botoes['Resetar'].collidepoint(evento.pos):  # Verifica o clique no botão Resetar
                        resetar_ranking(arquivo_ranking)  # Chama a função de reset
                        exibir_ranking(arquivo_ranking, pygame.display.get_caption()[0], proxima_funcao, voltar_funcao)

# Função para resetar o ranking
def resetar_ranking(arquivo_ranking):
    with open(arquivo_ranking, 'w') as f:
        json.dump([], f)
    print(f"Ranking resetado em {arquivo_ranking}")

# Função para salvar o ranking específico do Nível 1
def salvar_ranking_nivel1(nome, pontosjg):
    salvar_ranking_especifico("saves/points/ranking.json", nome, pontosjg)

# Função para salvar o ranking específico do Nível 2
def salvar_ranking_nivel2(nome, pontosjg):
    salvar_ranking_especifico("saves/points/ranking2.json", nome, pontosjg)

# Função para salvar o ranking específico do Nível 3
def salvar_ranking_nivel3(nome, pontosjg):
    salvar_ranking_especifico("saves/points/ranking3.json", nome, pontosjg)

# Função para salvar o ranking específico do Nível 4
def salvar_ranking_nivel4(nome, pontosjg):
    salvar_ranking_especifico("saves/points/ranking4.json", nome, pontosjg)

# Função para salvar o ranking específico do Nível 5
def salvar_ranking_nivel5(nome, pontosjg):
    salvar_ranking_especifico("saves/points/ranking5.json", nome, pontosjg)

# Função para salvar o ranking específico do Nível 6
def salvar_ranking_nivel6(nome, pontosjg):
    salvar_ranking_especifico("saves/points/ranking6.json", nome, pontosjg)

# Função para salvar os rankings
def salvar_ranking_especifico(arquivo_ranking, nome, pontosjg):
    try:
        with open(arquivo_ranking, 'r') as f:
            ranking = json.load(f)
    except FileNotFoundError:
        ranking = []

    # Adiciona o novo resultado ao ranking
    ranking.append({'nome': nome, 'pontos': pontosjg})

    # Ordena o ranking pelos pontos em ordem decrescente
    ranking = sorted(ranking, key=lambda x: x['pontos'], reverse=True)

    # Salva o ranking atualizado
    with open(arquivo_ranking, 'w') as f:
        json.dump(ranking, f)

# Função para voltar ao menu principal
def voltar_menu():
    from main_menu import menu_principal
    menu_principal()
