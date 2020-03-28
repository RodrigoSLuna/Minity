import os
import sys
import socket   
#Com essa lib eu consigo realizar a conexao ao servidor FTP
import ftplib

def main():

    ftp = ftplib.FTP()
        
    print(sys.argv)

    IPAddr = sys.argv[1]
    port = 2121

    
    path = sys.argv[2]
    filename = sys.argv[3]
    ftp.connect(IPAddr, port)
    ftp.login('user','12345')

    #Configura o diretorio que se quer obter as informacoes
    # print(conn.dir("/home/rodrigoluna"))

    file = open(path+"/"+filename, 'wb')
    
    ftp.retrbinary("RETR " + 'files/' +filename, file.write)
    #Retorna os nomes dos arquivos
    
if __name__ == '__main__':
    main()