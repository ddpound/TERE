from django.views import View  
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse  
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Board, BoardCategory, BoardCon
from .forms import BoardForm, SearchForm, signup_stForm, signup_pfForm, loginForm, changeForm, FileForm
from .models import MyUser
from datetime import datetime
from django.db.models import Count
import os
from django.conf import settings

class main(View):
    def get(self, request, *args, **kwargs):
        if not request.session.get('login', False):
            return render(request, 'main.html')
        else:
            return render(request, 'main.html',{'Name': request.session.get('user_name')})

class login(View):
    def get(self, request, *args, **kwargs):
        request.session['login'] = False
        lform = loginForm()
        return render(request, 'login.html',{'form':lform})

    def post(self, request, *args, **kwargs):
        lform = loginForm(request.POST)
        if lform.is_valid():
            ID = lform.cleaned_data['ID']
            PW = lform.cleaned_data['PassWords']
            if MyUser.objects.filter(ID=ID, PassWords=PW):
                data = MyUser.objects.get(ID=ID)
                request.session['session_id'] = ID
                request.session['user_name'] = data.Name
                request.session['login'] = True
                return HttpResponseRedirect(reverse('community:main'))
            else:
                lform = loginForm()
                request.session['login'] = False
                return render(request, 'login.html',{'form':lform,'fail':"아이디 또는 패스워드가 잘못 되었습니다."})
        else:
            lform = loginForm()
            request.session['login'] = False
            return render(request, 'login.html',{'form':lform,'fail':"아이디 또는 패스워드가 잘못 되었습니다."})

class logout(View):
    def get(self, request, *args, **kwargs):
        if not request.session.get('login', False):
            raise PermissionDenied
        else:
            request.session['login'] = False
            return HttpResponseRedirect(reverse('community:main'))

class signup_select(TemplateView):
    template_name= 'signup_select.html'

class signup_pf(View):
    def get(self, request, *args, **kwargs):
        sform = signup_pfForm()
        return render(request, 'signup_pf.html',{'form':sform})

    def post(self, request, *args, **kwargs):
        sform=signup_pfForm(request.POST)
        if sform.is_valid():
            cleaned_ID = sform.cleaned_data['ID']
            data = MyUser.objects.filter(ID=cleaned_ID)
            flag = False
            for ID in data:
                if ID.ID == cleaned_ID:
                    flag = True          
            if flag:
                sform = signup_stForm()
                return render(request, 'signup_pf.html',{'form':sform,'fail':"이미 사용중인 아이디 입니다."})
            else:
                cleaned_PassWords = sform.cleaned_data['PassWords']
                cleaned_Name = sform.cleaned_data['Name']
                cleaned_SN = sform.cleaned_data['SN']
                MyUser.objects.create(ID=cleaned_ID,PassWords=cleaned_PassWords,Identifier='교수',Grade='교수',Name = cleaned_Name,SN=cleaned_SN)
                return HttpResponseRedirect(reverse('community:main'))
        else:
            sform = signup_pfForm()
            return render(request, 'signup_pf.html',{'form':sform,'fail':"입력 잘못 됨"})

class signup_st(View):
    def get(self, request, *args, **kwargs):
        sform = signup_stForm()
        return render(request, 'signup_st.html',{'form':sform})

    def post(self, request, *args, **kwargs):
        sform=signup_stForm(request.POST)
        if sform.is_valid():
            cleaned_ID = sform.cleaned_data['ID']
            data = MyUser.objects.filter(ID=cleaned_ID)
            flag = False
            for ID in data:
                if ID.ID == cleaned_ID:
                    flag = True          
            if flag:
                sform = signup_stForm()
                return render(request, 'signup_st.html',{'form':sform,'fail':"이미 사용중인 아이디 입니다."})
            else:
                cleaned_PassWords = sform.cleaned_data['PassWords']
                cleaned_Name = sform.cleaned_data['Name']
                cleaned_Grade = sform.cleaned_data['Grade']
                cleaned_SN = sform.cleaned_data['SN']
                MyUser.objects.create(ID=cleaned_ID,PassWords=cleaned_PassWords,Identifier='학생', Grade = cleaned_Grade, Name = cleaned_Name,SN=cleaned_SN)
                return HttpResponseRedirect(reverse('community:main'))
        else:
            sform = signup_stForm()
            return render(request, 'signup_st.html',{'form':sform,'fail':"입력 잘못 됨"})

