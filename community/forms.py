from django import forms

class signup_pfForm(forms.Form):
    ID = forms.EmailField(label= "아이디",empty_value="example@naver.com")
    PassWords = forms.CharField(label= "비밀번호",widget=forms.PasswordInput,max_length=20,empty_value="")
    SN = forms.CharField(label= "사번",max_length=20,empty_value="")
    Name = forms.CharField(label= "이름",max_length=20,empty_value="")

class signup_stForm(forms.Form):
    ID = forms.EmailField(label= "아이디",empty_value="example@naver.com")
    PassWords = forms.CharField(label= "비밀번호",widget=forms.PasswordInput,max_length=20,empty_value="")
    Name = forms.CharField(label= "이름",max_length=20,empty_value="")
    SN = forms.CharField(label= "학번",max_length=20,empty_value="")
    grade_choice = (("1학년","1학년"),("2학년","2학년"),("3학년","3학년"),("4학년","4학년"))
    Grade = forms.ChoiceField(label= "학년",widget=forms.Select, choices=grade_choice)

class loginForm(forms.Form):
    ID = forms.CharField(label= "아이디",max_length=20)
    PassWords = forms.CharField(label= "비밀번호",widget=forms.PasswordInput,max_length=20)

class changeForm(forms.Form):
    PassWords_pre = forms.CharField(label= "현재 비밀번호",widget=forms.PasswordInput,max_length=20)
    PassWords = forms.CharField(label= "바꿀 비밀번호",widget=forms.PasswordInput,max_length=20)

class BoardForm(forms.Form):
    m_title = forms.CharField(label= "게시글 제목",max_length=200)
    m_content = forms.CharField(label= "게시글 내용",widget=forms.Textarea)

class FileForm(forms.Form):
    desc = forms.CharField(label="설명", max_length=50)
    file = forms.FileField(label="파일" )

class SearchForm(forms.Form):
    Type_choice = (("게시글 번호","게시글 번호"),("게시글 제목","게시글 제목"),("게시글 작성자","게시글 작성자"))
    select = forms.ChoiceField(widget=forms.Select, choices=Type_choice)
    s_content = forms.CharField(max_length=200)
