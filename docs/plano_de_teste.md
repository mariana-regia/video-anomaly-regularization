# Plano de teste - Regularização em detecção de anomalias em vídeos

Este documento descreve o plano experimental do projeto, incluindo a seleção dos datasets, a justificativa do modelo, as técnicas de regularização avaliadas e o protocolo de comparação.

## Objetivo

Desenvolver e avaliar estratégias de regularização em modelos de aprendizado profundo para detecção de comportamento humano anômalo em vídeos.

O experimento deve comparar a capacidade de generalização do mesmo modelo em diferentes configurações:

- Sem regularização.
- Com técnicas de regularização individuais.
- Com uma configuração combinada de regularização.

A comparação será feita a partir de métricas de classificação frame-level e da análise do comportamento das curvas de treino e validação.

## Datasets avaliados

Os detalhes de download, links oficiais, estrutura esperada e características observadas estão documentados em [datasets.md](datasets.md).

Para o escopo principal, foram escolhidos:

- **UCSD Ped2**, como dataset piloto, por ser pequeno, organizado e adequado para validar rapidamente o pipeline de dados, o modelo, as métricas e a comparação entre regularizações.
- **ShanghaiTech**, como dataset principal, por oferecer maior diversidade de cenas, 330 vídeos de treino, 107 sequências de teste e máscaras frame-level em `.npy`, facilitando a avaliação de anomalias por frame.

Os demais datasets avaliados ficam como alternativas:

- **Avenue Dataset (CUHK)**: boa alternativa acadêmica, mas exige suporte a arquivos `.mat`.
- **UCF-Crime Dataset**: realista e amplo, porém pesado para o escopo inicial e mais trabalhoso em pré-processamento.
- **UMN Dataset**: leve e útil para demonstração visual, mas limitado para sustentar a comparação principal de regularização.

## Escopo

O projeto será conduzido em duas etapas:

1. Validar o pipeline no UCSD Ped2.
2. Executar o experimento principal no ShanghaiTech.

Essa estratégia reduz o risco técnico. O UCSD Ped2 permite implementar e validar rapidamente o fluxo completo, enquanto o ShanghaiTech oferece uma avaliação mais robusta em um conjunto maior e mais diverso.

## Modelo proposto

O modelo principal será um autoencoder convolucional temporal treinado para reconstrução de comportamento normal.

### Abordagem

- Treinar apenas com dados normais.
- Reconstruir frames ou janelas temporais.
- Calcular erro de reconstrução por frame.
- Definir anomalia quando o erro ultrapassar um limiar.
- Comparar o mesmo modelo com e sem regularização.

### Arquitetura inicial

- Entrada: janelas de 8 ou 16 frames.
- Pré-processamento: redimensionamento para 160x90 ou 224x128 e normalização para `[0, 1]`.
- Encoder convolucional 2D aplicado por frame, ou encoder 3D simples.
- Bloco temporal com ConvLSTM ou convoluções 3D.
- Decoder para reconstrução.
- Loss: MSE ou MAE.
- Score de anomalia: erro médio de reconstrução por frame.

### Justificativa para a escolha do modelo

O autoencoder convolucional temporal foi escolhido porque a detecção de anomalias pode ser formulada como aprendizado do comportamento normal. O modelo é treinado com sequências normais e, no teste, entradas com padrões incomuns tendem a apresentar maior erro de reconstrução.

A parte convolucional captura características espaciais dos frames, enquanto a parte temporal modela movimento entre frames consecutivos. Isso é importante porque muitas anomalias em vídeo aparecem mais claramente na dinâmica da cena do que em uma imagem isolada.

A abordagem também favorece a comparação entre regularizações. Usando a mesma arquitetura como base, é possível medir o impacto de Dropout, Weight Decay, Batch Normalization, Early Stopping e Data Augmentation sobre overfitting, generalização e métricas frame-level.

## Configurações experimentais

### Baseline sem regularização

O baseline será usado como referência para medir o efeito das técnicas de regularização.

- Sem dropout.
- Sem weight decay.
- Sem data augmentation.
- Sem early stopping, ou com número fixo de épocas para diagnóstico de overfitting.
- Batch Normalization desativada, se a arquitetura permitir comparação limpa.

