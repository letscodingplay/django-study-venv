from django.shortcuts import render
from django.views.generic import View
class Index(View):
    template_name = 'index.html'
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        code = request.POST.get('code', '')
        # 입력된 코드를 파일로 저장
        with open('temp.py', 'w') as f:
            f.write(code)
        
        # 파이썬 파일 실행
        result = subprocess.run(['python', 'temp.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 결과 반환
        return render(request, 'compiler/home.html', {'code': code, 'result': result.stdout, 'error': result.stderr})