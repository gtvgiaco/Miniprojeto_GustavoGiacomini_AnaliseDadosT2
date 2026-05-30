import pandas as pd

pd.set_option('display.max_columns', None) #Exibição de todas as colunas do DataFrame
pd.set_option('display.float_format','{:.2f}'.format) #Formatar float para 2 casas decimais

#Lendo o dataset original
df_limpo = pd.read_csv('data/base_varejo.csv', sep=';', encoding = 'utf-8', decimal = ',')

#Parte 1: Carregamento e Diagnóstico Rápido.
#Criação de função para verificações basicas(Linhas, colunas, nulos, duplicados e tipos de dados
def qualidade_dados(df, nome):
    print(f'Relatório de Qualidade: {nome}')
    print(f'{'=' * 100}')
    print(f'Total Linhas: {df.shape[0]} | Total Colunas: {df.shape[1]}')  #mostar qtde de linahs e colunas
    print(f'\nNulos por Coluna:') 
    nulos = df.isnull().sum()
    for col in df.columns:
        if nulos[col] > 0:  #para mostrar apenas as colunas que tem algum nulo
            print(f'- {col}: {nulos[col]}')    
    print(f'\nLinhas Duplicadas: {df.duplicated().sum()}')
    print(f'\nTipos de Dados: \n{df.dtypes}')
    print(f'\nExibição das primeiras linhas: \n{df.head(5)}')
    print(f'{'=' * 100}')

qualidade_dados(df_limpo, 'Varejo')

#Parte 2: Eliminar duplicadas, remover nulos, tratar nulos disfarçados, ajustar tipos de dados e padronizar strings.

#2.1 Eliminar duplicadas: será mantida apenas primeira ocorrência. Todas as outras repetições serão removidas.
df_limpo = df_limpo.drop_duplicates(keep='first') #dro_duplicates sem subset pois quero remover apenas as linhas totalmente iguais.
#Verificando se há duplicadas após a remoção
print(f'Duplicadas Após Keep: {df_limpo.duplicated().sum()}')
print(f'{'=' * 100}')
#Reindexar após remoção de linhas
df = df_limpo.reset_index(drop=True)

#2.2 Remover nulos: as colunas 11, 12, 13 e 14 tem 100% de nulos e serão excluidas, pois não contribuem com informações para a análise
df = df.drop(columns=['Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13'])

#2.3 Nulos disfarçados da coluna PR_CAT (categoria do produto)
print(f'Categorias únicas: {df_limpo['PR_CAT'].unique()}') #aqui foi verificado que existem linhas preenchidas com categoria #N/D 
print(f'{'=' * 100}')
#Substituição de #N/D por Sem Categoria e transformação para title (primeira letra maiuscula)
df_limpo['PR_CAT'] = df_limpo['PR_CAT'].replace({'#N/D':'Sem Categoria'})

#2.4 Padronizar strings (colunas PR_CAT e PR_NOME)
df_limpo['PR_CAT'] = df_limpo['PR_CAT'].str.strip().str.title()
df_limpo['PR_NOME'] = df_limpo['PR_NOME'].str.strip().str.title()
print(f'Nome do Produto após tratamento: {df_limpo['PR_NOME'].unique()}')
print(f'Categoria únicas após tratamento: {df_limpo['PR_CAT'].unique()}')
print(f'{'=' * 100}')
'''
Apenas as colunas de Categoria e Nome do produto precisam ser padronizadas,
pois conforme mostrado abaixo as colunas de Genero e Segmentação do cliente 
já estão 'padronizadas' (as 2 colunas são preenchidas com apenas caractere únicos e maiúsculos.)
'''
print(f'Generos únicos: {df_limpo['CL_GENERO'].unique()}')
print(f'Segmentaçao economica:{df_limpo['CL_SEG'].unique()}')
print(f'{'=' * 100}')

#2.5 Ajustar tipos de dados:  coluna data está como string.Precisamos converter para datetime.
df_limpo['DATA'] = pd.to_datetime(df_limpo['DATA'], 
    dayfirst=True, errors='coerce')  
