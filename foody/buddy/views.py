from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse


class Index(View):
    template_name = 'index.html'

    def get(self, request):
        monthList = [i for i in range(1, 13)]
        context = {"month": monthList}
        return render(request, self.template_name, 
                      context)
        
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
        