# MKM Lab 디자인 시스템 & UI/UX 가이드라인 v8.0

**문서 ID:** MKM-DESIGN-SYSTEM-v8.0  
**생성일:** 2025-07-08  
**상태:** 최종 확정  
**역할:** 통합 디자인 시스템 및 구현 가이드라인  

---

## 🎨 **디자인 철학**

**핵심 철학**: **"기록은 가볍게, 통찰은 깊게 (Recording is Light, Insight is Deep)"**

모든 UI/UX는 사용자가 건강 데이터를 쉽고 빠르게 기록할 수 있도록 하되, 그 결과로 얻는 통찰과 분석은 깊이 있고 의미 있는 경험을 제공해야 합니다.

---

## 🏗️ **1. 디자인 시스템 기초**

### **1.1 색상 시스템 (Color System)**

```css
/* Primary Colors */
--color-primary-50: #F0FDF4;
--color-primary-100: #DCFCE7;
--color-primary-200: #BBF7D0;
--color-primary-300: #86EFAC;
--color-primary-400: #4ADE80;
--color-primary-500: #22C55E; /* Main Primary */
--color-primary-600: #16A34A;
--color-primary-700: #15803D;
--color-primary-800: #166534;
--color-primary-900: #14532D;

/* Secondary Colors */
--color-gray-50: #F9FAFB;
--color-gray-100: #F3F4F6;
--color-gray-200: #E5E7EB;
--color-gray-300: #D1D5DB;
--color-gray-400: #9CA3AF;
--color-gray-500: #6B7280;
--color-gray-600: #4B5563;
--color-gray-700: #374151;
--color-gray-800: #1F2937;
--color-gray-900: #111827;

/* Accent Colors */
--color-accent-coral: #FF7F50;
--color-accent-yellow: #FCD34D;
--color-accent-blue: #3B82F6;
--color-accent-red: #EF4444;

/* Semantic Colors */
--color-success: #10B981;
--color-warning: #F59E0B;
--color-error: #EF4444;
--color-info: #3B82F6;
```

### **1.2 타이포그래피 시스템 (Typography)**

```css
/* Font Families */
--font-primary: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
--font-secondary: 'Noto Sans KR', sans-serif;
--font-mono: 'JetBrains Mono', Consolas, monospace;

/* Font Sizes */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */

/* Font Weights */
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* Line Heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
```

### **1.3 간격 시스템 (Spacing System)**

```css
/* Spacing Scale */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
```

### **1.4 그림자 시스템 (Shadow System)**

```css
/* Box Shadows */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
```

---

## 📱 **2. 모바일 앱 컴포넌트**

### **2.1 하단 탭 바 (Bottom Tab Bar)**

```vue
<template>
  <div class="bottom-tab-bar">
    <TabItem icon="home" label="홈" :active="currentTab === 'home'" />
    <TabItem icon="chart" label="리포트" :active="currentTab === 'reports'" />
    <TabItem icon="plus" label="노트" :active="currentTab === 'new'" class="center-button" />
    <TabItem icon="search" label="발견" :active="currentTab === 'discover'" />
    <TabItem icon="menu" label="더보기" :active="currentTab === 'more'" />
  </div>
</template>

<style scoped>
.bottom-tab-bar {
  @apply fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200;
  @apply flex items-center justify-around py-2 px-4;
  @apply safe-area-padding-bottom;
}

.center-button {
  @apply bg-primary-500 text-white rounded-full;
  @apply transform scale-110 shadow-lg;
}
</style>
```

### **2.2 카드 컴포넌트 (Card Component)**

```vue
<template>
  <div class="health-card" :class="cardClasses">
    <div class="card-header" v-if="$slots.header">
      <slot name="header"></slot>
    </div>
    <div class="card-content">
      <slot></slot>
    </div>
    <div class="card-footer" v-if="$slots.footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<style scoped>
.health-card {
  @apply bg-white rounded-xl shadow-md p-6 mb-4;
  @apply border border-gray-100;
}

.health-card.warm {
  @apply bg-gradient-to-br from-primary-50 to-white;
  @apply border-primary-200;
}

.card-header {
  @apply mb-4 pb-3 border-b border-gray-100;
}

.card-content {
  @apply space-y-3;
}

.card-footer {
  @apply mt-4 pt-3 border-t border-gray-100;
}
</style>
```

