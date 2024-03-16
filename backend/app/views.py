from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from bs4 import BeautifulSoup as bs
import requests 
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.
def SingleWordMode(request):
  word = request.GET.get("word")
  url = 'https://redkiwiapp.com/ko/english-guide/words/'
  sentence_list = []
  korean_sentence_list =[]
  full_mean_list =[]
  req = requests.get(url+word)
  soup = bs(req.text, 'html.parser')
  # class 이름이 'jss58'인 span 태그 찾기
  means = soup.find_all('div', class_='jss58')
  ex_sentences = soup.find_all('p', class_='jss64')
  ex_sentences_korean = soup.find_all('p', class_='jss65')
  if(len(means)>0):
    means = [mean.text for mean in means]
    full_mean =', '.join(  means)
    if (len(ex_sentences) == len(ex_sentences_korean)):
      for i, sentence in enumerate(ex_sentences):
        sentence_list.append(sentence.text)
        korean_sentence_list.append(ex_sentences_korean[i].text)
        full_mean_list.append(full_mean)
  df = {'sentence' : sentence_list,
                "translation" : korean_sentence_list,
                "word_means": full_mean_list}

  return JsonResponse(df)
from io import StringIO
import xlsxwriter
def WriteToExcel(weather_data, town=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)

    # Here we will adding the code to add data

    workbook.close()
    xlsx_data = output.getvalue()
    # xlsx_data contains the Excel file
    return xlsx_data
@method_decorator(csrf_exempt)
def MultipleWordMode(request):
    url = 'https://redkiwiapp.com/ko/english-guide/words/'
    
    
    if request.method == 'POST' and 'file' in request.FILES:
        # 파일이 올바르게 전송된 경우
      uploaded_file = request.FILES['file']
      print(type(uploaded_file))
      if uploaded_file.name.endswith('.txt'):
          file_content = uploaded_file.read().decode('utf-8')
          print(file_content)
      else:
          return HttpResponse('File submission error: Only text files (.txt) are allowed.')
      print(file_content)
      words = file_content.split('\n')
      aa= []
      for word in words:
        req = requests.get(url+word)
        soup = bs(req.text, 'html.parser')
        means = soup.find_all('div', class_='jss58')
        ex_sentences = soup.find_all('p', class_='jss64')
        ex_sentences_korean = soup.find_all('p', class_='jss65')
        if(len(means)>0):
          means = [mean.text for mean in means]
          full_mean =', '.join(  means)
          if (len(ex_sentences) == len(ex_sentences_korean)):
            for i, sentence in enumerate(ex_sentences):
              aa.append({'sentence' : sentence.text,
                    "translation" : ex_sentences_korean[i].text,
                    "word_means": full_mean})
            print(aa)
            return JsonResponse(aa, safe=False)
    else: 
        print(1)
        # 파일이 제출되지 않은 경우 에러 메시지 반환
        return HttpResponse('Bad Request: Missing data', status=400)
    