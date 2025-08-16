# 🎨 MKM Lab 디자인 시스템 v2.0
## "사이버펑크 딥 다이브 + 따뜻한 치유" (Cyberpunk Deep Dive + Warm Healing)

---

## 📋 **1. 디자인 철학 (Design Philosophy)**

### 🎯 **핵심 개념**
- **"기술의 차가움과 인간 영혼의 따뜻함이 공존하는 네온 빛의 미래"**
- **"AI가 단순한 분석 도구를 넘어, 디지털 세계의 깊이를 탐험하는 안내자"**
- **"치유와 건강이라는 따뜻한 주제를 미래지향적 기술로 표현"**

### 🌟 **브랜드 정체성**
- **MKM LAB**: 메인 브랜드 (강조)
- **목소리네트워크**: 푸터에만 표시 (회사 정보)
- **AI DIGITAL ECOSYSTEM**: 서브 브랜드

---

## 🎨 **2. 색상 체계 (Color System)**

### 🌈 **기본 색상 팔레트**

#### **배경 (Background)**
```css
--deep-navy: #0A0A1A;        /* 깊은 심연을 연상시키는 다크 네이비 */
--dark-purple: #1A1A2E;      /* 보조 배경 */
```

#### **주요 네온 (Primary Neon)**
```css
--electric-blue: #00F6FF;    /* MKM Lab의 신뢰와 기술력 */
--neon-cyan: #00F6FF;        /* 일렉트릭 블루/시안 */
```

#### **보조 네온 (Secondary Neon)**
```css
--neon-magenta: #FF00E5;     /* 생명과 에너지, 창의성 */
--lime-green: #7FFF00;       /* 데이터와 주의 */
```

#### **따뜻한 색상 (Warm Colors)**
```css
--gold: #FFD700;             /* 따뜻함과 프리미엄 */
--soft-white: #E6E6FA;       /* 부드러운 화이트 */
--warm-lavender: #E6E6FA;    /* 따뜻한 라벤더 */
```

### 🎭 **색상 조합 규칙**

#### **기본 조합**
- **배경**: `#0A0A1A` (깊은 네이비)
- **주요 텍스트**: `#E6E6FA` (소프트 화이트)
- **강조**: `#FFD700` (골드)
- **네온 효과**: `#00F6FF` (일렉트릭 블루)

#### **호버 효과**
- **링크 호버**: `#FFD700` (골드)
- **버튼 호버**: `#FFD700` (골드)
- **카드 호버**: `#FFD700` (골드 보더)

---

## 🔤 **3. 타이포그래피 (Typography)**

### 📝 **폰트 스택**
```css
/* 헤드라인 */
font-family: 'Orbitron', sans-serif;    /* 미래적, 기계적 느낌 */

/* 본문 */
font-family: 'Fira Code', monospace;    /* 가독성 높은 모노스페이스 */
```

### 📏 **폰트 크기 체계**
```css
/* 헤드라인 */
--h1-size: 3rem;             /* 메인 타이틀 */
--h2-size: 2.5rem;           /* 섹션 타이틀 */
--h3-size: 2rem;             /* 서브 타이틀 */

/* 본문 */
--body-large: 1.2rem;        /* 큰 본문 */
--body-normal: 1rem;         /* 일반 본문 */
--body-small: 0.9rem;        /* 작은 텍스트 */
--caption: 0.8rem;           /* 캡션 */
```

### 🎨 **폰트 스타일**
- **헤드라인**: `font-weight: 700`, `letter-spacing: 1px`
- **본문**: `font-weight: 400`, `line-height: 1.6`
- **강조**: `font-weight: 500`, `text-shadow` 효과

---

## 🧩 **4. 컴포넌트 디자인 (Component Design)**

### 🃏 **카드 (Cards)**
```css
.cyberpunk-card {
  background: rgba(10, 10, 26, 0.9);
  border: 2px solid #00F6FF;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 246, 255, 0.3);
  transition: all 0.3s ease;
}

.cyberpunk-card:hover {
  border-color: #FFD700;
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
  transform: translateY(-5px);
}
```

### 🔘 **버튼 (Buttons)**
```css
.cyberpunk-btn {
  background: transparent;
  border: 2px solid #00F6FF;
  color: #00F6FF;
  padding: 12px 24px;
  border-radius: 4px;
  font-family: 'Fira Code', monospace;
  transition: all 0.3s ease;
}

.cyberpunk-btn:hover {
  border-color: #FFD700;
  color: #FFD700;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
  transform: translateY(-2px);
}
```

### 🔗 **링크 (Links)**
```css
.cyberpunk-link {
  color: #E6E6FA;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}

.cyberpunk-link:hover {
  color: #FFD700;
  border-color: #FFD700;
  text-shadow: 0 0 5px rgba(255, 215, 0, 0.5);
}
```

### 🎯 **아이콘 (Icons)**
```css
.cyberpunk-icon-container {
  width: 48px;
  height: 48px;
  background: linear-gradient(45deg, #00F6FF, #FF00E5, #FFD700);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

---

## ✨ **5. 애니메이션 (Animations)**

### 🌊 **배경 애니메이션**
```css
@keyframes scan {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.scan-line {
  background: linear-gradient(45deg, transparent 30%, rgba(0, 246, 255, 0.1) 50%, transparent 70%);
  animation: scan 3s linear infinite;
}
```

### 💫 **글로우 효과**
```css
@keyframes glow {
  from { box-shadow: 0 0 20px rgba(0, 246, 255, 0.5); }
  to { box-shadow: 0 0 30px rgba(0, 246, 255, 0.8), 0 0 15px rgba(255, 215, 0, 0.3); }
}

.cyberpunk-glow {
  animation: glow 2s ease-in-out infinite alternate;
}
```

### 🎭 **호버 애니메이션**
```css
.card-hover {
  transition: all 0.3s ease;
}

.card-hover:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
}
```

---

## 📱 **6. 반응형 디자인 (Responsive Design)**

### 📐 **브레이크포인트**
```css
/* 모바일 */
@media (max-width: 768px) {
  --h1-size: 2rem;
  --h2-size: 1.5rem;
  --body-large: 1rem;
}

