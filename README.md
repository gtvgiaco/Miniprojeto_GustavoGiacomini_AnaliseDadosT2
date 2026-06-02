## Gustavo Giacomini
## Análise de Dados (Turma 2)


# Mini Projeto de Análise de Dados

Este projeto é uma atividade avaliativa do curso de análise de dados do SCTEC.
O objetivo é realizar a limpeza, tratamento e análise exploratória de uma base de dados de vendas e clientes do setor de varejo.

## Base de Dados

A base de dados é um arquivo csv disponível no link (https://www.kaggle.com/datasets/namespaiva/base-varejo/data).

É composto por 830.000 linhas com informações sobre as vendas no setor de varejo.

Para rodar a análise você pode usar VsCode ou Colab. Execute todas as células.

### Colunas existentes

##
* **'DATA'**: Data da compra;
* **'CO_ID'**: Código de compra;
* **'CL_ID'**: Código do cliente;
* **'CL_GENERO'**: Sexo do cliente;
* **'CL_EC'**: Estado civil do cliente;
    1: Casado ou união estával;
    2: Divorciado;
    3: Separado;
    4. Solteiro;
    5: Viúvo; 
* **'CL_FHL'**: Número de filhos do cliente;
* **'CL_SEG'**: Segmentação econômica (classe social) do cliente;
* **'PR_ID'**: Código do produto (SKU) comprado;
* **'PR_CAT'**: Categoria do produto comprado;
* **'PR_NOME'**: Nome do produto adquirido;
* **'CL_PERFIL'**: Perfil do cliente. (criada na análise)

## Estutura do Projeto

O repositório está estruturado conforme abaixo:
* **'data'**: Pasta com o arquivo de dados brutos (base_varejo_csv) e arquivo limpo.
* **'script'**: Pasta com o arquivo após os tratamentos e análises realizadas (df_limpo.py).
* **'README.md'**: Documentação do projeto.

## Tecnologias e Bibliotecas

* **Python**
* **Pandas** (para manipulação e limpeza de dados)
* **Numpy**
* **VS Code** (Ambiente de desenvolvimento)


### Problemas e Tratamentos ###

* **'Duplicadas'**: Foram encontradas 96.553 linhas duplicadas. As linhas duplicadas foram eliminadas para não comprometer a análise.
* **'Colunas Vazias'**:  As últimas 4 colunas (Unnamed: 10 até Unnamed: 13) estão 100% vazias. Essas colunas foram removidas pois não contribuem com informações para a análise.
* **'Nulos Disfarçados'**:  Na coluna PR_CAT havia nulos disfarçados como "#N/D". Foram alterados para "Sem categoria".
* **'Padronização de Strings'**: As colunas PR_CAT e PR_NOME estavam preenchidas com todas as letras maiúsculas. Foram alteradas para apenas a primeira letra em maiúsculo.
* **'Ajuste do Tipo de Dados'**: A coluna DATA estava como string. Foi convertida para datetime.
* **'Verificação de outliers'**: Foram verficados outliers na coluna CO_ID usando o método IQR, para tentar identificar se existiam compras com volume de itens muito acima do normal.


### Insigths

* **A maioria dos clientes são pessoas divorciadas, sendo 48.8% (desses 25.4% não possuem filhos).**
* **A frequencia de compra é bem equilibrada entre os gêneros. As mulheres são responsáveis por 52% das compras.**
* **A ordem das categorias mais vendidas é igual para homens e mulheres, demonstrando um comportamento parecido ao realizar suas compras. A categoria de Alimentos é a mais vendida, seguida por Higiene e Limpeza.**
* **Percebe-se que o presunto cozido é o produto mais vendido, indiferente do gênero do comprador. Esse item nunca pode faltar na área de venda, em hipótese alguma. Itens para criança e de higiene estão no top 10 dos 2 gêneros. As mulheres compram mais itens para limpeza da casa do que os homens.**
* **Embora a média de filhos seja parecida, existe uma tendência clara. Conforme a segmentação econômica diminui, a média de filhos aumenta.**
* **O movimento na loja não é impactado fortemente pelo pagamento de salário. Ao contrário do que se esperava (maior movimentação coincidindo com as datas de pagamento de salário.)**








