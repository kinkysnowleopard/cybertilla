# coding: utf-8
# Author: Bertilla Fabris

from bottle import get, route, abort, run, template, request, redirect, static_file
import os



@route("/")
@route("/index.html")
def list_articles():
    """
    This is the home page, which shows a list of links to all content.
    """
    return template("index")


@route("/bio")
@route("/bio.html")
def list_articles():
    """
    This is my biography.
    """
    return template("bio")


def get_article_from_file(file_name):
        try:
            my_file = open(f"storage/articles/{file_name}", "r")
            content = my_file.read()
            a = content.split("  ")
            my_file.close()
            return a

        except:
            return None


def get_poem_from_file(file_name):
        try:
            my_file = open(f"storage/poems/{file_name}", "r")
            content = my_file.read()
            a = content.split("  ")
            my_file.close()
            return a

        except:
            return None


@route ('/articles')
@route('/articles.html')
def show_all_articles():
    """
    List all articles in storage
    """
    return template("articles", root="views/")


@route('articles/<pagename>/')
@route('articles/<pagename>')
def show_article(pagename):
    """
    Displays a single article (loaded from a text file).
    """
    content = get_article_from_file(pagename)
    if content is None:
        return abort(404, "No such page exists.")

    return template("article", content=content, title=pagename)


@route('/bio-hacks.html')
@route('/bio-hacks')
def show_biohacks():
    """
    Display static Bio-Hacks redirection page.
    """
    return template('bio-hacks.html', root="views")


@route('/poetry.html')
@route('/poetry')
def list_all_poems():
    """
    Display a list with all poems titles and tags
    """
    return template('poetry', root="views")


@route('poems/<pagename>/')
@route('poems/<pagename>')
def show_article(pagename):
    """
    Displays a single poem (loaded from a text file).
    """
    content = get_poem_from_file(pagename)
    if content is None:
        return abort(404, "No such poem exists (yet).")

    return template("article", content=content, title=pagename)







####################################

@route('/edit/')
@route('/edit')
def edit_form():
    """
    Shows a form which allows the user to input a title and content
    for an article. This form should be sent via POST to /update/.
    """
    return static_file("edit.html", root="views/")


def save_to_file(title, content):
    '''
    Make a new file with title and content,
    title needs to be at least two words long,
    text needs to be at least 15 words long.
    '''
    if len(content) > 15 and len(title) > 2:
        my_file = open(f"storage/{title.strip()}", "w")
        my_file.write(content)
        my_file.close()
    else:
        abort(400, "Content insufficient. \nPlease write more that a few words to save a new article to the wiki. \nYour title must also contain at least two words.")


@route('/update/', method="POST")
@route('/update', method="POST")
def update_article():
    """
    Receives page title and contents from a form, and creates/updates a
    text file for that page.
    """
    title = request.forms.title
    content = request.forms.content
    print(content)

    save_to_file(title, content)
    redirect(f'/wiki/{title}')



@route('/remove')
@route('/remove/')
def remove_form():
    """
    Shows a form which allows the user to input a title and delete
    an article. This form should be sent via POST to /delete/.
    """
    return static_file("remove.html", root="views/")


def remove_file(title):
    '''
    Removes file from local storage system.
    '''
    os.remove(f"storage/{title.strip()}")


@route('/delete/', method="POST")
@route('/delete', method="POST")
def delete_article():
    """
    Removes article from file system, redirects to home page.
    """
    title = request.forms.title
    print(title)
    remove_file(title)
    redirect('/')

#######################################

@get("/<filepath:re:.*\.css>")
def css(filepath):
    """
    Afford .css files in static directory.
    """
    return static_file(filepath, root="static/")


@get("/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    """
    Afford images.
    """
    return static_file(filepath, root="static/images/")



run(host='localhost', port=8080, debug=True, reloader=True)