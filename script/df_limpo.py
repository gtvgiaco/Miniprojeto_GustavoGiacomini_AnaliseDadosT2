import pandas as pd
import numpy as np

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

#Parte 2: Tratamentos

#2.1 Eliminar duplicadas: será mantida apenas primeira ocorrência. Todas as outras repetições serão removidas.
df_limpo = df_limpo.drop_duplicates(keep='first') #dro_duplicates sem subset pois quero remover apenas as linhas totalmente iguais.
#Verificando se há duplicadas após a remoção
print(f'Duplicadas Após Keep: {df_limpo.duplicated().sum()}')
print(f'{'=' * 100}')
#Reindexar após remoção de linhas
df_limpo = df_limpo.reset_index(drop=True)

#2.2 Remover nulos: as colunas 11, 12, 13 e 14 tem 100% de nulos e serão excluidas, pois não contribuem com informações para a análise
df_limpo = df_limpo.drop(columns=['Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13'])

#2.3 Tratamento de nulos disfarçados

#Coluna PR_CAT (categoria do produto). 
print(f'Categorias únicas: {df_limpo['PR_CAT'].unique()}') #aqui foi verificado que existem linhas preenchidas com categoria #N/D 
#Substituição de #N/D por Sem Categoria
print(f'{'=' * 100}')

df_limpo['PR_CAT'] = df_limpo['PR_CAT'].replace({'#N/D':'Sem Categoria'})
print(f'Categorias únicas após substituição de #N/D: {df_limpo['PR_CAT'].unique()}')  #verificando a alteração.
print(f'{'=' *100}')

#Verificação de nulos disfarçados das demais colunas. 
demais_colunas = ['CO_ID', 'CL_ID', 'CL_GENERO', 'CL_EC', 'CL_FHL', 'CL_SEG','PR_ID' ,'PR_NOME' ]
df_limpo[demais_colunas] = df_limpo[demais_colunas].replace('#N/D', np.nan) #subsituir #N/A (padrão de nulo disfaraçado do dataset) por nulos reais.
print(f'Quantidade de disfarçados nas demais coluna: \n{df_limpo[demais_colunas].isna().sum()}')
print(f'{'=' *100}')

#Na coluna PR_NOME existem 3228 registros de nulos disfarçados (#N/D). Será substituído por Sem Nome
df_limpo['PR_NOME'] = df_limpo['PR_NOME'].fillna('Sem Nome')
print(f'Quantidade de nulos disfarçados na coluna PR_NOME após alteração: {df_limpo['PR_NOME'].isna().sum()}') 
print(f'{'=' *100}')
#Observação: será verificado os nulos disfarçados da coluna DATA junto com a conversão para datetime.

#2.4 Padronizar strings nas colunas PR_CAT e PR_NOME (primeira letra em maiusculo)
df_limpo['PR_CAT'] = df_limpo['PR_CAT'].str.strip().str.title()
df_limpo['PR_NOME'] = df_limpo['PR_NOME'].str.strip().str.title()
print(f'Nome do Produto após tratamento: {df_limpo['PR_NOME'].unique()[:10]}') #mostrar apenas os 10 primeiros produtos, pois são muitos.
print(f'{'=' * 100}')
print(f'Categoria únicas após tratamento: {df_limpo['PR_CAT'].unique()}')
print(f'{'=' * 100}')
'''
Apenas as colunas de Categoria e Nome do produto precisam ser padronizadas,
pois conforme mostrado abaixo as colunas de Genero e Segmentação do cliente 
já estão 'padronizadas' (as 2 colunas são preenchidas com apenas caracteres únicos e maiúsculos.)
'''

#2.5 Ajustar tipos de dados:  coluna DATA está como string. Precisamos converter para datetime.
df_limpo['DATA'] = pd.to_datetime(df_limpo['DATA'], 
    dayfirst=True, errors='coerce')  
print('Datas inválidas (NaT):', df_limpo['DATA'].isna().sum())
print('Tipo da coluna DATA:', df_limpo['DATA'].dtype)
print(f'{'=' *100}')

#2.6 Vertificando outliers no volume de itens por compra com IQR.
'''
A inteção é saber se existem compras com volume de itens muito acima do normal.
Com isso, podemos identificar quais são os clientes que efetuaram essas compras e se
esse comportamento se repete nas demais compras desses clientes.
'''
itens_compra = df_limpo['CO_ID'].value_counts()

#2.6.1 Calcular os quartis
print('Verificação de Outliers no volume de itens por compra.')
Q1 = itens_compra.quantile(0.25)
Q3 = itens_compra.quantile(0.75)
IQR = Q3 - Q1

#2.6.2 Calcular os limites
limite_inf = Q1 - 1.5 * IQR #Abaixo disso é outlier
limite_sup = Q3 + 1.5 * IQR #Acima disso é outlier

print(f'Faixa normal de itens por compra: [{limite_inf}, {limite_sup}]')

#2.6.2 Ver quais são os outliers
print('Outliers:')
mascara = (itens_compra < limite_inf) | (itens_compra > limite_sup)
print(f'Outliers encontrados (maiores quantidade de itens por compra): {mascara.sum()}') 
print(itens_compra[mascara])
print(f'{'=' *100}')

'''
Não foram detectados outliers (compras com volume de itens muito acima do normal)
'''

#Parte 3:  Análise exploratória

#3.1 Estatísticas para as colunas número de filhos dos clientes (Já verificamos acima os nulos disfarçados na coluna número de filhos.)

