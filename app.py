from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql

app = Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)
app.secret_key = 'nccugogo'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/reader')
def reader():
    return render_template('reader.html')

@app.route('/new_reader')
def new_reader():
    return render_template('new_reader.html')

@app.route('/new_staff')
def new_staff():
    return render_template('new_staff.html')

@app.route('/r_signup',methods = ['POST', 'GET'])
def r_signup():
   if request.method == 'POST':
      try:
        rname = request.form["rname"]
        ssn = request.form["ssn"]
        address = request.form["address"]
        mail = request.form["mail"]
        phone = request.form["phone"]
         
        with sql.connect("library_database") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO readers (rname, ssn, address, mail, phone) VALUES (?,?,?,?,?)",(rname,ssn,address,mail,phone) )
            con.commit()
            msg = "讀者帳號已成功建立！"
      except:
         con.rollback()
         msg = "error in insert operation"
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/s_signup',methods = ['POST', 'GET'])
def s_signup():
   if request.method == 'POST':
      try:
        sname = request.form["sname"]
        empid = request.form["empid"]
        
        with sql.connect("library_database") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO staffs (sname,empid) VALUES (?,?)",(sname, empid) )
            con.commit()
            msg = "管理員帳號已成功建立！"
      except:
         con.rollback()
         msg = "error in insert operation"
      finally:
         return render_template("result.html",msg = msg)
         con.close()
      

# @app.route('/list')
# def list():
#    con = sql.connect("student_database.db")
#    con.row_factory = sql.Row
   
#    cur = con.cursor()
#    cur.execute("select * from students")
   
#    students = cur.fetchall();
#    return render_template("list.html", students = students)
# 網路範例結尾


# @app.route('/r_signup', methods=["POST"])
# def signup():
#     name = request.form["name"]
#     ssn = request.form["ssn"]
#     address = request.form["address"]
#     mail = request.form["mail"]
#     phone = request.form["phone"]
#     print(name, ssn, address, mail, phone)
#     return "註冊成功"

# @app.route('/s_signup', methods=["POST"])
# def signup():
#     sname = request.form["name"]
#     ssn = request.form["empid"]
#     print(name, ssn)
#     return "註冊成功"

@app.route("/error")
def error():
    message = request.args.get("msg", "發生錯誤，請聯繫圖書館")
    return render_template("error.html", message=message)

# 查詢所有書本
# @app.route('/list')
# def list():
#     con = sql.connect("student_database.db")
#     con.row_factory = sql.Row

#     cur = con.cursor()
#     cur.execute("select * from students")

#     students = cur.fetchall()
#     return render_template("list.html", students=students)

if __name__ == '__main__':
    app.run(debug=True)
