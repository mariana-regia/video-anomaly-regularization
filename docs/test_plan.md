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

Esse notebook base representa o modelo "cru": ele pode conter componentes que já fazem parte da arquitetura escolhida, como Batch Normalization caso esteja embutida no modelo, mas não deve adicionar técnicas externas de regularização ao pipeline experimental.

## Notebook base

O notebook base é o ponto de comparação para todos os experimentos seguintes.

Ele não deve incluir, por enquanto:

- Early Stopping;
- regularização L2 ou Weight Decay;
- Dropout adicionado como experimento;
- Data Augmentation;
- combinações de técnicas de regularização.

O objetivo é ter uma execução completa e simples, que sirva como controle para medir o impacto das alterações posteriores.

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

Métricas principais:

- Accuracy;
- Precision;
- Recall;
- F1-score;
- AUROC;
- AUPRC.

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
    1. Revisar a implementação do modelo.
    2. Adicionar métrica de avaliação EER (Equal Error Rate). 
2. Criar versões derivadas alterando uma técnica por vez.
3. Executar os notebooks com o mesmo protocolo.
4. Registrar métricas, curvas e gráficos.
5. Comparar os resultados em uma tabela final.