### Regularizações individuais

Cada técnica será avaliada separadamente para medir seu impacto isolado:

- Dropout.
- Weight Decay L2.
- Batch Normalization.
- Early Stopping.
- Data Augmentation.

### Regularização combinada

Após os testes individuais, será avaliada uma configuração combinada com as técnicas que melhorarem a validação sem degradar o recall:

- Dropout moderado.
- Weight Decay pequeno.
- Batch Normalization.
- Early Stopping.
- Data Augmentation leve.

## Data augmentation

O data augmentation será aplicado apenas no treino e com intensidade baixa, para evitar distorções que descaracterizem o comportamento temporal.

Transformações propostas:

- Flip horizontal, quando fizer sentido para a cena.
- Pequena variação de brilho e contraste.
- Ruído gaussiano leve.
- Crop/rescale discreto.

Transformações que alterem fortemente a dinâmica temporal ou criem anomalias artificiais devem ser evitadas.

## Métricas

### Métricas principais

- Accuracy.
- Precision.
- Recall.
- F1-score.

### Métricas complementares

- AUROC.
- AUPRC.
- Curvas de loss de treino e validação.
- Diferença entre loss de treino e validação como indício de overfitting.

Em detecção de anomalias, F1-score, recall e AUPRC tendem a ser mais informativos que accuracy, porque os dados podem ser desbalanceados.

## Protocolo de teste

### Fase 1 - Validação rápida em UCSD Ped2

1. Carregar frames de treino normal.
2. Criar janelas temporais.
3. Separar parte do treino normal para validação.
4. Treinar o baseline sem regularização.
5. Calcular erro de reconstrução no teste.
6. Converter anotações `.m` em vetor binário frame-level.
7. Escolher o threshold usando os dados de validação.
8. Reportar precision, recall, F1-score e curvas de loss.

Critérios de sucesso:

- Pipeline carrega os dados corretamente.
- Scores de anomalia são gerados por frame.
- Métricas são calculadas sem ajustes manuais.
- Há evidência visual ou numérica da diferença entre o baseline e as versões regularizadas.

### Fase 2 - Experimento principal em ShanghaiTech

1. Carregar vídeos normais de treino.
2. Extrair ou amostrar frames/janelas de treino.
3. Carregar frames de teste já extraídos.
4. Carregar máscaras `test_frame_mask/*.npy`.
5. Treinar o mesmo modelo usado no piloto.
6. Repetir baseline, regularizações individuais e configuração combinada.
7. Avaliar frame-level usando as máscaras `.npy`.
8. Comparar resultados com UCSD Ped2.

Critérios de sucesso:

- A mesma metodologia é aplicada em um dataset maior.
- A tabela comparativa inclui todas as configurações relevantes.
- A discussão final relaciona regularização, generalização e overfitting.

## Resultados esperados

| Dataset | Configuração | Train Loss | Val Loss | Accuracy | Precision | Recall | F1 | AUROC | Observação |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UCSD Ped2 | Sem regularização | | | | | | | | |
| UCSD Ped2 | Dropout | | | | | | | | |
| UCSD Ped2 | Weight Decay | | | | | | | | |
| UCSD Ped2 | BatchNorm | | | | | | | | |
| UCSD Ped2 | Early Stopping | | | | | | | | |
| UCSD Ped2 | Data Augmentation | | | | | | | | |
| UCSD Ped2 | Combinado | | | | | | | | |
| ShanghaiTech | Sem regularização | | | | | | | | |
| ShanghaiTech | Combinado | | | | | | | | |

## Próximas etapas

Implementar primeiro o pipeline completo do UCSD Ped2:

1. Dataset loader.
2. Conversão das anotações frame-level.
3. Criação de janelas temporais.
4. Modelo baseline de reconstrução.
5. Cálculo de score de anomalia.
6. Métricas frame-level.

Depois que esse fluxo estiver funcionando de ponta a ponta, adaptar o loader para ShanghaiTech usando `testing/test_frame_mask/*.npy` como ground truth principal.
