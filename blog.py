from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,DateField,SelectField
#from wtforms.fields.html5 import DateField
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
import os
from functools import wraps


#admin giriş decoder
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["username"]=="admin":
         return f(*args, **kwargs)
        else :
         return redirect(url_for("index"))

    return decorated_function

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or \
    'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

#user giris decoder
def userlogin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["username"]!="":
         return f(*args, **kwargs)
        else :
         return redirect(url_for("index"))

    return decorated_function

#kullanıcı giris formu
class LoginForm(Form):
   
     userName=StringField("user name :",validators=[validators.length(min=5,max=15)])
     password=PasswordField("password :",validators=[

       validators.DataRequired(message="please enter your password")        
     ])
   

#kullanıcı kayıt formu
class RegisterForm(Form):
     name=StringField("personal name : ",validators=[validators.length(min=5,max=25)]) 
     userName=StringField("username :",validators=[validators.length(min=5,max=15)])
     email=StringField("email adress : ",validators=[validators.Email(message="Please enter a valid email address")])
     password=PasswordField("enter password :",validators=[
       validators.DataRequired(message="please enter your password")     , 
       validators.EqualTo(fieldname = "confirm" , message="password does not match")  
     ]) 
     confirm=PasswordField("password verification")




app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="kuffar_blog"
app.config["MYSQL_CURSORCLASS"]="DictCursor"

mysql=MySQL(app)

@app.route("/")
def index():
  cursor=mysql.connection.cursor()

  sorgu="Select * From mainpage"
  
  result=cursor.execute(sorgu)

  if result > 0 :
    index=cursor.fetchall()
    return render_template("index.html",index=index)
  else:
    return render_template("index.html")

@app.route("/articles")
def articles():


  cursor=mysql.connection.cursor()

  sorgu="Select * From arthicles"
  
  result=cursor.execute(sorgu)

  if result > 0 :
    articles=cursor.fetchall()
    return render_template("articles.html",articles=articles)
  else:
    return render_template("articles.html")


@app.route("/projects")    
def projects():
  cursor=mysql.connection.cursor()

  sorgu="Select * From project"
  
  result=cursor.execute(sorgu)

  if result > 0 :
    projects=cursor.fetchall()
    return render_template("projects.html",projects=projects)
  else:
    return render_template("projects.html")
    

@app.route("/cv")    
def cv():
  education=mysql.connection.cursor()
  certificate=mysql.connection.cursor()
  seminar=mysql.connection.cursor()
  language=mysql.connection.cursor()
  workexperince=mysql.connection.cursor()
  talanted=mysql.connection.cursor()

  Esorgu="Select * From education ORDER BY school_data  "
  Csorgu="Select * From certificate ORDER BY 	cer_data  "
  Ssorgu="Select * From seminar ORDER BY 	sem_data"
  Lsorgu="Select * From 	language "
  WOsorgu="Select * From 	workexperience ORDER BY 	work_data"
  Tsorgu="Select * From 	talented "
  
  Eresult=education.execute(Esorgu)
  Cresult=certificate.execute(Csorgu)
  Sresult=seminar.execute(Ssorgu)
  Lresult=language.execute(Lsorgu)
  WOresult=workexperince.execute(WOsorgu)
  Tresult=talanted.execute(Tsorgu)

  if Eresult > 0 or Cresult > 0 or Sresult > 0 or Lresult > 0 or WOresult > 0 or Tresult > 0:
    educationRead=education.fetchall()
    certificateRead=certificate.fetchall()
    seminarRead=seminar.fetchall()
    languageRead=language.fetchall()
    workexperinceRead=workexperince.fetchall()
    talantedRead=talanted.fetchall()
    return render_template("cv.html",educationRead=educationRead,certificateRead=certificateRead,seminarRead=seminarRead,languageRead=languageRead,workexperinceRead=workexperinceRead,talantedRead=talantedRead)
    
  else:
    return render_template("cv.html") 
  

@app.route("/contact")    
def contact():
  cursor=mysql.connection.cursor()

  sorgu="Select * From contact"
  
  result=cursor.execute(sorgu)

  if result > 0 :
    contact=cursor.fetchall()
    return render_template("contact.html",contact=contact)
  else:
    return render_template("index.html")

