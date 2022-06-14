import email
import re
from flask import Flask, render_template, request , flash, redirect, url_for, session, g
import flask
#from flask_session import session

# from werkzeug  import secure_filename
from werkzeug.utils import secure_filename
import uuid as uuid
from forms import *



import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretpass'


from modules import *

app.config['UPLOAD_FOLDER'] = 'static/images/'



@app.before_request
def before_request():
    g.email = None 
    if 'email' in session:
        g.email = session['email']
        print('g.email ____________', g.email)


@app.route('/show_post')
def show_my_post():
    return 'asfsafa'
    # if g.email: 
    #     user_data = Users.query.filter_by(email=session['email']).first()
    #     user_id = user_data.id 
    #     posts = Post.query.filter_by(user_id=user_id)  
        
    #     for i in  posts:
    #         print("post details : ",  i.file, i.content)
    #     return render_template('show_post.html', posts=posts, user_name=user_data.user_name)
    # return redirect(url_for('log_in'))    


@app.route('/profile', methods=['POST',  'GET'])
def profile():
    if g.email: 
        try:
            print("in try block ")
            user_detail = Users.query.filter_by(email=session['email']).first()
            
            
            if request.method == 'POST':
            
                user_name = request.form.get('user_name')
                
                mobile_number = request.form.get('mobile_number')

                about_author = request.form.get('about_author')
                file = request.files['user_pic']

                filename = secure_filename(file.filename)
                if filename != '':
                    filename = str(uuid.uuid1()) +  filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    user_detail.user_name = user_name
                   
                    user_detail.about_author = about_author
                    user_detail.user_pic =  filename
                    db.session.commit()
                    flash("Your details uploded successfully ")
                return redirect(url_for('profile'))
                
        except:
            return redirect(url_for('log_in'))

        return render_template('profile.html', user_detail = user_detail)
    return redirect('log_in')    




# @app.route('/delete_post/<int:id>')
# def delete_post(id):
#     post_delete = Post.query.get_or_404(id)
#     print('User delete *********** : ', post_delete)
#     try:
#         db.session.delete(post_delete)
#         db.session.commit()
#     except:
#       flash("Error invalid user id ")
#       return 'deleted post'
#     finally:
#         return  'deleted'






@app.route('/add_post', methods= ['POST', 'GET'])
def add_post():
    print('g.email +++++++++++++ ', g.email)
    if g.email: 
        form = Posts()
        # user_detail =  Users.query.get(id)
        user_detail = Users.query.filter_by(email=session['email']).first()
        user_id = user_detail.id 
        if request.method == 'POST':
            print('in post ************* ')
            if form.validate_on_submit():
                
                file = request.files['post_pic']
                print("in validate_on_submit *************  ")

                filename = secure_filename(file.filename)
                filename = str(uuid.uuid1()) +  filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       
                post =  Post(title=form.title.data, content=form.content.data, user_id= user_id, file=filename )
                db.session.add(post)
                db.session.commit()
                print('hellasdds fadsfad fdfa sd(((( ')
                flash("successfully add post")
                return redirect(url_for('dashboard'))
       
            
            # form.title.data, form.content.data = '', ''

        return render_template('add_post.html', form=form, user_detail=user_detail) 
    return redirect('log_in')          

# @login_required
@app.route('/dashboard')
def dashboard():
    if g.email: 
    # get_or_404 if id is not available so error occure and program break and get() is not error occuring.
        print('session["user_name"]  ', session["email"], session.get("email") )

        
        # user_detail =  Users.query.get(id)
        user_detail = Users.query.filter_by(email=session['email'])
        all_post = Post.query.order_by(Post.date_posted.desc())
        user_obj = Users()
        flash('welcome to dashboard')
        return render_template('dashboard.html', session= session['email'])
    return redirect(url_for('log_in'))  
          


# working !
@app.route('/', methods = ['GET', 'POST'])
@app.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    form = Registraion()
    print(form)
    success = None 
    if request.method == 'POST': 
      
        if form.validate_on_submit():
            user = Users.query.filter_by(user_name=form.username.data).first()
            if(user == None):
                user = Users(user_name=form.username.data,
                            full_name=form.full_name.data, 
                            password=form.password.data,
                            email=form.email.data,)


                db.session.add(user)
                db.session.commit()
                # returnning message or redirecting to the specific page
                return 'registeration successs'
        else:
            success = 'User Name is already exist'

            # empty the input form fields
            form.username.data  = ''
            form.full_name.data = ''
            form.password.data = ''    
            form.email.data = ''

    return render_template('registration.html', form=form, success=success)


@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    message = None 
    form = LoginForm()
    if request.method == 'POST':
        session.pop('email', None)
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data, password=form.password.data).first()

            if user: 
                #print('user from log_in(): ',user)
                session["email"] = form.email.data
                #print('session["email"]  : ', session["email"] )

                form.email, form.password = '', '' 
                return redirect(url_for('dashboard'))
                return 'login successfully!! '
                  
            else:
                # empty the input form fields
                form.password.data = ''    
                form.email.data = ''

                #return redirect('sign_up')        
                return 'Incorrect User name or password !!'    

    return render_template('login.html', form=form, message=message )                



@app.route('/log_out')
def log_out():
    session['email'] = None 
    return redirect(url_for('log_in'))


# @app.route("/show_data")
# def show_data(): 
#     user_data = Users.query.order_by(Users.date_added)
#     return render_template('show_data.html', user_data=user_data)

# @app.route('/update_and_delete/<int:id>')
# def update_and_delete(id):
#     return render_template('delete_and_update_user.html', id=id)


# # Update user details 

# @app.route("/update/<int:id>", methods = ["POST", "GET"])
# def update(id):
#      form = Registraion()
#      update_user =  Users.query.get_or_404(id)
#      if request.method == "POST":
#         print("get id  ********* ", update_user)
#         update_user.user_name = request.form['user_name']
#         update_user.mobile_number = request.form['mobile_number']

#         try: 
#             db.session.commit()
#             print("updaated *****")
#             flash("User updated successfully ")
#             return redirect(url_for('show_data'))


#         except:
#             flash("Error")
#             return 'this is error page'

#      return render_template('update_data.html', form=form, update_user=update_user )


# @app.route('/delete/<int:id>')
# def delete(id):
#     print('id *********** : ', id)
#     user_delete = Users.query.get_or_404(id)
#     print('User delete *********** : ', user_delete)
#     try:
#         db.session.delete(user_delete)
#         db.session.commit()
#         print('User delete ***************************  ')
#         flash("user deleted ")
#     except:
#       flash("Error invalid user id ")
#       print('Except ****************  ')
#     finally:
#         return  redirect(url_for('show_data'))



# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# @app.route('/username/<name>')
# def username(name):
#     return f"my name fd is this {name}"







