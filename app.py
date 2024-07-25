#2ND Project  
import flask
from flask import Flask,render_template,url_for,redirect,request,flash,session
import flask_mysqldb
from flask_mysqldb import MySQL



app=Flask(__name__)



app.secret_key = 'Prask'

#MYSQL--CONECTION
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'prasham'
app.config['MYSQL_DB'] = 'NOTES'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS']="DictCursor"
mysql = MySQL(app)




ADMIN_ID={'Prasham':'LK121'}
IDS_USER=0
@app.route('/note',methods=['GET','POST'])
def home():
    
    if request.method=='POST':
        
        title1=request.form['input_title']
        content1=request.form['input_des']
        
        con=mysql.connection.cursor()
        syn=f'insert into USER{IDS_USER} (TITLE , CONTENT) values(%s,%s)'
        
        qry=[title1,content1]
        con.execute(syn,qry)
        mysql.connection.commit()
        con.close()
  
    con=mysql.connection.cursor()
    sql=f'select * from USER{IDS_USER} '
    con.execute(sql)
    result=con.fetchall()
    if 'logged_in' in session:
        
        return render_template('index.html',datas=result)
    else:
        return redirect(url_for('signin'))


@app.route('/delnote/<string:id>',methods=['POST','GET'])
def delnote(id):
    con=mysql.connection.cursor()
    syn = f'delete from USER{IDS_USER} where ID = %s'
    con.execute(syn,[id])
    mysql.connection.commit()
    con.close()
    return redirect(url_for('home'))



@app.route('/edit/<string:id>',methods=['POST','GET'])
def edit(id):
    
    if request.method=='POST':
        title1=request.form['input_title1']
        content1=request.form['input_des1']
        con=mysql.connection.cursor()
        syn = f'update USER{IDS_USER} set TITLE = %s,CONTENT = %s where ID= %s'
        qry=[title1,content1,id]
        con.execute(syn,qry)
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    con=mysql.connection.cursor()
    sql=f'select * from USER{IDS_USER} where ID=%s '
    con.execute(sql,[id])
    result2=con.fetchone()
    
    return render_template('edithpage.html',datas1=result2)


@app.route('/signin',methods=['POST','GET'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con=mysql.connection.cursor()
        usernames=str(username)
        syn='select*from Auth where Username=%s and Password = %s'
        
        con.execute(syn,[username,password])
        global IDS_USER
        IDS_USER=result[ID]
        result=con.fetchone()
        if result or username and ADMIN_ID[username]==password:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return redirect(url_for('signin'))
    return render_template('none/sign.html')    
    
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username1 = request.form['username1']
        password1 = request.form['password1']
        con=mysql.connection.cursor()
        
        qry='insert into Auth (Username,Password) values(%s,%s)'
        con.execute(qry,[username1,password1])
        mysql.connection.commit()
        
        
        syn='select*from Auth where Username=%s and Password = %s'
        
        con.execute(syn,[username1,password1])
        result=con.fetchone()
        global IDS_USER
        IDS_USER=result['ID']
        
        qry2=f"""
                CREATE TABLE USER{IDS_USER} (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            TITLE VARCHAR(50) NOT NULL,
            CONTENT VARCHAR(50) NOT NULL
                                            
                                        )
            """
        con.execute(qry2)
        mysql.connection.commit()
        
        
        
        con.close()
        if result:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return redirect(url_for('signin'))
    return render_template('none/signup.html')
    
    
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html') 
  


@app.route('/')
def out():
    return redirect(url_for('signin'))
 


if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
