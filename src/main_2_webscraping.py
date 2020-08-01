from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
from datetime import datetime
import pandas as pd
import schedule
#from openpyxl import Workbook

'''O objetivo desse script é continuar a coleta de dados das mesmas páginas de x em x dias e armazenar esses dados no arquivo original gerado pelo 1º script.'''


def crc_scraping():
    dia = datetime.today().date()
    dia = dia.strftime('%d/%m/%y').replace('/', '.')
    #Páginas a serem scrapeadas.
    urls_CRC = ['https://www.chainreactioncycles.com/es/es/ruedas/ruedas-de-montana', 'https://www.chainreactioncycles.com/es/es/calzado-ciclismo/shoes-mtb', 'https://www.chainreactioncycles.com/es/es/bicis-montana/doble-suspension?ss=2487&sort=pricelow']


    #Criando as listas que vão armazenar os dados que eu quero extrair das páginas selecionadas.
    #Mais abaixo os dados dessas listas serão usados para montar o data frame.
    description_df = []
    price_df = []
    rating_df = []
    comments_df = []


    #Começando a analisar cada uma das páginas selecionadas lá no início.
    for url in urls_CRC:
        #Essa linha serve para 'desviar' de um dispositivo de segurança adotado pela url escolhida. O comando engana o sevidor para que ele não pense que é um bot executando o script.
        req_CRC = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        #Abre a conexão com a página.
        CRC_client = uReq(req_CRC)
        #Faz o download da pagina e suas informações e as armazena nessa variável.
        CRC_page = CRC_client.read()
        #Essa linha fecha a conexão.
        CRC_client.close()
        #Analisa a pagina como codigo HTML.
        CRC_soup = soup(CRC_page, 'html.parser')
        #Lê todos os 'containers' dos produtos que existem nessa página. Cada container possui todas as infos que queremos exrair.
        containers = CRC_soup.find_all('div', {'class': 'products_details_container'})

        #Para cada container em containers...
        for c in containers:
            #Nesse primeiro bloco eu separo o código HTML com as informações que quero sobre cada produto, através das 'tags' onde essas informações se localizam.

            #Em description busco a 'tag' (li) e a classe ('description'), que contém o texto do nome/descrição do produto. Usamos a função 'strip' para retirar qualquer espaço em branco.
            description_html = c.find_all('li', {'class': 'description'})
            description_text = description_html[0].text.strip().replace(',', '.').strip()
            description_df.append(description_text)

            #Em price busco a 'tag' (li) e a classe ('fromamt'), que contém o texto do preço do produto. Usamos a função 'strip' para retirar qualquer espaço em branco.
            price_html = c.find_all('li', {'class': 'fromamt'})
            try:
                price_text = price_html[0].text.strip().replace('Desde', '').strip()
            except:
                price_text = '.'
            price_df.append(price_text)

            #O tratamento para extrair o texto que quero aqui em 'rating' é um pouco diferente dos anteriores, já que o elemento de 'rating' que eu quero é o texto da própria tag e não o texto inserido nela, como nos anteriores.
            # Em rating busco a 'tag' (li) e a classe ('product_rating_star'), que contém o rating do produto.
            rating_html = c.find_all('li', {'class': 'product_rating_star'})
            try:
                rating_text = rating_html[0].span['class'][0]
            except:
                rating_text = '0'
            rating_df.append(rating_text)

            #No caso de comments, como não são todos os produtos que contém essa informação, eu tenho que usar um try-except para ele.
            #Já que eu não posso terminar essa variável diretamente, eu inicializo a variável 'comments_text' aqui, para poder usá-la mais abaixo.
            #Busco a 'tag' (span) e a classe ('reviews_text'), que contém o texto com a qtd de comentários feitos sobre o produto.
            comments_html = c.find_all('span', {'class': 'reviews_text'})
            comments_text = ''

            #Nesse segundo bloco eu passo efetivamente a imprimir cada uma das informações que quero no terminal.
            #Como em todos os produtos que estou analisando, as variáveis abaixo estão presentes, eu não preciso incluí-los no try-except.
            print(description_text)
            print(price_text)
            print(rating_text)

            #Porém, no caso dos comentários, uso o try-except pq essa informação não está presente em todos os produtos e isso iria gerar um erro de Index,
            #já que a lista dessa variável seria menor do que as listas das outras variáveis (description, price e rating).
            try:
                comments_text = comments_html[0].text.strip()
                print(comments_text)
                comments_df.append(comments_text)

            #Nos produtos em que não houver comentários, eu determino que o programa imprima 'ND'. Dessa maneira o programa pode seguir funcinando normalmente.
            except IndexError:
                #Em todos os espaços em branco que haja na variável 'comments_text' vou inserir a string 'ND'.
                comments_text = comments_text.strip().replace('', 'ND')
                comments_df.append(comments_text)

            print()


    #Criando uma lista para agregar todos os elementos scrapeados para depois usá-la para montar o df.
    final_array = []


    #Organizando os dados dentro de cada "etiqueta".
    for d, p, r, c in zip(description_df, price_df, rating_df, comments_df):
        final_array.append({'PRODUCT': d, 'PRICE': p, 'RATING': r, 'COMMENTS': c})


    #Regulando o tamanho e apresentação do df que será mostrado no terminal.
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)


    df = pd.DataFrame(final_array)
    print(df)


    #Gravando os dados no mesmo arquivo, porém, em uma pestana diferente. O nome da pestana será o dia de coleta dos dados.
    with pd.ExcelWriter('CRC_prices.xlsx', engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name=dia)


#schedule.every().day.at('14:00').do(crc_scraping)
#
#while True:
#    schedule.run_pending()

crc_scraping()