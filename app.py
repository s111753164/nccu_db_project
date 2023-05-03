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

@app.route('/book_search')
def books():
    con = sql.connect("books.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from books where title LIKE '%{}%'".format(request.args.get("book_search", "")))
    
    books = cur.fetchall();
    return render_template("book_search.html", book_search = books)
    
@app.route('/r_signin',methods = ['POST'])
def r_signin():
    con = sql.connect("readers.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    rname=request.form["rname"]
    rpassword=request.form["password"]
    cur.execute("SELECT * FROM readers WHERE rname=? and password=?", (rname, rpassword))
    people = cur.fetchall()
    if len(people) == 0:
        return redirect("/result?msg=帳號或密碼錯誤")
           
    session["reader"] = rname
    return redirect("/member")
       
@app.route('/member')
def member():
    

@app.route('/booklist')
def booklist():
    con = sql.connect("books.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("select * from books")
    
    books = cur.fetchall();
    return render_template("booklist.html", books = books)

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
         
         with sql.connect("readers.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO readers (rname, ssn, address, mail, phone) VALUES (?,?,?,?,?)",(rname,ssn,address,mail,phone) )
            con.commit()
            msg = "讀者帳號已成功建立！"
      except:
         con.rollback()
         msg = "讀者註冊失敗，請聯絡管理員！"
         
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/s_signup',methods = ['POST', 'GET'])
def s_signup():
   if request.method == 'POST':
      try:
         sname = request.form["sname"]
         empid = request.form["empid"]
         
         with sql.connect("staffs.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO staffs (sname, empid) VALUES (?,?)",(sname, empid) )
            con.commit()
            msg = "管理員帳號已成功建立！"
      except:
         con.rollback()
         msg = "管理員註冊失敗，請聯絡管理員！"
         
      finally:
         return render_template("result.html",msg = msg)
         con.close()
      
@app.route("/result")
def error():
    message = request.args.get("msg", "發生錯誤，請聯繫圖書館")
    return render_template("result.html", msg=message)

if __name__ == '__main__':
    app.run(debug=True)