#register islemi
@app.route("/register",methods=["GET","POST"])
def register():
  form=RegisterForm(request.form)
  if request.method == "POST" and form.validate():

        name=form.name.data
        user_name=form.userName.data
        email=form.email.data
        password=sha256_crypt.encrypt( form.password.data)

        cursor=mysql.connection.cursor()

        sorgu="Insert into users(name,user_email,user_name,password) VALUES(%s,%s,%s,%s) "
        
        cursor.execute(sorgu,(name,email,user_name,password))

        mysql.connection.commit()

        cursor.close()

        return redirect(url_for("login"))
  else:    
        return render_template("register.html",form=form)
  
#login islemi
@app.route("/login",methods=["GET","POST"])    
def login():
    form=LoginForm(request.form)
    username=form.userName.data
    password_entered=form.password.data

    cursor=mysql.connection.cursor()

    sorgu="select * from users where user_name = %s"

    result = cursor.execute(sorgu,(username,))
    


    if request.method == "POST":
          if result > 0 :
           data=cursor.fetchone()
           real_password=data["password"]
           if sha256_crypt.verify(password_entered,real_password):

             session["logged_in"] = True
             session["username"]=username
              
             return redirect(url_for("index"))
           else: 
             return redirect(url_for("login"))
          else:
            return redirect(url_for("login"))
    else:    
      return render_template("login.html",form=form)
#logout islemi
@app.route("/logout")    
def logout():
  session.clear()
  return render_template("index.html")


#dashboard islemi
@app.route("/dashbord")    
@login_required
def dashbord():
    return render_template("dashbord.html")

#dashboard2 islemi
@app.route("/dashbord2")    
@login_required
def dashbord2():
    return render_template("dashbord2.html")    

#Control Panel Start

#updateIndex islemi
@app.route("/updateIndex",methods=["GET","POST"])
@login_required    
def updateIndex():
    if request.method == "GET":
     cursor=mysql.connection.cursor()
     sorgu="Select * From mainpage where id = %s "
     id=1
     result = cursor.execute(sorgu,(id,))
     if result == 0:
      
      return redirect(url_for("index"))
     else:
      article=cursor.fetchone()
      form=IndexForm() 
      form.content.data=article["content"]
      return render_template("ControlPanel/updateIndex.html",form=form)
  #POST REQUEST
    else:
      form = IndexForm(request.form)
      newContent=form.content.data
    
      sorgu2 = "Update mainpage Set content = %s where id = %s"
      cursor = mysql.connection.cursor()
      id=1
      cursor.execute(sorgu2,(newContent,id))
      mysql.connection.commit()
    
      return redirect(url_for("updateIndex"))

#Index Form
class IndexForm(Form):
  content=TextAreaField("Index Content",validators=[validators.Length(min = 10)])



#addArticles islemi
@app.route("/addArticles",methods=["GET","POST"])  
@login_required  
def addArticles():
    form = ArticlesForm(request.form)

    if request.method == "POST" and form.validate() :
      title=form.title.data
      content=form.content.data

      cursor=mysql.connection.cursor()

      sorgu="Insert into arthicles(arthicles_title,arthicles_author,arhticles_comment) VALUES(%s,%s,%s) "
      cursor.execute(sorgu,(title,session["username"],content))
      mysql.connection.commit()
      cursor.close()
      return redirect(url_for("articles"))

    return render_template("ControlPanel/addArticles.html",form = form)

#makale Form
class ArticlesForm(Form):
  title=StringField("Articles Headers",validators=[validators.Length(min = 5,max = 100)]  )
  content=TextAreaField("Articles Content",validators=[validators.Length(min = 10)])

#UpDeArticles
@app.route("/UpDeArticles")  
@login_required  
def UpDeArticles():
  cursor=mysql.connection.cursor()
  sorgu="Select * From arthicles "
  result=cursor.execute(sorgu)
  if result >0:
    articles=cursor.fetchall()
    return render_template("ControlPanel/UpDeArticles.html",articles=articles)
  else :
    return render_template("ControlPanel/UpDeArticles.html")

