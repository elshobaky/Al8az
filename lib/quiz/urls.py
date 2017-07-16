"""
url mapping for quiz app a part of OpenAl8az project.
By : Mahmoud Elshobaky (mahmoud.elshobaky@gmail.com).
"""

# import app engine frameworks
import webapp2
from webapp2_extras import routes

# import app settings
from settings import *

#import project modules and request handlers
from request_handlers import *

#URL Mapping
# ex. [webapp2.Route(_u+'/signup', SignUp, 'user-signup'),]
_u = URLS_PREFIX + '/quiz' # you can add prefix for app ex. -u = URLS_PREFIX + '/page'
urls = [
   webapp2.Route('/admin/addquiz', AddQuiz, 'add-quiz'),
   ('/admin/editquiz/([0-9]+)', EditQuiz),
   webapp2.Route('/test', NewTest, 'new-test'),
   webapp2.Route('/customtest', CustomTest, 'custom-test'),
   (_u+'/([0-9]+)', QuizPerma),
   webapp2.Route('/randomquiz', RandomQuiz, 'random-quiz'),
   webapp2.Route('/ajax/randomquiz', AjaxRandomQuiz, 'ajax-random-quiz'),
   webapp2.Route('/ajax/checkquizanswer', CheckAnswer, 'check-quiz-answer'),
   ('/result/([0-9]+)', ResultPerma),
   webapp2.Route('/tasks/resettodayscore', ResetTodayScore),
]

# rendring urls
#app = webapp2.WSGIApplication(urls,
#	config=INTERNATIONAL_CFG, debug=DEBUG)
