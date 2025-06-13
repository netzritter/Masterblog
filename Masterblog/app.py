from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
POSTS_FILE = 'blog_posts.json'

def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=4)


def fetch_post_by_id(posts, post_id):
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()
        new_post = {
            'id': posts[-1]['id'] + 1 if posts else 1,
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'content': request.form.get('content')
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()
    posts = [p for p in posts if p['id'] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET','POST'])
def update(post_id):
    posts = load_posts()
    post  = fetch_post_by_id(posts, post_id)   # <-- pass the same list in

    if post is None:
        return 'Not found', 404

    if request.method == 'POST':
        post['author']  = request.form['author']
        post['title']   = request.form['title']
        post['content'] = request.form['content']
        save_posts(posts)                        # <-- now “posts” holds your changes
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