### **2.3 입력 폼 컴포넌트 (Form Components)**

```vue
<!-- 건강 기록 입력 폼 -->
<template>
  <form class="health-form">
    <div class="form-group">
      <label class="form-label">오늘의 기분</label>
      <div class="mood-selector">
        <button
          v-for="mood in moods"
          :key="mood.value"
          type="button"
          class="mood-button"
          :class="{ active: selectedMood === mood.value }"
          @click="selectedMood = mood.value"
        >
          <span class="mood-emoji">{{ mood.emoji }}</span>
          <span class="mood-label">{{ mood.label }}</span>
        </button>
      </div>
    </div>
  </form>
</template>

<style scoped>
.health-form {
  @apply space-y-6;
}

.form-group {
  @apply space-y-3;
}

.form-label {
  @apply block text-sm font-medium text-gray-700;
}

.mood-selector {
  @apply grid grid-cols-5 gap-2;
}

.mood-button {
  @apply flex flex-col items-center p-3 rounded-lg;
  @apply border-2 border-gray-200 bg-gray-50;
  @apply transition-all duration-200;
}

.mood-button:hover {
  @apply border-primary-300 bg-primary-50;
}

.mood-button.active {
  @apply border-primary-500 bg-primary-100;
  @apply ring-2 ring-primary-200;
}

.mood-emoji {
  @apply text-2xl mb-1;
}

.mood-label {
  @apply text-xs text-gray-600;
}
</style>
```

---

## 💻 **3. 웹 대시보드 컴포넌트**

### **3.1 사이드바 네비게이션 (Sidebar Navigation)**

```vue
<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <img src="/logo.svg" alt="MKM Lab" class="logo" />
      <h1 class="brand-name">MKM Lab</h1>
    </div>
    
    <nav class="sidebar-nav">
      <NavItem 
        v-for="item in navItems" 
        :key="item.path"
        :icon="item.icon"
        :label="item.label"
        :path="item.path"
        :active="currentPath === item.path"
      />
    </nav>
    
    <div class="sidebar-footer">
      <UserProfile />
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  @apply w-64 h-screen bg-gray-900 text-white;
  @apply flex flex-col;
}

.sidebar-header {
  @apply p-6 border-b border-gray-700;
  @apply flex items-center space-x-3;
}

.logo {
  @apply w-8 h-8;
}

.brand-name {
  @apply text-xl font-semibold;
}

.sidebar-nav {
  @apply flex-1 py-6;
}

.sidebar-footer {
  @apply p-6 border-t border-gray-700;
}
</style>
```

### **3.2 환자 대시보드 (Patient Dashboard)**

```vue
<template>
  <div class="patient-dashboard">
    <header class="dashboard-header">
      <div class="patient-info">
        <h1 class="patient-name">{{ patient.name }}</h1>
        <div class="patient-meta">
          <span class="constitution-type">{{ patient.constitutionType }}</span>
          <span class="last-visit">마지막 방문: {{ patient.lastVisit }}</span>
        </div>
      </div>
      <div class="dashboard-actions">
        <button class="btn-primary">새 소견 작성</button>
        <button class="btn-secondary">리포트 다운로드</button>
      </div>
    </header>
    
    <main class="dashboard-content">
      <div class="content-grid">
        <section class="timeline-section">
          <h2 class="section-title">통합 노트</h2>
          <PatientTimeline :entries="patient.entries" />
        </section>
        
        <section class="analysis-section">
          <h2 class="section-title">심층 분석</h2>
          <AnalysisCharts :data="patient.analysisData" />
        </section>
        
        <section class="expert-note-section">
          <h2 class="section-title">전문가 소견</h2>
          <ExpertNoteEditor :patient-id="patient.id" />
        </section>
      </div>
    </main>
  </div>
</template>

<style scoped>
.patient-dashboard {
  @apply min-h-screen bg-gray-50;
}

.dashboard-header {
  @apply bg-white shadow-sm px-6 py-4;
  @apply flex items-center justify-between;
}

.patient-info {
  @apply space-y-1;
}

.patient-name {
  @apply text-2xl font-semibold text-gray-900;
}

.patient-meta {
  @apply flex items-center space-x-4 text-sm text-gray-600;
}

.constitution-type {
  @apply px-2 py-1 bg-primary-100 text-primary-700 rounded-md;
}

.dashboard-actions {
  @apply flex space-x-3;
}

.dashboard-content {
  @apply p-6;
}

.content-grid {
  @apply grid grid-cols-1 lg:grid-cols-3 gap-6;
}

.timeline-section {
  @apply lg:col-span-2;
}

.section-title {
  @apply text-lg font-semibold text-gray-900 mb-4;
}
</style>
```

