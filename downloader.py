#!/usr/bin/python
#encoding: utf-8

from splinter.browser import Browser
from pprint import pprint
from urlparse import urlsplit
from subprocess import Popen
from multiprocessing import Process

from argparser import parsear_argumentos
from log import configura_log, configura_log_db
from model import *

# prepara estrutura do banco de dados
setup_all()
#  criar o banco se ele não existir
create_all()

argumentos = parsear_argumentos()
logger = configura_log(argumentos.log)
configura_log_db(argumentos.log_db)

DOWNLOAD_URL='http://www.miui.com/development.html'
CONNECTIONS=10
OUTPUT_DIR='/tmp'
LOG_DIR='/tmp'
logger.info("Downloading roms from %s, each download with %d connections." % (DOWNLOAD_URL, CONNECTIONS))
logger.info("Output dir is '%s'." % OUTPUT_DIR)
logger.info("Download Log dir is '%s'." % LOG_DIR)

browser = Browser('firefox')
logger.info('Loading the page.')
browser.visit(DOWNLOAD_URL)
logger.info('Page loaded.')

# encontrando todos os links das roms (tag <a> com classe 'download')
links = browser.find_by_css('a.download')
# pegando nome do arquivo da url
nomes_arquivos = [urlsplit(link['href']).path.split('/')[-1] for link in links]
# pegando nome do aparelho no nome do arquivo
nomes_aparelhos = [nome_arquivo.split('_')[1] for nome_arquivo in nomes_arquivos]
# pegando a versão da MIUI
versoes_miui = [nome_arquivo.split('_')[2] for nome_arquivo in nomes_arquivos]
# pegando a versão do Android em que a MIUI foi feita
versoes_android = [nome_arquivo.split('_')[-1][:-4] for nome_arquivo in nomes_arquivos]

# montando um dicionario com os dados
dados = zip(links, nomes_arquivos, nomes_aparelhos, versoes_miui, versoes_android)
for (link, nome_arquivo, nome_aparelho, versao_miui, versao_android) in dados:
    if not Rom.existe(nome_aparelho):
        logger.debug('Device %s not found in database, adding it.' % nome_aparelho)
        rom = Rom.cria(nome_aparelho, versao_miui, versao_android, link['href'], nome_arquivo)
    else:
        logger.debug('Already found the device %s in the database, checking the version.' % nome_aparelho)
        rom = Rom.query.filter_by(aparelho=nome_aparelho).first()
        # rom = session.query(Rom).filter(Rom.aparelho == nome_aparelho).first()
        if rom.versao_miui == versao_miui and rom.baixada:
            logger.debug('Rom version %s for device %s was already downloaded.' % (rom.versao_miui, rom.aparelho))
        elif rom.versao_miui == versao_miui and not rom.baixada:
            logger.debug('Rom version %s for device %s found in database but it is not downloaded.' % (rom.versao_miui, rom.aparelho))
        elif rom.versao_miui != versao_miui:
            logger.debug('Found a new version (%s) of the rom for the device %s. Last was %s.' % (versao_miui, nome_aparelho, rom.versao_miui))
            rom.versao_miui = versao_miui
            rom.baixada = False

logger.info('Committing the devices the were not previously in the database or had its version updated.')
session.commit()

# fechando o navegador
browser.quit()

# funcao pra fazer download dos arquivos
def download_rom(rom, session):
    logger.debug('Starting/resuming the download of rom %s for device %s.' % (rom.versao_miui, rom.aparelho))
    # comando para fazer o download para o OUTPUT_DIR de cada rom, com CONNECTIONS número de conexões cada
    comando = "axel -n%d -o %s %s" % (CONNECTIONS, OUTPUT_DIR, rom.link)
    comando = comando.split()
    log = open("%s/%s.log" % (LOG_DIR, rom.aparelho), 'w+')
    # roda o comando de download e redireciona a saida para o arquivo definido em log
    download = Popen(comando, stdout=log)
    download.wait()
    log.close()
    log = open("%s/%s.log" % (LOG_DIR, rom.aparelho), 'r').read()
    if not 'Downloaded' in log:
        logger.debug('Failed to download the rom %s for device %s' % (rom.versao_miui, rom.aparelho))
        rom.baixada = False
        session.commit()
        return
    # atualizando dados da rom no banco de dados
    logger.debug('Updating the download status for device %s.' % rom.aparelho)
    rom.baixada = True
    session.commit()


# esse codigo cria um processo pra download da rom de cada aparelho e inicia ele
logger.info('Preparing the download processes pool.')
processos = []
for rom in Rom.query.all():
    if not rom.baixada:
        processo = Process(
                        target=download_rom,
                        args=(rom, session)
                    )
        processo.start()
        processos.append(processo)
    else:
        logger.debug('Rom %s for %s was already downloaded last time this script ran, skipping.' % (rom.versao_miui, rom.aparelho))
# bloqueia o script até todos os downloads paralelos terminarem
logger.info('Waiting for all pending downloads to complete.')
[processo.join() for processo in processos]
logger.info('Downloads done.')

import ipdb; ipdb.set_trace()
