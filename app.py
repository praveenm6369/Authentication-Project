from flask import Flask,render_template,redirect,url_for,request
import sqlite3
app=Flask(__name__)


@app.route("/")
def home():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/register",methods=["POST"])
def register():
    try:
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("psw")
        con_password=request.form.get("cpsw")

        con=sqlite3.connect("signup.db")
        cur=con.cursor()
        

        #password validation
        if len(password)<=8:
            return render_template("signup.html",perror="❌ passsword must contain at least 8 characters!",name=name,email=email)
        
        if not any(i.isdigit() for i in password):
            return render_template("signup.html",perror="❌ passsword must contain a number!",name=name,email=email)
        
        if not any(i.isalnum() for i in password):
            return render_template("signup.html",perror="❌ passsword must contain a special Characters!",name=name,email=email)
        
        if not any(i.isupper() for i in password):
            return render_template("signup.html",perror="❌ passsword must contain a Uppercase!",name=name,email=email)

        if not any(i.islower() for i in password):
            return render_template("signup.html",perror="❌ passsword must contain a Lowercase!",name=name,email=email)

        if con_password != password:
            return render_template("signup.html",con_error="❌ passsword do not Match!",name=name,email=email)
        cur.execute("insert into signup(name,email,password,con_password) values (?,?,?,?)",(name,email,password,con_password))
        con.commit()
        if cur.rowcount >= 1:
            return render_template("login.html",success="✅ Sing Up Sucessfully!🎉")
    
    except sqlite3.IntegrityError:
        return render_template("signup.html",error="❌Email Already Exists!",name=name,email=email,psw=password)
    finally:
        con.close()


@app.route("/login",methods=["POST"])
def login():
    email=request.form.get("email")
    password=request.form.get("psw")

    con=sqlite3.connect("signup.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from signup where email=? and password=?",(email,password))
    f=cur.fetchone()
    con.commit()
    con.close()
    print(f)
    if f==None:
        return render_template("login.html",success="invalid password or email")

    else:
        return render_template("demo.html")






    


if __name__ == "__main__":
    app.run(debug=True)