#addProjects islemi
@app.route("/addProjects",methods=["GET","POST"]) 
@login_required   
def addProjects():
    Aproject = ProjectForm(request.form)
    Plist=mysql.connection.cursor()
    Psorgu="Select * From project"

    PListresult=Plist.execute(Psorgu)

    
    if request.method == "POST" and Aproject.validate() :
      header=Aproject.header.data
      content=Aproject.content.data
      time=Aproject.time.data
      url=Aproject.url.data

      addProject=mysql.connection.cursor()

      sorgu="Insert into project(	p_header,p_content,p_time,p_url) VALUES(%s,%s,%s,%s) "
      addProject.execute(sorgu,(header,content,time,url))
      mysql.connection.commit()
      addProject.close()
      return redirect(url_for("projects"))
   
    
    if PListresult > 0 or PListresult == 0:
     PprojectList=Plist.fetchall()
     return render_template("ControlPanel/addProjects.html",PprojectList=PprojectList,Aproject=Aproject)
    else:
     return render_template("ControlPanel/addProjects.html")


#project delete operation
@app.route("/PROJECTdelete/<string:id>") 
@login_required  
def PROJECTdelete(id):
  
 cursor=mysql.connection.cursor()
 sorgu="Select * From 	project where p_id = %s"

 result=cursor.execute(sorgu,(id,))
   
 if result > 0:
   sorgu2 = "Delete from project where p_id = %s"
   cursor.execute(sorgu2,(id,))
   mysql.connection.commit()
   return redirect(url_for("addProjects"))
 else:
   return redirect(url_for("index"))


#project update operation
@app.route("/PROJECTedit/<string:id>",methods=["GET","POST"])
@login_required
def PROJECTedit(id):
  #GET REQUEST 
  if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From project where p_id = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      project=cursor.fetchone()
      form=ProjectForm() 
      form.header.data = project["p_header"]
      form.content.data=project["p_content"]
      form.time.data = project["p_time"]
      form.url.data=project["p_url"]
      return render_template("ControlPanel/projectUpdate.html",form=form)  
  #POST REQUEST
  else:
    form = ProjectForm(request.form)
    newHeader=form.header.data
    newContent=form.content.data
    newTime=form.time.data
    newUrl=form.url.data
    
    sorgu2 = "Update project Set p_header = %s , p_content = %s,p_time = %s , p_url = %s where p_id = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newHeader,newContent,newTime,newUrl,id))
    mysql.connection.commit()
    
    return redirect(url_for("addProjects"))


# Proje Form
class ProjectForm(Form):
  header=StringField("Project Headers",validators=[validators.Length(min = 5,max = 100)]  )
  content=TextAreaField("Project Content",validators=[validators.Length(min = 10)])
  time=StringField("Project Time",validators=[validators.Length(min = 5,max = 100)]  )
  url=StringField("Project Url",validators=[validators.Length(min = 5,max = 100)]  )

#curriculum_vitae islemi
@app.route("/curriculum_vitae",methods=["GET","POST"])   
@login_required   
def curriculum_vitae():
  

  #GET REQUEST   
  if request.method == "GET":
     cursor=mysql.connection.cursor()
     sorgu="Select * From curriculum_vitae where cv_id = %s "
     id=1
     result = cursor.execute(sorgu,(id,))
     if result == 0:
      
      return redirect(url_for("index"))
     else:
      curriculum_vitae=cursor.fetchone()
      form=curriculum_vitaeFORM() 
      form.name.data=curriculum_vitae["cv_name"]
      form.lastname.data=curriculum_vitae["cv_lastname"]
      form.birthdata.data=curriculum_vitae["cv_birthdate"]
      form.hobbies.data=curriculum_vitae["cv_habbies"]
      
      
      return render_template("ControlPanel/curriculum_vitae.html",form=form)
  #POST REQUEST     
  else:  
    form = curriculum_vitaeFORM(request.form)
    newName=form.name.data
    newLastname=form.lastname.data
    newBirthData=form.birthdata.data
    newHobbies=form.hobbies.data
    
    sorgu2 = "Update curriculum_vitae Set cv_name = %s , cv_lastname = %s , cv_birthdate = %s , cv_habbies = %s  where cv_id = %s"
    cursor = mysql.connection.cursor()
    cursor = mysql.connection.cursor()
    id=1
    cursor.execute(sorgu2,(newName,newLastname,newBirthData,newHobbies,id))
    mysql.connection.commit()
    return redirect(url_for("curriculum_vitae"))    

   
