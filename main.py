import numpy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from carrega_dados import carrega_dados_tomografia
from segmentacao import rotula_tomografia_3d, conta_celula_por_tipo

def grafico_dispersao_3d(volume, tipo_cinza, titulo, cor, total):
    """
    Cria um gráfico de dispersão 3D para visualizar um tipo de célula específico.

    Args:
        volume (numpy.ndarray): A matriz 3D da tomografia.
        tipo_cinza (int): O valor de cinza da célula a ser visualizada.
        titulo (str): O título do gráfico.
    """
    z_coords, y_coords, x_coords = numpy.where(volume == tipo_cinza)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_coords, y_coords, z_coords, c=cor, s=3)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'{titulo}\nTotal de Células: {total}')
    plt.show()
    
def grafico_dispersao_3d_combinado(volume, tipos_de_celulas, cores, totais):
    """
    Cria um único gráfico de dispersão 3D combinando todos os tipos de células, 
    diferenciados por cor.
    
    Args:
        volume (numpy.ndarray): A matriz 3D da tomografia.
        tipos_de_celulas (dict): Dicionário com os valores e nomes das células.
        cores (dict): Dicionário com as cores de cada tipo de célula.
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    for nome, valor in tipos_de_celulas.items():
        z_coords, y_coords, x_coords = numpy.where(volume == valor)
        cor = cores[nome]
        total = totais[nome.lower()]
        ax.scatter(x_coords, y_coords, z_coords, c=cor, s=3, label=f'{nome}: {total}')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Visualização 3D de Todos os Tipos de Células')
    ax.legend()
    plt.show()

def cria_histograma(tamanhos_dos_grupos, titulo, cor_barra):
    """
    Cria um gráfico de barras com o volume de cada agrupamento de célula.
    
    Args:
        tamanhos_dos_grupos (dict): Dicionário com os tamanhos de cada agrupamento.
        titulo (str): O título do gráfico.
        cor_barra (str): A cor das barras do gráfico.
    """
    if not tamanhos_dos_grupos:
        print(f"Não há agrupamentos para gerar o gráfico de barras para: {titulo}")
        return
    
    # Extrai os rótulos e os tamanhos dos agrupamentos do dicionário
    rotulos = [str(k) for k in tamanhos_dos_grupos.keys()]
    volumes = list(tamanhos_dos_grupos.values())
    
    maior_grupo = max(volumes)
    menor_grupo = min(volumes)
    media_grupos = numpy.mean(volumes)
    
    plt.figure(figsize=(12, 6))
    plt.bar(rotulos, volumes, color=cor_barra)
    plt.yscale('log')
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.title(f'Volume de Cada Agrupamento de Células: {titulo}')
    plt.xlabel('Rótulo do Agrupamento')
    plt.ylabel('Número de Células (Voxels)')
    plt.grid(axis='y', alpha=0.75)
    plt.xticks(rotation=45, ha='right') # Rotaciona os rótulos para melhor visualização
    plt.tight_layout() # Ajusta o layout para evitar sobreposição
    
    # Adiciona o texto no canto superior esquerdo do gráfico
    plt.text(0.02, 0.95, 
             f'Maior Grupo: {maior_grupo} voxels\n'
             f'Menor Grupo: {menor_grupo} voxels\n'
             f'Média: {media_grupos:.2f} voxels', 
             transform=plt.gca().transAxes,
             fontsize=12,
             verticalalignment='top',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.5))
    
    plt.show()


def main(caminho, conectividade):
    """
    Função principal para executar todo o processo de análise.
    """
    # Define os valores de cinza para cada tipo de célula
    PROLIFERATIVA_VAL = 255
    QUIESCENTE_VAL = 200
    NECROTICA_VAL = 140

    # Carrega os dados da tomografia
    dados_tomografia = carrega_dados_tomografia(caminho)
    if dados_tomografia is None:
        return

    print(f"\n--- Análise com conectividade {conectividade} ---")
     
    # Processamento para cada tipo de célula
    tipos_de_celulas = {
        'Proliferativas': PROLIFERATIVA_VAL,
        'Quiescentes': QUIESCENTE_VAL,
        'Necroticas': NECROTICA_VAL
    }
    
    # Define cores para cada tipo de célula
    cores = {
        'Proliferativas': 'red',
        'Quiescentes': 'blue',
        'Necroticas': 'black'
    }
    
    # 2.a: Calcula o total de células de cada tipo
    contagens_totais = conta_celula_por_tipo(dados_tomografia, PROLIFERATIVA_VAL, QUIESCENTE_VAL, NECROTICA_VAL)

    for nome, valor in tipos_de_celulas.items():
        print(f"\nprocessando agrupamentos de células {nome}...")
        
        # Rotulação e segmentação do volume
        volume_rotulado, tamanhos_dos_grupos = rotula_tomografia_3d(dados_tomografia, valor, conectividade)
        
        # 2.b: Gera o histograma de distribuição dos tamanhos dos agrupamentos
        cria_histograma(tamanhos_dos_grupos, nome, cores[nome])
        
        # 2.c: Gera um volume segmentado e a visualização 3D
        grafico_dispersao_3d(dados_tomografia, valor, f"Agrupamentos de Células {nome} ({conectividade}-conectividade)", cores[nome], contagens_totais[nome.lower()])
    
    print("\nGerando gráfico 3D combinado...")
    grafico_dispersao_3d_combinado(dados_tomografia, tipos_de_celulas, cores, contagens_totais)

if __name__ == '__main__':
    # Exemplo de uso: Rodar a análise para as duas conectividades pedidas
    caminho = 'volume_TAC.pickle'
    
    # Executa a análise com 6-conectividade
    main(caminho, 6)
    
    # Executa a análise com 26-conectividade
    main(caminho, 26)