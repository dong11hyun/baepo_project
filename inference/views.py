# baepo_project/inference/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from transformers import pipeline
import json

# ✨ 핵심 포인트: 모델은 웹서버가 시작될 때 딱 한 번만 불러오는 게 좋아!
# 사용자가 요청할 때마다 모델을 로딩하면 엄청나게 느려지거든.
# 이렇게 밖에 변수로 빼두면, 서버 실행 시 메모리에 한 번만 올라가서 효율적이야.
try:
    sentiment_classifier = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
except Exception as e:
    print(f"모델 로딩 중 오류 발생: {e}")
    sentiment_classifier = None

def analyze_sentiment(request):
    """기존 HTML 뷰 (웹 브라우저용)"""
    text_to_analyze = ""
    result = {}

    # 사용자가 form을 통해 문장을 입력하고 'POST' 방식으로 요청했을 때
    if request.method == "POST":
        text_to_analyze = request.POST.get('text_input', '')
        if text_to_analyze and sentiment_classifier:
            # 파이프라인 덕분에 코드가 아주 간단해져. 문장만 넣어주면 돼!
            result_list = sentiment_classifier(text_to_analyze)
            # 결과는 [{'label': 'positive', 'score': 0.99...}] 이런 식의 리스트로 나와.
            # 우리는 첫 번째 결과만 쓸 거니까 [0]을 사용했어.
            result = result_list[0]

    # HTML 파일에 전달할 데이터들을 context 딕셔너리에 담아.
    context = {
        'text': text_to_analyze,
        'result': result,
    }
    return render(request, 'inference/index.html', context)


@api_view(['POST'])
def analyze_sentiment_api(request):
    """프론트엔드를 위한 API 엔드포인트"""
    try:
        # POST 요청에서 텍스트 추출
        text_input = request.data.get('text', '')
        
        if not text_input:
            return Response({
                'error': '텍스트를 입력해주세요.'
            }, status=400)
        
        if not sentiment_classifier:
            return Response({
                'error': '모델이 로딩되지 않았습니다.'
            }, status=500)
        
        # 감성 분석 실행
        result_list = sentiment_classifier(text_input)
        result = result_list[0]
        
        # 라벨을 한국어로 변환
        label_map = {
            '5 stars': '매우 긍정적',
            '4 stars': '긍정적', 
            '3 stars': '중립적',
            '2 stars': '부정적',
            '1 star': '매우 부정적',
            'POSITIVE': '긍정적',
            'NEGATIVE': '부정적'
        }
        
        korean_label = label_map.get(result['label'], result['label'])
        
        return Response({
            'success': True,
            'text': text_input,
            'result': {
                'label': result['label'],
                'korean_label': korean_label,
                'score': round(result['score'], 4),
                'confidence_percent': round(result['score'] * 100, 2)
            }
        })
        
    except Exception as e:
        return Response({
            'error': f'분석 중 오류가 발생했습니다: {str(e)}'
        }, status=500)
