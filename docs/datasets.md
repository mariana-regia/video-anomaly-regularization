# Datasets

Os datasets não são versionados neste repositório devido ao tamanho dos arquivos. Para reproduzir os experimentos, baixe os datasets a partir dos links indicados e organize os arquivos seguindo a estrutura esperada.

## Estrutura esperada

```text
datasets/
├── UCSD Anomaly Detection Dataset/
├── ShanghaiTech Dataset/
├── Avenue Dataset (CUHK)/
├── UCF-Crime Dataset/
└── UMN Dataset/
```

## Datasets avaliados

### UCSD Anomaly Detection Dataset

- Uso no projeto: dataset piloto.
- Link oficial: https://www.svcl.ucsd.edu/projects/anomaly/dataset.html
- Tamanho aproximado dos arquivos disponíveis: 1,2 GB.
- Estrutura esperada: `UCSDped1/` e `UCSDped2/`, ambos com pastas `Train/` e `Test/`.
- UCSD Ped1: 34 sequências de treino e 36 sequências de teste.
- UCSD Ped2: 16 sequências de treino e 12 sequências de teste.
- Formato dos frames: `.tif`.
- Treino composto apenas por frames normais.
- Teste com anotações frame-level em arquivos `.m`.
- UCSD Ped2: 2.550 frames de treino e 2.010 frames de teste.
- Resolução observada:
  - Ped1: 238x158.
  - Ped2: 360x240.

O UCSD Ped2 foi escolhido como dataset piloto por ser pequeno, organizado e adequado para validar rapidamente o pipeline, o modelo, as métricas e a comparação entre regularizações.

### ShanghaiTech Dataset

- Uso no projeto: experimento principal.
- Link oficial: https://svip-lab.github.io/dataset/campus_dataset.html
- Página geral do laboratório: https://svip-lab.github.io/datasets.html
- Tamanho aproximado dos arquivos disponíveis: 23 GB.
- Estrutura esperada:
  - `shanghaitech/training/videos`
  - `shanghaitech/testing/frames`
  - `shanghaitech/testing/test_frame_mask`
  - `shanghaitech/testing/test_pixel_mask`
- Treino: 330 vídeos `.avi`.
- Teste: 107 sequências de frames.
- Frames de teste: 40.791 imagens `.jpg`.
- Máscaras frame-level: 107 arquivos `.npy`.
- Máscaras pixel-level: 107 arquivos `.npy`.
- Resolução observada: 856x480.
- Vídeo de treino observado: 24 FPS, 856x480.
- Máscaras frame-level binárias, com valores `0` e `1`.

O ShanghaiTech foi escolhido como dataset principal por ter maior diversidade de cenas, anotações frame-level em formato simples de carregar com NumPy e estrutura adequada para avaliação de detecção de anomalias em vídeo.

### Avenue Dataset (CUHK)

- Uso no projeto: dataset alternativo.
- Link oficial: https://www.cse.cuhk.edu.hk/~leojia/projects/detectabnormal/dataset.html
- Tamanho aproximado dos arquivos disponíveis: 793 MB.
- Estrutura esperada:
  - `Avenue Dataset/training_videos`
  - `Avenue Dataset/testing_videos`
  - `Avenue Dataset/training_vol`
  - `Avenue Dataset/testing_vol`
  - `ground_truth_demo/testing_label_mask`
- Treino: 16 vídeos.
- Teste: 21 vídeos.
- Volumes e máscaras em formato `.mat`.
- Vídeo observado: 640x360, 25 FPS.

O Avenue é uma boa alternativa por ser menor que o ShanghaiTech e conter anotações úteis, mas exige suporte a arquivos `.mat` no pipeline de dados.

### UCF-Crime Dataset

- Uso no projeto: extensão futura ou subamostra exploratória.
- Página oficial: https://www.crcv.ucf.edu/research/real-world-anomaly-detection-in-surveillance-videos/
- Link direto informado pela página oficial: https://www.crcv.ucf.edu/data1/chenchen/UCF_Crimes.zip
- Tamanho aproximado dos arquivos disponíveis: 98 GB.
- Estrutura esperada: vídeos extraídos e arquivos de split/anotação.
- Vídeos `.mp4`: 1.950.
- Anotações temporais de teste: 290 linhas.
- Classes anômalas presentes: Abuse, Arrest, Arson, Assault, Burglary, Explosion, Fighting, RoadAccidents, Robbery, Shooting, Shoplifting, Stealing e Vandalism.

O UCF-Crime é relevante e realista, mas exige muito pré-processamento, amostragem, alinhamento temporal e controle de desbalanceamento. Por isso, não será usado como base inicial.

### UMN Dataset

- Uso no projeto: demonstração visual opcional.
- Link do dataset: http://mha.cs.umn.edu/movies/crowdactivity-all.avi
- Tamanho aproximado dos arquivos disponíveis: 24 MB.
- Arquivo principal: `Crowd-Activity-All.avi`.
- Vídeo observado: 320x240, 30 FPS, 7.739 frames.

O UMN é leve e útil para demonstrações simples, mas é limitado para sustentar a comparação principal de regularização.

## Observações

- A pasta `datasets/` deve permanecer fora do controle de versão.
- Links oficiais devem ser priorizados em relação a cópias espelho.
- Caso seja necessário usar Google Drive ou outro serviço como espelho, o link deve ser documentado como alternativa, mantendo a referência oficial quando existir.
