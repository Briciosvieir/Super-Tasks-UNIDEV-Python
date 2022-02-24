import pymysql

conexao = pymysql.connect(
host='localhost',
user='root',
password='',
database=""

)

curso = conexao.cursor()
curso.execute("show databases")

for data in curso:
    print(data)