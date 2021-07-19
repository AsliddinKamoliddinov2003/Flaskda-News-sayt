from wtforms import Form ,StringField,validators,PasswordField


class UserRegister(Form):
    fullname=StringField("fullname",[
        validators.Length(min=4,max=50)],
        render_kw={"class":"form-control"}
    )
    username=StringField("username",[
        validators.Length(min=4,max=25),
        validators.DataRequired()],
        render_kw={"class":"form-control"}
    )
    password=PasswordField("password",[
        validators.DataRequired(),
        validators.EqualTo("password2")],
        render_kw={"class":"form-control"}
    )
    password2=PasswordField("password Confirmation",
        render_kw={"class":"form-control"}
    )

class Newsform(Form):
    name=StringField("kategoriya nomi",[validators.Length(min=4),validators.DataRequired()],render_kw={"class":"form-control"})


# class Loginform(Form):
#     username=StringField("username",[
#         validators.Length(min=4,max=25),
#         validators.DataRequired()],
#         render_kw={"class":"form-control"}
#     )
#     password=PasswordField("password",[
#         validators.DataRequired(),
#         validators.EqualTo("password2")],
#         render_kw={"class":"form-control"}
#     )
