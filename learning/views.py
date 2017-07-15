from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import UserForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Course,Course_Content,Quiz,Question1,CoursePerformance,Quiz_Performance,CoursePerformanceHistory,QuizPerformanceHistory
from django.db.models import Q

# Create your views here.

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'learning/login.html')
    else:
        course_results = Course.objects.all()
        return render(request, 'learning/index.html',{'courses':course_results})



def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'learning/login.html', context)



def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                course_results = Course.objects.all()
                return render(request, 'learning/index.html',{'courses':course_results})
            else:
                return render(request, 'learning/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'learning/login.html', {'error_message': 'Invalid login'})
    return render(request, 'learning/login.html')



def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #albums = Album.objects.filter(user=request.user)
                return render(request, 'learning/index.html')
    context = {
        "form": form,
    }
    return render(request, 'learning/register.html', context)


def detail(request,course_id):
    if not request.user.is_authenticated():
        return render(request, 'learning/login.html')
    else:
        user = request.user
        course = get_object_or_404(Course,pk = course_id)
        return render(request, 'learning/detail.html', {'course': course})


def index_page(request):
    if not request.user.is_authenticated():
        return render(request, 'learning/login.html')
    else:
        course_results = Course.objects.all()
        return render(request, 'learning/index.html',{'courses':course_results})





def content_display(request,course_id,course_content_id):
    if not request.user.is_authenticated():
        return render(request, 'learning/login.html')
    else:
        user = request.user
        course = get_object_or_404(Course,pk = course_id)
        course_content = get_object_or_404(Course_Content,pk = course_content_id)
        return render(request, 'learning/content_display.html', {'course': course,'course_content':course_content})

def currentStartQuizId(quiz_id_numeric):
    totalNum = 0
    #quiz 1 has 2 questions
    if quiz_id_numeric == 1:
        return 0

    #quiz 2 has 6 questions
    if quiz_id_numeric == 2:
        return 2

    #quiz 3 has 3 questions
    if quiz_id_numeric == 3:
        return 8

    #quiz 4 has 4 questions
    if quiz_id_numeric == 4:
        return 8

    #quis 5 has 5 questions:
    if quiz_id_numeric == 5:
        return 11

     #quis 5 has 5 questions:
    if quiz_id_numeric == 6:
        return 15

    else:
        for i in xrange(1,quiz_id_numeric):
            x = str(quiz_id_numeric)
            quiz = get_object_or_404(Quiz,pk = x)
            totalNum = totalNum + int(quiz.numOfQuestions)
        return totalNum



def start_quiz(request,course_id,course_content_id,quiz_id):
    if not request.user.is_authenticated():
        return render(request, 'learning/login.html')
    else:
        course = get_object_or_404(Course,pk = course_id)
        course_content = get_object_or_404(Course_Content,pk = course_content_id)
        quiz = get_object_or_404(Quiz,pk = quiz_id)
        noOfQuestions = quiz.numOfQuestions
        quiz_id_numeric = int(quiz_id)
        #to find the current quiz id
        quiz_id_numeric1 = currentStartQuizId(quiz_id_numeric)
        quiz_id_numeric1 = quiz_id_numeric1+1
        question1 = Question1.objects.get(id = quiz_id_numeric1)

        val1 = course_id+'_'+quiz_id
        #This is done to save current performance of user in course
        a = CoursePerformance(course = course,quiz_attempted = val1, quiz_question_wrong = val1,quiz_question_hintTaken = val1)
        a.save()

        user = request.user
        b = Quiz_Performance(user = user,quiz_no = quiz_id,noOfQuestionsCorrect = 0,noOfQuestionsAttempted = 0,
                             numOfQuestions = noOfQuestions)
        b.save()

        return render(request, 'learning/start_quiz.html',{'course': course,'course_content':course_content,'quiz':quiz,
                                                           'question1':question1,'quiz_id_numeric1':quiz_id_numeric1})



def start_quiz1(request,course_id,course_content_id,quiz_id,question1_id):
    if not request.user.is_authenticated():
        return render(request, 'learning/login.html')
    else:
        course = get_object_or_404(Course,pk = course_id)
        course_content = get_object_or_404(Course_Content,pk = course_content_id)
        quiz = get_object_or_404(Quiz,pk = quiz_id)
        prevQuestion1 = get_object_or_404(Question1,id = question1_id)
        user = request.user
        quiz_id_numeric = int(quiz_id)
        #offset_val calculate the value of correct question id
        offset_val = currentStartQuizId(quiz_id_numeric)


        numOfQuestions = quiz.numOfQuestions

        if request.method=='POST' and 'submitBtn' in request.POST:
            try:
                selectedChoice = request.POST['choice']
                expectedAnswer = prevQuestion1.question_right_answer

                if(expectedAnswer == selectedChoice):

                    quiz_performance1 = get_object_or_404(Quiz_Performance,pk = quiz_id)

                    tempQuestionCorrect = quiz_performance1.noOfQuestionsCorrect
                    quiz_performance1.noOfQuestionsCorrect = int(tempQuestionCorrect) +1
                    #quiz_performance1.save()

                    tempQuestionAttempt = quiz_performance1.noOfQuestionsAttempted
                    quiz_performance1.noOfQuestionsAttempted = int(tempQuestionAttempt) + 1

                    quiz_performance1.save()
                    return render(request, 'learning/start_quiz1.html',{'course': course,'course_content':course_content,'quiz':quiz,
                                                           'question1':prevQuestion1 ,'boolVal': True})
                else:
                     #wrong answer
                     val1 = course_id+'_'+quiz_id
                     course_p1 = get_object_or_404(CoursePerformance,pk = val1)
                     prevValWrong = course_p1.quiz_question_wrong
                     prevValHint = course_p1.quiz_question_hintTaken
                     prevValWrong = prevValWrong+'_'+ question1_id

                     course_p1.quiz_question_wrong = prevValWrong
                     course_p1.quiz_question_hintTaken = prevValHint
                     course_p1.save()

                     quiz_performance1 = get_object_or_404(Quiz_Performance,pk = quiz_id)
                     tempQuestionAttempt = quiz_performance1.noOfQuestionsAttempted
                     quiz_performance1.noOfQuestionsAttempted = int(tempQuestionAttempt) + 1
                     quiz_performance1.save()

                     return render(request, 'learning/start_quiz1.html',{'course': course,'course_content':course_content,'quiz':quiz,
                                                           'question1':prevQuestion1 ,'boolVal1':True })

            except:
                return render(request, 'learning/start_quiz1.html',{'course': course,'course_content':course_content,'quiz':quiz,

                                                          'question1':prevQuestion1,'error_message': "You didn't select a choice."})





        if request.method=='POST' and 'nextBtn' in request.POST:
              val = int(question1_id)+1

              if(val <= int(quiz.numOfQuestions) + offset_val):
                  question1 =get_object_or_404(Question1,id = val)
                  return render(request, 'learning/start_quiz1.html',{'course': course,'course_content':course_content,'quiz':quiz,
                                                           'question1':question1 })
              else:


                  (h_List1,q_List1) = feedback_quiz(request,course_id,course_content_id,quiz_id)

                  quiz_performance1 = get_object_or_404(Quiz_Performance,pk = quiz_id)
                  noOfQuestionsCorrect = quiz_performance1.noOfQuestionsCorrect
                  numOfQuestions = quiz_performance1.numOfQuestions
                  noOfQuestionsAttempted = quiz_performance1.noOfQuestionsAttempted

                  noOfWrongAttempts = int(noOfQuestionsAttempted) - int(noOfQuestionsCorrect)

                  boolZeroCorrect = False
                  if noOfQuestionsCorrect == 0:
                      boolZeroCorrect = True

                  QuizPerformanceHistory1 = get_object_or_404(QuizPerformanceHistory,pk = quiz_id)
                  prevValAttempt = QuizPerformanceHistory1.noOfQuestionsAttempted
                  prevValAttempt = prevValAttempt + '_'+ noOfQuestionsAttempted

                  preValCorrect = QuizPerformanceHistory1.noOfQuestionsCorrect
                  preValCorrect = preValCorrect + '_' + noOfQuestionsCorrect

                  prevValWrong = QuizPerformanceHistory1.numOfQuestionsWrong

                  hintQuest = QuizPerformanceHistory1.quiz_question_hintTaken
                  hintQuest = hintQuest + str(h_List1)

                  wrongList = QuizPerformanceHistory1.quiz_question_wrongNo
                  wrongList = wrongList +'_'+ str(q_List1)



                  a = QuizPerformanceHistory(user = user,quiz_no = quiz_id, noOfQuestionsCorrect = preValCorrect,
                                             noOfQuestionsAttempted = prevValAttempt,numOfQuestionsWrong = prevValWrong,
                                             quiz_question_hintTaken = hintQuest,quiz_question_wrongNo = wrongList)
                  a.save()

                  return render(request, 'learning/feedback.html', {'course': course, 'hint_list': h_List1,'alt_qList':q_List1,
                                                                  'noOfQuestionsAttempted': noOfQuestionsAttempted ,'noOfQuestionsCorrect':noOfQuestionsCorrect,
                                                                  'numOfQuestions':numOfQuestions, 'boolZeroCorrect':boolZeroCorrect,'noOfWrongAttempts': noOfWrongAttempts,
                                                                     'showFeedback': True ,'course_content_id' :course_content_id,'course_content':course_content,'quiz':quiz
                                                                  })



        if request.method=='POST' and 'hintBtn' in request.POST:
              val2 = course_id+'_'+quiz_id
              course_p2 = get_object_or_404(CoursePerformance,pk = val2)
              prevValHint = course_p2.quiz_question_hintTaken
              prevValHint = prevValHint+'_'+ question1_id
              prevValWrong = course_p2.quiz_question_wrong


              course_p2.quiz_question_hintTaken = prevValHint
              course_p2.quiz_question_wrong = prevValWrong
              course_p2.save()

              return render(request, 'learning/start_quiz1.html',{'course': course,'course_content':course_content,'quiz':quiz,
                                                           'question1':prevQuestion1,'hint_message': "Hint message",})



def feedback_quiz(request,course_id,course_content_id,quiz_id):
    if not request.user.is_authenticated():
        return render(request, 'learning/login.html')
    else:
         course = get_object_or_404(Course,pk = course_id)
         course_content = get_object_or_404(Course_Content,pk = course_content_id)
         val1 = course_id+'_'+quiz_id
         course_p1 = get_object_or_404(CoursePerformance,pk = val1)
         question_wrong = course_p1.quiz_question_wrong
         q_List = question_wrong.split("_")
         q_List1 = []
         if len(q_List) > 2:
             q_List1 = q_List[2:]
             q_List1 = [x.encode('ascii') for x in q_List1]

         hint_tak = course_p1.quiz_question_hintTaken
         hint_List = hint_tak.split("_")
         h_List1 = []
         if len(hint_List) > 2:
             h_List1 = hint_List[2:]
             h_List1 = [x.encode('ascii') for x in h_List1]

         return (h_List1,q_List1)


         #return render(request, 'learning/feedback_quiz_ind.html',{'course': course,'course_content':course_content,
                                                                   #'quiz_id':quiz_id, 'hint_list': h_List1,
                                                               #'alt_qList':q_List1,})

def findfirstIndex(strVal):
    position = 0
    for i in xrange(0,len(strVal)):
        if strVal[i] == ',':
            position = i
            break
    return position

def findfirstNo(strVal):
    str1 = ''
    for i in xrange(0,len(strVal)):
        if strVal[i] == ',':
            break
        else:
            str1 = str1 +strVal[i]
    return int(str1)

#This function is written for writing alternate quiz
def alternate_quiz(request,course_id,quiz_id,course_content_id):
    if not request.user.is_authenticated():
        return render(request, 'learning/login.html')

    if request.method=='POST' and 'Next' in request.POST:
        course = get_object_or_404(Course,pk = course_id)
        course_content = get_object_or_404(Course_Content,pk = course_content_id)
        quiz = get_object_or_404(Quiz,pk = quiz_id)
        numQuestions = quiz.questions_alternate_size
        numQuestions = numQuestions - 1
        quiz.questions_alternate_size = numQuestions
        quiz.save()
        if(numQuestions <= 0):
            return render(request, 'learning/endAlternateQuiz.html', {'course': course})


        if(numQuestions == 1):
            alternateQuestionNo = quiz.questions_alternate_string[-1]
            alternateQuestionNo = alternateQuestionNo.encode('ascii')
            alternateQuestion1 = get_object_or_404(Question1,pk = alternateQuestionNo)
            return render(request, 'learning/feedback_quiz_ind.html',{'course': course,'course_content':course_content,
                                                                  'quiz':quiz,'firstQuizObj': alternateQuestion1},)

        else:
            alternateQuestionNo = quiz.questions_alternate_string
            alternateQuestionNo = str(alternateQuestionNo)
            firstCommaIndex = findfirstIndex(alternateQuestionNo)
            alternateQuestionNo = alternateQuestionNo[firstCommaIndex+1 :]

            quiz.questions_alternate_string = alternateQuestionNo

            #alternateQuestionNo = alternateQuestionNo[0].encode('ascii')
            alternateQuestionNo = findfirstNo(alternateQuestionNo)
            quiz.save()
            alternateQuestion1 = get_object_or_404(Question1,pk = alternateQuestionNo)
            return render(request, 'learning/feedback_quiz_ind.html',{'course': course,'course_content':course_content,
                                                                  'quiz':quiz,'firstQuizObj': alternateQuestion1},)


        return render(request, 'learning/detail.html', {'course': course})

    else:
         #course = get_object_or_404(Course,pk = course_id)
        course = get_object_or_404(Course,pk = course_id)
        course_content = get_object_or_404(Course_Content,pk = course_content_id)
        quiz = get_object_or_404(Quiz,pk = quiz_id)
        numQuestions = quiz.questions_alternate_size
        (h_List1,q_List1) = feedback_quiz(request,course_id,course_content_id,quiz_id)
        dictQuestion= {}
        for i in xrange(0,len(q_List1)):
            dictQuestion[q_List1[i]]= q_List1[i]
        for j in xrange(0,len(h_List1)):
             dictQuestion[h_List1[j]]= h_List1[j]

        dictLen = len(dictQuestion)
        questionObjList = []
        finalAltQuestionString = ''
        for k in dictQuestion.values():
            alternateQuestion1 = get_object_or_404(Question1,pk = k)
            questionObjList.append(alternateQuestion1)
            finalAltQuestionString = finalAltQuestionString + k
            finalAltQuestionString = finalAltQuestionString +','

        finalAltQuestionString = finalAltQuestionString[0 : len(finalAltQuestionString) -1]

        quiz.questions_alternate_size = len(questionObjList)
        quiz.questions_alternate_string = finalAltQuestionString
        quiz.save()

        firstQuizObj = questionObjList[0]

        return render(request, 'learning/feedback_quiz_ind.html',{'course': course,'course_content':course_content,
                                                                  'quiz':quiz,'questionObjList':questionObjList,
                                                                   'finalAltQuestionString':finalAltQuestionString,
                                                                    'firstQuizObj': firstQuizObj},)













