from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:YES@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String (255))

    def __init__(self, title, body):
        self.title = title
        self.body = body

#app routes for blog, newpost

#blog should render the blogs in order with a link for them to pull up individually
#individual can be posted under here in an if else statement. 
#if you're not displaying blog you will display the individual post

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    id = request.args.get("id")
    if id:
        id_post = Blog.query.get(id)
        return render_template('individual.html',all_blog=id_post)
    else:
        all_blog = Blog.query.all()
        return render_template('blog.html',all_blog=all_blog)
    
 
#newpost should render a page where you can enter the blog
#along with displaying errors when they don't input the correct things
#make sure to call a method.request for post that way you don't run into errors

@app.route('/newpost', methods=['POST','GET'])
def newpost():
    

    #start with this if since this will be both a GET and POST page
    if request.method == 'POST':
        title_error = ""
        blog_error = ""

        title = request.form["title"]
        blog = request.form["blog"]
        error = 0

        if len(title) < 3:
            error +=1
            title_error = "Please Enter a title"
        if len(blog) < 3:
            error += 1 
            blog_error ="Enter a blog Post"
        if error !=0:
            return render_template('newpost.html',title=title,title_error=title_error,blog=blog,blog_error=blog_error)
        else:
            #rewrite this to fit into your posts to save it to the server
        #make sure to make checks to see if everything is correct before saving the server
            new_blog = Blog(title,blog)
            db.session.add(new_blog)
            db.session.commit()
            return redirect ("/blog?id=" + str(new_blog.id))
    else:  
        return render_template('newpost.html')

#leave this as is
if __name__ == '__main__':
    app.run()