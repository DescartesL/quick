import json

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# 爬虫部分，将爬虫爬到的数据放到数据库中
import requests
import pymongo
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
@csrf_exempt
def get_one_information(request):
    response = {}
    res = requests.get('http://wufazhuce.com/')
    soup = BeautifulSoup(res.text, 'lxml')
    client = pymongo.MongoClient("mongodb://admin:123456@60.205.188.9:27017/")
    db = client['one']
    for item in soup.select(".item"):
        data = {}
        data['url'] = item.select("a img")[0].attrs['src']
        data['date'] = item.select(".fp-one-titulo-pubdate .dom")[0].string + " " + \
                       item.select(".fp-one-titulo-pubdate .may")[0].string
        data['day'] = item.select(".fp-one-titulo-pubdate .dom")[0].string
        data['month'] = item.select(".fp-one-titulo-pubdate .may")[0].string.split(' ')[0]
        data['year'] = item.select(".fp-one-titulo-pubdate .may")[0].string.split(' ')[1]
        data['content'] = item.select(".fp-one-cita a")[0].string
        db['one'].update_one(data, {'$setOnInsert': data}, upsert=True)

    client.close()
    response['code'] = 200
    response['msg'] = 'success'
    return HttpResponse(json.dumps(response))


@require_http_methods(['GET'])
@csrf_exempt
def get_one(request):
    response = {}
    client = pymongo.MongoClient("mongodb://admin:123456@60.205.188.9:27017/")
    db = client['one']
    data = []
    for item in db['one'].find():
        item['_id'] = str(item['_id'])
        data.append(item)

    response['code'] = 200
    response['msg'] = 'success'
    response['data'] = data
    return HttpResponse(json.dumps(response))


@require_http_methods(['GET'])
@csrf_exempt
def get_random_poem(request):
    response = {}
    res = requests.get("https://v1.jinrishici.com/all.json")
    data = res.json()
    data['category'] = data['category'].split('-')
    response['code'] = 200
    response['msg'] = 'success'
    response['data'] = data

    return HttpResponse(json.dumps(response))