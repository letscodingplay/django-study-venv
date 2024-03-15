from django import forms

class LicenseForm(forms.Form):
    student_name = forms.CharField(label="학생이름", max_length=100)
    score = forms.IntegerField(label="성적")
    student_birth = forms.CharField(label="생년월일", max_length = 8)
    # student_id = forms.CharField(label="주민등록번호 뒷자리", max_length = 7)