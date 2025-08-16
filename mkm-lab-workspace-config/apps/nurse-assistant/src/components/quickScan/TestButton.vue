<template>
  <div class="test-button-container">
    <div class="test-grid">
      <!-- 설진 검사 버튼 -->
      <div class="test-card" :class="getTestStatusClass('tongue')">
        <div class="test-icon">
          <q-icon name="visibility" size="xl" />
        </div>
        <div class="test-content">
          <h4>설진 촬영</h4>
          <p>혀를 내밀어주세요</p>
          <div class="test-status">
            <q-icon 
              :name="getStatusIcon('tongue')" 
              :color="getStatusColor('tongue')"
              size="sm"
            />
            <span>{{ getStatusText('tongue') }}</span>
          </div>
        </div>
        <q-btn
          :label="getButtonText('tongue')"
          :color="getButtonColor('tongue')"
          :disable="isProcessing"
          size="lg"
          class="test-btn"
          @click="startTest('tongue')"
        />
      </div>
      
      <!-- 면진 검사 버튼 -->
      <div class="test-card" :class="getTestStatusClass('face')">
        <div class="test-icon">
          <q-icon name="face" size="xl" />
        </div>
        <div class="test-content">
          <h4>얼굴 검사</h4>
          <p>정면을 바라봐주세요</p>
          <div class="test-status">
            <q-icon 
              :name="getStatusIcon('face')" 
              :color="getStatusColor('face')"
              size="sm"
            />
            <span>{{ getStatusText('face') }}</span>
          </div>
        </div>
        <q-btn
          :label="getButtonText('face')"
          :color="getButtonColor('face')"
          :disable="isProcessing"
          size="lg"
          class="test-btn"
          @click="startTest('face')"
        />
      </div>
      
      <!-- 음성 검사 버튼 -->
      <div class="test-card" :class="getTestStatusClass('voice')">
        <div class="test-icon">
          <q-icon name="mic" size="xl" />
        </div>
        <div class="test-content">
          <h4>음성 녹음</h4>
          <p>'아~' 소리 3초</p>
          <div class="test-status">
            <q-icon 
              :name="getStatusIcon('voice')" 
              :color="getStatusColor('voice')"
              size="sm"
            />
            <span>{{ getStatusText('voice') }}</span>
          </div>
        </div>
        <q-btn
          :label="getButtonText('voice')"
          :color="getButtonColor('voice')"
          :disable="isProcessing"
          size="lg"
          class="test-btn"
          @click="startTest('voice')"
        />
      </div>
    </div>
    
    <!-- 진행률 표시 -->
    <div v-if="completedTests > 0" class="progress-section">
      <div class="progress-info">
        <span>검사 진행률</span>
        <span>{{ completedTests }}/3 완료</span>
      </div>
      <q-linear-progress
        :value="completedTests / 3"
        color="primary"
        size="md"
        class="progress-bar"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useQuickScanStore } from '@/stores/quickScan'

const quickScanStore = useQuickScanStore()

// 검사 상태 계산
const completedTests = computed(() => {
  const results = quickScanStore.testResults
  return Object.values(results).filter(test => test.quality === 'ok').length
})

const isProcessing = computed(() => {
  const results = quickScanStore.testResults
  return Object.values(results).some(test => test.quality === 'processing')
})

// 검사 상태별 스타일 클래스
const getTestStatusClass = (testType) => {
  const quality = quickScanStore.testResults[testType].quality
  return {
    'test-pending': quality === 'pending',
    'test-processing': quality === 'processing',
    'test-ok': quality === 'ok',
    'test-retry': quality === 'retry'
  }
}

// 상태 아이콘
const getStatusIcon = (testType) => {
  const quality = quickScanStore.testResults[testType].quality
  switch (quality) {
    case 'ok': return 'check_circle'
    case 'retry': return 'error'
    case 'processing': return 'hourglass_empty'
    default: return 'radio_button_unchecked'
  }
}

// 상태 색상
const getStatusColor = (testType) => {
  const quality = quickScanStore.testResults[testType].quality
  switch (quality) {
    case 'ok': return 'positive'
    case 'retry': return 'negative'
    case 'processing': return 'warning'
    default: return 'grey'
  }
}

// 상태 텍스트
const getStatusText = (testType) => {
  const quality = quickScanStore.testResults[testType].quality
  switch (quality) {
    case 'ok': return '완료'
    case 'retry': return '재촬영 필요'
    case 'processing': return '처리 중...'
    default: return '대기 중'
  }
}

// 버튼 텍스트
const getButtonText = (testType) => {
  const quality = quickScanStore.testResults[testType].quality
  switch (quality) {
    case 'ok': return '완료됨'
    case 'retry': return '재촬영'
    case 'processing': return '처리 중...'
    default: return '시작하기'
  }
}

// 버튼 색상
const getButtonColor = (testType) => {
  const quality = quickScanStore.testResults[testType].quality
  switch (quality) {
    case 'ok': return 'positive'
    case 'retry': return 'negative'
    case 'processing': return 'warning'
    default: return 'primary'
  }
}

// 검사 시작
const startTest = (testType) => {
  // 검사 품질을 'processing'으로 설정
  quickScanStore.setTestQuality(testType, 'processing')
  
  // 시뮬레이션: 2초 후 결과 생성
  setTimeout(() => {
    // 80% 확률로 성공, 20% 확률로 재촬영 필요
    const isSuccess = Math.random() > 0.2
    quickScanStore.setTestQuality(testType, isSuccess ? 'ok' : 'retry')
  }, 2000)
}
</script>

<style scoped>
.test-button-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.test-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.test-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 3px solid transparent;
}

.test-card.test-pending {
  border-color: #e9ecef;
}

.test-card.test-processing {
  border-color: #ffc107;
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
}

.test-card.test-ok {
  border-color: #28a745;
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
}

.test-card.test-retry {
  border-color: #dc3545;
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
}

.test-icon {
  text-align: center;
  margin-bottom: 16px;
  color: #6c757d;
}

.test-content {
  text-align: center;
  margin-bottom: 20px;
}

.test-content h4 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 18px;
  font-weight: 600;
}

.test-content p {
  margin: 0 0 12px 0;
  color: #6c757d;
  font-size: 14px;
}

.test-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 500;
}

.test-btn {
  width: 100%;
  height: 48px;
  font-weight: 600;
  border-radius: 12px;
}

.progress-section {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
}

.progress-bar {
  border-radius: 8px;
}

/* 애니메이션 */
.test-card.test-processing {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .test-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .test-card {
    padding: 20px;
  }
  
  .test-content h4 {
    font-size: 16px;
  }
  
  .test-btn {
    height: 44px;
  }
}
</style> 