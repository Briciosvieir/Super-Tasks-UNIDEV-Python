from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)


#preciso dessa secret kay para liberar o flash e não da erro na hora de enviar a msg
app.secret_key='pode ser uma chave ou senha, criptografia e por ai vai (senhasecreta)'

app.config["MYSQL_HOST"] ="localhost"
app.config["MYSQL_USER"] ="root"
app.config["MYSQL_PASSWORD"] =""
app.config["MYSQL_DB"] = "task"
app.config["MYSQL_PORT"] = 3306

db=MySQL(app)

#function que recebe todos os dados da tabela
def get_all_task():
    query = "SELECT * FROM task"
    cursor = db.connection.cursor()
    cursor.execute(query)
    task = cursor.fetchall()
    task_list=[] # criado uma variavel que recebe todos os dados da tabela
    for tasks in task:
        task_list.append({
            "id":tasks[0],
            "title": tasks[1],
            "completed": tasks[2]=='Y',
            "daytime":tasks[3].strftime('%d/%m/%Y')
        })

    cursor.close()
    return task_list

# importando o render_template para exibir a informação da anterior na tela, obs que
#
@app.route("/")
def index():
    if 'enter_id'  not in  session:
        return redirect(url_for("login_"))

    return render_template('list.html', tasks=get_all_task())




#metodo que insere no bando de dados
def insert_tesk(tittle):
    query= "INSERT INTO task (title) VALUES (%s)"
    cursor = db.connection.cursor()
    cursor.execute(query,[tittle])
    db.connection.commit()
    cursor.close()
#
@app.route("/store/",methods=['POST'])
def insert_task():
    inserty = request.form["name"]
    insert_tesk(inserty)
    flash("Item cadastrado com sucesso!", "success")
    return redirect(url_for("index"))


#metodo para deletar um item do banco de dados MariaDB.
def delet_tesk(id):
    query = "delete from task where id = %s "
    cursor = db.connection.cursor()
    cursor.execute(query,[id])
    db.connection.commit()
    cursor.close()

@app.route("/delet/<int:id>")
def remove(id):
    delet_tesk(id)
    flash("Item deletado com sucesso!", "warning")
    return redirect(url_for("index"))

#Sobre da pagina
@app.route("/sobre/")

def about():
    return render_template( "about.html" )


#aqui tem o botão com complete, ou seja, ele muda conforme o clique e identifica se já foi analisado ou não
'''def complete_tesk(id):
    query = "UPDATE task SET completed ='Y' where id=%s "
    cursor=db.connection.cursor()
    cursor.execute(query,[id])
    db.connection.commit()
    cursor.close()

@app.route("/completed/<int:id>")
def completed_task(id):
    complete_tesk(id)
    return redirect(url_for("index"))


#esse faz faz o contrário do anterior
def dexfixed_tesk(id):
    query = "UPDATE task SET completed ='N' where id=%s "
    cursor=db.connection.cursor()
    cursor.execute(query,[id])
    db.connection.commit()
    cursor.close()

@app.route("/dexfixed/<int:id>")
def dexfixed(id):
    dexfixed_tesk(id)
    return redirect(url_for("index"))

'''

# function que altera a informação, concluído/fixado
def switch(id):
    status = request.args.get("status")
    if status =='True':
        query = "UPDATE task SET completed ='N' where id=%s "
    else:
        query = "UPDATE task SET completed ='Y' where id=%s "
    cursor = db.connection.cursor()
    cursor.execute(query, [id])
    db.connection.commit()
    cursor.close()


@app.route("/switch/<int:id>")
def switch_task(id):
    switch(id)

    return redirect(url_for("index"))


#criando uma rota para o login
@app.route("/login/")
def login_():
    return render_template("login.html")

#criando uma rota para pegar no metodo post as informações login
@app.route("/authenticate", methods=['GET','POST'])
def authent():
    login_txt = request.form['login']

    password_txt = request.form['password']

    query = "SELECT * FROM users WHERE login = %s AND PASSWORD = %s"
    cursor = db.connection.cursor()
    cursor.execute(query, [login_txt, password_txt])
    logger_user = cursor.fetchone()
    cursor.close()

    if logger_user is None:
        return redirect(url_for('login_'))

    session['enter_id'] = logger_user[0]
    session['enter_name'] = logger_user[1]
    return redirect(url_for('index'))


# fazendo logof do programa
@app.route('/logout')
def logout():
    session.pop('enter_id')
    session.pop('enter_name')
    return redirect(url_for('index'))




app.run(debug=True)