/* 태블릿 */
@media (min-width: 769px) and (max-width: 1024px) {
  --h1-size: 2.5rem;
  --h2-size: 2rem;
}

/* 데스크톱 */
@media (min-width: 1025px) {
  --h1-size: 3rem;
  --h2-size: 2.5rem;
}
```

### 📱 **모바일 최적화**
- **터치 친화적**: 최소 44px 터치 영역
- **가독성**: 충분한 텍스트 크기
- **성능**: 최적화된 애니메이션

---

## 🎨 **7. 레이아웃 시스템 (Layout System)**

### 📐 **그리드 시스템**
```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.grid {
  display: grid;
  gap: 2rem;
}

.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid-3 { grid-template-columns: repeat(3, 1fr); }
.grid-4 { grid-template-columns: repeat(4, 1fr); }
```

### 📏 **스페이싱**
```css
--spacing-xs: 0.5rem;    /* 8px */
--spacing-sm: 1rem;      /* 16px */
--spacing-md: 2rem;      /* 32px */
--spacing-lg: 3rem;      /* 48px */
--spacing-xl: 4rem;      /* 64px */
```

---

## 🎯 **8. 접근성 (Accessibility)**

### 👁️ **시각적 접근성**
- **대비율**: WCAG AA 기준 준수 (4.5:1)
- **색맹 친화적**: 색상만으로 정보 전달 금지
- **포커스 표시**: 명확한 포커스 인디케이터

### 🎧 **모션 감소**
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 🚀 **9. 성능 최적화 (Performance)**

### ⚡ **최적화 규칙**
- **CSS 최소화**: 불필요한 스타일 제거
- **폰트 최적화**: 웹폰트 preload
- **이미지 최적화**: WebP 포맷 사용
- **애니메이션 최적화**: GPU 가속 활용

### 📊 **성능 지표**
- **First Contentful Paint**: < 1.5초
- **Largest Contentful Paint**: < 2.5초
- **Cumulative Layout Shift**: < 0.1

---

## 🎨 **10. 브랜드 가이드라인 (Brand Guidelines)**

### 🏷️ **로고 사용**
- **최소 크기**: 24px (디지털), 10mm (인쇄)
- **클리어스페이스**: 로고 높이의 1/2
- **배경**: 어두운 배경에서만 사용

### 📝 **톤앤매너**
- **공식적이지만 친근한**
- **기술적이지만 이해하기 쉬운**
- **미래지향적이지만 실용적인**

---

## 📋 **11. 구현 체크리스트 (Implementation Checklist)**

### ✅ **기본 설정**
- [ ] CSS 변수 정의
- [ ] 폰트 로드 설정
- [ ] 기본 색상 적용
- [ ] 반응형 브레이크포인트 설정

### ✅ **컴포넌트 구현**
- [ ] 카드 스타일 적용
- [ ] 버튼 스타일 적용
- [ ] 링크 스타일 적용
- [ ] 아이콘 스타일 적용

### ✅ **애니메이션 구현**
- [ ] 배경 애니메이션 적용
- [ ] 호버 효과 구현
- [ ] 글로우 효과 적용
- [ ] 성능 최적화

### ✅ **접근성 검증**
- [ ] 색상 대비 검사
- [ ] 키보드 네비게이션 테스트
- [ ] 스크린 리더 호환성 확인
- [ ] 모션 감소 설정 테스트

---

## 📚 **12. 참고 자료 (References)**

### 🎨 **디자인 영감**
- **Blade Runner 2049**: 미래적 도시 풍경
- **Ghost in the Shell**: 사이버펑크 미학
- **Tron: Legacy**: 네온과 글로우 효과

### 🔧 **기술적 참고**
- **CSS Grid**: 레이아웃 시스템
- **CSS Custom Properties**: 테마 관리
- **Framer Motion**: 애니메이션 라이브러리

---

## 📝 **13. 버전 관리 (Version Control)**

### 🔄 **변경 이력**
- **v2.0** (2025-07-31): 사이버펑크 딥 다이브 + 따뜻한 치유 스타일
- **v1.0** (2025-07-30): 기본 디자인 시스템

### 🎯 **향후 계획**
- **v2.1**: 다크/라이트 모드 지원
- **v2.2**: 고급 애니메이션 효과
- **v2.3**: PWA 최적화

---

## 🎖️ **14. 결론 (Conclusion)**

**MKM Lab 디자인 시스템 v2.0**은 기술의 차가움과 인간의 따뜻함을 조화롭게 결합한 독보적인 디자인 언어입니다. 이 시스템을 통해 우리는:

- ✅ **독보적인 브랜드 정체성** 구축
- ✅ **사용자 경험 최적화** 달성
- ✅ **기술적 우수성** 표현
- ✅ **치유와 건강** 메시지 전달

**이 디자인 시스템은 MKM Lab의 모든 디지털 자산의 기준이 되며, 일관성 있고 강력한 브랜드 경험을 제공합니다.** 🚀✨

---

*문서 버전: v2.0*  
*최종 업데이트: 2025-07-31*  
*작성자: MKM Lab 디자인 팀* 