#curriculum_vitae FORM
class curriculum_vitaeFORM(Form):
 name=StringField("NAME :",validators=[validators.Length(min = 5,max = 100)])
 lastname=StringField("LAST NAME :",validators=[validators.Length(min = 5,max = 100)]  )
 birthdata=StringField("BİRTHDATA :",validators=[validators.Length(min = 5,max = 100)])
 hobbies=StringField("HOBBIES :",validators=[validators.Length(min = 5,max = 100)]  )

#curriculum_vitae islemi talanted
@app.route("/talanted",methods=["GET","POST"])   
@login_required   
def talanted():
  cursor=mysql.connection.cursor()

  sorgu="Select * From 	talented"
  
  result=cursor.execute(sorgu)

  if result > 0 :
    talanted=cursor.fetchall()
    return render_template("ControlPanel/talanted.html",talanted=talanted)
  else:
    return render_template("ControlPanel/talanted.html")



#curriculum_vitae islemi workexperince
@app.route("/workexperince",methods=["GET","POST"])   
@login_required   
def workexperince():
  cursor=mysql.connection.cursor()

  sorgu="Select * From 	workexperience"
  
  result=cursor.execute(sorgu)

  if result > 0 :
    workexperince=cursor.fetchall()
    return render_template("ControlPanel/workexperince.html",workexperince=workexperince)
  else:
    return render_template("ControlPanel/workexperince.html")


 #curriculum_vitae islemi LANGUAGE

@app.route("/language",methods=["GET","POST"])   
@login_required   
def language():
  cursor=mysql.connection.cursor()

  sorgu="Select * From 	language"
  
  result=cursor.execute(sorgu)

  if result > 0 :
    language=cursor.fetchall()
    return render_template("ControlPanel/language.html",language=language)
  else:
    return render_template("ControlPanel/language.html")

#curriculum_vitae islemi seminar

@app.route("/seminar",methods=["GET","POST"])   
@login_required   
def seminar():
  cursor=mysql.connection.cursor()

  sorgu="Select * From 	seminar"
  
  result=cursor.execute(sorgu)

  if result > 0 :
    seminar=cursor.fetchall()
    return render_template("ControlPanel/seminar.html",seminar=seminar)
  else:
    return render_template("ControlPanel/seminar.html")

#curriculum_vitae islemi certificate

@app.route("/certificate",methods=["GET","POST"])   
@login_required   
def certificate():
  cursor=mysql.connection.cursor()

  sorgu="Select * From 	certificate"
  
  result=cursor.execute(sorgu)

  if result > 0 :
    certificate=cursor.fetchall()
    return render_template("ControlPanel/certificate.html",certificate=certificate)
  else:
    return render_template("ControlPanel/certificate.html")
  

#curriculum_vitae islemi Education
@app.route("/education",methods=["GET","POST"])   
@login_required   
def education():
  cursor=mysql.connection.cursor()

  sorgu="Select * From education"
  
  result=cursor.execute(sorgu)

  if result > 0 :
    education=cursor.fetchall()
    return render_template("ControlPanel/education.html",education=education)
  else:
    return render_template("ControlPanel/education.html")
  
  
#updateContact islemi
@app.route("/updateContact",methods=["GET", "POST"])
@login_required    
def updateContact():
  if request.method == "GET":
     cursor=mysql.connection.cursor()
     sorgu="Select * From contact where id = %s "
     id=1
     result = cursor.execute(sorgu,(id,))
     if result == 0:
      
      return redirect(url_for("index"))
     else:
      contact=cursor.fetchone()
      form=ContactForm() 
      form.name.data=contact["name"]
      form.lastname.data=contact["lastname"]
      form.mail.data=contact["gmail"]
      form.socialmedia.data=contact["socialmedia"]
      form.url_adress.data=contact["url_adress"]
      return render_template("ControlPanel/updateContact.html",form=form)
  #POST REQUEST    
  else:
    form = ContactForm(request.form)

    newName=form.name.data
    newLastname=form.lastname.data
    newMail=form.mail.data
    newSocialmedia=form.socialmedia.data
    newUrladress=form.url_adress.data
    
    sorgu2 = "Update contact Set name = %s , lastname = %s , gmail = %s , socialmedia = %s , url_adress = %s where id = %s"
    cursor = mysql.connection.cursor()
    id=1
    cursor.execute(sorgu2,(newName,newLastname,newMail,newSocialmedia,newUrladress,id))
    mysql.connection.commit()
    
    return redirect(url_for("updateContact"))   
    
   
