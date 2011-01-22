import os
import datetime

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

globalID = 1000

class UserIdentity:
    name = ""
    protocol = ""
    
class Question(db.Model):

    # here we define our database structure

    userName = db.StringProperty()
    Title = db.StringProperty()
    Ques = db.StringProperty(multiline=True)
    questionID = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class Answer(db.Model):
    userName = db.StringProperty()
    Title = db.StringProperty()
    Ans = db.StringProperty(multiline=True)
    answerID = db.IntegerProperty()
    tags = db.StringListProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
class MainPage(webapp.RequestHandler):
    questionID = 0
    
    def get(self):
        
        template_values = {}
        self.response.out.write(template.render('index.html',template_values))

class QuestionSubmit(webapp.RequestHandler):
    
    def post(self):
        global globalID
    
        qData = Question()
        
        qData.Title = self.request.get('title')
        qData.Ques = self.request.get('q')
        qData.questionID = globalID
        globalID += 1
        qData.put()
        self.redirect("/qanda?"+str(qData.questionID))

        
class QuestionPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(template.render('question.html',template_values))

class HelpPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(template.render('help.html',template_values))

class AnswerPage(webapp.RequestHandler):
    def get(self):
        questions_query = Question.all()
        questions = questions_query.fetch(5)
        template_values = {
            'questions': questions
        }

        self.response.out.write(template.render('alist.html',template_values))

class QnAPage(webapp.RequestHandler):
    def get(self):
        qId = self.request.query_string
        qs = db.GqlQuery("select * from Question where questionID = "+qId)
        template_values = {
            'title':qs[0].Title,
            'question':qs[0].Ques
            }
        self.response.out.write(template.render('qanda.html',template_values))

application = webapp.WSGIApplication(
                                     [
                                         
                                     ('/', MainPage),
                                     ('/alist.html', AnswerPage),
                                     ('/index.html', MainPage),
                                     ('/question.html', QuestionPage),
                                     ('/qanda*', QnAPage),
                                     ('/submitQuestion', QuestionSubmit),
                                     ('/help.html',HelpPage)
                                     ],
                        
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
