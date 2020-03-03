import os

#Com essa lib eu consigo realizar a conexao ao servidor FTP
import ftplib

def main():

    conn = ftplib.FTP()
    conn.connect('10.0.0.1', 2121)
    conn.login('user','12345')

    #Configura o diretorio que se quer obter as informacoes
    # print(conn.dir("/home/rodrigoluna"))

    filename = 'Anotacoes.txt'

    # conn.retrbinary("RETR " + filename, open(filename, 'wb').write)
    #Retorna os nomes dos arquivos
    conn.retrlines('LIST')


if __name__ == '__main__':
    main()