#Contact Form    
class ContactForm(Form):
  name=StringField("NAME :",validators=[validators.Length(min = 5,max = 100)])
  lastname=StringField("LAST NAME :",validators=[validators.Length(min = 5,max = 100)]  )
  mail=StringField("MAIL :",validators=[validators.Length(min = 5,max = 100)]  )
  socialmedia=StringField("SOCIAL MEDIA",validators=[validators.Length(min = 5,max = 100)]  )
  url_adress=StringField("URL ADRESS",validators=[validators.Length(min = 5,max = 100)]  )

#Control Panel Finish

#Detay Sayfası
@app.route("/article/<string:id>")


#login islemi yapılacak
#eksik

def article(id):
  cursor=mysql.connection.cursor()

  sorgu="Select * From arthicles where arthicles_id = %s"
  result = cursor.execute(sorgu,(id,))
  if result > 0:
    article=cursor.fetchone()
    return render_template("article.html",article=article)
  else:
    return render_template("article.html")  


@app.route("/project/<string:id>")
def project(id):
  cursor=mysql.connection.cursor()

  sorgu="Select * From project where p_id = %s"
  result = cursor.execute(sorgu,(id,))
  if result > 0:
    project=cursor.fetchone()
    return render_template("project.html",project=project)
  else:
    return render_template("project.html") 

##cv Talantede add islemi
@app.route("/cvTalantedeAdd",methods=["GET","POST"])
@login_required
def cvTalantedeAdd():
  form=TalantedAddForm(request.form)
  if request.method == "POST" and form.validate() :
      name=form.name.data
      level=form.level.data
      Cv_id=1
      cursor=mysql.connection.cursor()
      sorgu="Insert into 	talented(	tal_name,tal_level,cv_idT) VALUES(%s,%s,%s) "
      cursor.execute(sorgu,(name,level,Cv_id))
      mysql.connection.commit()
      cursor.close()
      return redirect(url_for("talanted"))
  return render_template("ControlPanel/cvTalantedeAdd.html",form = form)    



#cv talented update islemi
@app.route("/Tedit/<string:id>",methods=["GET","POST"])
@login_required
def cvTalantedUpdate(id):
 #GET REQUEST 
  if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From 	talented where tal_id = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      TalantedUpdate=cursor.fetchone()
      form=TalantedAddForm()
      form.name.data=TalantedUpdate["tal_name"] 
      form.level.data=TalantedUpdate["tal_level"]
      return render_template("ControlPanel/cvTalantedUpdate.html",form=form)
  else:
    form = TalantedAddForm(request.form)
    newName=form.name.data
    newLevel=form.level.data
    sorgu2 = "Update talented Set tal_name = %s , tal_level = %s where 	tal_id = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newName,newLevel,id))
    mysql.connection.commit()
    return redirect(url_for("talanted"))



#ExperinceAdd Form
class TalantedAddForm(Form):
  name=StringField("TALANTED  NAME :",validators=[validators.Length(min = 5,max = 100)])
  level=StringField("TALANTED LEVEL :",validators=[validators.Length(min = 5,max = 100)])

#cv talanted delete islemi
@app.route("/Tdelete/<string:id>") 
@login_required  
def Tdelete(id):
  
 cursor=mysql.connection.cursor()
 sorgu="Select * From  	talented where  tal_id = %s"

 result=cursor.execute(sorgu,(id,))
   
 if result > 0:
   sorgu2 = "Delete from 		talented where tal_id = %s"
   cursor.execute(sorgu2,(id,))
   mysql.connection.commit()
   return redirect(url_for("talanted"))
 else:
   return redirect(url_for("index"))

