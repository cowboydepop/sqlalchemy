

from flask import Flask, render_template, redirect, url_for
from models import db, Tag, Post, PostTag, User 
from forms import UserForm, PostForm  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'your_secret_key'

connect_db(app)

with app.app_context():
    db.create_all()


@app.route('/')
def redirect_to_users():
    return redirect(url_for('show_users'))

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def add_user():
    form = UserForm()

    if form.validate_on_submit():
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            image_url=form.image_url.data or None
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('show_users'))

    return render_template('users/new.html', form=form)

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.image_url = form.image_url.data or None
        db.session.commit()
        return redirect(url_for('show_users'))

    return render_template('users/edit.html', user=user, form=form)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('show_users'))

@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def add_post(user_id):
    user = User.query.get_or_404(user_id)
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            user=user
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Post added successfully!', 'success')
        return redirect(url_for('show_user', user_id=user_id))

    return render_template('posts/new.html', form=form, user=user)

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('show_post', post_id=post_id))

    return render_template('posts/edit.html', post=post, form=form)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id  # Save the user_id before deleting the post
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('show_user', user_id=user_id))

if __name__ == '__main__':
    app.run(debug=True)
