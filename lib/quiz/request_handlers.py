"""
Request handlers for quiz app a part of OpenAl8az project.
By : Mahmoud Elshobaky (mahmoud.elshobaky@gmail.com).
"""
# importing frequently used handlers
from fu import *
_ = t
# Data Models
from data_models import *
from user.data_models import LocalUser
import logs.request_handlers as log


# Add New Quiz Handler
class AddQuiz(MainHandler):
    def get(self):
        if self.admin:
            self.render('/admin/add-quiz.html')
        else :
            self.redirect('/')
    def post(self):
        have_error = False
        self.title = self.request.get('title')
        self.details = self.request.get('details')
        self.answer1 = self.request.get('answer1')
        self.answer2 = self.request.get('answer2')
        self.answer3 = self.request.get('answer3')
        self.answer4 = self.request.get('answer4')
        self.answer5 = self.request.get('answer5')
        self.true_a = self.request.get('true_a')
        self.explain = self.request.get('explain')
        self.status = self.request.get('status')
        if self.status:
            self.status = 1
        if not self.status:
            self.status = 0

        params = dict(title = self.title,
                      details = self.details)

        if not self.details:
            params['error_title'] = "You must enter details."
            have_error = True
        if not self.admin:
            have_error = True
        if not self.true_a or not self.answer1 :
            have_error = True
        if have_error:
            self.render('/admin/add-quiz.html', **params)
        else:
            self.answers = [self.answer1,
                    self.answer2,
                    self.answer3,
                    self.answer4,
                    self.answer5]
            n = 1
            self.all_ans = []
            for i in self.answers :
                if int(self.true_a) == n:
                    self.all_ans.append(Answer(no = n,
                                               text = i,
                                               true_a = True))
                else :
                    self.all_ans.append(Answer(no = n,
                                               text = i,
                                               true_a = False))
                n += 1

            q = Quiz.register(self.details,
                              self.all_ans,
                              self.title,
                              self.explain)
            q.status = self.status; q.put()
            self.render('/admin/add-quiz.html', done='yes', url=q.key.id())

# Edit Quiz Handler
class EditQuiz(MainHandler):
    def get(self,quiz_id):
        if self.admin :
            quiz = Quiz.by_id(int(quiz_id))
            if not quiz:
                self.render('404.html')
            else:
                for a in quiz.answers :
                        if a.true_a == True :
                            t_a = str(a.no)
                self.render('/admin/edit-quiz.html', quiz=quiz, t_a =t_a)
        else:
            self.redirect('/')
    def post(self,quiz_id):
        have_error = False
        self.quiz_id = self.request.get('quiz_id')
        self.title = self.request.get('title')
        self.details = self.request.get('details')
        self.answer1 = self.request.get('answer1')
        self.answer2 = self.request.get('answer2')
        self.answer3 = self.request.get('answer3')
        self.answer4 = self.request.get('answer4')
        self.answer5 = self.request.get('answer5')
        self.true_a = self.request.get('true_a')
        self.explain = self.request.get('explain')
        self.status = self.request.get('status')
        if self.status:
            self.status = 1
        if not self.status:
            self.status = 0

        params = dict(title = self.title,
                      details = self.details)

        if not self.quiz_id:
            self.render('404.html')
        else :
            self.quiz = Quiz.by_id(int(self.quiz_id))
            params['quiz'] = self.quiz
            if not self.details:
                params['error_title'] = "You must enter details."
                have_error = True
            if not self.true_a or not self.answer1 :
                have_error = True
            if have_error:
                self.render('/admin/edit-quiz.html', **params)
            else:
                self.answers = [self.answer1,
                    self.answer2,
                    self.answer3,
                    self.answer4,
                    self.answer5]
                n = 1
                self.all_ans = []
                for i in self.answers :
                    if int(self.true_a) == n:
                        self.all_ans.append(Answer(no = n,
                                                   text = i,
                                                   true_a = True))
                    else :
                        self.all_ans.append(Answer(no = n,
                                                   text = i,
                                                   true_a = False))
                    n += 1
                self.quiz.title = self.title
                self.quiz.details = self.details
                self.quiz.answers = self.all_ans
                self.quiz.explain = self.explain; self.quiz.status = self.status
                self.quiz.put()
                self.redirect('/admin')



class ResultPerma(MainHandler):
    def get(self, res_id):
        result = Result.by_id(int(res_id))
        if not result:
            self.render('404.html')
        else:
            if result.user_name:
                user_name = result.user_name
            if not result.user_name:
                if result.user_id:
                    user_name = LocalUser.by_id(int(result.user_id)).nickname
                else:
                    user_name = ''
            if int(result.result) < 95 :
                est = int(str(int(result.result)+5)[0])*10
            if int(result.result) >= 95 :
                est = 100
            self.render('result.html', result=result, user_name=user_name, est=est)


class QuizPerma(MainHandler):
    def get(self, q_id):
        quiz = Quiz.by_id(int(q_id))
        if not quiz:
            self.render('404.html')
        else:
            self.render('quiz.html', quiz=quiz)


