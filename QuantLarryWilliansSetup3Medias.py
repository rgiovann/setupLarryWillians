# =============================================================================
# Autor: @opvistar (Twitter)                                                  #
# SETUP LARRY WILLIANS 3 MÉDIAS MÓVEIS MODIFICADO PARA ATENUAR O              #
# DRAWDOWN                                                                    #
# DESCRIÇÃO DO SETUP : https://www.youtube.com/watch?v=QXzkrR-dX1E            #
# VERSÃO: 2.3.0 (06.01.2021) - FINAL                                          #
#                                                                             #
#  LW ORIGINAL, ENTRADA E SAIDA VALORES DE FECHAMENTO DO CANDLE               #
#  TAMBÉM APRESENTA UM PEQUENO RELATORIO RENTABILIDADE NO CONSOLE             #
# =============================================================================

import datetime
import pandas as pd
import Migracao_Tryd_para_Python  as migratryd
import os as os
import math as math

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
import csv

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

# VERIFICA MÉDIAS CURTAS, DURANTE ABERTURA
# ESTÃO ABAIXO OU ACIMA DO PREÇO 
#
def HabilitaEntrada(entrada, valor1, valor2,lUp):
    if (lUp): 
        return (valor1+valor2)/2 <  entrada
    else:
        return (valor1+valor2)/2 >  entrada

      
# DEFINE O VALOR DE ENTRADA DURANTE O PREGAO, CASO QUEIRA ENTRAR
# ANTES DO FECHAMENTO, NO CASO O SCRIPT ESTA PROGRAMADO PARA
# LER O VALOR DAS MÉDIAS MOVEIS NO FECHAMENTO DO CANDLE 
def estimaEntradaouAlvo( valor1, valor2):
    return  (valor1+valor2)/2 
  

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

# ESTIMA O MELHOR VALOR PARA ENTRAR CASO USE A FUNCAO "estimaEntradaou Alvo" que é
# UM VALOR QUEBRADO E PODE NÃO REPRESENTAR UM VALOR REAL DO ATIVO
def converteValorMediaCurta(valor,lUp,tipo_ativo):
    if (tipo_ativo == WDO_DOLAR ):
        #  
        if (valor - math.floor(valor) == 0.5 or valor - math.floor(valor) == 0.0 ):  
            return(valor)   
            
        if (lUp):
            # SMAMax é 5736.45 eu saio em 5736.0  < 0,5
            # SMAMax é 5736.51 eu saio em 5736.51    >= 0.5
            if (valor - math.floor(valor) < 0.5):
                return(math.floor(valor))
            elif(valor - math.floor(valor) > 0.5):
                return(math.floor(valor) + 0.5)
        else:
            # SMAMin é 5736.45 eu saio em 5736.5  < 0,5
            # SMAMin é 5736.51 eu saio em 5736    >= 0.5
            if (valor - math.floor(valor) > 0.5):
                return(math.floor(valor) + 1.0)
            elif (valor - math.floor(valor) < 0.5):
                return( math.floor(valor) + 0.5 )
           
    elif (tipo_ativo == WIN_INDICE ):
            # SMAMax é 112878,45 eu saio em 112875
            # SMAMax é 112874,45 eu saio em 112870  
            if(math.floor(valor/5)*5 - valor == 0):
                #print("Valor não ajustado: " + str(valor) + " Valor ajustado: " + str(valor) + " lUp: " +str(lUp))            
                return valor
            if (lUp):
                # debug
                #print("Valor não ajustado: " + str(valor) + " Valor ajustado: " + str(math.floor(valor/5)*5) + " lUp: " +str(lUp))
                return(math.floor(valor/5)*5)
            else:
                # debug
                #print("Valor não ajustado: " + str(valor) + " Valor ajustado: " + str(math.floor(valor/5)*5  + 5) + " lUp: " +str(lUp))                
                return(math.floor(valor/5)*5  + 5)              
    # acoes (2 casas decimais)
    elif(tipo_ativo == A_VISTA ):                    
        if(lUp):
            #debug
            #print("Valor não ajustado: " + str(valor) + " Valor ajustado: " + str(round_down(valor,5)) + " lUp: " +str(lUp))                            
            return(round_down(valor,CASAS_DECIMAIS))
        else:
            #debug
            #print("Valor não ajustado: " + str(valor) + " Valor ajustado: " + str(round_up(valor,5)) + " lUp: " +str(lUp))                                        
            return(round_up(valor,CASAS_DECIMAIS))         
    else:
        print("**ERRO** Tipo de Ativo não definido...")
        return(valor)

