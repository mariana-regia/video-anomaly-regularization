# Regularização em Detecção de Anomalias em Vídeos

![Static Badge](https://img.shields.io/badge/Open_in_Colab-373E40?logo=googlecolab)
![Static Badge](https://img.shields.io/badge/Open_in_Kaggle-373E40?logo=kaggle)

Projeto experimental em Jupyter Notebooks para avaliar como técnicas de regularização afetam um modelo de detecção de anomalias em vídeos. O pipeline usa o UCSD Ped2 como dataset piloto e compara variações controladas de um Spatio-Temporal AutoEncoder (STAE) baseado no artigo [Spatio-Temporal AutoEncoder for Video Anomaly Detection](https://dl.acm.org/doi/10.1145/3123266.3123451).

O objetivo principal não é reproduzir exatamente os resultados publicados no artigo, mas manter um protocolo comparável entre notebooks: mesmo dataset, mesma divisão fixa, mesma arquitetura-base, mesmas métricas e uma técnica de regularização alterada por vez.

## Sumário

- [Visão geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Datasets](#datasets)
- [Como executar](#como-executar)
- [Notebooks](#notebooks)
- [Métricas](#métricas)
- [Resultados atuais](#resultados-atuais)
- [Referências](#referências)

## Visão geral

O modelo aprende padrões de normalidade a partir de vídeos normais. Durante a avaliação, frames com maior erro de reconstrução são tratados como mais suspeitos. O projeto compara as seguintes configurações:

- Baseline sem técnicas externas de regularização
- Early stopping
- Spatial dropout 3D
- Regularização L2
- Data augmentation

Todos os experimentos usam um protocolo fixo para reduzir variação acidental: `SEED = 42`, janelas temporais de 16 frames, predição dos próximos 16 frames, frames redimensionados para `128x128`, batches de tamanho 8 e threshold calibrado no percentil 95 dos scores dos vídeos normais de validação.

## Arquitetura

O notebook base implementa um STAE com:

- Encoder 3D com `Conv3D`, `BatchNormalization`, `LeakyReLU` e `MaxPooling3D`
- Bottleneck espaço-temporal
- Decoder de reconstrução da janela de entrada
- Decoder de predição dos frames seguintes
- Loss de reconstrução e loss ponderada de predição temporal
- Score de anomalia baseado no erro médio de reconstrução por frame

A batch normalization faz parte da arquitetura-base adotada nos notebooks. As técnicas avaliadas como regularização experimental são adicionadas separadamente nas versões derivadas.

## Datasets

### UCSD Ped2

Dataset piloto usado nos notebooks principais. Ele contém vídeos de pedestres em ambiente de vigilância, treino composto por frames normais e teste com eventos anômalos anotados em nível de frame.

Estrutura esperada no ambiente Kaggle usado pelos notebooks:

```text
/kaggle/input/datasets/karthiknm1/ucsd-anomaly-detection-dataset/
└── UCSD_Anomaly_Dataset.v1p2/
    └── UCSDped2/
        ├── Train/
        └── Test/
```

No protocolo atual, os vídeos `Train014`, `Train015` e `Train016` ficam reservados para validação. Os demais vídeos normais de treino são usados para ajuste do modelo, e os vídeos de teste são avaliados apenas depois da calibração do threshold.

### ShanghaiTech

Dataset planejado para experimentos posteriores em escala maior. Ele oferece maior diversidade de cenas e anotações em arquivos NumPy, mas exige mais custo computacional e organização de dados.

## Como executar

Os notebooks foram preparados para execução em ambiente com GPU, especialmente Kaggle. Para reproduzir localmente, crie um ambiente Python com suporte a Jupyter e instale as dependências principais:

```bash
pip install tensorflow opencv-python matplotlib numpy scikit-learn albumentations jupyter
```

Depois, ajuste o caminho do dataset nas células de configuração dos notebooks, caso não esteja usando o mesmo caminho do Kaggle.

Fluxo recomendado:

1. Abra `src/train/DL_UCSD_STAE_Train.ipynb`
2. Execute o notebook base para confirmar dataset, pré-processamento, treino e avaliação
3. Execute cada notebook derivado mantendo o mesmo protocolo
4. Compare as métricas e as visualizações geradas

## Notebooks

| Notebook | Arquivo | Configuração |
| --- | --- | --- |
| 0 | `src/train/DL_UCSD_STAE_Train.ipynb` | Baseline STAE |
| 1 | `src/train/DL_UCSD_STAE_01_Early_Stopping.ipynb` | Early stopping com `patience = 5` |
| 2 | `src/train/DL_UCSD_STAE_02_Dropout.ipynb` | Spatial dropout 3D com taxa `0.3` no bottleneck |
| 3 | `src/train/DL_UCSD_STAE_03_L2.ipynb` | Penalização L2 `1e-4` nos kernels convolucionais |
| 4 | `src/train/DL_UCSD_STAE_04_Data_Augmentation.ipynb` | Flip horizontal, brilho/contraste e rotação moderada |
| ShanghaiTech | `src/train/DL_ShanghaiTech_Train.ipynb` | Notebook inicial para expansão do experimento |

## Métricas

As metricas são calculadas em nível de frame:

- AUROC
- EER
- AUPRC
- Precision
- Recall
- F1-score
- Accuracy

O threshold de classificação é calibrado no percentil 95 dos scores dos vídeos normais de validação e depois aplicado ao conjunto de teste. AUROC, EER e AUPRC são as métricas mais importantes para comparação geral; precision, recall, F1-score e accuracy ajudam a interpretar o comportamento no threshold adotado.

## Resultados atuais

Resultados salvos nos notebooks para o UCSD Ped2:

| Configuração | AUROC | EER | AUPRC | Precision | Recall | F1-score | Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | 0.8128 | 0.2684 | 0.9499 | 0.9864 | 0.0880 | 0.1616 | 0.2512 |
| Early stopping | 0.8093 | 0.2759 | 0.9493 | 0.9795 | 0.0868 | 0.1594 | 0.2498 |
| Dropout | 0.8045 | 0.2690 | 0.9498 | 0.9876 | 0.1450 | 0.2529 | 0.2975 |
| L2 | 0.8652 | 0.2164 | 0.9686 | 1.0000 | 0.0813 | 0.1504 | 0.2468 |
| Data augmentation | 0.7773 | 0.2933 | 0.9396 | 0.9752 | 0.0953 | 0.1736 | 0.2562 |

No estado atual, a regularização L2 apresenta a melhor AUROC, EER e AUPRC. O dropout aumenta o recall e o F1-score no threshold adotado, embora não supere o baseline em AUROC. Esses resultados devem ser interpretados como comparação interna entre variantes do projeto.

## Referências

- [Spatio-Temporal AutoEncoder for Video Anomaly Detection](https://dl.acm.org/doi/10.1145/3123266.3123451)
- [UCSD Anomaly Detection Dataset](https://www.svcl.ucsd.edu/projects/anomaly/dataset.html)
- [ShanghaiTech Campus Dataset](https://svip-lab.github.io/dataset/campus_dataset.html)