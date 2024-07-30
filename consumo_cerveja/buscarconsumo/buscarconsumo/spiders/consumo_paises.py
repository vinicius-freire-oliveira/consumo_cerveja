import scrapy

class ConsumoPaisesSpider(scrapy.Spider):
    name = 'consumo_paises'
    start_urls = ['https://pt.wikipedia.org/wiki/Lista_de_pa%C3%ADses_por_consumo_de_cerveja_por_pessoa']

    def parse(self, response):
        # Encontra todas as tabelas na página
        tabelas = response.xpath('//table[contains(@class, "wikitable")]')
        self.log(f'Número de tabelas encontradas: {len(tabelas)}')

        for tabela in tabelas:
            for linha in tabela.xpath('.//tr')[1:]:  # Ignora o cabeçalho
                colunas = linha.xpath('.//td')

                # Verifica se há o número correto de colunas
                if len(colunas) >= 3:
                    # Extrai o texto da coluna de classificação
                    classificacao = colunas[0].xpath('.//text()').getall()
                    classificacao = ' '.join(c.strip() for c in classificacao if c.strip())

                    # Extrai o texto da coluna do país
                    pais = colunas[1].xpath('.//text()').getall()
                    pais = ' '.join(p.strip() for p in pais if p.strip())

                    # Extrai o texto da coluna de consumo
                    consumo = colunas[2].xpath('.//text()').getall()
                    consumo = ' '.join(c.strip() for c in consumo if c.strip())

                    if classificacao and pais and consumo:
                        # Adiciona logs para verificar os dados extraídos
                        self.log(f'Classificação: {classificacao}, País: {pais}, Consumo: {consumo}')

                        # Cria um dicionário para armazenar os dados raspados
                        yield {
                            'Classificação': classificacao,
                            'País': pais,
                            'Consumo (L/per capita)': consumo
                        }
