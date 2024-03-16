from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView, ListView
from django.http import HttpResponse
from buddy.models import License
from buddy.forms import LicenseForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages

class Index(View):
    
    template_name = 'index.html'

    def get(self, request):
        licences = License.objects.all().order_by('student_name')
        context={'students':licences}
        return render(request, self.template_name, context)
    
class ShowAll(ListView):
    model = License
    template_name = 'license/list.html'
    ordering = 'student_name'
    context_object_name = 'licenses'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        #return License.objects.order_by('student_name')
        return context
    
class Insert(View):
    form_class = LicenseForm
    model = License
    template_name = 'license/insert.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name,
                      context={
                          'form':form,
                          'message':'',
                          'next':request.GET.get('next')
                      })
    def post(self, request):
        print("insert post")
        form = self.form_class(request.POST)
        
        if form.is_valid():
            cleaned_data = form.clean()
            name = cleaned_data.get("student_name")
            print(f"name:{name}")
            score = cleaned_data.get("score")
            birth = cleaned_data.get("student_birth")
            license = License(student_name=name, score=score, student_birth=birth)
            license.save()
            
        return HttpResponseRedirect(reverse_lazy('buddy:index'))
class AskBirth(View):
    template_name='license/ask_birth.html'
    
    def get(self, request):
        param = request.GET.get('id', '')
        student = License.objects.get(pk=param)
        context={'student':student}
        return render(request, self.template_name, context)
    
    def post(self, request):
        id = request.POST.get('id',-1)
        birth = request.POST.get('birth', '')
        student_id = request.POST.get('student_id', '')
        student = License.objects.get(pk=id)
        
        if len(birth) == 0 or len(student_id) == 0 or birth.isdecimal() == False or student_id.isdecimal() == False:
            messages.error(self.request, '다시 확인해 주세요.', extra_tags='danger')
            context={'message':messages, 'student': student}
            return render(request, self.template_name, context)
        else:
            #print(f"id:{id}/birth:{birth}/student_id:{student_id}")
            
            isValid = self.valid(birth, student_id)
            #print(f"isValid:{isValid}")
            #print(f"student.student_birth:{student.student_birth}")
            
            result = (student.student_birth == birth) and isValid
            
            if result == False:
                #print("올바르게 입력하지 않음")
                
                messages.error(self.request, '다시 확인해 주세요.', extra_tags='danger')
                context={'message':messages, 'student': student}
                return render(request, self.template_name, context)
            else :
                student.student_id = student_id
                student.save()
                return HttpResponseRedirect(reverse_lazy('buddy:show', args=(str(id),)))
    def valid(self, birth, std_id):
        codes = birth + std_id
        nums = [2,3,4,5,6,7,8,9]
        sum = 0
        for i in range(len(codes)-1):
            sum += int(codes[i]) * (nums[i % len(nums)])
        validCode = sum % 11
        #print(f"validCode:{validCode}")
        
        validCode = 11 - validCode
        if validCode >= 10:
            validCode = validCode % 10

        return validCode == int(codes[-1])
        
class ShowScore(DetailView):
    model = License
    template_name = 'license/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(License, pk = self.kwargs['pk'])
        if student.score >= 400 :
            student.grade = 'A'
        elif student.score >= 300 :
            student.grade = 'B'
        elif student.score >= 200 :
            student.grade = 'C'
        context['student']= student
        return context
    
    
    
class ShowMonth(View):
    template_name = 'show_month.html'
    
    def get(self, request):
        param = request.GET.get('month', '')
        print('param:', param)
        days = [i for i in range(1, 30)]
        context={
            'm' : param,
            'day_list' : days
        }
        return render(request, self.template_name, context)
    

class ShowDay(View):
    template_name = 'show_day.html'
    
    def get(self, request):
        param1 = request.GET.get('month', '')
        param2 = request.GET.get('day', '')
        
        morning = ['밥', '미역국', '김치', '어묵', '고등어']
        lunch = ['떡국', '김치', '멸치볶음', '떡갈비']
        
        context = {
            'm':param1, 
            'd':param2, 
            'morning_food':morning, 
            'lunch_food':lunch, 
        }
        return render(request, self.template_name, context)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import urllib.parse
import urllib.request
import xml.etree.ElementTree as elemTree 
from .models import Books

@method_decorator(csrf_exempt, name='dispatch')
class getBarcodeData2(View):
    def get(self, requets):
        param = requets.GET.get('data')
        print('param:', param)
        secret_key = "758560af2a1e7991d010f8d51f172a49"
        api_url = f"https://www.nl.go.kr/NL/search/openApi/search.do?"
        api_url += f"key={secret_key}"
        api_url += "&detailSearch=true"
        api_url += "&isbnOp=isbn"
        api_url += f"&isbnCode={param}"
        
        print(api_url)
        
        req = urllib.request.Request(api_url)
        with urllib.request.urlopen(req) as response :
            the_page = response.read()
            string_data = the_page.decode('utf-8')
            root = elemTree.fromstring(string_data)
            result = root.find("result")
            item = result.find("item")
            
            title_info = item.find('title_info').text
            isbn_info = item.find('isbn').text
            print(f"title info: {title_info}")
            
            search_result = Books.objects.filter(isbn=isbn_info)
            if len(search_result) == 0:
                print("find result zero~!")
                book = Books(title = title_info, isbn = isbn_info)
                book.save()
                return HttpResponse(book.__str__(), status=200)
            else :
                return HttpResponse("hello", status=200)
            
        
        
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse

@method_decorator(csrf_exempt, name='dispatch')
class getBarcodeData(View):
    def get(self, requets):
        param = requets.GET.get('data')
        print('param:', param)
        xml = self.read_api(param)
        title = self.parse_xml(xml)
        
        return HttpResponse(f"isbn:{param}", status=200)
    
    def read_api(self, isbn):
        secret_key = "758560af2a1e7991d010f8d51f172a49"
        api_url = f"https://www.nl.go.kr/NL/search/openApi/search.do?"
        api_url += f"key={secret_key}"
        api_url += "&detailSearch=true"
        api_url += "&isbnOp=isbn"
        api_url += f"&isbnCode={isbn}"
        
        print(api_url)
        
        req = urllib.request.Request(api_url)
        with urllib.request.urlopen(req) as response :
            the_page = response.read()
            string_data = the_page.decode('utf-8')
            return string_data
    
    def parse_xml(self, xml):
        root = elemTree.fromstring(xml)
        result = root.find("result")
        item = result.find("item")
        
        title_info = item.find('title_info').text
        isbn_info = item.find('isbn').text
        print(f"title info: {title_info}")
        print(f"isbn info: {isbn_info}")
        
        return title_info
        