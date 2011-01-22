import os
import datetime

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class UserIdentity:
    name = ""
    protocol = ""
    
class Question(db.Model):

    # here we define our database structure
    
    userID = db.StringProperty() 
    userName = db.StringProperty()
    Title = db.StringProperty()
    Type = db.StringProperty()
    Ques = db.StringProperty(multiline=True)
    questionID = db.IntegerProperty()
    tags = db.StringListProperty()
    date = db.DateTimeProperty(auto_now_add=True)

    
class MainPage(webapp.RequestHandler):
    def get(self):
        
        template_values = {}
        self.response.out.write(template.render('index.html',template_values))

class QuestionSubmit(webapp.RequestHandler):
    def post(self):

        
class QuestionPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(template.render('question.html',template_values))

class AnswerPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(template.render('alist.html',template_values))

class QnAPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(template.render('qanda.html',template_values))

application = webapp.WSGIApplication(
                                     [
                                         
                                     ('/', MainPage),
                                     ('/alist.html', AnswerPage),
                                     ('/index.html', MainPage),
                                     ('/question.html', QuestionPage),
                                     ('/qanda.html', QnAPage),
                                     ('/submitQuestion.html', QuestionSubmit)
                                     ],
                        
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
