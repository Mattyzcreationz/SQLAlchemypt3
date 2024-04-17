from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mattyz:password@localhost:5432/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

toolbar = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

# Root route redirecting to users
@app.route('/')
def root():
    return redirect('/users')

# User index route
@app.route('/users')
def user_index():
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('base.html', users=users)

# New user form route
@app.route('/users/newuser', methods=['GET'])
def new_user_form():
    return render_template('newusers.html')

# Create new user route
@app.route('/users/newuser', methods=['POST'])
def create_user():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url']
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

# User detail route
@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('detail.html', user=user)

# Edit user route
@app.route('/users/<int:user_id>/edit', methods=['GET'])
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('editbtn.html', user=user)

# Update user route
@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.commit()
    return redirect('/users')

# Delete user route
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

# Add post route
@app.route('/users/<int:user_id>/addpost', methods=['POST'])
def add_post(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('PostForm.html', user=user)

# Create post route
@app.route('/post/<int:post_id>/add', methods=['POST'])
def create_post(post_id):
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user_id=post_id
    )
    db.session.add(new_post)
    db.session.commit()
    return redirect('/post')

# Post detail route
@app.route('/post/<int:post_id>/postdetail')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('postDetail.html', post=post)

# Delete post route
@app.route('/post/<int:post_id>/postdelete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/post')

# Edit post route
@app.route('/post/<int:post_id>/editPost', methods=['GET'])
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('EditPost.html', post=post)

# Update post route
@app.route('/post/<int:post_id>/finishedPost', methods=['POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()
    return redirect('/post')

# Tag page route
@app.route('/tag/createtag', methods=['GET'])
def tag_page():
    return render_template('createTag.html')

# Create tag route
@app.route('/tag/createtag', methods=['POST'])
def create_tag():
    new_tag = Tag(
        name=request.form['name']
    )
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tag')

# Edit tag page route
@app.route('/tag/<int:tag_id>/EditPage')
def edit_tag_page(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tagedit.html', tag=tag)

# Edit tag route
@app.route('/tag/<int:tag_id>/editTag', methods=['POST'])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    db.session.commit()
    return redirect('/tag')

# List tag route
@app.route('/tag/<int:tag_id>/listTag')
def list_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('ListTag.html', tag=tag)

# Show tag route
@app.route('/tag/<int:tag_id>/ShowTag')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('ShowTags.html', tag=tag)

# Show tag edit route
@app.route('/tag/<int:tag_id>/ShowTagEdit', methods=['POST'])
def show_tag_edit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tag')

# Post tags route
@app.route('/posttags/<int:post_id>/PostTags')
def post_tags(post_id):
    post_tags = PostTag.query.get_or_404(post_id)
    return render_template('/post/user_id', post_tags=post_tags)

# Post with tags route
@app.route('/posttags/postwitTags')
def post_with_tags(post_tag_id):
    post_with_tags = PostTag.query.get_or_404(post_tag_id)
    return render_template('PostwitTags.html', post_with_tags=post_with_tags)
