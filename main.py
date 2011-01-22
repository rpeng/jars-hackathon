import os
import datetime
import string

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

globalID = 1000
currentQuestion = ""
    
class Question(db.Model):

    # here we define our database structure

    userName = db.StringProperty()
    email = db.StringProperty()
    Title = db.StringProperty()
    Ques = db.StringProperty(multiline=True)
    questionID = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now=True)

class Answer(db.Model):
    userName = db.StringProperty()
    Ans = db.StringProperty(multiline=True)
    answerID = db.IntegerProperty()
    email = db.StringProperty()
    date = db.DateTimeProperty(auto_now=True)
    
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
        qData.userName = self.request.get('n')
        qData.email = self.request.get('email')
        qData.questionID = globalID
        
        globalID += 1
        qData.put()
        self.redirect("/qanda?"+str(qData.questionID))
        
class AnswerSubmit(webapp.RequestHandler):
    
    def post(self):
        global globalID
        global currentQuestion
        
        aData = Answer()

        aData.Ans = self.request.get('ans')
        aData.userName = self.request.get('na')
        aData.email = self.request.get('ema')
        aData.answerID = int(currentQuestion)
        aData.put()
                
        self.redirect("/qanda?"+str(currentQuestion))

        
class QuestionPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(template.render('question.html',template_values))

class HelpPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(template.render('help.html',template_values))
        
class SearchResults(webapp.RequestHandler):
    def post(self):
        search = self.request.get('s')
        results = db.GqlQuery("select * from Question")
        template_values = {}
        self.response.out.write(template.render('sresults.html',template_values))
        for s in results:
            lstring = string.lower(s.Title)
            l2string = string.lower(s.Ques)
            rstring = string.lower(search)
            if (lstring.find(rstring) >= 0) or (l2string.find(rstring) >= 0):
                self.response.out.write("<li><a href = \"/qanda?"+str(s.questionID)+"\">"+s.Title+"</a></li>")
        self.response.out.write("""
  </div>
  <div style="clear: both;">&nbsp;</div>
			</div>
</div>				
	<!-- end #page -->
<div id="footer">
	<p>Copyright (c) 2011. All rights reserved. Design by jars();</a>.</p>
</div>

<!-- end #footer -->
</body>
</html>
""")
            

class AnswerPage(webapp.RequestHandler):
    def get(self):
        questions_query = Question.all()
        questions_query.order("-date")
        questions = questions_query.fetch(5)
        template_values = {
            'questions': questions
        }

        self.response.out.write(template.render('alist.html',template_values))

class QnAPage(webapp.RequestHandler):
    def get(self):
        global currentQuestion
        qId = self.request.query_string
        currentQuestion = qId
        qs = db.GqlQuery("select * from Question where questionID = "+qId)
        ans = db.GqlQuery("select * from Answer where answerID = "+qId)
        template_values = {
            'title':qs[0].Title,
            'question':qs[0].Ques,
            'user':qs[0].userName,
            'email':qs[0].email,
            'date':qs[0].date.strftime("%m/%d/%Y %H:%M"),
            'id':str(qs[0].questionID),
            'answers':ans
            }
        self.response.out.write(template.render('qanda.html',template_values))

application = webapp.WSGIApplication(
                                     [
                                         
                                     ('/', MainPage),
                                     ('/alist.html', AnswerPage),
                                     ('/index.html', MainPage),
                                     ('/question.html', QuestionPage),
                                     ('/qanda*', QnAPage),
                                     ('/submitAnswer*',AnswerSubmit),
                                     ('/submitQuestion', QuestionSubmit),
                                     ('/help.html',HelpPage),
                                     ('/sresults.html',SearchResults),
                                     ('/submitSearch*',SearchResults)
                                     ],
                        
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
