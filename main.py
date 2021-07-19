from config import app,login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first_or_404()

from News_vews import *
from Context import *
from admin_news_view import *
from errors_views import *

if __name__ == "__main__":
    app.run(debug=True)


  # if request.method=="POST":
    #     username=request.form.get("username",None)
    #     password=request.form.get("password",None)

    #     if not username or not password:
    #         flash("Iltimos login va parolni tog'ri kiriting!!!","warning")

    #     else:
    #         user=User.query.filter_by(username=username.strip()).first_or_404()

    #         if bcrypt.checkpw(password.encode(),user.password):
    #             flash("Siz kabinetga kirdingiz")
    #             session['login']=username
    #             session['password']=password.strip()
    #             login_user(user)
    #             return redirect(url_for("admin_news_list_view"))
    #         else:
    #             flash("parol xato","danger")