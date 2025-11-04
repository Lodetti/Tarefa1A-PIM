import pickle
import numpy

def carrega_dados_tomografia(caminho_arquivo):
    """
    Carrega a matriz numpy 3D do arquivo .pickle.

    Args:
        caminho_arquivo (str): O caminho para o arquivo .pickle.

    Returns:
        numpy.ndarray: A matriz 3D da tomografia.
    """
    try:
        with open(caminho_arquivo, 'rb') as f:
            volume_tomografia = pickle.load(f)
        print(f"Dados da tomografia carregados com sucesso de {caminho_arquivo}")
        return volume_tomografia
    except FileNotFoundError:
        print(f"Erro: O arquivo {caminho_arquivo} não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao carregar o arquivo: {e}")
        return None