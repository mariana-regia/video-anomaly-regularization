import numpy as np
import cv2
import VideoSequence
import VideoDataset

def redimensiona_frame(frame: np.ndarray, largura=128, altura=128) -> np.ndarray:
    # converte para escala de cinza (1 canal) se o frame for colorido
    if len(frame.shape) == 3:
        frame_processado = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        frame_processado = frame.copy()
        
    # redimensiona 
    frame_processado = cv2.resize(frame_processado, (largura, altura), interpolation=cv2.INTER_AREA)
    
    return frame_processado

def normalizar_canal(frame: np.ndarray) -> np.ndarray:
    frame_normalizado = frame.astype(np.float32) / 255.0
    return np.expand_dims(frame_normalizado, axis=-1)

def gerar_batch(dataset: VideoDataset, batch_size: int, window_size: int = 16):
    """
    Gera um batch com batch_size trechos, cada um com window_size frames, a cada
    chamada da função.
    
    Retorna:
        Um array NumPy estruturado para Convoluções 3D com o formato:
        [batch_size, window_size, altura, largura, canais]
        Exemplo: [32, 16, 128, 128, 1]
    """
    batch_de_sequencias = []

    for video in dataset.videos:
        total_frames = len(video)
        
        # Se o vídeo for menor que a janela necessária, pulamos ele
        if total_frames < window_size:
            continue
            
        # Janela deslizante consecutiva (passo de 1 em 1 frame)
        for i in range(total_frames - window_size + 1):
            sequencia = []
            
            # Coleta os 16 frames estritamente sequenciais
            for f in range(window_size):
                # i = indice do primeiro frame da janela
                # f = qual frame da janela estamos olhando
                frame_original = video.get_frame(i + f)
                
                # Processamento isolado do frame
                frame_cinza = redimensiona_frame(frame_original)
                frame_pronto = normalizar_canal(frame_cinza)
                
                sequencia.append(frame_pronto)
            
            # Adiciona a sequência de formato [16, 128, 128, 1] ao lote atual
            batch_de_sequencias.append(sequencia)
            
            # Quando atingir o tamanho do lote, retorna o resultado parcial e limpa a lista
            if len(batch_de_sequencias) == batch_size:
                yield np.array(batch_de_sequencias, dtype=np.float32)
                batch_de_sequencias = []
                
    # Envia o último lote incompleto (se houver resíduo no final do dataset)
    if batch_de_sequencias:
        yield np.array(batch_de_sequencias, dtype=np.float32)