class change(View):
    def get(self, request, *args, **kwargs):
        cform = changeForm()
        if not request.session.get('login', False):
            raise PermissionDenied
        return render(request, 'change.html',{'form':cform})

    def post(self, request, *args, **kwargs):
        cform = changeForm(request.POST)
        ID = request.session.get('session_id')
        if cform.is_valid():
            pre_PW = cform.cleaned_data['PassWords_pre']
            PW = cform.cleaned_data['PassWords']
            temp_data = MyUser.objects.get(ID=ID)
            if(temp_data.PassWords==pre_PW):
                if(pre_PW == PW):
                    cform = changeForm()
                    return render(request, 'change.html',{'form':cform,'fail':"바꿀 비밀번호와 현재 비밀번호가 같습니다."})
                else:
                    temp_data.PassWords=PW
                    temp_data.save()
                return HttpResponseRedirect(reverse('community:change_success'))
            else:
                cform = changeForm()
                return render(request, 'change.html',{'form':cform,'fail':"현재 비밀번호가 다릅니다."})
        else:
            cform = changeForm()
            return render(request, 'change.html',{'form':cform,'fail':"입력이 잘못 되었습니다."})

class change_success(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'change_success.html', {'Name': request.session.get('user_name'),'ID':request.session.get('session_id')})

class IndexView(View):
    def get(self, request, *args, **kwargs):
        if not request.session.get('login', False):
            raise PermissionDenied
        data = Board.objects.all()
        return render(request, 'index.html',{'object_list':data})

class BoardCa(View):
    def get(self, request, identifier):
        if not request.session.get('login', False):
            raise PermissionDenied
        data = BoardCategory.objects.filter(refer=identifier)
        t_identifier = identifier
        return render(request, 'BoardCa.html',{'object_list':data,'t_identifier':t_identifier})
   
class BoardCons(View):
    def get(self, request, identifier, identifier2):
        if not request.session.get('login', False):
            raise PermissionDenied
        board_data = BoardCategory.objects.get(identifier=identifier2)
        user_data = MyUser.objects.get(ID=request.session.get('session_id'))
        if user_data.Identifier == "학생":
            pf_ID = str(user_data.tutor)[:str(user_data.tutor).find('/')]
            if board_data.c_name == user_data.Grade:
                sform = SearchForm()
                data = BoardCon.objects.filter(refer=identifier2)
                first_identifier = identifier
                second_identifier = identifier2
                return render(request, 'BoardCon.html',{'object_list':data,'sform':sform, 'first_identifier':first_identifier,'second_identifier':second_identifier})
            elif board_data.c_name == pf_ID:
                sform = SearchForm()
                data = BoardCon.objects.filter(refer=identifier2)
                first_identifier = identifier
                second_identifier = identifier2
                return render(request, 'BoardCon.html',{'object_list':data,'sform':sform, 'first_identifier':first_identifier,'second_identifier':second_identifier})
            elif board_data.c_name == "개설요청":
                sform = SearchForm()
                data = BoardCon.objects.filter(refer=identifier2)
                first_identifier = identifier
                second_identifier = identifier2
                return render(request, 'BoardCon.html',{'object_list':data,'sform':sform, 'first_identifier':first_identifier,'second_identifier':second_identifier})
            else:
                raise PermissionDenied
        elif user_data.Identifier == "교수":
            board_data = Board.objects.get(identifier=identifier)
            category_data = BoardCategory.objects.get(identifier=identifier2)
            if board_data.b_purpose == "지도교수":
                print(user_data.Name)
                if category_data.c_name == user_data.Name:
                    sform = SearchForm()
                    data = BoardCon.objects.filter(refer=identifier2)
                    first_identifier = identifier
                    second_identifier = identifier2
                    return render(request, 'BoardCon.html',{'object_list':data,'sform':sform, 'first_identifier':first_identifier,'second_identifier':second_identifier})
                else:
                    raise PermissionDenied
            else:
                sform = SearchForm()
                data = BoardCon.objects.filter(refer=identifier2)
                first_identifier = identifier
                second_identifier = identifier2
                return render(request, 'BoardCon.html',{'object_list':data,'sform':sform, 'first_identifier':first_identifier,'second_identifier':second_identifier})
        else:
            sform = SearchForm()
            data = BoardCon.objects.filter(refer=identifier2)
            first_identifier = identifier
            second_identifier = identifier2
            return render(request, 'BoardCon.html',{'object_list':data,'sform':sform, 'first_identifier':first_identifier,'second_identifier':second_identifier})

    def post(self, request, identifier, identifier2):
        if not request.session.get('login', False):
            raise PermissionDenied
        sform = SearchForm(request.POST)
        if sform.is_valid():
            first_identifier = identifier
            second_identifier = identifier2
            select = sform.cleaned_data['select']
            s_content = sform.cleaned_data['s_content']
            if(select == "게시글 번호"):
                data = BoardCon.objects.filter(refer=identifier2, identifier__contains=s_content)
            elif(select == "게시글 제목"):
                data = BoardCon.objects.filter(refer=identifier2, m_title__contains=s_content)
            elif(select == "게시글 작성자"):
                data = BoardCon.objects.filter(refer=identifier2, m_WriterName__contains=s_content)
            return render(request, 'BoardCon.html',{'object_list':data,'sform':sform, 'first_identifier':first_identifier,'second_identifier':second_identifier})
        else:
            first_identifier = identifier
            second_identifier = identifier2
            sform = SearchForm()
            data = BoardCon.objects.filter(refer=identifier2)
            return render(request, 'BoardCon.html',{'object_list':data,'sform':sform, 'first_identifier':first_identifier,'second_identifier':second_identifier})