##cv WORKEXPERİNCE add islemi
@app.route("/cvWorkExperinceAdd",methods=["GET","POST"])
@login_required
def cvWorkExperinceAdd():
  form=ExperinceAddForm(request.form)
  if request.method == "POST" and form.validate() :
      name=form.name.data
      time=form.time.data
      Cv_id=1
      cursor=mysql.connection.cursor()
      sorgu="Insert into 	workexperience(work_name,work_data,cv_idW) VALUES(%s,%s,%s) "
      cursor.execute(sorgu,(name,time,Cv_id))
      mysql.connection.commit()
      cursor.close()
      return redirect(url_for("workexperince"))
  return render_template("ControlPanel/cvWorkExperinceAdd.html",form = form)    




#cv workexperince update islemi
@app.route("/WEedit/<string:id>",methods=["GET","POST"])
@login_required
def cvWorkExperinceUpdate(id):
 #GET REQUEST 
  if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From 	workexperience where work_id = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      ExperinceUpdate=cursor.fetchone()
      form=ExperinceAddForm()
      form.name.data=ExperinceUpdate["work_name"] 
      form.time.data=ExperinceUpdate["work_data"]
      return render_template("ControlPanel/cvWorkExperinceUpdate.html",form=form)
  else:
    form = ExperinceAddForm(request.form)
    newName=form.name.data
    newTime=form.time.data
    sorgu2 = "Update workexperience Set work_name = %s , work_data = %s where 	work_id = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newName,newTime,id))
    mysql.connection.commit()
    return redirect(url_for("workexperince"))


#ExperinceAdd Form
class ExperinceAddForm(Form):
  name=StringField("WORK EXPERINCE  NAME :",validators=[validators.Length(min = 5,max = 100)])
  time=StringField("WORK EXPERINCE TIME :",validators=[validators.Length(min = 5,max = 100)])

#cv workexperince delete islemi
@app.route("/WEdelete/<string:id>") 
@login_required  
def WEdelete(id):
  
 cursor=mysql.connection.cursor()
 sorgu="Select * From  workexperience where  work_id = %s"

 result=cursor.execute(sorgu,(id,))
   
 if result > 0:
   sorgu2 = "Delete from 	workexperience where work_id = %s"
   cursor.execute(sorgu2,(id,))
   mysql.connection.commit()
   return redirect(url_for("workexperince"))
 else:
   return redirect(url_for("index"))

##cv seminar add islemi
@app.route("/cvSeminarAdd",methods=["GET","POST"])
@login_required
def cvSeminarAdd():
  form=SeminarAddForm(request.form)
  if request.method == "POST" and form.validate() :
      name=form.name.data
      time=form.time.data
      Cv_id=1
      cursor=mysql.connection.cursor()
      sorgu="Insert into 	seminar(sem_name,sem_data,cv_idS) VALUES(%s,%s,%s) "
      cursor.execute(sorgu,(name,time,Cv_id))
      mysql.connection.commit()
      cursor.close()
      return redirect(url_for("seminar"))
  return render_template("ControlPanel/cvSeminarAdd.html",form = form)    



#cv seminar update islemi
@app.route("/Sedit/<string:id>",methods=["GET","POST"])
@login_required
def cvSeminarUpdate(id):
 #GET REQUEST 
  if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From 	seminar where sem_id = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      SeminarUpdate=cursor.fetchone()
      form=SeminarAddForm()
      form.name.data=SeminarUpdate["sem_name"] 
      form.time.data=SeminarUpdate["sem_data"]
      return render_template("ControlPanel/cvSeminarUpdate.html",form=form)
  else:
    form = EducationAddForm(request.form)
    newName=form.name.data
    newTime=form.time.data
    sorgu2 = "Update seminar Set sem_name = %s , sem_data = %s where sem_id = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newName,newTime,id))
    mysql.connection.commit()
    return redirect(url_for("seminar"))


#SeminarAdd Form
class SeminarAddForm(Form):
  name=StringField("SEMINAR NAME :",validators=[validators.Length(min = 5,max = 100)])
  time=StringField("SEMINAR TIME :",validators=[validators.Length(min = 5,max = 100)])


#cv seminar delete islemi
@app.route("/Sdelete/<string:id>") 
@login_required  
def Sdelete(id):
  
 cursor=mysql.connection.cursor()
 sorgu="Select * From  seminar where  sem_id = %s"

 result=cursor.execute(sorgu,(id,))
   
 if result > 0:
   sorgu2 = "Delete from 	seminar where sem_id = %s"
   cursor.execute(sorgu2,(id,))
   mysql.connection.commit()
   return redirect(url_for("seminar"))
 else:
   return redirect(url_for("index"))