###################################################################################################################################
#                                                                                                                                 #
######                                                     INICIO DO PROGRAMA                                                ######
#                                                                                                                                 #
###################################################################################################################################

   

#############                 PARÂMETROS DE CONFIGURACAO    ##############################

# lista de ativos
# NAO PODE MISTURAR DOLAR COM INDICE COM AVISTA (só um tipo)
#LISTA_B3 = {"VALE3","BBSA3","MFRG3","ENBR3",'VIVT3'}     # lista de ativos que vou pegar os dados (TICKER DA B3!!)

LISTA_B3 = {"VIVT3" }     # lista de ativos que vou pegar os dados (TICKER DA B3!!)

# período das médias longas
MEDIA_LONGA   = 21   # parametro média longa
 
# qtdade de candles que vai pegar do histórico do Tryd
NUMERO_DE_CANDLES = 10000     

EH_COMPRA = 1
EH_VENDA  = 2
EH_COMPRA_E_VENDA = 3
# tipo de operação 1: SO COMPRA, 2: SO VENDA 3: COMPRA E VENDA
TIPO_OPERACAO = EH_COMPRA_E_VENDA          

# periodo das médias curtas
MEDIAS_CURTAS = 3        # parametro médias curtas

# nome dos diretorios de entrada e saída
DIR_ENTRADA = "ENTRADA"   #
DIR_SAIDA = "SAIDA"       #
     
# ativos (tipo)        
WDO_DOLAR = 0
WIN_INDICE = 1
A_VISTA = 2

#  
UP = True       # CALCULA THRESHOLD PARA MEDIA CURTA MAXIMA
DOWN = False    # CALCULA THRESHOLD PARA MEDIA CURTA MINIMA


# tipo de ativos
# CADA ATIVO TEM UMA FORMA DE CALCULAR O THRESHOLD DE ENTRADA E 
# SAIDA --- CONFIGURAR DE ACORDO

#TIPO_ATIVO = WIN_INDICE         # 0: FUTURO DOLAR, 

TIPO_ATIVO = A_VISTA         # 0: FUTURO DOLAR, 
                             # 1: FUTURO INDICE 
                             # 2: A VISTA (necessário para arendondar os thresholds de saida)                       
CASAS_DECIMAIS = 2  
 
#############################################################################################  


# converte arquivo do Tryd para datframe Python 
migratryd.ConverteArquivosTryd(LISTA_B3,NUMERO_DE_CANDLES,DIR_ENTRADA,DIR_SAIDA)

dict_ativos_precos = {}

# crio uma lista de arrays com dados das operacoes    0           1            2            3       4         5     
#                                                 DATA_en    DATA_sai      ENTRADA    SAIDA     RESULTADO  ACUMULADO  
DATA_EN    = 0
DATA_SAI   = 1
ENTRADA    = 2                         
SAIDA      = 3
RESULTADO  = 4
ACUMULADO  = 5
TIPO       = 6
TIPO_SAIDA = 7


for ativo in LISTA_B3:
 
     file_name_py = os.path.join(os.getcwd(), DIR_SAIDA,ativo + "_Python.csv" )

     lSucesso = True
     ativo_python = pd.DataFrame(columns = ["Data","Hora","Abertura", "Fechamento","Maxima","Minima"])    
     
     try:         
         ativo_python = pd.read_csv(file_name_py, encoding = "ISO-8859-1")
     except ( IOError, NameError,PermissionError,FileNotFoundError) as e:
         print("#################################################################################################")
         print("         ### ATENÇÃO ### ocorreu um problema na leitura do arquivo .csv do ativo : " + ativo + " ..." )
         print(e)
         lSucesso = False
         print("#################################################################################################")
     if lSucesso and len(ativo_python) > 0:   
        print("Leitura arquivo .csv do ativo " + ativo + ' bem sucedida...' )
         
        # cria dicionario para cada ticker com o historico de preços
        dict_ativos_precos[ativo] = ativo_python       
print('\n')