---

## 🎯 **4. 상호작용 가이드라인**

### **4.1 애니메이션 및 트랜지션**

```css
/* 기본 트랜지션 */
.smooth-transition {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 페이지 전환 */
.page-enter-active, .page-leave-active {
  transition: all 0.3s ease-in-out;
}

.page-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* 모달 애니메이션 */
.modal-enter-active, .modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
```

### **4.2 로딩 상태**

```vue
<template>
  <div class="loading-container">
    <div class="loading-spinner">
      <div class="spinner"></div>
    </div>
    <p class="loading-text">건강 데이터를 분석 중입니다...</p>
  </div>
</template>

<style scoped>
.loading-container {
  @apply flex flex-col items-center justify-center py-12;
}

.spinner {
  @apply w-8 h-8 border-4 border-primary-200 border-t-primary-500 rounded-full;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  @apply mt-4 text-gray-600 text-sm;
}
</style>
```

---

## 📐 **5. 반응형 디자인 브레이크포인트**

```css
/* Tailwind CSS 기반 브레이크포인트 */
:root {
  --breakpoint-sm: 640px;   /* 모바일 가로 */
  --breakpoint-md: 768px;   /* 태블릿 */
  --breakpoint-lg: 1024px;  /* 소형 데스크탑 */
  --breakpoint-xl: 1280px;  /* 대형 데스크탑 */
  --breakpoint-2xl: 1536px; /* 초대형 화면 */
}

/* 모바일 우선 설계 */
@media (max-width: 640px) {
  .mobile-hidden { display: none; }
  .mobile-full { width: 100%; }
}

@media (min-width: 768px) {
  .tablet-grid { 
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .desktop-sidebar {
    display: block;
    width: 256px;
  }
}
```

---

## ✅ **6. 구현 체크리스트**

### **6.1 MVP 단계 (Phase 1)**
- [ ] 기본 색상 시스템 구현
- [ ] 타이포그래피 시스템 적용
- [ ] 모바일 하단 탭 바 컴포넌트
- [ ] 기본 카드 및 폼 컴포넌트
- [ ] 간단한 로딩 상태 처리

### **6.2 베타 단계 (Phase 2)**
- [ ] 완전한 컴포넌트 라이브러리
- [ ] 웹 대시보드 사이드바
- [ ] 환자 대시보드 레이아웃
- [ ] 고급 애니메이션 및 트랜지션
- [ ] 반응형 디자인 완성

### **6.3 정식 출시 (Phase 3)**
- [ ] 접근성 기능 완성
- [ ] 다크 모드 지원
- [ ] 고급 인터랙션 패턴
- [ ] 성능 최적화
- [ ] 크로스 브라우저 호환성

---

**이 디자인 시스템은 MKM Lab의 모든 UI/UX 구현의 단일 진실 공급원(Single Source of Truth)으로 작동하며, 모든 개발자는 이 가이드라인을 준수해야 합니다.**

*디자인 시스템 버전 v8.0 | 제정일자 2025-07-08 | 제정자 MKM Lab 디자인팀*
