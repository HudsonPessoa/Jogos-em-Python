import pygame
import random

pygame.init()
pygame.mixer.init()
pew_pew_sound = pygame.mixer.Sound("pew_pew.mp3")
pew_pew_sound.set_volume(1.0)  # Define o volume do som
obstaculos_pontuados = []

# Adiciona música de fundo
pygame.mixer.music.load("musicafundo.mp3")
volume_musica = 0.5
pygame.mixer.music.set_volume(volume_musica)  # Volume da música de fundo (0.0 a 1.0)
pygame.mixer.music.play(-1)  # -1 faz a música repetir infinitamente

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()

jogador = pygame.Rect(100, 500, 50, 50)
velocidade = 5
obstaculos = []
computador = pygame.Rect(600, 250, 150, 50)

def criar_obstaculo():
    x = random.randint(0, largura - 50)
    y = 0  # Sempre no topo da tela
    obstaculo = pygame.Rect(x, y, 50, 50)
    obstaculos.append(obstaculo)

# Cria obstáculos aleatórios
for _ in range(5):
    criar_obstaculo()  

# Loop principal do jogo
pygame.display.set_caption("Jogo Pygame")  

frame_count = 0
intervalo_obstaculo = 60  # Cria obstáculos a cada 60 frames (~1 segundo)
obstaculos_por_intervalo = 1
tempo_ultimo_aumento = pygame.time.get_ticks()
pontuacao = 0
tempo_ultimo_ponto = pygame.time.get_ticks()

rodando = True
perdeu = False

# Carregue a imagem da moto
imagem_moto = pygame.image.load("moto.png").convert_alpha()
imagem_moto = pygame.transform.smoothscale(imagem_moto, (50, 50))  # Usa smoothscale para melhor qualidade

def reiniciar_jogo():
    global jogador, obstaculos, pontuacao, perdeu, frame_count, obstaculos_por_intervalo, tempo_ultimo_aumento, tempo_ultimo_ponto, obstaculos_pontuados, tempo_inicio
    jogador = pygame.Rect(100, 500, 50, 50)
    obstaculos = []
    pontuacao = 0
    perdeu = False
    frame_count = 0
    obstaculos_por_intervalo = 1
    tempo_ultimo_aumento = pygame.time.get_ticks()
    tempo_ultimo_ponto = pygame.time.get_ticks()
    obstaculos_pontuados = []
    tempo_inicio = pygame.time.get_ticks()  # Reinicia o temporizador

tempo_inicio = pygame.time.get_ticks()

def alterar_volume(delta):
    """
    Altera o volume da música de fundo.
    delta: valor a ser somado ou subtraído do volume atual (ex: +0.1 ou -0.1)
    """
    global volume_musica
    volume_musica = min(1.0, max(0.0, volume_musica + delta))
    pygame.mixer.music.set_volume(volume_musica)

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if perdeu and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if botao_restart.collidepoint(mouse_pos):
                reiniciar_jogo()
        # Configuração de volume usando a função
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                alterar_volume(+0.1)
            if event.key == pygame.K_DOWN:
                alterar_volume(-0.1)

    if not perdeu:
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a] and jogador.left > 0:
            jogador.x -= velocidade
        if teclas[pygame.K_d] and jogador.right < largura:
            jogador.x += velocidade

        # Jogador descendo
        if jogador.bottom < altura:
            jogador.y += velocidade

        # Movimento do computador descendo
        if computador.bottom < altura:
            computador.y += velocidade

        som_tocado = False
        for obstaculo in obstaculos:
            obstaculo.y += velocidade

            if obstaculo.y > jogador.y + jogador.height and obstaculo not in obstaculos_pontuados:
                pew_pew_sound.play()
                obstaculos_pontuados.append(obstaculo)

        # Cria obstáculos novos a cada intervalo
        frame_count += 1
        if frame_count >= intervalo_obstaculo:
            for _ in range(obstaculos_por_intervalo):
                criar_obstaculo()
            frame_count = 0

        # Aumenta a quantidade de obstáculos a cada 10 segundos
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_ultimo_aumento >= 10000:  # 10 segundos
            obstaculos_por_intervalo += 1
            tempo_ultimo_aumento = tempo_atual

        # Pontuação: a cada 5 segundos, ganha 50 pontos
        if tempo_atual - tempo_ultimo_ponto >= 5000:  # 5 segundos
            pontuacao += 50
            tempo_ultimo_ponto = tempo_atual

        # Remove obstáculos que saíram da tela
        obstaculos = [o for o in obstaculos if o.top < altura]

        # Verifica colisão
        for obstaculo in obstaculos:
            if jogador.colliderect(obstaculo):
                pew_pew_sound.play()  # Toca o som ao colidir
                perdeu = True

    tela.fill((255, 255, 255))
    # pygame.draw.rect(tela, (0, 0, 255), jogador)
    tela.blit(imagem_moto, (jogador.x, jogador.y))
    for obstaculo in obstaculos:
        pygame.draw.rect(tela, (255, 0, 0), obstaculo)

    # Exibe pontuação
    fonte = pygame.font.SysFont(None, 36)
    texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, (0, 0, 0))
    tela.blit(texto_pontos, (10, 10))

    # Exibe temporizador no canto superior direito
    if not perdeu:
        tempo_atual = pygame.time.get_ticks()
        segundos = (tempo_atual - tempo_inicio) // 1000
    texto_tempo = fonte.render(f"Tempo: {segundos}s", True, (0, 0, 0))
    tela.blit(texto_tempo, (largura - texto_tempo.get_width() - 10, 10))

    # Exibe campo de configuração de volume
    fonte_config = pygame.font.SysFont(None, 28)
    texto_volume = fonte_config.render(f"Volume: {int(volume_musica*100)}%", True, (0, 0, 0))
    tela.blit(texto_volume, (largura - texto_volume.get_width() - 10, 50))

    if perdeu:
        fonte = pygame.font.SysFont(None, 60)
        texto = fonte.render("Você perdeu!", True, (255, 0, 0))
        tela.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2 - texto.get_height() // 2))

        # Botão de reiniciar
        fonte_btn = pygame.font.SysFont(None, 40)
        texto_btn = fonte_btn.render("Reiniciar", True, (255, 255, 255))
        botao_restart = pygame.Rect(largura // 2 - 100, altura // 2 + 50, 200, 50)
        pygame.draw.rect(tela, (0, 128, 0), botao_restart)
        tela.blit(texto_btn, (botao_restart.x + 40, botao_restart.y + 5))

    pygame.display.flip()
    clock.tick(90)  # Limita a 90 FPS
