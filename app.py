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
    
    books = cur.fetchall()
    return render_template("book_search.html", book_search = books)

@app.route('/modify0')
def modify0():
    con = sql.connect("readers.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    reader = session["reader"]
    cur.execute("SELECT ssn FROM readers WHERE rname = ?", (reader,))
    people = cur.fetchone()[0]
    return render_template("modify.html", rname = reader, ssn = people)

@app.route('/modify',methods = ['POST', 'GET'])
def modify():
   if request.method == 'POST':
      try:
         address = request.form["address"]
         mail = request.form["mail"]
         phone = request.form["phone"]
         password = request.form["password"]
         
         with sql.connect("readers.db") as con:
            cur = con.cursor()
            if address:
                cur.execute("update readers set address=? WHERE rname=?", (address, session["reader"]))
            if mail:
                cur.execute("update readers set mail=? WHERE rname=?", (mail, session["reader"]))
            if phone:
                cur.execute("update readers set phone=? WHERE rname=?", (phone, session["reader"]))
            if password:
                cur.execute("update readers set password=? WHERE rname=?", (password, session["reader"]))
            con.commit()
            msg = "資料修改成功！"
      except:
         con.rollback()
         msg = "讀者註冊失敗，請聯絡管理員！"
      finally:
         con.close()
         return render_template("result.html",msg = msg)
         

# @app.route('/borrow')
# def borrow():
#     con = sql.connect("readers.db")
#     con.row_factory = sql.Row
#     cur = con.cursor()
#     reader = session["reader"]
#     cur.execute("select ssn from readers where rname = ?", reader)
    
#     people = cur.fetchone()
#     # 1
#     ISBN = request.args.get("row['ISBN']")
#     con = sql.connect("reports.db")
#     con.row_factory = sql.Row
    
#     cur = con.cursor()
#     cur.execute("INSERT INTO reports(User_id, book_no) VALUES (?, ?)",(people,ISBN))
#     return render_template("result.html", msg ="借閱成功！")
##

@app.route('/book_available')
def book_available():
    con = sql.connect("books.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from books")
    books = cur.fetchall()


    con1 = sql.connect("reports.db")
    con1.row_factory = sql.Row
    cur1 = con1.cursor()
    cur1.execute("select book_no from reports")
    reports = cur1.fetchall()
    return render_template("book_available.html", books = books, reports = reports)

@app.route('/borrow')
def borrow():
    con = sql.connect("readers.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    reader = session["reader"]
    cur.execute("SELECT ssn FROM readers WHERE rname = ?", (reader,))
    people = cur.fetchone()[0]

    ISBN = request.args.get("book")
    con = sql.connect("reports.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("INSERT INTO reports(User_id, book_no) VALUES (?, ?)", (people, ISBN))
    con.commit()
    return render_template("result.html", msg="借閱成功！")

@app.route('/test_report')
def test_report():
    con = sql.connect("reports.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("select * from reports")
    
    reports = cur.fetchall()
    return render_template("test_report.html", reports = reports)
    
    
    
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
    return redirect("/r_member")

@app.route('/s_signin',methods = ['POST'])
def s_signin():
    con = sql.connect("staffs.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    empid=request.form["empid"]
    spassword=request.form["password"]
    cur.execute("SELECT * FROM staffs WHERE empid=? and password=?", (empid, spassword))
    people = cur.fetchall()
    cur.execute("SELECT sname FROM staffs WHERE empid=? and password=?", (empid, spassword,))
    sname = cur.fetchone()[0]
    if len(people) == 0:
        return redirect("/result?msg=帳號或密碼錯誤")
    session["staff"] = empid
    return render_template("/s_member.html", sname = sname)

@app.route('/s_member')
def s_member():
  if "staff" in session:
    return render_template("s_member.html", sname = session["staff"])
  else:
    return render_template("/")

@app.route('/r_signout')
def r_signout():
  del session["reader"]
  return redirect("/")

@app.route('/s_signout')
def s_signout():
  del session["staff"]
  return redirect("/")
       
@app.route('/r_member')
def r_member():
  if "reader" in session:
    return render_template("r_member.html", rname = session["reader"])
  else:
    return render_template("/")
    
@app.route('/booklist')
def booklist():
    con = sql.connect("books.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("select * from books")
    
    books = cur.fetchall()
    return render_template("booklist.html", books = books)

@app.route('/reader_list')
def reader_list():
  if "staff" in session:
    con = sql.connect("readers.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("select * from readers")
    
    readers = cur.fetchall()
    return render_template("reader_list.html", readers = readers)
  else:
    return redirect("/")

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
         con.close()
         return render_template("result.html",msg = msg)
         

@app.route('/s_signup',methods = ['POST', 'GET'])
def s_signup():
   if request.method == 'POST':
      try:
         sname = request.form["sname"]
         empid = request.form["empid"]
         password = request.form["password"]
         
         with sql.connect("staffs.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO staffs (sname, empid, password) VALUES (?,?,?)",(sname, empid, password) )
            con.commit()
            msg = "管理員帳號已成功建立！"
      except:
         con.rollback()
         msg = "管理員註冊失敗，請聯絡管理員！"
         
      finally:
         con.close()
         return render_template("result.html",msg = msg)
         
@app.route("/result")
def result():
    message = request.args.get("msg", "發生錯誤，請聯繫圖書館")
    return render_template("result.html", msg=message)

if __name__ == '__main__':
    app.run(debug=True)