# 🚀 즉시 공유 가이드 (ngrok 사용)

## 1️⃣ ngrok 설치 및 사용

### 설치
1. https://ngrok.com/ 에서 무료 회원가입
2. ngrok 다운로드 후 압축 해제
3. 토큰 설정: `ngrok authtoken YOUR_TOKEN`

### 사용법
```bash
# Django 서버 실행 (터미널 1)
python manage.py runserver 0.0.0.0:8000

# ngrok으로 터널 생성 (터미널 2)
ngrok http 8000
```

### 결과
```
ngrok by @inconshreveable

Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                        Korea (kr)
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000
```

**🌐 공유 URL**: `https://abc123.ngrok.io`
- 전 세계 어디서든 접근 가능
- HTML 인터페이스: `https://abc123.ngrok.io/`
- API 엔드포인트: `https://abc123.ngrok.io/api/analyze/`

## 2️⃣ 프론트엔드팀에게 전달할 정보

```javascript
// 프론트엔드 연동 코드
const API_BASE_URL = 'https://abc123.ngrok.io';  // ngrok URL로 변경

const analyzeSentiment = async (text) => {
  const response = await fetch(`${API_BASE_URL}/api/analyze/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text: text })
  });
  
  return await response.json();
};
```

## ⚠️ ngrok 주의사항
- **무료 버전**: 8시간 후 URL 변경됨
- **유료 버전**: 고정 URL 사용 가능
- **임시 사용**: 개발/테스트 목적으로 적합

## 🔄 매번 새로운 URL 받기
무료 ngrok은 재시작할 때마다 새 URL이 생성됩니다:
1. ngrok 재실행
2. 새 URL 확인
3. 프론트엔드팀에게 새 URL 공유
