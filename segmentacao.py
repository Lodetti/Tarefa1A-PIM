import numpy
from collections import deque

def rotula_tomografia_3d(volume, tipo_cinza, conectividade):
    """
    Realiza a rotulação de componentes conectados em 3D para um tipo de célula específico.

    Args:
        volume (numpy.ndarray): A matriz 3D da tomografia.
        tipo_cinza (int): O valor de cinza da célula a ser segmentada.
        conectividade (int): O tipo de conectividade (6 ou 26).

    Returns:
        tuple: Uma tupla contendo:
               - volume_rotulado (numpy.ndarray): Um volume com os agrupamentos rotulados.
               - tamanhos_dos_grupos (dict): Um dicionário com os tamanhos de cada agrupamento.
    """
    if conectividade not in [6, 26]:
        raise ValueError("A conectividade deve ser 6 ou 26.")

    # Copia o volume para evitar modificar o original
    volume_trabalhavel = numpy.copy(volume)
    # Inicializa o volume rotulado com zeros
    volume_rotulado = numpy.zeros_like(volume, dtype=numpy.int32)
    contador_rotulos = 1
    tamanhos_dos_grupos = {}
    
    # Obtém as dimensões do volume
    dims = volume_trabalhavel.shape
    
    # Define os vizinhos com base na conectividade
    if conectividade == 6:
        # 6-conectividade: vizinhos diretos (frente, trás, cima, baixo, direita, esquerda)
        vizinhos = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)
        ]
    elif conectividade == 26:
        # 26-conectividade: todos os 26 vizinhos
        vizinhos = [(dx, dy, dz) for dx in [-1, 0, 1] for dy in [-1, 0, 1] for dz in [-1, 0, 1] if not (dx == 0 and dy == 0 and dz == 0)]
    
    # Itera sobre cada voxel do volume
    for z in range(dims[0]):
        for y in range(dims[1]):
            for x in range(dims[2]):
                # Se o voxel corresponde ao valor da célula e ainda não foi rotulado
                if volume_trabalhavel[z, y, x] == tipo_cinza and volume_rotulado[z, y, x] == 0:
                    tamanho_agrupamento_atual = 0
                    queue = deque([(z, y, x)])
                    volume_rotulado[z, y, x] = contador_rotulos
                    
                    # BFS para encontrar todos os voxels conectados
                    while queue:
                        cz, cy, cx = queue.popleft()
                        tamanho_agrupamento_atual += 1
                        
                        # Itera sobre os vizinhos
                        for dz, dy, dx in vizinhos:
                            nz, ny, nx = cz + dz, cy + dy, cx + dx
                            
                            # Verifica se o vizinho está dentro dos limites do volume
                            if 0 <= nz < dims[0] and 0 <= ny < dims[1] and 0 <= nx < dims[2]:
                                # Se o vizinho tem o mesmo valor e ainda não foi rotulado
                                if volume_trabalhavel[nz, ny, nx] == tipo_cinza and volume_rotulado[nz, ny, nx] == 0:
                                    volume_rotulado[nz, ny, nx] = contador_rotulos
                                    queue.append((nz, ny, nx))
                    
                    tamanhos_dos_grupos[contador_rotulos] = tamanho_agrupamento_atual
                    contador_rotulos += 1
    
    return volume_rotulado, tamanhos_dos_grupos

def conta_celula_por_tipo(volume, proliferativa=255, quiescente=200, necrotica=140):
    """
    Calcula o total de células para cada tipo.

    Args:
        volume (numpy.ndarray): A matriz 3D da tomografia.
        proliferativa (int): Valor de cinza para células proliferativas.
        quiescente (int): Valor de cinza para células quiescentes.
        necrotica (int): Valor de cinza para células necróticas.

    Returns:
        dict: Dicionário com o total de voxels para cada tipo de célula.
    """
    counts = {
        'proliferativas': numpy.sum(volume == proliferativa),
        'quiescentes': numpy.sum(volume == quiescente),
        'necroticas': numpy.sum(volume == necrotica)
    }
    return counts