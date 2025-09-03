# 🚀 Django AI 감성분석 서비스 배포 가이드

## 📁 프로젝트 구조
```
baepo_project/
├── config/                 # Django 프로젝트 설정
│   ├── settings.py         # 메인 설정 파일
│   ├── urls.py            # URL 라우팅
│   └── wsgi.py            # WSGI 설정
├── inference/              # AI 추론 앱
│   ├── templates/         # HTML 템플릿
│   ├── views.py           # 뷰 로직 (HTML + API)
│   └── urls.py            # 앱 URL 설정
├── requirements.txt        # 패키지 의존성
├── manage.py              # Django 관리 명령어
└── venv/                  # 가상환경 (배포시 제외)
```

## 🌐 API 엔드포인트

### 1. HTML 인터페이스
- **URL**: `http://your-domain.com/`
- **Method**: GET/POST
- **설명**: 브라우저에서 직접 사용할 수 있는 웹 인터페이스

### 2. REST API
- **URL**: `http://your-domain.com/api/analyze/`
- **Method**: POST
- **Content-Type**: application/json

**요청 예시:**
```json
{
    "text": "이 영화 정말 감동적이고 재미있었어요!"
}
```

**응답 예시:**
```json
{
    "success": true,
    "text": "이 영화 정말 감동적이고 재미있었어요!",
    "result": {
        "label": "4 stars",
        "korean_label": "긍정적",
        "score": 0.8945,
        "confidence_percent": 89.45
    }
}
```

## 🚀 배포 옵션

### 1. 📦 Heroku 배포

1. **Heroku CLI 설치 및 로그인**
```bash
# Heroku CLI 설치 후
heroku login
```

2. **Procfile 생성**
```bash
echo "web: gunicorn config.wsgi" > Procfile
```

3. **gunicorn 설치**
```bash
pip install gunicorn
pip freeze > requirements.txt
```

4. **배포**
```bash
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
git push heroku main
```

### 2. ☁️ AWS EC2 배포

1. **EC2 인스턴스 생성 및 접속**

2. **서버 설정**
```bash
# Python, pip 설치
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# 프로젝트 클론
git clone your-repository
cd baepo_project

# 가상환경 설정
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 정적 파일 수집
python manage.py collectstatic

# Gunicorn으로 실행
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

3. **Nginx 설정**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. 🐳 Docker 배포

1. **Dockerfile 생성**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

2. **docker-compose.yml 생성**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
```

3. **실행**
```bash
docker-compose up -d
```

## 🎯 프론트엔드 연동 예시

### React.js 연동
```javascript
const analyzeSentiment = async (text) => {
  try {
    const response = await fetch('http://your-domain.com/api/analyze/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: text })
    });
    
    const data = await response.json();
    console.log(data.result);
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
};

// 사용 예시
analyzeSentiment("이 제품 정말 좋아요!")
  .then(result => {
    console.log(`감정: ${result.result.korean_label}`);
    console.log(`신뢰도: ${result.result.confidence_percent}%`);
  });
```

### Vue.js 연동
```javascript
// Vue 3 Composition API
import { ref } from 'vue'

export default {
  setup() {
    const result = ref(null)
    
    const analyzeSentiment = async (text) => {
      try {
        const response = await fetch('http://your-domain.com/api/analyze/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        })
        
        result.value = await response.json()
      } catch (error) {
        console.error('Error:', error)
      }
    }
    
    return { result, analyzeSentiment }
  }
}
```

## ⚙️ 운영 환경 최적화

### 1. 성능 개선
- **모델 캐싱**: 현재 구현됨 (서버 시작시 한번만 로딩)
- **Redis 캐싱**: 결과 캐싱으로 응답 속도 향상
- **로드 밸런싱**: 여러 인스턴스 운영

### 2. 보안 설정
```python
# settings.py (운영환경)
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
CORS_ALLOW_ALL_ORIGINS = False  # 개발용 설정 제거
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
]
```

### 3. 로깅 설정
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 📊 모니터링

### 1. 헬스 체크 엔드포인트
```python
# views.py에 추가
def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'model_loaded': sentiment_classifier is not None,
        'timestamp': timezone.now().isoformat()
    })
```

### 2. 사용량 추적
```python
# 간단한 카운터 추가
import logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
def analyze_sentiment_api(request):
    logger.info(f"API 요청 - 텍스트 길이: {len(request.data.get('text', ''))}")
    # ... 기존 코드
```

이제 프로덕션 환경에서 안정적으로 운영할 수 있는 AI 서비스가 준비되었습니다! 🎉
