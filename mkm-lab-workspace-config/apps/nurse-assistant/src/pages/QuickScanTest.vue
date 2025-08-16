<template>
  <q-page class="quickscan-test-page">
    <div class="page-container">
      <!-- 헤더 -->
      <div class="page-header">
        <div class="header-content">
          <h1>검사 진행</h1>
          <p class="subtitle">3대 검사를 순서대로 진행해주세요</p>
        </div>
        <div class="patient-info">
          <div class="patient-id">
            <q-icon name="person" size="sm" />
            <span>{{ patientId }}</span>
          </div>
          <div class="patient-name" v-if="basicInfo.nickname">
            {{ basicInfo.nickname }}
          </div>
        </div>
      </div>
      
      <!-- 검사 진행률 -->
      <div class="progress-section">
        <div class="progress-header">
          <h3>검사 진행률</h3>
          <div class="progress-count">
            {{ completedTests }}/3 완료
          </div>
        </div>
        <q-linear-progress
          :value="completedTests / 3"
          color="primary"
          size="lg"
          class="main-progress"
        />
        <div class="progress-labels">
          <span>설진</span>
          <span>면진</span>
          <span>음성</span>
        </div>
      </div>
      
      <!-- 검사 버튼들 -->
      <TestButton />
      
      <!-- 검사 완료 후 다음 단계 -->
      <div v-if="isAllTestsComplete" class="completion-section">
        <div class="completion-card">
          <div class="completion-icon">
            <q-icon name="check_circle" color="positive" size="xl" />
          </div>
          <h3>모든 검사 완료!</h3>
          <p>검사 데이터를 한의사 대시보드로 전송할 준비가 되었습니다.</p>
          <q-btn
            label="전송하기"
            color="primary"
            size="lg"
            class="transmit-btn"
            @click="goToResultStep"
          >
            <template v-slot:prepend>
              <q-icon name="send" />
            </template>
          </q-btn>
        </div>
      </div>
      
      <!-- 검사 가이드 -->
      <div class="guide-section">
        <div class="guide-card">
          <h4>검사 가이드</h4>
          <div class="guide-items">
            <div class="guide-item">
              <q-icon name="visibility" color="primary" />
              <div class="guide-content">
                <strong>설진 촬영:</strong> 혀를 자연스럽게 내밀어주세요
              </div>
            </div>
            <div class="guide-item">
              <q-icon name="face" color="primary" />
              <div class="guide-content">
                <strong>얼굴 검사:</strong> 정면을 바라보고 자연스러운 표정을 유지해주세요
              </div>
            </div>
            <div class="guide-item">
              <q-icon name="mic" color="primary" />
              <div class="guide-content">
                <strong>음성 녹음:</strong> '아~' 소리를 3초간 길게 발음해주세요
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 뒤로가기 버튼 -->
      <div class="navigation-section">
        <q-btn
          icon="arrow_back"
          label="이전 단계"
          flat
          color="grey"
          @click="goBack"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuickScanStore } from '@/stores/quickScan'
import TestButton from '@/components/quickScan/TestButton.vue'

const router = useRouter()
const quickScanStore = useQuickScanStore()

// 상태 계산
const patientId = computed(() => quickScanStore.patientId)
const basicInfo = computed(() => quickScanStore.basicInfo)
const completedTests = computed(() => {
  const results = quickScanStore.testResults
  return Object.values(results).filter(test => test.quality === 'ok').length
})
const isAllTestsComplete = computed(() => quickScanStore.isAllTestsComplete)

// 페이지 접근 권한 확인
onMounted(() => {
  if (!quickScanStore.canProceedToTest) {
    router.push('/quickscan/start')
    return
  }
})

// 결과 단계로 이동
const goToResultStep = () => {
  if (isAllTestsComplete.value) {
    quickScanStore.goToStep('result')
    router.push('/quickscan/result')
  }
}

// 이전 단계로 이동
const goBack = () => {
  router.push('/quickscan/start')
}
</script>

<style scoped>
.quickscan-test-page {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

.page-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.header-content h1 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 28px;
  font-weight: 700;
}

.subtitle {
  margin: 0;
  color: #7f8c8d;
  font-size: 16px;
}

.patient-info {
  text-align: right;
}

.patient-id {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  color: #6c757d;
  margin-bottom: 4px;
}

.patient-name {
  font-weight: 600;
  color: #2c3e50;
  font-size: 16px;
}

.progress-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.progress-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 18px;
  font-weight: 600;
}

.progress-count {
  font-weight: 600;
  color: #667eea;
  font-size: 16px;
}

.main-progress {
  height: 12px;
  border-radius: 6px;
  margin-bottom: 12px;
}

.progress-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #6c757d;
  font-weight: 500;
}

.completion-section {
  margin: 32px 0;
}

.completion-card {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  box-shadow: 0 8px 32px rgba(40, 167, 69, 0.3);
  border: 2px solid #28a745;
}

.completion-icon {
  margin-bottom: 16px;
}

.completion-card h3 {
  margin: 0 0 12px 0;
  color: #155724;
  font-size: 24px;
  font-weight: 700;
}

.completion-card p {
  margin: 0 0 24px 0;
  color: #155724;
  font-size: 16px;
}

.transmit-btn {
  height: 56px;
  font-size: 18px;
  font-weight: 600;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(40, 167, 69, 0.3);
}

.guide-section {
  margin: 32px 0;
}

.guide-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.guide-card h4 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 18px;
  font-weight: 600;
}

.guide-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.guide-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.guide-content {
  color: #6c757d;
  line-height: 1.5;
}

.guide-content strong {
  color: #2c3e50;
}

.navigation-section {
  margin-top: 32px;
  text-align: center;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .page-container {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 16px;
    text-align: center;
    padding: 20px;
  }
  
  .header-content h1 {
    font-size: 24px;
  }
  
  .patient-info {
    text-align: center;
  }
  
  .progress-section {
    padding: 20px;
  }
  
  .completion-card {
    padding: 24px;
  }
  
  .completion-card h3 {
    font-size: 20px;
  }
  
  .transmit-btn {
    height: 48px;
    font-size: 16px;
  }
  
  .guide-card {
    padding: 20px;
  }
}
</style> 