media = df_limpo['CL_FHL'].mean()
mediana = df_limpo['CL_FHL'].median()
desvio = df_limpo['CL_FHL'].std()
moda = df_limpo['CL_FHL'].mode()
maximo = df_limpo['CL_FHL'].max()
minimo = df_limpo['CL_FHL'].min()
contagem = df_limpo['CL_FHL'].count()
quartil_1 = df_limpo['CL_FHL'].quantile(0.25)
quartil_3 = df_limpo['CL_FHL'].quantile(0.75)

print('Estatísticas da coluna CL_FLH (qtade filhos dos cliente:)')
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


#3.2 Perfil do Cliente

condicoes = [
    (df_limpo['CL_EC'] == 1) & (df_limpo['CL_FHL'] == 0), #Casados sem filho (famlia 2 pessoas)
    (df_limpo['CL_EC'] == 1) & (df_limpo['CL_FHL'] == 1), #casados com filhos único (famílias 3 pessoas)
    (df_limpo['CL_EC'] == 1) & (df_limpo['CL_FHL'] > 1), #casados com mais de 1 filho (familias de 4 pessoas ou mais)
    (df_limpo['CL_EC'] == 4) & (df_limpo['CL_FHL'] == 0), #Solteiros sem filhos 
    (df_limpo['CL_EC'] == 4) & (df_limpo['CL_FHL'] >=1 ), #Solteiros com filho(s) 
    ((df_limpo['CL_EC'] == 2) | (df_limpo['CL_EC'] == 3)) & (df_limpo['CL_FHL'] == 0), #Divorciado/Separado sem filho
    ((df_limpo['CL_EC'] == 2) | (df_limpo['CL_EC'] == 3)) & (df_limpo['CL_FHL'] >= 1), #Divorciado/Separado com filho
    (df_limpo['CL_EC'] == 5) & (df_limpo['CL_FHL'] == 0), #Viúvo sem filho
    (df_limpo['CL_EC'] == 5) & (df_limpo['CL_FHL'] >= 1), #Viúvo com filho
]

resultados = [
    'Casados Sem Filhos',
    'Casados Com 1 Filho',
    'Casados Mais 1 Filho',
    'Solteiro Sem Filho', 
    'Solteiro Com Filho(s)',
    'Divorciado/Separado Sem filho',
    'Divorciado/Separado com filho(s)',
    'Víuvo Sem Filho',
    'Viúvo Com Filho(s)']

df_limpo['CL_PERFIL'] = np.select(               # criando a coluna CL_PERFIL
    condicoes, resultados, default='Sem Perfil'
)

'''
Como os registros são feitos por produtos comprados e o mesmo cliente pode comprar vários produtos e retornar várias vezes ao estabelecimento, o CL_ID se repete muitas vezes.
O mesmo cliente deve ser contado apenas uma vez, portanto será criado um df_clientes e mantido apenas a primeira ocorrencia do id do cliente.
'''

df_clientes = df_limpo.drop_duplicates(subset=['CL_ID'], keep='first')

#exibindo a porcentagem dos perfis
print('Perfil dos Clientes:')
perfil = df_clientes['CL_PERFIL'].value_counts()
perfil_perc = df_clientes['CL_PERFIL'].value_counts(normalize=True) * 100
perfil_resumo = pd.DataFrame({
    'QTD_CLIENTES': perfil,
    '(%)': perfil_perc})
print(perfil_resumo)

'''
48.8% dos clientes da base são pessoas divorciadas, sendo 25.40% sem filhos e 23.40% com filhos. 
   
'''

#3.3  Gênero que mais frequenta o mercado (numero de compras)?
print('Frequência de compras por Gênero: ')
genero_frequente = df_limpo.groupby('CL_GENERO')['CO_ID'].nunique().reset_index(name='QTD_COMPRAS') #Compras únicas por genero
total_compras = genero_frequente['QTD_COMPRAS'].sum()  
genero_frequente['(%)'] = (genero_frequente['QTD_COMPRAS'] / total_compras) * 100
print(genero_frequente)
print(f'{'=' *100}')

'''
A frequencia de compra é bem equilibrada entre os gêneros. As mulheres são responsáveis por 52% das compras.
'''

#3.4 Verificar quais são as categorias  mais compradas por homens e mulheres usando groupby()
print('Categorias mais compradas por gênero')
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

#3.5 Para aprofundar mais, vamos verificar quais são os produtos mais vendidos para homem e mulheres;
print('Produtos mais comprados por gênero')
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

#3.6 Média de filhos por segmentação econômica do cliente usando pivot_table

#Antes do agrupamento precisamos filtrar o ID único dos clientes, para nao distorcer a análise.
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


# 3.7 Ver quais dias tem mais movimento (hipótese: confirmar se as datas coincidem com os dias de pagamento de salário)

from datetime import date, datetime

df_limpo['dia_mes'] = df_limpo['DATA'].dt.day #extrair o dia
df_limpo['periodo_compra'] = pd.cut(
    df_limpo['dia_mes'],
    bins = [1, 10, 20, 31],
    labels = ['Pgto Salário', 'Meio do Mês', 'Final do mês']
)

compras_por_dia = df_limpo.groupby('periodo_compra')['CO_ID'].nunique().reset_index(name='total_compras')
total_compras_dia = compras_por_dia['total_compras'].sum()
compras_por_dia['(%)'] = (compras_por_dia['total_compras'] / total_compras_dia) * 100
print(compras_por_dia)

'''
O movimento na loja não é impactado fortemente pelo pagamento de salário. 
Ao contrário do que se esperava (maior movimentação coincidindo com as datas de pagamento de salário.)
'''

df_limpo = df_limpo.drop(columns=['dia_mes', 'periodo_compra'])
df_limpo.to_csv('data/base_varejo_limpa.csv', sep=';', encoding = 'utf-8', decimal = ',')

