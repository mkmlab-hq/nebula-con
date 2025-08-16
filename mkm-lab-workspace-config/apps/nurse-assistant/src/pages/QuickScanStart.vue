<template>
  <q-page class="quickscan-start-page">
    <div class="page-container">
      <!-- 헤더 -->
      <div class="page-header">
        <div class="header-content">
          <h1>MKM QuickScan</h1>
          <p class="subtitle">빠른 검사 시작</p>
        </div>
        <div class="header-actions">
          <q-btn
            icon="refresh"
            label="새 환자 시작"
            color="primary"
            @click="startNewPatient"
            :loading="isGenerating"
          />
        </div>
      </div>
      
      <!-- 비식별 환자 ID 표시 -->
      <PatientIdDisplay />
      
      <!-- 기본 정보 입력 폼 -->
      <BasicInfoForm />
      
      <!-- 다음 단계 버튼 -->
      <div class="next-step-section">
        <q-btn
          label="검사 시작하기"
          color="primary"
          size="lg"
          class="next-step-btn"
          :disable="!canProceed"
          @click="goToTestStep"
        >
          <template v-slot:prepend>
            <q-icon name="arrow_forward" />
          </template>
        </q-btn>
        
        <div v-if="!canProceed" class="step-hint">
          <q-icon name="info" color="warning" size="sm" />
          <span>기본 정보를 모두 입력해주세요</span>
        </div>
      </div>
      
      <!-- 앱 정보 -->
      <div class="app-info">
        <div class="info-card">
          <h4>MKM QuickScan이란?</h4>
          <ul>
            <li>환자 개인정보 없이 빠른 검사</li>
            <li>설진, 면진, 음성 3대 검사 자동화</li>
            <li>검사 완료 후 즉시 한의사 대시보드 전송</li>
            <li>데이터 전송 후 자동 폐기로 개인정보 보호</li>
          </ul>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuickScanStore } from '@/stores/quickScan'
import PatientIdDisplay from '@/components/quickScan/PatientIdDisplay.vue'
import BasicInfoForm from '@/components/quickScan/BasicInfoForm.vue'

const router = useRouter()
const quickScanStore = useQuickScanStore()

// 상태 계산
const canProceed = computed(() => quickScanStore.canProceedToTest)
const isGenerating = computed(() => !quickScanStore.patientId)

// 새 환자 시작
const startNewPatient = () => {
  quickScanStore.startNewPatient()
}

// 검사 단계로 이동
const goToTestStep = () => {
  if (canProceed.value) {
    quickScanStore.goToStep('test')
    router.push('/quickscan/test')
  }
}

// 페이지 로드 시 자동으로 새 환자 시작
onMounted(() => {
  if (!quickScanStore.patientId) {
    startNewPatient()
  }
})
</script>

<style scoped>
.quickscan-start-page {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

.page-container {
  max-width: 800px;
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

.next-step-section {
  margin: 32px 0;
  text-align: center;
}

.next-step-btn {
  width: 100%;
  max-width: 400px;
  height: 56px;
  font-size: 18px;
  font-weight: 600;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.step-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
  color: #856404;
  font-size: 14px;
}

.app-info {
  margin-top: 40px;
}

.info-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.info-card h4 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  font-size: 18px;
  font-weight: 600;
}

.info-card ul {
  margin: 0;
  padding-left: 20px;
  color: #6c757d;
  line-height: 1.6;
}

.info-card li {
  margin-bottom: 8px;
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
  
  .next-step-btn {
    height: 48px;
    font-size: 16px;
  }
  
  .info-card {
    padding: 20px;
  }
}
</style> 