def check_answer(answer, quiz_id):
    quiz = Quiz.by_id(quiz_id)
    if quiz :
        if quiz.answers[0].text != '' and\
        quiz.answers[1].text=='' and\
        quiz.answers[2].text=='' and\
        quiz.answers[3].text=='' and\
        quiz.answers[4].text=='':
            if answer == quiz.answers[0].text:
                return True , quiz.title
        else:
            for a in quiz.answers :
                if a.true_a == True :
                    t_a = str(a.no)
                    logging.error('t_a = %s and answer = %s'%(t_a,answer))
            if answer == t_a :
                return True , quiz.title
        return False , quiz.title
    return False , None

def add_score(user_id, item_id, score):
    l = Logs.check_log(user_id, item_id, 'q')
    if not l:
        u = LocalUser.by_id(user_id)
        if u.score is None:
            u.score = score
        if u.todayscore is None:
            u.todayscore = score
        else:
            u.score += score
            u.todayscore += score
        u.put()
        return
    return


class CheckAnswer(MainHandler):
    def post(self):
        u_answer = self.request.get('u_answer')
        quiz_id = self.request.get('quiz_id')
        #logging.error('quiz_id equals %s' %quiz_id)
        #logging.error('u_answer %s' %u_answer)
        res , quiz_title = check_answer(u_answer, int(quiz_id))
        if res:
            data = {'correct_a':True}
        else:
            data = {'correct_a':False}
        self.response.headers['Content-Type'] = 'application/json'
        self.write(json.dumps(data))
        if self.user:
            if data['correct_a']:
                add_score(self.user.key.id(), int(quiz_id) ,5)
                log.add_log(self.user.key.id(),
                            self.user.nickname,
                            'q',
                            int(quiz_id),
                            quiz_title)
            else:
                log.add_log(self.user.key.id(),
                            self.user.nickname,
                            'qtry',
                            int(quiz_id),
                            quiz_title)


class ResetTodayScore(MainHandler):
    def get(self):
        LocalUser.reset_today_score()
        self.write('done')


class RandomQuiz(MainHandler):
    def get(self):
        quiz = Quiz.random(count=1)
        quiz = quiz[0]
        self.render('quiz.html',quiz=quiz)


class AjaxRandomQuiz(MainHandler):
    def get(self):
        quiz = Quiz.random(count=1)
        quiz = quiz[0]
        self.render('ajax-quiz.html',quiz=quiz)


class NewTest(MainHandler):
    def add_log(self, ans, quiz_id, quiz_name):
        score = 0
        if self.user:
            if ans == 'q':
                if not Logs.check_log(self.user.key.id(),
                                quiz_id,
                                'q'):
                        score += 5
            log.add_log(self.user.key.id(),
                        self.user.nickname,
                        ans,
                        quiz_id,
                        quiz_name)
        return score
    def get(self):
        self.q_no = self.request.get('q_no')
        if self.q_no:
            self.q_no = int(self.q_no)
            if self.q_no > 50 and not self.admin :
                self.q_no = 50
        if not self.q_no:
            self.q_no = 10
        self.quiz = Quiz.random(count=self.q_no)
        self.qlist = ""
        for i in self.quiz :
            if self.qlist == "" :
                self.qlist += str(i.key.id())
            else :
                self.qlist += ','+str(i.key.id())


        self.render('test.html', quiz=self.quiz, qlist = self.qlist, q_no= self.q_no)
    def post(self):
        true_q = 0
        self.q_no = int(self.request.get('q_no'))
        self.qlist = self.request.get('qlist').split(',')
        self.user_id = None
        if self.user:
            self.user_id = self.user.key.id()
        self.user_name = self.request.get('name')

        n = 0
        new_quiz_score = 0
        for i in self.qlist:
            ans = self.request.get(str(n))
            q = Quiz.by_id(int(i))
            if q.answers[0].text != '' and q.answers[1].text=='' and q.answers[2].text=='' and q.answers[3].text=='' and q.answers[4].text=='':
                if ans == q.answers[0].text:
                    true_q += 1
                    new_quiz_score += self.add_log('q', int(i), q.title)
                else:
                    self.add_log('qtry', int(i), q.title)
            else:
                for a in q.answers :
                    if a.true_a == True :
                        t_a = str(a.no)
                if ans == t_a :
                    true_q += 1
                    new_quiz_score += self.add_log('q', int(i), q.title)
                else:
                    self.add_log('qtry', int(i), q.title)
            n += 1
        res = str((((true_q + 0.0)/self.q_no)*100)+0.5)
        self.result = res[:res.find('.')]
        r = Result.register(self.user_name,
                            self.q_no,
                            true_q,
                            self.qlist,
                            self.result,
                            self.user_id)
        r.put()
        self.redirect('/result/%s' % r.key.id())
        if self.user:
            user_id = self.user.key.id()
            for q in self.qlist:
                if not Logs.check_log(user_id, int(q), 'q'):
                    new_quiz_score += 5
            u = LocalUser.by_id(self.user.key.id())
            if u.score is None:
                u.score = new_quiz_score
            if u.todayscore is None:
                u.todayscore = new_quiz_score
            else:
                u.score += new_quiz_score
                u.todayscore += new_quiz_score
            u.put()


class CustomTest(MainHandler):
    def get(self):
        self.render('custom-test.html')
    def post(self):
        q_no = self.request.get('q_no')
        self.redirect('/test?q_no=%s' % q_no)