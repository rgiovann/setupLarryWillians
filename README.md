# SetupLarryWillians
Setup Larry Willians (detalhes em https://www.youtube.com/watch?v=QXzkrR-dX1E

***Este script executa o setup LW de 3 médias móveis SMA21(fechamento) SMA3(max) e SMA3(min). O script usa com arquivos de entrada os arquivos CSV gerados pelo Tryd (homebroker). Os arquivos salvos pelo Tryd deverão estar no formato <TICKER_B3>_Tryd.csv (exemplo: ABEV3_Tryd.csv)***

São dois scripts:

**Migracao_Tryd_para_Python.py**
Este scripts le os arquivos gerados pelo Tryd e os converte em tabelas que são tranformadas em DATAFRAME para posterior processamento. Os arquivos gerados tem a nomemclatura <TICKER_B3>_Python.csv (ex. ABEV3_Python.csv).

**QuantLarryWilliansSetup3Medias.py**

#############     PARÂMETROS DE CONFIGURACAO     ###############################################################

- LISTA_B3 = {"NEOE3","ITSA4"}     # lista de ativos csv que vou pegar os dados no diretório DIR_ENTRADA (TICKER DA B3!!)
- MEDIA_LONGA = 21           # parametro média longa
- NUMERO_DE_DIAS = 5000      # qtdade dias que vai pegar do histórico do Tryd
- DESABILITA_VENDA = False   # somente operacões de compra = True
- MEDIAS_CURTAS = 3          # parametro médias curtas
- DIR_ENTRADA = "ENTRADA"    # nome do diretório que vc vai criar antes de rodar o script, para popular com os arquivos salvos do Tryd default é "ENTRADA"
- DIR_SAIDA = "SAIDA"        # nome do diretório que vc vai criar antes de rodar o script, que estão os arquivos com os resultados do backtest default é "SAIDA"

##########################################################################################################  

O resultado do backtest é armazenado em arquivo de log (com todos os ativos) e planilha csv (por ativo)

NOTA: SÓ FUNCIONA PARA TIMEFRAME DIÁRIO.