class BoardMessage(View):
    def get(self, request, identifier, identifier2, identifier3):
        if not request.session.get('login', False):
            raise PermissionDenied
        data = BoardCon.objects.filter(identifier=identifier3)
        first_identifier = identifier
        second_identifier = identifier2
        return render(request, 'BoardMessage.html',{'object_list':data, 'first_identifier':first_identifier,'second_identifier':second_identifier})
    def post(self, request, identifier, identifier2, identifier3):
        if not request.session.get('login', False):
            raise PermissionDenied
        data = BoardCon.objects.filter(identifier=identifier3)
        for item in data:
            print(item.file_path)
            if os.path.isfile(os.path.join(settings.MEDIA_ROOT, str(item.file_path))):
                os.remove(os.path.join(settings.MEDIA_ROOT, str(item.file_path)))
        first_identifier = identifier
        second_identifier = identifier2
        data.delete()
        return HttpResponseRedirect(reverse('community:board_con',args=[identifier,identifier2]))

class PostWrite(FormView):
    def get(self, request, identifier, identifier2):
        if not request.session.get('login', False):
            raise PermissionDenied
        bform = BoardForm()
        fform = FileForm()
        first_identifier = identifier
        second_identifier = identifier2
        return render(request, 'postwrite.html',{'form':bform,'fform':fform,'first_identifier':first_identifier,'second_identifier':second_identifier})

    def post(self, request, identifier, identifier2):
        ID = MyUser.objects.get(ID=request.session.get('session_id'))    
        Name = request.session.get('user_name')
        refer = BoardCategory.objects.get(identifier=identifier2)
        bform = BoardForm(request.POST)
        fform = FileForm(request.POST, request.FILES)
        
        if bform.is_valid() and fform.is_valid():
            cleaned_title = bform.cleaned_data['m_title']
            cleaned_content = bform.cleaned_data['m_content']
            BoardCon.objects.create(m_title=cleaned_title, m_content=cleaned_content, m_WriterID=ID, m_WriterName=Name,m_create_date=datetime.now().strftime('%Y-%m-%d %H:%M'), m_update_date=datetime.now(),refer=refer,file_path=request.FILES['file'],file_desc = request.POST['desc'])
        elif bform.is_valid() and not fform.is_valid():
            cleaned_title = bform.cleaned_data['m_title']
            cleaned_content = bform.cleaned_data['m_content']
            BoardCon.objects.create(m_title=cleaned_title, m_content=cleaned_content, m_WriterID=ID, m_WriterName=Name,m_create_date=datetime.now().strftime('%Y-%m-%d %H:%M'), m_update_date=datetime.now(),refer=refer)
        return HttpResponseRedirect(reverse('community:board_con',args=[identifier,identifier2]))

class PostModify(FormView):
    def get(self, request, identifier, identifier2, identifier3):
        if not request.session.get('login', False):
            raise PermissionDenied
        bform = BoardForm()
        fform = FileForm()
        first_identifier = identifier
        second_identifier = identifier2
        third_identifier = identifier3
        return render(request, 'postmodify.html',{'form':bform,'fform':fform,'first_identifier':first_identifier,'second_identifier':second_identifier, 'third_identifier':third_identifier})

    def post(self, request, identifier, identifier2, identifier3):
        if not request.session.get('login', False):
            raise PermissionDenied
        ID = MyUser.objects.get(ID=request.session.get('session_id'))
        Name = request.session.get('user_name')
        refer = BoardCategory.objects.get(identifier=identifier2)
        bform = BoardForm(request.POST)
        fform = FileForm(request.POST, request.FILES)
        print(fform.is_valid())
        if bform.is_valid() and fform.is_valid():
            cleaned_title = bform.cleaned_data['m_title']
            cleaned_content = bform.cleaned_data['m_content']
            post = BoardCon.objects.get(identifier=identifier3)
            post.m_title = cleaned_title
            post.m_content = cleaned_content
            post.m_update_date = datetime.now().strftime('%Y-%m-%d %H:%M')
            post.file_path = request.FILES['file']
            post.file_desc = request.POST['desc']
            post.save()
            #post.update(m_title=cleaned_title, m_content=cleaned_content, m_update_date=datetime.now().strftime('%Y-%m-%d %H:%M'),file_path=request.FILES['file'],file_desc = request.POST['desc'])
        elif bform.is_valid() and not fform.is_valid():
            cleaned_title = bform.cleaned_data['m_title']
            cleaned_content = bform.cleaned_data['m_content']
            post = BoardCon.objects.filter(identifier=identifier3)
            post.update(m_title=cleaned_title, m_content=cleaned_content, m_update_date=datetime.now().strftime('%Y-%m-%d %H:%M'))
        return HttpResponseRedirect(reverse('community:board_message',args=[identifier,identifier2,identifier3]))
        
            
            