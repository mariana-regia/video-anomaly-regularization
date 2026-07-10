# Datasets

Para reproduzir os experimentos em ambiente local, baixe os dados a partir dos links oficiais indicados e ajuste os caminhos nas células de configuração dos notebooks quando necessário.

## Dataset em uso

### UCSD Anomaly Detection Dataset

- Uso no projeto: dataset piloto e base dos notebooks experimentais atuais
- Link oficial: https://www.svcl.ucsd.edu/projects/anomaly/dataset.html
- Tamanho aproximado dos arquivos disponíveis: 1,2 GB
- Subconjunto usado: `UCSDped2`
- Estrutura original: `UCSDped1/` e `UCSDped2/`, ambos com pastas `Train/` e `Test/`
- UCSD Ped1: 34 sequências de treino e 36 sequências de teste
- UCSD Ped2: 16 sequências de treino e 12 sequências de teste
- Formato dos frames: `.tif`
- Treino composto apenas por frames normais
- Teste com anotações frame-level em arquivo `.m`
- UCSD Ped2: 2.550 frames de treino e 2.010 frames de teste
- Resolução observada:
  - Ped1: 238x158
  - Ped2: 360x240

O UCSD Ped2 foi escolhido como dataset piloto por ser pequeno, organizado e adequado para validar rapidamente o pipeline completo: carregamento, pré-processamento, criação de janelas temporais, treino, validação, teste, métricas e visualização.

### Estrutura usada nos notebooks

Os notebooks UCSD atuais assumem o dataset disponível no ambiente Kaggle neste caminho:

```text
/kaggle/input/datasets/karthiknm1/ucsd-anomaly-detection-dataset/
└── UCSD_Anomaly_Dataset.v1p2/
    └── UCSDped2/
        ├── Train/
        │   ├── Train001/
        │   ├── ...
        │   └── Train016/
        └── Test/
            ├── Test001/
            ├── ...
            ├── Test012/
            └── UCSDped2.m
```

Se o dataset estiver em outro caminho, atualize a variável `kaggle_dataset_directory` nos notebooks em `src/train/`.

### Protocolo atual com UCSD Ped2

- Notebooks principais:
  - `src/train/DL_UCSD_STAE_Train.ipynb`
  - `src/train/DL_UCSD_STAE_01_Early_Stopping.ipynb`
  - `src/train/DL_UCSD_STAE_02_Dropout.ipynb`
  - `src/train/DL_UCSD_STAE_03_L2.ipynb`
  - `src/train/DL_UCSD_STAE_04_Data_Augmentation.ipynb`
- Vídeos fixos de validação: `Train014`, `Train015` e `Train016`
- Vídeos de treino: demais sequências normais em `Train/`
- Vídeos de teste: sequências oficiais em `Test/`
- Anotações de teste: `Test/UCSDped2.m`
- Pré-processamento: leitura em escala de cinza, redimensionamento para `128x128` e normalização para o intervalo `[0, 1]`
- Janela de entrada: 16 frames
- Janela de predição: 16 frames seguintes
- Threshold de classificação: percentil 95 dos scores dos vídeos normais de validação

Essa divisão fixa é importante porque o objetivo do projeto é comparar regularizações sob o mesmo protocolo. Assim, as diferenças observadas vêm principalmente da técnica testada, e não de uma mudança casual na separação entre treino e validação.

## Dataset para expansão

### ShanghaiTech Dataset

- Uso no projeto: expansão posterior em dataset maior e mais diverso
- Notebook relacionado: `src/train/DL_ShanghaiTech_Train.ipynb`
- Link oficial: https://svip-lab.github.io/dataset/campus_dataset.html
- Página geral do laboratório: https://svip-lab.github.io/datasets.html
- Tamanho aproximado dos arquivos disponíveis: 23 GB
- Estrutura esperada:
  - `shanghaitech/training/videos`
  - `shanghaitech/testing/frames`
  - `shanghaitech/testing/test_frame_mask`
  - `shanghaitech/testing/test_pixel_mask`
- Treino: 330 vídeos `.avi`
- Teste: 107 sequências de frames
- Frames de teste: 40.791 imagens `.jpg`
- Máscaras frame-level: 107 arquivos `.npy`
- Máscaras pixel-level: 107 arquivos `.npy`
- Resolução observada: 856x480
- Vídeo de treino observado: 24 FPS, 856x480
- Máscaras frame-level binárias, com valores `0` e `1`

O ShanghaiTech é o próximo candidato natural para avaliar se as conclusões obtidas no UCSD Ped2 se mantêm em um cenário mais diverso. Antes de compará-lo com os notebooks UCSD, ainda é necessário consolidar o carregamento, o pré-processamento, a geração de rótulos e o protocolo de métricas no mesmo padrão experimental.

## Datasets avaliados como alternativas

### Avenue Dataset (CUHK)

- Uso no projeto: dataset alternativo
- Link oficial: https://www.cse.cuhk.edu.hk/~leojia/projects/detectabnormal/dataset.html
- Tamanho aproximado dos arquivos disponíveis: 793 MB
- Estrutura esperada:
  - `Avenue Dataset/training_videos`
  - `Avenue Dataset/testing_videos`
  - `Avenue Dataset/training_vol`
  - `Avenue Dataset/testing_vol`
  - `ground_truth_demo/testing_label_mask`
- Treino: 16 vídeos
- Teste: 21 vídeos
- Volumes e máscaras em formato `.mat`
- Vídeo observado: 640x360, 25 FPS

O Avenue é uma boa alternativa por ser menor que o ShanghaiTech e conter anotações úteis, mas exige suporte a arquivos `.mat` no pipeline de dados.

### UCF-Crime Dataset

- Uso no projeto: extensão futura ou subamostra exploratória
- Página oficial: https://www.crcv.ucf.edu/research/real-world-anomaly-detection-in-surveillance-videos/
- Link direto informado pela página oficial: https://www.crcv.ucf.edu/data1/chenchen/UCF_Crimes.zip
- Tamanho aproximado dos arquivos disponíveis: 98 GB
- Estrutura esperada: vídeos extraídos e arquivos de split/anotação
- Vídeos `.mp4`: 1.950
- Anotações temporais de teste: 290 linhas
- Classes anômalas presentes: Abuse, Arrest, Arson, Assault, Burglary, Explosion, Fighting, RoadAccidents, Robbery, Shooting, Shoplifting, Stealing e Vandalism

O UCF-Crime é relevante e realista, mas exige muito pré-processamento, amostragem, alinhamento temporal e controle de desbalanceamento. Por isso, não será usado como base inicial.

### UMN Dataset

- Uso no projeto: demonstração visual opcional
- Link do dataset: http://mha.cs.umn.edu/movies/crowdactivity-all.avi
- Tamanho aproximado dos arquivos disponíveis: 24 MB
- Arquivo principal: `Crowd-Activity-All.avi`
- Vídeo observado: 320x240, 30 FPS, 7.739 frames

O UMN é leve e útil para demonstrações simples, mas é limitado para sustentar a comparação principal de regularização.

## Observações

- Links oficiais devem ser priorizados em relação a cópias espelho
- Caso seja necessário usar Google Drive, Kaggle Dataset ou outro serviço como espelho, o link deve ser documentado como alternativa, mantendo a referência oficial quando existir
- Qualquer novo dataset deve registrar estrutura esperada, formato dos frames, formato das anotações e como será feita a separação entre treino, validação e teste