import os
import shutil

# Diretório atual
diretorio_atual = os.getcwd()

# Definir extensões para cada categoria
extensoes_imagens = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg']
extensoes_docs = ['.txt', '.pdf', '.doc', '.docx',
                  '.xls', '.xlsx', '.ppt', '.pptx', '.rtf']
extensoes_videos = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm']

# Criar subpastas se não existirem
subpastas = ['imagens', 'docs', 'videos']
for subpasta in subpastas:
    caminho_subpasta = os.path.join(diretorio_atual, subpasta)
    if not os.path.exists(caminho_subpasta):
        os.makedirs(caminho_subpasta)

# Contadores para log
contador_imagens = 0
contador_docs = 0
contador_videos = 0

# Função para mover arquivo para a subpasta apropriada


def mover_arquivo(arquivo, subpasta):
    origem = os.path.join(diretorio_atual, arquivo)
    destino = os.path.join(diretorio_atual, subpasta, arquivo)
    shutil.move(origem, destino)
    print(f"Arquivo '{arquivo}' movido para '{subpasta}'")


# Listar arquivos no diretório atual
arquivos = os.listdir(diretorio_atual)

for arquivo in arquivos:
    if os.path.isfile(arquivo):  # Apenas arquivos, não pastas
        _, extensao = os.path.splitext(arquivo)
        extensao = extensao.lower()

        if extensao in extensoes_imagens:
            mover_arquivo(arquivo, 'imagens')
            contador_imagens += 1
        elif extensao in extensoes_docs:
            mover_arquivo(arquivo, 'docs')
            contador_docs += 1
        elif extensao in extensoes_videos:
            mover_arquivo(arquivo, 'videos')
            contador_videos += 1
        # Outros arquivos permanecem no diretório atual

total_movidos = contador_imagens + contador_docs + contador_videos
print("Organização de arquivos concluída!")
print(
    f"Arquivos movidos: Imagens: {contador_imagens}, Docs: {contador_docs}, Vídeos: {contador_videos}")
print(f"Total de arquivos movidos: {total_movidos}")
