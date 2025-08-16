<template>
  <q-page class="quickscan-result-page">
    <div class="page-container">
      <!-- 헤더 -->
      <div class="page-header">
        <div class="header-content">
          <h1>검사 완료</h1>
          <p class="subtitle">데이터 전송 및 결과 확인</p>
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
      
      <!-- 전송 상태 표시 -->
      <div class="transmission-section">
        <div v-if="!isTransmitting && !transmissionComplete" class="ready-card">
          <div class="ready-icon">
            <q-icon name="cloud_upload" color="primary" size="xl" />
          </div>
          <h3>전송 준비 완료</h3>
          <p>검사 데이터를 한의사 대시보드로 전송할 준비가 되었습니다.</p>
          
          <div class="data-summary">
            <h4>전송할 데이터</h4>
            <div class="summary-items">
              <div class="summary-item">
                <q-icon name="person" color="primary" />
                <span>기본 정보: {{ basicInfo.nickname }} ({{ getGenderText(basicInfo.gender) }}, {{ getAgeGroupText(basicInfo.ageGroup) }})</span>
              </div>
              <div class="summary-item">
                <q-icon name="visibility" color="positive" />
                <span>설진 촬영: 완료</span>
              </div>
              <div class="summary-item">
                <q-icon name="face" color="positive" />
                <span>얼굴 검사: 완료</span>
              </div>
              <div class="summary-item">
                <q-icon name="mic" color="positive" />
                <span>음성 녹음: 완료</span>
              </div>
              <div v-if="basicInfo.mainSymptoms.length > 0" class="summary-item">
                <q-icon name="healing" color="warning" />
                <span>주요 증상: {{ basicInfo.mainSymptoms.join(', ') }}</span>
              </div>
            </div>
          </div>
          
          <q-btn
            label="데이터 전송하기"
            color="primary"
            size="lg"
            class="transmit-btn"
            @click="startTransmission"
            :disable="!canTransmit"
          >
            <template v-slot:prepend>
              <q-icon name="send" />
            </template>
          </q-btn>
        </div>
        
        <!-- 전송 중 -->
        <div v-if="isTransmitting" class="transmitting-card">
          <div class="transmitting-icon">
            <q-spinner-dots color="primary" size="xl" />
          </div>
          <h3>데이터 전송 중...</h3>
          <p>한의사 대시보드로 검사 데이터를 안전하게 전송하고 있습니다.</p>
          
          <q-linear-progress
            indeterminate
            color="primary"
            size="lg"
            class="transmission-progress"
          />
          
          <div class="transmission-info">
            <q-icon name="security" color="positive" />
            <span>암호화된 안전한 전송</span>
          </div>
        </div>
        
        <!-- 전송 완료 -->
        <div v-if="transmissionComplete" class="success-card">
          <div class="success-icon">
            <q-icon name="check_circle" color="positive" size="xl" />
          </div>
          <h3>전송 완료!</h3>
          <p>{{ basicInfo.nickname }} 환자의 검사 데이터가 성공적으로 전송되었습니다.</p>
          
          <div class="success-details">
            <div class="detail-item">
              <q-icon name="schedule" color="primary" />
              <span>전송 시간: {{ getCurrentTime() }}</span>
            </div>
            <div class="detail-item">
              <q-icon name="code" color="primary" />
              <span>비식별 코드: {{ patientId }}</span>
            </div>
            <div class="detail-item">
              <q-icon name="delete_sweep" color="warning" />
              <span>로컬 데이터 자동 폐기 예정</span>
            </div>
          </div>
          
          <div class="next-actions">
            <q-btn
              label="새 환자 시작"
              color="primary"
              size="lg"
              class="new-patient-btn"
              @click="startNewPatient"
            >
              <template v-slot:prepend>
                <q-icon name="person_add" />
              </template>
            </q-btn>
            
            <q-btn
              label="홈으로 돌아가기"
              flat
              color="grey"
              @click="goHome"
            />
          </div>
        </div>
      </div>
      
      <!-- 개인정보 보호 안내 -->
      <div class="privacy-section">
        <div class="privacy-card">
          <h4>개인정보 보호 안내</h4>
          <div class="privacy-items">
            <div class="privacy-item">
              <q-icon name="security" color="positive" />
              <div class="privacy-content">
                <strong>비식별화:</strong> 환자의 실명, 주민번호 등 민감한 개인정보는 수집하지 않습니다.
              </div>
            </div>
            <div class="privacy-item">
              <q-icon name="cloud_upload" color="primary" />
              <div class="privacy-content">
                <strong>안전한 전송:</strong> 모든 데이터는 암호화되어 한의사 대시보드로 전송됩니다.
              </div>
            </div>
            <div class="privacy-item">
              <q-icon name="delete_forever" color="warning" />
              <div class="privacy-content">
                <strong>자동 폐기:</strong> 전송 완료 후 로컬 데이터는 즉시 자동 삭제됩니다.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuickScanStore } from '@/stores/quickScan'
