import os, re, markdown

from flask import *
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message

from werkzeug.utils import secure_filename

from myapp import myapp_obj, basedir, db, mail
from myapp.forms import LoginForm, RegisterForm, FileForm, uploadForm
from myapp.models import User, Post, todo_list\

@myapp_obj.route("/")
def hello():
    title = 'Meno-Time HomePage'
    return render_template("hello.html", title=title)

@myapp_obj.route("/register" ,methods=['GET','POST'])
def register():
    form = RegisterForm()
   # all_users = User.query.all()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, password = form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html",form=form)

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    getuser=User.query.all()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        return redirect('/loggedin')
    return render_template("login.html", form=form)

@myapp_obj.route("/loggedin")
@login_required
def log():
    flash('You are logged in', 'error')
    return redirect('/')

@myapp_obj.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@myapp_obj.route("/renderFlashCard", methods=['GET', 'POST'])
def markdownToFlashcard():
    title = 'Flash Cards'
    form = uploadForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(basedir, 'flashcards', filename))
        flash('Uploaded Flash Cards Successfully!')

    filenames = os.listdir(os.path.join(basedir, 'flashcards'))
    flashCardTitles = list(sorted(re.sub(r"\.md$", "", filename)
        for filename in filenames if filename.endswith(".md")))

    return render_template('flashcards.html', form=form, title=title, cardTitles=flashCardTitles)

@myapp_obj.route('/FlashCard/<title>')
def showFlashCards(title):
    filenames = os.listdir(os.path.join(basedir, 'flashcards'))
    flashCardTitles = list(sorted(re.sub(r"\.md$", "", filename)
        for filename in filenames if filename.endswith(".md")))

    if title in flashCardTitles:
        with open(os.path.join(f"{basedir}/flashcards/{title}.md"), 'r') as f:
            text = f.read()
            return render_template('flashcard.html', flashcard=markdown.markdown(text), title=title)
    return redirect('/')

@myapp_obj.route('/shareFlash', methods=['GET', 'POST'])
def shareFlash():
    title = 'Share Flash'
    if  request.method == "POST":
        try:
            email = str(request.form['email'])
            subject = str(request.form['subject'])
            msg_body = str(request.form['message'])

            message = Message(subject, sender="sjm9509@gmail.com", recipients=[email])
            message.body = msg_body
            mail.send(message)
            flash("Email Sent!")
            return redirect('/')

        except ConnectionRefusedError as connectionRefusedError_:
            return "Failed to send Email. Please try again later!"
    else:
        return render_template("shareFlashcards.html",title=title)

@myapp_obj.route('/notes', methods=['GET', 'POST'])
def upload_note():
    name = 'Jim'
    title='Note'

    form = FileForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            basedir, 'notes', filename
        ))
        flash('Uploaded note successfully')

    filenames = os.listdir(os.path.join(basedir, 'notes'))
    note_titles = list(sorted(re.sub(r"\.md$", "", filename)
        for filename in filenames if filename.endswith(".md")))

    return render_template('notes.html',
        form=form,
        title=title,
        note_titles=note_titles,
        name=name
    )

@myapp_obj.route('/note/<title>')
def show_note(title):
    filenames = os.listdir(os.path.join(basedir, 'notes'))
    note_titles = list(sorted(re.sub(r"\.md$", "", filename)
        for filename in filenames if filename.endswith(".md")))

    if title in note_titles:
        with open(os.path.join(f"{basedir}/notes/{title}.md"), 'r') as f:
            text = f.read()
            return render_template('note.html',
                note=markdown.markdown(text),
                title=title)
    return redirect('/')


@myapp_obj.route('/shareNotes', methods=['GET', 'POST'])
def shareNotes():
    title = 'Share Note'
    if  request.method == "POST":
        try:
            email = str(request.form['email'])
            subject = str(request.form['subject'])
            msg_body = str(request.form['message'])

            message = Message(subject, sender="sjm9509@gmail.com", recipients=[email])
            message.body = msg_body
            mail.send(message)
            flash("Email Sent!")
            return redirect('/')

        except ConnectionRefusedError as connectionRefusedError_:
            return "Failed to send Email. Please try again later!"
    else:
        return render_template("shareNote.html",title=title)

@myapp_obj.route("/pomodoroTimer")
def pomodoroTimer():
    title = 'pomodoroTimer'
    return render_template("pomodoroTimer.html",title=title)

@myapp_obj.route('/todolist')
def todolist():
    title = 'To-Do List'
    complete = todo_list.query.filter_by(complete=True).all()
    incomplete = todo_list.query.filter_by(complete=False).all()

    return render_template('todolist.html', title = title,complete = complete, incomplete = incomplete)

@myapp_obj.route("/add", methods=['POST'])
def add():
    todo = todo_list(todo_item = request.form["todoitem"], complete = False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('todolist'))

@myapp_obj.route("/complete/<id>")
def complete(id):
    todo = todo_list.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('todolist'))



# @myapp_obj.route('/share-flashcards', methods=['POST'])
# def share_flashCards():
#     flashcards = FlashCards.query.all()
#     if request.method == "POST":
#         try:
#             email = str(request.form['email'])
#             subject = 'Flash Cards'
#             message = Message(subject, sender="sjm9509@gmail.com", recipients=[email])
#             message.body = render_template("share_flashcards.html",flashcards=flashcards)
#             message.html = render_template("share_flashcards.html",flashcards=flashcards)
#             message.attach = render_template("share_flashcards.html",flashcards=flashcards)
#             mail.send(message) #Sends email
#             flash("Flashcards Email Sent!")
#             return redirect('/')

#         except ConnectionRefusedError as connectionRefusedError_:
#             return "Failed to send Email. Please try again later!"
#     else:
#         return render_template("view_flashcards.html")
