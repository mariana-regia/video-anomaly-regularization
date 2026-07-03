# Plano de teste - Regularização em detecção de anomalias em vídeos

Este documento resume o plano experimental do projeto. Os detalhes sobre download, estrutura esperada e características dos datasets ficam em [datasets.md](datasets.md).

## Objetivo

Avaliar o impacto de técnicas de regularização em um modelo de detecção de anomalias em vídeos, comparando versões controladas do mesmo pipeline.

A ideia é começar com um notebook base, já implementado em `src/train/DL_UCSD_STAE_Train.ipynb`, contendo:

- carregamento do dataset;
- pré-processamento dos frames;
- criação de janelas temporais;
- treino;
- validação;
- teste;
- cálculo de métricas;
- visualização dos resultados.

Esse notebook base representa o modelo "cru": ele mantém componentes que fazem parte da arquitetura do artigo, como Batch Normalization, mas não adiciona técnicas externas de regularização ao pipeline experimental.

A arquitetura é baseada no STAE descrito no artigo de referência, mas o protocolo do baseline é deliberadamente diferente do experimento completo do artigo: ele reserva três vídeos normais para validação e não inclui L2 nem Data Augmentation. Portanto, os resultados serão usados para comparar os notebooks deste projeto, e não como reprodução direta dos valores publicados.

## Notebook base

O notebook base é o ponto de comparação para todos os experimentos seguintes.

Ele não deve incluir, por enquanto:

- Early Stopping;
- regularização L2 ou Weight Decay;
- Dropout adicionado como experimento;
- Data Augmentation;
- combinações de técnicas de regularização.

O objetivo é ter uma execução completa e simples, que sirva como controle para medir o impacto das alterações posteriores.

Para manter a comparação reproduzível sem treinar com batches compostos por janelas consecutivas do mesmo vídeo, os tensores de treino são reorganizados uma única vez com uma permutação fixa baseada em `SEED`. O `model.fit` mantém `shuffle=False`, garantindo que todas as variantes recebam os mesmos batches na mesma ordem.

## Notebooks experimentais

Os próximos notebooks serão derivados do notebook base. Cada versão deve alterar apenas uma técnica principal, para permitir comparação isolada.

Configuração prevista:

| Notebook | Configuração |
| --- | --- |
| Notebook 0 | Base |
| Notebook 1 | Base + Early Stopping |
| Notebook 2 | Base + Dropout |
| Notebook 3 | Base + Weight Decay ou L2 |
| Notebook 4 | Base + Data Augmentation |

Outras combinações podem ser criadas depois, mas somente após analisar os resultados individuais.

## Datasets

O primeiro pipeline está sendo validado com o UCSD Ped2, por ser menor e adequado para testar rapidamente o fluxo completo de treino, validação, teste e visualização.

Também é possível usar o ShanghaiTech em experimentos posteriores, especialmente os frames normais do conjunto de treino, para avaliar o comportamento das regularizações em um dataset maior e mais diverso.

As informações detalhadas sobre UCSD Ped2, ShanghaiTech e demais datasets avaliados estão em [datasets.md](datasets.md).

## Métricas e comparação

Todos os notebooks devem reportar as mesmas métricas e visualizações, para que a comparação seja justa.

As métricas devem ser analisadas nesta ordem de prioridade:

1. AUROC.
2. EER.
3. AUPRC.
4. Precision.
5. Recall.
6. F1-score.
7. Accuracy.

AUROC e EER permitem aproximação ao protocolo do artigo. AUPRC complementa a análise em dados desbalanceados. Precision, Recall e F1-score descrevem o resultado no threshold adotado, enquanto Accuracy deve ser tratada apenas como diagnóstico.

O threshold de classificação deve ser calibrado no percentil 95 dos scores dos vídeos normais de validação. Depois de calculado, ele é aplicado ao conjunto de teste sem usar seus rótulos nem sua distribuição. Todos os notebooks devem repetir exatamente esse protocolo.

Também devem ser mantidas:

- curvas de loss de treino e validação;
- score de anomalia por frame;
- gráficos comparando score e ground truth nos vídeos de teste.

## Critérios de comparação

As técnicas de regularização serão comparadas observando:

- melhora ou piora nas métricas frame-level;
- diferença entre loss de treino e validação;
- impacto no recall de anomalias;
- estabilidade do score de anomalia;
- comportamento visual dos resultados nos vídeos de teste.

Para a análise final, o mais importante é verificar quais técnicas melhoram a generalização sem degradar demais a detecção de frames anômalos.

## Próximas etapas

1. Manter o notebook base como referência.
2. Criar versões derivadas alterando uma técnica por vez.
3. Executar os notebooks com o mesmo protocolo.
4. Registrar métricas, curvas e gráficos.
5. Comparar os resultados em uma tabela final.