import quickScanApi from '@/services/quickScanApi'

const router = useRouter()
const quickScanStore = useQuickScanStore()

// 상태 계산
const patientId = computed(() => quickScanStore.patientId)
const basicInfo = computed(() => quickScanStore.basicInfo)
const isTransmitting = computed(() => quickScanStore.isTransmitting)
const transmissionComplete = computed(() => quickScanStore.transmissionComplete)
const canTransmit = computed(() => quickScanStore.canTransmit)

// 페이지 접근 권한 확인
onMounted(() => {
  if (!quickScanStore.isAllTestsComplete) {
    router.push('/quickscan/test')
    return
  }
})

// 성별 텍스트 변환
const getGenderText = (gender) => {
  return gender === 'male' ? '남성' : '여성'
}

// 나이대 텍스트 변환
const getAgeGroupText = (ageGroup) => {
  const ageMap = {
    '20s': '20대',
    '30s': '30대',
    '40s': '40대',
    '50s': '50대',
    '60s+': '60대 이상'
  }
  return ageMap[ageGroup] || ageGroup
}

// 현재 시간 포맷
const getCurrentTime = () => {
  return new Date().toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 데이터 전송 시작
const startTransmission = async () => {
  if (!canTransmit.value) return
  
  try {
    const transmissionData = {
      patientId: patientId.value,
      sessionStartTime: quickScanStore.sessionStartTime,
      basicInfo: basicInfo.value,
      testResults: quickScanStore.testResults
    }
    
    const result = await quickScanApi.transmitScanData(transmissionData)
    
    if (result.success) {
      // 전송 성공 시 스토어에서 자동으로 처리됨
      console.log('전송 성공:', result)
    } else {
      // 전송 실패 시 오프라인 대기열에 추가
      quickScanApi.addToOfflineQueue(transmissionData)
      console.log('오프라인 대기열에 추가됨')
    }
  } catch (error) {
    console.error('전송 중 오류:', error)
  }
}

// 새 환자 시작
const startNewPatient = () => {
  quickScanStore.startNewPatient()
  router.push('/quickscan/start')
}

// 홈으로 이동
const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.quickscan-result-page {
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

.transmission-section {
  margin-bottom: 32px;
}

.ready-card,
.transmitting-card,
.success-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.ready-icon,
.transmitting-icon,
.success-icon {
  margin-bottom: 16px;
}

.ready-card h3,
.transmitting-card h3,
.success-card h3 {
  margin: 0 0 12px 0;
  color: #2c3e50;
  font-size: 24px;
  font-weight: 700;
}

.ready-card p,
.transmitting-card p,
.success-card p {
  margin: 0 0 24px 0;
  color: #6c757d;
  font-size: 16px;
  line-height: 1.5;
}

.data-summary {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  margin: 24px 0;
  text-align: left;
}

.data-summary h4 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
}

.summary-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #6c757d;
  font-size: 14px;
}

.transmit-btn {
  height: 56px;
  font-size: 18px;
  font-weight: 600;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.transmission-progress {
  margin: 24px 0;
  border-radius: 8px;
}

.transmission-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #28a745;
  font-size: 14px;
  font-weight: 500;
}

.success-details {
  background: #d4edda;
  border-radius: 12px;
  padding: 20px;
  margin: 24px 0;
  text-align: left;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  color: #155724;
  font-size: 14px;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.next-actions {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 24px;
}

.new-patient-btn {
  height: 56px;
  font-size: 18px;
  font-weight: 600;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(40, 167, 69, 0.3);
}

.privacy-section {
  margin-top: 32px;
}

.privacy-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.privacy-card h4 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 18px;
  font-weight: 600;
}

.privacy-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.privacy-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.privacy-content {
  color: #6c757d;
  line-height: 1.5;
  font-size: 14px;
}

.privacy-content strong {
  color: #2c3e50;
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
  
  .ready-card,
  .transmitting-card,
  .success-card {
    padding: 24px;
  }
  
  .ready-card h3,
  .transmitting-card h3,
  .success-card h3 {
    font-size: 20px;
  }
  
  .transmit-btn,
  .new-patient-btn {
    height: 48px;
    font-size: 16px;
  }
  
  .privacy-card {
    padding: 20px;
  }
}
</style> 