##cv education add islemi
@app.route("/cvEducationAdd",methods=["GET","POST"])
@login_required
def cvEducationAdd():
  form=EducationAddForm(request.form)
  if request.method == "POST" and form.validate() :
      name=form.name.data
      time=form.time.data
      Cv_id=1
      cursor=mysql.connection.cursor()
      sorgu="Insert into 	education(school_name,school_data,cv_idE) VALUES(%s,%s,%s) "
      cursor.execute(sorgu,(name,time,Cv_id))
      mysql.connection.commit()
      cursor.close()
      return redirect(url_for("education"))
  return render_template("ControlPanel/cvEducationAdd.html",form = form)    


#cv education update islemi
@app.route("/Eedit/<string:id>",methods=["GET","POST"])
@login_required
def cvEducationUpdate(id):
 #GET REQUEST 
  if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From 	education where Ed_id = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      EducationUpdate=cursor.fetchone()
      form=EducationAddForm()
      form.name.data=EducationUpdate["school_name"] 
      form.time.data=EducationUpdate["school_data"]
      return render_template("ControlPanel/cvEducationUpdate.html",form=form)
  else:
    form = EducationAddForm(request.form)
    newName=form.name.data
    newTime=form.time.data
    sorgu2 = "Update education Set school_name = %s , school_data = %s where Ed_id = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newName,newTime,id))
    mysql.connection.commit()
    return redirect(url_for("education"))


#EducationAdd Form
class EducationAddForm(Form):
  name=StringField("SCHOOL NAME :",validators=[validators.Length(min = 5,max = 100)])
  time=StringField("SCHOOL TIME :",validators=[validators.Length(min = 5,max = 100)])


#cv education delete islemi
@app.route("/Edelete/<string:id>") 
@login_required  
def Edelete(id):
  
 cursor=mysql.connection.cursor()
 sorgu="Select * From 	education where  Ed_id = %s"

 result=cursor.execute(sorgu,(id,))
   
 if result > 0:
   sorgu2 = "Delete from 	education where Ed_id = %s"
   cursor.execute(sorgu2,(id,))
   mysql.connection.commit()
   return redirect(url_for("education"))
 else:
   return redirect(url_for("index"))


##cv certficate add islemi
@app.route("/cvCertificateAdd",methods=["GET","POST"])
@login_required
def cvCertificateAdd():
  form=CertificateAddForm(request.form)
  if request.method == "POST" and form.validate() :
      name=form.name.data
      time=form.time.data
      Cv_id=1
      cursor=mysql.connection.cursor()
      sorgu="Insert into certificate(cer_name,cer_data,cv_idC) VALUES(%s,%s,%s) "
      cursor.execute(sorgu,(name,time,Cv_id))
      mysql.connection.commit()
      cursor.close()
      return redirect(url_for("certificate"))
  return render_template("ControlPanel/cvCertificateAdd.html",form = form)    

#cv certficate update islemi
@app.route("/Cedit/<string:id>",methods=["GET","POST"])
@login_required
def cvCertificateUpdate(id):
 #GET REQUEST 
  if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From certificate where cer_id = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      CertificateUpdate=cursor.fetchone()
      form=CertificateAddForm()
      form.name.data=CertificateUpdate["cer_name"] 
      form.time.data=CertificateUpdate["cer_data"]
      return render_template("ControlPanel/cvCertificateUpdate.html",form=form)
  else:
    form = CertificateAddForm(request.form)
    newName=form.name.data
    newTime=form.time.data
    sorgu2 = "Update certificate Set cer_name = %s , cer_data = %s where cer_id = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newName,newTime,id))
    mysql.connection.commit()
    return redirect(url_for("certificate"))


#CertificateAdd Form
class CertificateAddForm(Form):
  name=StringField("CERTIFICATE NAME :",validators=[validators.Length(min = 5,max = 100)])
  time=StringField("CERTIFICATE TIME :",validators=[validators.Length(min = 5,max = 100)])

