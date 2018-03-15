import requests
from datetime import datetime
from lxml import html

def getPageContent(page_url):
    return requests.get(page_url).content;

def extractAllLinksFromPage(page_content):
    html_tree = html.fromstring(page_content)
    html_tree.resolve_base_href()
    elements = html_tree.xpath('//a')
    return map(lambda element: element.get('href'), elements);

def saveFile(file_name, file_content):
    print('saving ' + file_name)
    with open(file_name, 'wb') as f:
        f.write(file_content)

def downloadExcelFiles(excel_links):
    downloads_count = 0
    date = datetime.now()
    for excel_link in excel_links:
      if MONTHS[date.month] in excel_link:
          file_name = 'Dados/Dados-' + str(date.day) + '-' + str(date.month) + '-' + str(date.year) + '-' + str(downloads_count) + '.xlsx'
          excel_content = getPageContent(excel_link);
          downloads_count = downloads_count + 1
          saveFile(file_name, excel_content)

    return downloads_count

MONTHS = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

def main():
    feam_url = "http://www.feam.br/noticias/1/1327-boletim-qualidade-do-ar"
    page_content = getPageContent(feam_url)
    links = extractAllLinksFromPage(page_content)
    excel_links = filter(lambda link: link is not None and ".xlsx" in link, links);
    result = downloadExcelFiles(excel_links);
    print(str(result) + ' files downloaded!');

if __name__ == "__main__":
    main()
