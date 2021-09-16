from flask import render_template,request,redirect,url_for,session,flash
from flask_login.utils import login_required, logout_user
from config import app, os_upload_path
from uuid import uuid4
from models import News,Category, User,db
from slugify.slugify import  slugify
import os
import bcrypt
from flask_login import login_user,login_required,logout_user
from forms import Newsform, UserRegister

    
@app.route("/admin/news/")
# @login_required
def admin_news_list_view():
    
    if ('action' and '_id') in request.args:
        try:
            _id=int(request.args.get("_id"))
        except:
            return redirect(url_for('admin_news_list_view'))

        if request.args.get("action")=="make_active":

            chosen_news=News.query.filter_by(id=_id).first_or_404()
            chosen_news.is_published=True
            db.session.commit()

        elif  request.args.get("action")=="make_inactive":

            chosen_news=News.query.filter_by(id=_id).first_or_404()
            chosen_news.is_published=False
            db.session.commit()

        elif  request.args.get("action")=="delete":

            chosen_news=News.query.filter_by(id=_id).first_or_404()
            news=db.session.delete(chosen_news)
            try:
                os.unlink(os.path.join("static","uploads","images",chosen_news.photo))
            except:
                pass
            db.session.commit()
            return redirect(url_for('admin_news_list_view'))



    all_news=News.query.all()
    return render_template("admin/news_list.html",yangiliklar=all_news)

@app.route("/admin/news/create/",methods=['GET','POST'])
# @login_required
def add_news_view():

    if request.method=="POST":

        news=News()

        news.title=request.form["news_title"]
        news.slug=slugify(news.title)
        news.content=request.form["news_content"]
        news.is_published=bool(request.form.get("publish_status",False))
        try:
            news.cat_id=int(request.form.get('category_id'))
        except:
            return redirect(url_for("add_news_view"))

        if "news_photo" in request.files:
            news_photo=request.files["news_photo"]
            photo_filename=str(uuid4())+"."+ news_photo.filename.split(".")[-1]
            news_photo.save(os.path.join(os_upload_path,photo_filename))

            if news_photo.filename.split(".")[-1]!="":
                news.photo=photo_filename
                


        news_cat=request.form.get("category_id",None)
        if news_cat:
            news.is_published=True
        else:
            news.is_published=False
        db.session.add(news)
        db.session.commit()

        return redirect(url_for('admin_news_list_view'))

    return render_template("admin/add_news.html")

@app.route("/admin/category/create/", methods=["GET","POST"])
# @login_required
def add_category_view():
    form=Newsform(request.form)
    if request.method=="POST" and form.validate():
        cat=Category(name=form.name.data)
        db.session.add(cat)
        db.session.commit()

    return render_template("admin/add_category.html",form=form)

@app.route("/admin/category/<int>:_id/update/", methods=["GET","POST"])
# @login_required
def update_category_view(_id):
    cat=Category.query.filter_by(id=int(_id)).first_or_404()
    form=Newsform(request.form,obj=cat)
    if request.method=="POST" and form.validate():
        form.populate_obj(cat)
        cat=Category(name=form.name.data)
        db.session.commit()

    return render_template("admin/add_category.html",form=form)

@app.route("/admin/news/<int:_id>/",methods=["GET","POST"])
# @login_required
def update_news_view(_id):
    if request.method=="POST":
        print("Post bu")

        news=News.query.filter_by(id=_id).first_or_404()
        
        news.title=request.form["news_title"]
        news.slug=slugify(news.title)
        news.content=request.form["news_content"]
        news.is_published=bool(request.form.get("publish_status",False))

        try:
            print(request.form.get('category_id'))
            news.cat_id=int(request.form.get('category_id'))
        except:
            return redirect(url_for("update_news_view"))

        if "news_photo" in request.files:
            news_photo=request.files["news_photo"]
            photo_filename=str(uuid4())+"."+ news_photo.filename.split(".")[-1]
            news_photo.save(os.path.join(os_upload_path,photo_filename))

            if news_photo.filename.split(".")[-1]!="":
                news.photo=photo_filename
            
        db.session.commit()
        return redirect(url_for("admin_news_list_view"))

    elif request.method=="GET":
        if request.args.get("action",None)=="delete-thumb":
            chosen_news=News.query.filter_by(id=_id).first_or_404()
            os.unlink(os.path.join("static","uploads","images",chosen_news.photo))
            chosen_news.photo=""
            db.session.commit()
            return redirect(url_for("update_news_view",_id=_id))
        chosen_news=News.query.filter_by(id=_id).first_or_404()
    return render_template("admin/updates_news.html",  yangilik=chosen_news)
   
@app.route("/admin/login/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username",None)
        password=request.form.get("password",None)

        if not username or not password:
            flash("Iltimos login va parolni tog'ri kiriting!!!","warning")

        else:
            user=User.query.filter_by(username=username.strip()).first_or_404()

            if bcrypt.checkpw(password.encode(),user.password):
                flash("Siz kabinetga kirdingiz","success")
                session['login'] = username
                session['password'] = password.strip()
                login_user(user)
                return redirect(url_for("admin_news_list_view"))
            else:
                flash("parol xato","danger")

    return render_template("admin/login.html")


@app.route("/register/", methods=["GET","POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname", None)
        username = request.form.get("username", None)
        password1 = request.form.get("password1", None)
        password2 = request.form.get("password2", None)

        if not username:
            flash("username kiritilmadi!", "danger")
            return render_template("admin/register.html")
        
        if not password1 or not password2:
            flash("parolni to'g'ri kiriting", "danger")
            return render_template("admin/register.html")

        elif password1 and password2 and password1.strip() != password2.strip():
            flash("Parollar mos kelmayapti!", "danger")
            return render_template("admin/register.html")

        else:
            user = User()
            user.username = username
            if fullname:
                user.fullname = fullname
                user.password = bcrypt.hashpw(password1.strip().encode(), bcrypt.gensalt())
                db.session.add(user)
                db.session.commit()
                flash("Siz ro'yhatdan o'tdingiz!", "success")
            return render_template("admin/register.html")

    return render_template("admin/register.html")
    

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('login'))
            
