#cv certficate delete islemi
@app.route("/Cdelete/<string:id>") 
@login_required  
def Cdelete(id):
  
 cursor=mysql.connection.cursor()
 sorgu="Select * From certificate where  cer_id = %s"

 result=cursor.execute(sorgu,(id,))
   
 if result > 0:
   sorgu2 = "Delete from certificate where cer_id = %s"
   cursor.execute(sorgu2,(id,))
   mysql.connection.commit()
   return redirect(url_for("certificate"))
 else:
   return redirect(url_for("index"))

##cv language add islemi
@app.route("/cvLanguageAdd",methods=["GET","POST"])
@login_required
def cvLanguageAdd():
  form=LanguageAddForm(request.form)
  if request.method == "POST" and form.validate() :
      name=form.name.data
      level=form.level.data
      Cv_id=1
      cursor=mysql.connection.cursor()
      sorgu="Insert into language(lang_name,lang_level,cv_idL) VALUES(%s,%s,%s) "
      cursor.execute(sorgu,(name,level,Cv_id))
      mysql.connection.commit()
      cursor.close()
      return redirect(url_for("language"))
  return render_template("ControlPanel/cvLanguageAdd.html",form = form)    


#cv language update islemi
@app.route("/Ledit/<string:id>",methods=["GET","POST"])
@login_required
def cvLanguageUpdate(id):
 #GET REQUEST 
  if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From language where lang_id = %s "
    result = cursor.execute(sorgu,(id,))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      LanguageUpdate=cursor.fetchone()
      form=LanguageAddForm()
      form.name.data=LanguageUpdate["lang_name"] 
      form.level.data=LanguageUpdate["lang_level"]
      return render_template("ControlPanel/cvLanguageUpdate.html",form=form)
  else:
    form = LanguageAddForm(request.form)
    newName=form.name.data
    newLevel=form.level.data
    sorgu2 = "Update language Set lang_name = %s , lang_level = %s where lang_id = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newName,newLevel,id))
    mysql.connection.commit()
    return redirect(url_for("language"))


#LanguageAdd Form
class LanguageAddForm(Form):
  name=StringField("LANGUAGE NAME :",validators=[validators.Length(min = 5,max = 100)])
  level=StringField("LANGUAGE LEVEL :",validators=[validators.Length(min = 5,max = 100)]  )

#cv language delete islemi
@app.route("/Ldelete/<string:id>") 
@login_required  
def Ldelete(id):
  
 cursor=mysql.connection.cursor()
 sorgu="Select * From language where  lang_id = %s"

 result=cursor.execute(sorgu,(id,))
   
 if result > 0:
   sorgu2 = "Delete from language where lang_id = %s"
   cursor.execute(sorgu2,(id,))
   mysql.connection.commit()
   return redirect(url_for("language"))
 else:
   return redirect(url_for("index"))

#delete islemi
@app.route("/delete/<string:id>") 
@login_required  
def delete(id):
  
 cursor=mysql.connection.cursor()
 sorgu="Select * From arthicles where arthicles_author = %s and arthicles_id = %s"

 result=cursor.execute(sorgu,(session["username"],id))
   
 if result > 0:
   sorgu2 = "Delete from arthicles where arthicles_id = %s"
   cursor.execute(sorgu2,(id,))
   mysql.connection.commit()
   return redirect(url_for("UpDeArticles"))
 else:
   return redirect(url_for("index"))


#upadate islemi

@app.route("/edit/<string:id>",methods=["GET","POST"])
@login_required
def update(id):
  #GET REQUEST 
  if request.method == "GET":
    cursor=mysql.connection.cursor()
    sorgu="Select * From arthicles where arthicles_id = %s and arthicles_author = %s"
    result = cursor.execute(sorgu,(id,session["username"]))
    if result == 0:
      
      return redirect(url_for("index"))
    else:
      article=cursor.fetchone()
      form=ArticlesForm() 
      form.title.data = article["arthicles_title"]
      form.content.data=article["arhticles_comment"]
      return render_template("ControlPanel/update.html",form=form)
  #POST REQUEST
  else:
    form = ArticlesForm(request.form)
    newTitle=form.title.data
    newContent=form.content.data
    
    sorgu2 = "Update arthicles Set arthicles_title = %s , arhticles_comment = %s where arthicles_id = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newTitle,newContent,id))
    mysql.connection.commit()
    
    return redirect(url_for("UpDeArticles"))



if __name__=="__main__":
    app.run(debug=True)
