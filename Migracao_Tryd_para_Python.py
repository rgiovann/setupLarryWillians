import pandas as pd
import sys
import os as os
#############################################################################################
#############################################################################################
#  AUTOR: @opvistar (Twitter)
#  DATA: dez/2021
#  ESSE SCRIPT LE OS ARQUIVOS DO TRYD E GERA (NÃO É PRA SER EXECUTADO, CHAMADO PELO SCRIPT
#  DO LW CLÁSSICO)
#  A TABELA DE DADOS PARA USAR NOS SCRIPT QuantLarryWilliansSetup3Medias.py
#  VERSÃO: 1.1.0 (30.12.21) - FINAL
############################################################################################
 

def ConverteArquivosTryd(listaAtivos, linhasLidas,dir_entrada,dir_saida):
 
    print("Convertendo dados _Tryd.csv para dataframe Python (_Python.csv...)")
     
    # colunas padrão
    colunas_Tryd_Basica = ['Data','Abertura','Fechamento','Máxima','Mínima']     # as colunas essenciais são DATA, FECHAMENTO, MAXIMA E MINIMA
    
    # caso leitura de colunas adicionais
    colunas_Tryd_Extra  = ['Data','Hora','Fechamento','Máxima','Mínima'] 
    lColunasExtras = False
     
    
    for ativo in listaAtivos:
        
        # semanal
        #str_path_tryd = "C:\\Users\\rgiovann\\OneDrive\\AULAS\Bagozzi\\PYTHON_SOURCE\\FINANCAS_QUANTITATIVAS\\Database_Tryd_Semanal\\"+ ativo + "_tryd.csv"
        
        # diario
        str_path_tryd = os.path.join(os.getcwd(), dir_entrada,ativo + "_Tryd.csv" )
        
        #str_path_tryd = ativo + "_Tryd.csv" 
    
        # semanal    
        #str_path_py  = "C:\\Users\\rgiovann\\OneDrive\\AULAS\Bagozzi\\PYTHON_SOURCE\\FINANCAS_QUANTITATIVAS\\Database_Python_Semanal\\"+ ativo + "_python.csv"
        
        #diario
        str_path_py = os.path.join(os.getcwd(), dir_saida,ativo + "_Python.csv" )
        
        #str_path_py  = ativo + "_python.csv"
           
        try:
            precos = pd.read_csv(str_path_tryd,encoding = "ISO-8859-1")

    
        except ( IOError, NameError,PermissionError,FileNotFoundError) as e:
            print("#################################################################################################")
            print("                ### ATENÇÃO ### ocorreu um problema na leitura arquivo DB Tryd ativo: " + ativo )
            print(e)
            print("#################################################################################################")
            sys.exit()
         
            ##############################################
            # processa só preco de fechamento, 
            # troca virgula por ponto, transforma em 
            # numerico
            ##############################################
            
        # define se le as colunas padrão ou extras
        if not lColunasExtras:
            qColunas = colunas_Tryd_Basica
        else:
            qColunas = colunas_Tryd_Extra
             
        df_csv_python = precos[qColunas].head(linhasLidas)
         
        # tira acentos do titulo para as colunas maxima, minima (essenciais)
        df_csv_python.rename(columns={'Máxima':'Maxima','Mínima':'Minima' },inplace=True)
             
        # virgula vira ponto (numeracao USA)
        for idx in df_csv_python.index: 
            for str_coluna in df_csv_python.columns:
                str_tmp = df_csv_python[str_coluna][idx]
                # no caso do mini indice tem ponto 100.203,000 - remover o ponto
                df_csv_python[str_coluna][idx] = str_tmp.replace('.','')
                
                # aqui troca a virgula pelo ponto.
                str_tmp = df_csv_python[str_coluna][idx]
                df_csv_python[str_coluna][idx] = str_tmp.replace(',','.')
            
          
             
        ############################# TESTE  ############################
        
             # df_csv_python_reversed = df_csv_python.iloc[::-1]
             # print(df_csv_python_reversed['Fechamento'][0])
             # print(df_csv_python['Fechamento'][0])
            
             # list_A = df_csv_python['Fechamento'].tolist()
             # list_A_rev = df_csv_python_reversed['Fechamento'].tolist()
             
             # for idx, (_, value) in enumerate(df_csv_python_reversed.iterrows()):
             #     #print(df_csv_python_reversed['Fechamento'][idx])
             #     print( df_csv_python_reversed['Fechamento'][ df_csv_python_reversed.index.get_loc(idx) ])
             #     list(df_csv_python_reversed.index)
          
        ############################# FIM TESTE  ############################
         
         ##############################################
         # salva panda serie em dataframe
         # e salve em arquivo csv
         ##############################################
         # migração para o BD Python...
        try:
            df_csv_python.to_csv(str_path_py, index=False)
        
        except ( IOError, NameError,PermissionError,FileNotFoundError) as e:
            print("#################################################################################################")
            print("         ### ATENÇÃO ### ocorreu um problema nas escrita do arquivo DB Python ativo: " + ativo )
            print(e)
            print("#################################################################################################")
            # SÓ PRINTA O ERRO E VAI ATE O FIM
            #sys.exit()
    return