print('Datas inválidas (NaT):', df_limpo['DATA'].isna().sum())
print('Tipo da coluna DATA:', df_limpo['DATA'].dtype)
print(f'{'=' *100}')


#Parte 3: Estatísticas para as colunas número de filhos dos clientes

#verificando se há nulos disfarçados na coluna número de filhos.
print(df_limpo['CL_FHL'].unique())
print('Não há nulos disfarçados na coluna número de filhos.')
print(f'{'=' *100}')

media = df_limpo['CL_FHL'].mean()
mediana = df_limpo['CL_FHL'].median()
desvio = df_limpo['CL_FHL'].std()
moda = df_limpo['CL_FHL'].mode()
maximo = df_limpo['CL_FHL'].max()
minimo = df_limpo['CL_FHL'].min()
contagem = df_limpo['CL_FHL'].count()
quartil_1 = df_limpo['CL_FHL'].quantile(0.25)
quartil_3 = df_limpo['CL_FHL'].quantile(0.75)

print(f'Média: {media}')
print(f'Mediana: {mediana}')
print(f'Desvio: {desvio}')
print(f'Moda: {moda}')
print(f'Máximo: {maximo}')
print(f'Minimo: {minimo}')
print(f'Contagem: {contagem}')
print(f'Quartil 1: {quartil_1}')
print(f'Quartil 3: {quartil_3}')
print(f'{'=' *100}')

#Parte 4: Explorar padrões de agrupamento

#4.1 Verificar quais são as categorias  mais compradas por homens e mulheres usando groupby()
print('Categorias mais compradas por homens e mulheres')
categoria_genero = (
    df_limpo.groupby(['CL_GENERO', 'PR_CAT'])['PR_CAT']
    .count()
    .reset_index(name='quantidade')
    .sort_values(['CL_GENERO', 'quantidade'], ascending=[True, False])  #ordernar por genero e quantidade
    .reset_index(drop=True)
)

print(categoria_genero)
print(f'{'=' *100}')
'''
Verificou-se que a ordem das categorias mais vendidas é igual para homens e mulheres, demonstrando um comportamento parecido ao realizar suas compras.
A categoria de Alimentos é a mais vendida, seguida por Higiene e Limpeza. 
'''

#4.2 Para aprofundar mais, vamos verificar quais são os produtos mais vendidos para homem e mulheres;
print('Produtos mais comprados por homens e mulheres')
produto_genero = (
    df_limpo.groupby(['CL_GENERO', 'PR_NOME'])['PR_NOME']
    .count()
    .reset_index(name='quantidade')
    .sort_values(['CL_GENERO', 'quantidade'], ascending=[True, False])  #ordernar por genero e quantidade
    .reset_index(drop=True)
    .groupby('CL_GENERO') #agrupa por genero novamente
    .head(10) #mostra os 10 primeiros de cada genero
    .reset_index(drop=True)
)

print(produto_genero)
print(f'{'=' *100}')

'''
Percebe-se que o presunto cozido é o mais vendido, indiferente do gênero do comprador. Esse item nunca pode faltar na área de venda, em hipótese alguma.
Itens para criança de higiene e para crianças estão no top 10 dos 2 gêneros, mulheres compram mais chupetas e homens mais fraldas.
As mulheres compram mais itens para limpeza da casa do que os homens.
'''

#4.3 Média de filhos por segmentação econômica do cliente usando pivot_table

#antes do agrupamento precisamos filtrar o ID único dos clientes, para nao distorcer a análise.
id_clientes_unicos = df_limpo.drop_duplicates(subset=['CL_ID'], keep='first')

print('Média de filhos por segmentação econômica')
media_filhos_seg = (
    id_clientes_unicos.pivot_table(
        values='CL_FHL',
        index= 'CL_SEG',
        aggfunc= 'mean')
        .reset_index()
)
print(media_filhos_seg)
print(f'{'=' *100}')

'''
Embora a média de filhos seja parecida, existe uma tendência clara. 
Conforme a segmentação econômica diminui, a média de filhos aumenta.
'''