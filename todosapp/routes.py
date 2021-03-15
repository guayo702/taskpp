from flask import render_template, url_for, flash, redirect, request, abort
from todosapp.forms import RegistrationForm, LoginForm, TaskForm, ForgotPasswordForm
from todosapp.model import User, ToDo
from todosapp import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/home',methods=['GET','POST'])
@app.route('/home/<int:order_by>', methods=['GET','POST'])
@login_required
def home(order_by=None):
    if(order_by == 1):
        tasks= ToDo.query.filter_by(user_id=current_user.id).order_by(ToDo.title.asc()).all()
    elif(order_by == 2):
        tasks= ToDo.query.filter_by(user_id=current_user.id).order_by(ToDo.title.desc()).all()
    elif(order_by == 3):
        tasks= ToDo.query.filter_by(user_id=current_user.id).order_by(ToDo.priority.desc()).all()
    elif(order_by == 4):
        tasks= ToDo.query.filter_by(user_id=current_user.id).order_by(ToDo.priority.asc()).all()
    elif(order_by == 6):
        tasks= ToDo.query.filter_by(user_id=current_user.id).order_by(ToDo.end_date.desc()).all()
    else:
        tasks= ToDo.query.filter_by(user_id=current_user.id).order_by(ToDo.end_date.asc()).all()
    
    size=len(tasks)
    return render_template('home.html', tasks=tasks, size=size)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pd=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data , email = form.email.data, password= hashed_pd)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in','success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/')
@app.route('/login',  methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')            
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else :
            flash('Login Unsuccessful','danger')      
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    image_file=url_for('static', filename='userimage.jpg')
    return render_template('account.html', image_file=image_file)


@app.route('/task/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form= TaskForm()
    if form.validate_on_submit():
        todo= ToDo(title=form.title.data.capitalize(), content=form.content.data, author=current_user, priority=form.priority.data, end_date=form.end_date.data)
        db.session.add(todo)
        db.session.commit()
        flash('Your task has been created!','success')
        return redirect(url_for('home'))  
    return render_template('create_task.html', form=form, legend='New Task')    


@app.route('/task/<int:task_id>')
@login_required
def task(task_id):
    task= ToDo.query.get_or_404(task_id)
    if task.author != current_user: 
        abort(403)
    return render_template('task.html',task=task)

@app.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def updatetask(task_id):
    task= ToDo.query.get_or_404(task_id)
    if task.author != current_user: 
        abort(403)
    form = TaskForm(priority=task.priority)
    if form.validate_on_submit():
        task.title=form.title.data.capitalize()
        task.content=form.content.data
        task.end_date=form.end_date.data
        task.priority=form.priority.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('task',task_id=task.id))
    elif request.method == 'GET':
        form.title.data = task.title
        form.content.data = task.content
        form.end_date.data = task.end_date
    return render_template('create_task.html', form=form, legend='Update Task')

@app.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def deletetask(task_id):
    task = ToDo.query.get_or_404(task_id)
    if task.author != current_user : 
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/task/<int:task_id>/complete', methods=['POST'])
@login_required
def completetask(task_id):
    task = ToDo.query.get_or_404(task_id)
    if task.author != current_user : 
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Your post has been completed!', 'success')
    return redirect(url_for('home'))

@app.route('/forgotpassword', methods=['GET','POST'])
def forgotpassword():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=ForgotPasswordForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()
        hashed_pd=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password= hashed_pd
        db.session.commit()
        flash('Your password has been modify! You are now able to log in','success')
        return redirect(url_for('login'))
    return render_template('forgotpassword.html',form=form)