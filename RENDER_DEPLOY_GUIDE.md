# 🚀 Render 무료 배포 가이드

## 🌟 **Render - 완전 무료 Django 배포!**

Render는 Heroku의 무료 대안으로, 매월 750시간 무료 사용 가능합니다!

## 📋 **배포 준비 완료 상태**

✅ 모든 설정 파일이 준비되었습니다:
- `build.sh` - Render 빌드 스크립트
- `requirements.txt` - 패키지 목록
- Django 설정 완료
- Git 저장소 초기화 완료

## 🌐 **Render 배포 단계**

### 1. GitHub에 코드 업로드

먼저 GitHub에 저장소를 만들어야 합니다:

1. **GitHub 접속**: https://github.com
2. **새 저장소 생성**: "New repository" 클릭
3. **저장소 이름**: `ai-sentiment-analyzer` (원하는 이름)
4. **Public** 선택 (무료 배포를 위해)
5. **Create repository** 클릭

### 2. 로컬 코드를 GitHub에 푸시

터미널에서 실행 (가상환경 활성화 상태에서):

```bash
# GitHub 저장소 연결 (위에서 만든 저장소 URL로 변경)
git remote add origin https://github.com/YOUR_USERNAME/ai-sentiment-analyzer.git

# 기본 브랜치를 main으로 설정
git branch -M main

# GitHub에 푸시
git push -u origin main
```

### 3. Render에서 배포

1. **Render 접속**: https://render.com
2. **무료 회원가입** (GitHub 계정으로 연동 가능)
3. **New Web Service** 클릭
4. **Connect a repository** → GitHub 저장소 선택
5. **배포 설정**:
   - **Name**: `ai-sentiment-analyzer`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free` 선택

6. **Create Web Service** 클릭

### 4. 환경 변수 설정 (선택사항)

Render 대시보드에서:
- **Environment** 탭 클릭
- 다음 변수들 추가:
  ```
  SECRET_KEY = your-secret-key-here
  DEBUG = False
  ```

## 🔗 **배포 완료 후**

배포가 완료되면 다음과 같은 URL을 받게 됩니다:
- **앱 URL**: `https://ai-sentiment-analyzer.onrender.com`
- **API 엔드포인트**: `https://ai-sentiment-analyzer.onrender.com/api/analyze/`

## 🎯 **프론트엔드 연동 코드**

```javascript
// Render에 배포된 API 사용
const API_BASE_URL = 'https://your-app-name.onrender.com';

const analyzeSentiment = async (text) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: text })
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};

// React.js에서 사용 예시
const SentimentAnalyzer = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const response = await analyzeSentiment(text);
      setResult(response);
    } catch (error) {
      console.error('분석 실패:', error);
    }
    setLoading(false);
  };

  return (
    <div>
      <textarea 
        value={text} 
        onChange={(e) => setText(e.target.value)}
        placeholder="분석할 텍스트를 입력하세요..."
      />
      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? '분석 중...' : '감정 분석'}
      </button>
      
      {result && (
        <div>
          <h3>분석 결과</h3>
          <p>감정: {result.result.korean_label}</p>
          <p>신뢰도: {result.result.confidence_percent}%</p>
        </div>
      )}
    </div>
  );
};
```

## 📊 **API 명세서**

### POST /api/analyze/

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "분석할 한국어 텍스트"
}
```

**Response (성공):**
```json
{
  "success": true,
  "text": "분석할 한국어 텍스트",
  "result": {
    "label": "4 stars",
    "korean_label": "긍정적",
    "score": 0.8945,
    "confidence_percent": 89.45
  }
}
```

**Response (오류):**
```json
{
  "error": "오류 메시지"
}
```

## ⚡ **Render 장점**

1. **완전 무료** - 월 750시간 (31일 × 24시간)
2. **자동 HTTPS** - SSL 인증서 자동 적용
3. **Git 연동** - 코드 변경시 자동 재배포
4. **무제한 대역폭** - 트래픽 제한 없음
5. **빠른 배포** - 5-10분 내 배포 완료

## ⚠️ **주의사항**

1. **첫 요청 지연**: 15분 비활성 시 슬립 모드 (30초 웨이크업)
2. **모델 로딩 시간**: 첫 요청 시 AI 모델 로딩 시간 필요
3. **메모리 제한**: 무료 플랜 512MB RAM

## 🚀 **배포 체크리스트**

- [ ] GitHub 저장소 생성
- [ ] `git remote add origin` 실행
- [ ] `git push origin main` 실행
- [ ] Render 회원가입
- [ ] New Web Service 생성
- [ ] 저장소 연결
- [ ] 배포 설정 완료
- [ ] 웹 브라우저에서 테스트
- [ ] API 테스트 완료

배포 완료 후 전 세계에서 접근 가능한 무료 AI 서비스가 됩니다! 🎉

## 🔄 **업데이트 방법**

코드 수정 후:
```bash
git add .
git commit -m "Update message"
git push origin main
```

Render가 자동으로 새 버전을 배포합니다!