##################################################################
#######################  INICIO DO ALGORITMO #####################
##################################################################
# itero sobre lista de ativos
nome_arquivo = os.path.join(os.getcwd(), DIR_SAIDA,"Logs_LWOriginal_" 
                            + datetime.datetime.now().strftime('%Y_%d_%m_%H_%M_%S') + ".txt" )

file_relat = open( nome_arquivo, "a")  # DEBUG


if dict_ativos_precos:


    for kx_ativo, vx_preco in sorted(dict_ativos_precos.items()):
        
        historico = []
        # inverto as linhas (de forma que linha 0 fique por ultimo e ultima linha por primeiro)   
        vx_preco  = vx_preco[::-1]
        sma21     = vx_preco['Fechamento'].rolling(window = MEDIA_LONGA).mean()
        sma3_max  = vx_preco['Maxima'].rolling(window = MEDIAS_CURTAS ).mean()
        sma3_min  = vx_preco['Minima'].rolling(window = MEDIAS_CURTAS ).mean()
        
        # transforma  a porra toda em list porque é muito mais facil de trabalhar que essa merda de dataframe....        
        l_sma21       = sma21.tolist()
        l_sma3_max    = sma3_max.tolist()
        l_sma3_min    = sma3_min.tolist()
        l_preco_max   =  vx_preco['Maxima'].tolist()        
        l_preco_min   = vx_preco['Minima'].tolist()
        l_preco_abe   = vx_preco['Abertura'].tolist()        
        l_preco_Data  = vx_preco['Data'].tolist()
        l_preco_fech  = vx_preco['Fechamento'].tolist()        
        print("Executando backtest ativo: " + kx_ativo + " Data Inicial : " + l_preco_Data[0] +
              " Data Final: " + l_preco_Data[len(l_preco_Data)-1] +"..." + "\n")
        
        for x in range(MEDIA_LONGA + 1,len(l_preco_Data)-1, 1):
             
            if not historico:
                somatoria = 0
                saida = 0
                premissa1 = True
                premissa2 = True
                elemento_historico = []
    
            else:
                
                elemento_historico = historico[len(historico)-1]
                somatoria = elemento_historico[ACUMULADO]
                saida = elemento_historico[SAIDA]  
                                  
            
            if( saida != -1 ): # Se SAIDA for diferente de -1, não tem operacao em aberto...
                
                # não tem operacao em aberto, mas só abro se premissa1 e premissa2 são verdadeiras
                # a 1a vez tem que ser verdadeira.  
                if( premissa1 and premissa2):
                    ##########################################################################
                    #
                    # PREMISSAS PARA ENTRAR NO TRADE DO LADO DA COMPRA
                    #
                    ##########################################################################
                    entradaEstimada = converteValorMediaCurta( l_sma3_min[x],DOWN,TIPO_ATIVO) # estima se preco vai cruzar média curta das minimas 
                    
                    premissa1a = l_preco_fech[x] <= entradaEstimada 
                    
                    premissa1b = False # HabilitaEntrada(l_preco_abe[x],l_preco_min[x-1],l_preco_min[x-2],DOWN)
                                      
                    premissa2a =  True  
                    #premissa2a =  l_sma21[x-1] < l_sma21[x] #and  l_sma21[x-2] < l_sma21[x-1] 

                    premissa7 = TIPO_OPERACAO == EH_COMPRA or TIPO_OPERACAO == EH_COMPRA_E_VENDA
    
                    ##########################################################################
                    
                    if( (premissa1a or premissa1b) and   premissa2a   and premissa7): # SMA21 mais recente menor que anterior
    
                        if( premissa1b): # abriu em gap, significa que ja está abaixo da minima anterior, compra na abertura
                            historico.append([l_preco_Data[x],"",l_preco_abe[x],-1,0,somatoria,"10 COMPRA","*" ] )
                        else:
                            historico.append([ l_preco_Data[x],"",l_preco_fech[x],-1,0,somatoria,"11 COMPRA","*" ] )
                            
     
    
                    ##########################################################################
                    #
                    # PREMISSAS PARA ENTRAR NO TRADE DO LADO DA VENDA
                    #
                    ##########################################################################
                    entradaEstimada = converteValorMediaCurta(l_sma3_max[x],UP,TIPO_ATIVO)
                    
                    premissa1a = l_preco_fech[x] >= entradaEstimada
                    
                    premissa1b = False # HabilitaEntrada(l_preco_abe[x],l_preco_max[x-1],l_preco_max[x-2],UP)

                    premissa2a =  True  
                    #premissa2a =  l_sma21[x] < l_sma21[x-1] #and l_sma21[x-1] < l_sma21[x-2] 
       
                    premissa7 = TIPO_OPERACAO == EH_VENDA or TIPO_OPERACAO == EH_COMPRA_E_VENDA
                    
                                                                                                        # tem que fechar acima da SMA21                  
                    if( (premissa1a or premissa1b) and premissa2a  and premissa7): # SMA21 mais recente menor que anterior
                      
                        if(premissa1b):  # GAP de alta, ja vendo na abertura
                            historico.append( [l_preco_Data[x],"",l_preco_abe[x],-1,0,somatoria,"20 VENDA","*" ] )
                        else:
                            historico.append([l_preco_Data[x],"",l_preco_fech[x],-1,0,somatoria,"22 VENDA","*" ] )
                            
            # OPERACAO EM ABERTO (saida==-1)! VERIFICA SE PODE ENCERRAR...                  
            else:    
    
            # verifico antes de mais nada se cheguei as HORARIO_ENCERRAh ou é antes das HORARIO_ENCERRAh mas vai ter meio expediente...
            # não atingiu o alvo (COMPRA OU VENDA), MAS....
            # preciso verificar se vai virar o dia antes das HORARIO_ENCERRA:00 ou proximo candle é HORARIO_ENCERRA:00h
            # e encerrar por timeout
                                     # só poder ser True se BACKTEST_M60 = True, senao sempre False            
                
                # agora verifico se algum dos criterios foram atendidos...
                                
                if ( int( elemento_historico[TIPO][0:1]) == EH_COMPRA) : 
                                        
                    ############################################## 
                    #      PREMISSAS PARA ALVO (COMPRA)          #
                    ##############################################                                         
                    saidaEstimada = converteValorMediaCurta(l_sma3_max[x],UP,TIPO_ATIVO)  
                    premissa1a    = l_preco_fech[x] >=  saidaEstimada               
                    premissa1b    = HabilitaEntrada(l_preco_abe[x],l_preco_max[x-1],l_preco_max[x-2],UP)  
                    #    = False
     
                    if (premissa1a and not premissa1b ):  
                        
                        #  zera se fechamento for maior ou igual a SMA3max                   
                        elemento_historico[SAIDA]      = l_preco_fech[x]
                        elemento_historico[TIPO_SAIDA] = "[GAIN] - SMA3Max"
                        elemento_historico[DATA_SAI]  = l_preco_Data[x]
                        elemento_historico[RESULTADO] = elemento_historico[SAIDA] - elemento_historico[ENTRADA]
                        elemento_historico[ACUMULADO] = somatoria + elemento_historico[RESULTADO]
                        historico[len(historico)-1]   = elemento_historico                        
                    
                    elif ( premissa1b ): # abertura maior que maxima do candle anterior (GAP ALTA), zero na abertura
                        elemento_historico[SAIDA]      = l_preco_abe[x] 
                        elemento_historico[TIPO_SAIDA] ="[GAIN] - GAP ALTA ZERO NA ABERTURA"
                        elemento_historico[DATA_SAI]  = l_preco_Data[x]
                        elemento_historico[RESULTADO] = elemento_historico[SAIDA] - elemento_historico[ENTRADA]
                        elemento_historico[ACUMULADO] = somatoria + elemento_historico[RESULTADO]
                        historico[len(historico)-1]   = elemento_historico
                    
                        
                elif ( int( elemento_historico[TIPO][0:1]) == EH_VENDA ):
                    
      
                    ############################################## 
                    #       PREMISSAS PARA ALVO (VENDA)          #
                    ##############################################                                   
                    saidaEstimada =  converteValorMediaCurta(l_sma3_min[x],DOWN,TIPO_ATIVO)
                    premissa1a    = l_preco_fech[x] <= saidaEstimada                       
                    premissa1b    = HabilitaEntrada(l_preco_abe[x],l_preco_min[x-1],l_preco_min[x-2],DOWN) 
                    #premissa1b    = False
                
                    if ( premissa1a and not premissa1b  ):              
                            # se fechamento igual ou abaixo da SMA3min
                            elemento_historico[SAIDA]        = l_preco_fech[x] 
                            elemento_historico[TIPO_SAIDA]   = "[GAIN] - SMA3Min"
                            elemento_historico[DATA_SAI]  = l_preco_Data[x]
                            elemento_historico[RESULTADO] = elemento_historico[ENTRADA] - elemento_historico[SAIDA]
                            elemento_historico[ACUMULADO] = somatoria + elemento_historico[RESULTADO]
                            historico[len(historico)-1]   = elemento_historico   
                            
                    elif( premissa1b ):
                    
                            # se abriu com gap, já zero na abertura
                            elemento_historico[SAIDA]         = l_preco_abe[x] 
                            elemento_historico[TIPO_SAIDA]    = "[GAIN] - GAP BAIXA ZERO NA ABERTURA"
                            elemento_historico[DATA_SAI]  = l_preco_Data[x]
                            elemento_historico[RESULTADO] = elemento_historico[ENTRADA] - elemento_historico[SAIDA]
                            elemento_historico[ACUMULADO] = somatoria + elemento_historico[RESULTADO]
                            historico[len(historico)-1]   = elemento_historico                                   
         
        print('\n',file=file_relat)        
        print("Resultados para o ativo :" + kx_ativo +'\n',file=file_relat )
        tabela = pd.DataFrame(historico,columns=['DATA_EN', 'DATA_SAI', 'ENTRADA','SAIDA','RESULTADO','ACUMULADO','TIPO','TIPO_SAIDA'])
        print('==================================================================================================',file=file_relat)       
        print(tabela.round(decimals=2),file=file_relat)
        
        historico_csv = [ ]
    
        print("===============================================")
        elemento_historico_0 =  historico[0]
        elemento_historico_1 =  historico[len(historico)-1]    
        print("Acumulado   : " + str(round(elemento_historico_1[ACUMULADO],2) )) 
        print("Nr operacoes: " + str(len(historico)))
        print("Valor/Trade : " + str(round(elemento_historico_1[ACUMULADO]/len(historico),2)))
        print('MEDIA_LONGA : ' + str(MEDIA_LONGA))
        print('PREÇO ENTRADA: ' + str(round(elemento_historico_0[ENTRADA],2)))
        print('PREÇO SAIDA  : ' + str(round(elemento_historico_1[ENTRADA],2)))    
        print('VALOR ACCUM  : ' + str(round(elemento_historico_1[ACUMULADO],2)))            
        print('DATA ENTRADA: ' + elemento_historico_0[DATA_EN])
        print('DATA SAIDA  : ' + elemento_historico_1[DATA_EN])

        
        rentabilidade_BH = ((elemento_historico_1[ENTRADA] - elemento_historico_0[ENTRADA])/elemento_historico_0[ENTRADA])*100
        rentabilidade_LW = ((elemento_historico_1[ACUMULADO] - elemento_historico_0[ENTRADA])/elemento_historico_0[ENTRADA])*100
        print('Rentabilidade BH: '+ str(round(rentabilidade_BH,2)) +'%')
        print('Rentabilidade LW: '+ str(round(rentabilidade_LW,2)) +'%')        
        print("===============================================")
        
        # comenta no momento
        for x in range(0,len(historico), 1): 
            elemento_historico = historico[x] 
            elemento_historico[SAIDA]           = str(round(elemento_historico[SAIDA],2)).replace('.',',')
            elemento_historico[ENTRADA]         = str(round(elemento_historico[ENTRADA],2)).replace('.',',')
            elemento_historico[RESULTADO]       = str(round(elemento_historico[RESULTADO],2)).replace('.',',')
            elemento_historico[ACUMULADO]       = str(round(elemento_historico[ACUMULADO],2)).replace('.',',')
    
            historico_csv.append(elemento_historico)
    
    
        nome_arquivo = os.path.join(os.getcwd(), DIR_SAIDA, 
                                    "Relatorio_LW_Original_" +   kx_ativo + "_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".csv" )  
        with open(nome_arquivo, 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            csvwriter = csv.writer(csvfile,delimiter =';')
            csvwriter.writerows(historico_csv)        
    
            
            
print("Backtest conluído, verifique o arquivo " + nome_arquivo)    
file_relat.close()    



