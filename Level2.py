import pygame
import sys
import json
import random  # Importa a biblioteca random
from screens import desenhar_botao
from Select_Level import selecionar

# Função para desenhar o botão "X" de voltar ao menu
def desenhar_botao_voltar(tela, font):
    largura_botao = 40
    altura_botao = 40
    pos_x = tela.get_width() - largura_botao - 125  # Posição no canto superior direito
    pos_y = 95

    # Obtém a posição do mouse
    mouse_pos = pygame.mouse.get_pos()

    # Cria uma superfície para o botão com suporte a transparência
    botao_surface = pygame.Surface((largura_botao, altura_botao), pygame.SRCALPHA)
    
    # Define a opacidade com base na posição do mouse
    if pygame.Rect(pos_x, pos_y, largura_botao, altura_botao).collidepoint(mouse_pos):
        opacidade = 180  # Quando o mouse passa por cima
    else:
        opacidade = 255  # Normal

    # Preenche a superfície do botão com a cor vermelha e a opacidade definida
    botao_surface.fill((255, 0, 0, opacidade))

    # Desenha a superfície do botão na tela
    tela.blit(botao_surface, (pos_x, pos_y))

    # Renderiza o texto "X" em branco e desenha sobre o botão
    texto_x = font.render("X", True, (255, 255, 255))
    tela.blit(texto_x, (pos_x + (largura_botao - texto_x.get_width()) // 2, pos_y + (altura_botao - texto_x.get_height()) // 2))

    # Retorna o retângulo do botão para detectar cliques
    return pygame.Rect(pos_x, pos_y, largura_botao, altura_botao)

# Função para salvar o ranking
def salvar_ranking(nome, pontosjg):
    try:
        with open('saves/points/ranking2.json', 'r') as f:
            ranking = json.load(f)
    except FileNotFoundError:
        ranking = []

    # Remove entradas anteriores com o mesmo nome para evitar duplicatas
    ranking = [entry for entry in ranking if entry['nome'] != nome]

    # Adiciona o novo resultado ao ranking no topo da lista
    ranking.insert(0, {'nome': nome, 'pontos': pontosjg})

    # Ordena o ranking pelos pontos em ordem decrescente, mantendo o novo no topo se os pontos forem iguais
    ranking = sorted(ranking, key=lambda x: (x['pontos'], -ranking.index(x)), reverse=True)

    # Limita a lista a um máximo de 5 registros
    ranking = ranking[:5]

    # Salva o ranking atualizado
    with open('saves/points/ranking2.json', 'w') as f:
        json.dump(ranking, f)

    return ranking


# Função para exibir o ranking
def exibir_ranking(tela, pontosjg):
    font_titulo = pygame.font.Font("assets/fonts/PropolishRufftu-BLLyd.ttf", 70)  # Fonte para o título
    font = pygame.font.SysFont("Arial", 40)  # Usando fonte do sistema para melhor legibilidade
    
    # Carrega e redimensiona a imagem de fundo
    imagem_fundo = pygame.image.load('assets/images/backgroundgame.jpg')  # Coloque o caminho correto da sua imagem
    imagem_fundo = pygame.transform.scale(imagem_fundo, (1366, 768))  # Redimensiona a imagem para o tamanho da tela

    # Inserção do nome
    nome = inserir_nome(tela, font)

    # Limpa a tela antes de exibir o ranking
    tela.blit(imagem_fundo, (0, 0))  # Desenha a imagem de fundo na tela

    # Desenha o título em 3D
    # Efeito de sombra para o título (desloca ligeiramente para simular profundidade)
    sombra_titulo = font_titulo.render("Ranking Nível 2", True, (50, 50, 50))  # Sombra cinza
    tela.blit(sombra_titulo, (tela.get_width() // 2 - sombra_titulo.get_width() // 2 + 5, 130))  # Deslocado

    # Título principal em amarelo
    texto_titulo = font_titulo.render("Ranking Nível 2", True, (255, 255, 0))  # Amarelo
    tela.blit(texto_titulo, (tela.get_width() // 2 - texto_titulo.get_width() // 2, 130))

    # Salva e carrega o ranking
    ranking = salvar_ranking(nome, pontosjg)

    # Exibe o ranking no topo da tela
    y_offset = 250
    for i, recorde in enumerate(ranking):  # Exibe todos os registros (top 5 já está garantido na função salvar)
        text = font.render(f"{i + 1}. {recorde['nome']} - {recorde['pontos']} pontos", True, (0, 0, 0))
        tela.blit(text, (200, y_offset))
        y_offset += 50

    pygame.display.flip()
    pygame.time.wait(5000)

    # Após exibir o ranking, volta para a tela de seleção de nível
    selecionar()


# Função para inserir o nome do jogador
def inserir_nome(tela, font):
    nome = ""
    nome_completo = False
    cursor_visivel = True
    cursor_tempo = pygame.time.get_ticks()

    font_titulo = pygame.font.Font("assets/fonts/PropolishRufftu-BLLyd.ttf", 70)  # Fonte para o título

    # Carrega e redimensiona a imagem de fundo
    imagem_fundo = pygame.image.load('assets/images/backgroundgame.jpg')  # Coloque o caminho correto da sua imagem
    imagem_fundo = pygame.transform.scale(imagem_fundo, (1366, 768))  # Redimensiona a imagem para o tamanho da tela

    while not nome_completo:
        tela.blit(imagem_fundo, (0, 0))  # Desenha a imagem de fundo na tela

        # Efeito de sombra para o título (desloca ligeiramente para simular profundidade)
        sombra_titulo = font_titulo.render("Digite seu nome:", True, (50, 50, 50))  # Sombra cinza
        tela.blit(sombra_titulo, (tela.get_width() // 2 - sombra_titulo.get_width() // 2 + 5, 205))  # Deslocado

        # Título principal em amarelo
        texto_titulo = font_titulo.render("Digite seu nome:", True, (255, 255, 0))  # Amarelo
        tela.blit(texto_titulo, (tela.get_width() // 2 - texto_titulo.get_width() // 2, 200))

        # Nome digitado
        nome_text = font.render(nome, True, (0, 0, 0))
        
        # Centraliza o nome na horizontal e verticalmente
        nome_x = tela.get_width() // 2 - nome_text.get_width() // 2
        nome_y = tela.get_height() // 2 - nome_text.get_height() // 2
        tela.blit(nome_text, (nome_x, nome_y))

        # Controla a visibilidade do cursor (pisca)
        if pygame.time.get_ticks() - cursor_tempo > 500:
            cursor_visivel = not cursor_visivel
            cursor_tempo = pygame.time.get_ticks()

        # Desenha o cursor piscando (linha vertical)
        if cursor_visivel:
            cursor_altura = font.get_height()
            pygame.draw.rect(tela, (0, 0, 0), (nome_x + nome_text.get_width() + 5, nome_y, 2, cursor_altura))

        # Linha centralizada para indicar a área de entrada do nome
        linha_x = tela.get_width() // 2 - 300 // 2  # Largura da linha 300
        pygame.draw.line(tela, (0, 0, 0), (linha_x, nome_y + 50), (linha_x + 300, nome_y + 50), 2)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Enter para finalizar
                    nome_completo = True
                elif evento.key == pygame.K_BACKSPACE:  # Apagar o último caractere
                    nome = nome[:-1]
                else:
                    nome += evento.unicode  # Adiciona o caractere digitado

    return nome

def nivel2():
    pygame.init()
    tela = pygame.display.set_mode((1366, 768))
    pygame.display.set_caption("Nível 2")

    pontosjg = 0

    soundcorrect = pygame.mixer.Sound('assets/sounds/correct3.wav')
    soundincorrect = pygame.mixer.Sound('assets/sounds/incorrect.mp3')

    font_pergunta = pygame.font.SysFont("Arial", 35)
    font_resposta = pygame.font.SysFont("Arial", 35)  # Ajustado para que o texto caiba no botão
    font_pontuação = pygame.font.SysFont("Arial", 30)
    font_voltar = pygame.font.SysFont("Arial", 40)  # Fonte para o botão "X"

    perguntas = [
        {
            "pergunta": "Qual é um exemplo de algoritmo?",
            "opcoes": ['Receita de um bolo', 'Desenho animado', 'Jogo de tabuleiro'],
            "correta": 0
        },
        {
            "pergunta": "O que é um loop?",
            "opcoes": ['Estrutura que repete uma sequência', 'Tipo de dado', 'Acontecimento único'],
            "correta": 0
        },
        {
            "pergunta": "O que é um diagrama?",
            "opcoes": ['Reprensentação visual de um algoritmo', 'Tipo de código-fonte', 'Um jogo'],
            "correta": 0
        },
        {
            "pergunta": "Primeiro passo para criar um algoritmo:",
            "opcoes": ['Definir o problema', 'Começar a resolver logo', 'Pensar nas possibilidades'],
            "correta": 0
        },
        {
            "pergunta": "Um algoritmo deve ser...",
            "opcoes": ['Claro e preciso', 'Complexo e diverso', 'Rapido e aleatório'],
            "correta": 0
        },
        {
            "pergunta": "Função de um algoritmo de busca:",
            "opcoes": ['Encontrar algo', 'Ordenar processos', 'Modificar meios'],
            "correta": 0
        }
    ]

    random.shuffle(perguntas)

    for pergunta in perguntas:
        opcoes = pergunta['opcoes']
        correta = pergunta['correta']

        opcoes_com_indices = list(enumerate(opcoes))
        random.shuffle(opcoes_com_indices)

        pergunta['opcoes'] = [opcao for _, opcao in opcoes_com_indices]
        pergunta['correta'] = next(i for i, (idx, _) in enumerate(opcoes_com_indices) if idx == correta)

    pergunta_atual = 0

    imagem_fundo = pygame.image.load('assets/images/backgroundgame.jpg')
    imagem_fundo = pygame.transform.scale(imagem_fundo, (1366, 768))

    while pergunta_atual < len(perguntas):
        tela.blit(imagem_fundo, (0, 0))

                # Desenhar o botão de voltar
        botao_voltar_rect = desenhar_botao_voltar(tela, font_voltar)

        rect_pergunta = pygame.Rect(185, 130, 1000, 120) # Ratângulo Verde
        pygame.draw.rect(tela, (0, 255, 0), rect_pergunta)

        pontuacao_texto = font_pontuação.render(f"Pontos: {pontosjg}", True, (0, 0, 0))
        tela.blit(pontuacao_texto, (tela.get_width() - pontuacao_texto.get_width() - 200, 200))

        pergunta = perguntas[pergunta_atual]

        linhas_pergunta = pergunta['pergunta'].split('\n')

        y_offset = 165
        for linha in linhas_pergunta:
            text = font_pergunta.render(linha, True, (0, 0, 0))
            tela.blit(text, (200, y_offset))
            y_offset += 50

        # Renderiza as opções de resposta como botões redondos estendidos
        y_offset_resposta = 300
        botoes = []
        letras_respostas = ['A', 'B', 'C']  # Letras para os botões

        # Calcula a largura do botão para ocupar o espaço da pergunta
        largura_botao = 1000  # A mesma largura da área da pergunta
        altura_botao = 60  # Altura do botão

        mouse_pos = pygame.mouse.get_pos()  # Obtém a posição do mouse

        for i, opcao in enumerate(pergunta['opcoes']):
            # Define a posição do botão
            pos_x = (tela.get_width() - largura_botao) // 2  # Centraliza os botões
            pos_y = y_offset_resposta + i * (altura_botao + 20)  # Espaçamento entre os botões

            # Define a cor de fundo do botão
            if pygame.Rect(pos_x, pos_y, largura_botao, altura_botao).collidepoint(mouse_pos):
                cor_botao = (255, 255, 0)  # Amarelo quando o mouse passa
            else:
                cor_botao = (100, 100, 100)  # Cor normal

            # Desenha o botão redondo
            pygame.draw.rect(tela, cor_botao, (pos_x, pos_y, largura_botao, altura_botao), border_radius=25)  # Botão arredondado
            pygame.draw.rect(tela, (150, 150, 150), (pos_x + 5, pos_y + 5, largura_botao - 10, altura_botao - 10), border_radius=20)  # Efeito 3D

            # Renderiza a letra da resposta no centro do botão
            letra_texto = font_resposta.render(letras_respostas[i], True, (0, 0, 0))  # Cor da letra
            tela.blit(letra_texto, (pos_x + 10, pos_y + 10))  # Centraliza a letra

            # Renderiza a opção de resposta dentro do botão
            opcao_texto = font_resposta.render(opcao, True, (0, 0, 0))  # Cor do texto da opção
            tela.blit(opcao_texto, (pos_x + 60, pos_y + 10))  # Posiciona à direita da letra

            # Salva a área do botão para detectar cliques
            botoes.append(pygame.Rect(pos_x, pos_y, largura_botao, altura_botao))

        pygame.display.flip()

        # Lida com os eventos de clique
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

                               # Detecção de clique no botão "X"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar_rect.collidepoint(evento.pos):
                    selecionar()  # Volta para o selecionar nivel


            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, botao in enumerate(botoes):
                    if botao.collidepoint(evento.pos):
                        if i == pergunta['correta']:
                            pontosjg += 100
                            soundcorrect.play()
                        else:
                            soundincorrect.play()

                        pergunta_atual += 1
                        break

    exibir_ranking(tela, pontosjg)
