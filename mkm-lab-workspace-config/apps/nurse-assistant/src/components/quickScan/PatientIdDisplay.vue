<template>
  <div class="patient-id-display">
    <div class="id-container">
      <div class="id-label">비식별 환자 코드</div>
      <div class="id-code" :class="{ 'generating': isGenerating }">
        {{ patientId || '생성 중...' }}
      </div>
      <div class="id-info">
        <q-icon name="info" size="sm" />
        <span>이 코드로 검사 데이터가 관리됩니다</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useQuickScanStore } from '@/stores/quickScan'

const quickScanStore = useQuickScanStore()

const patientId = computed(() => quickScanStore.patientId)
const isGenerating = computed(() => !patientId.value)
</script>

<style scoped>
.patient-id-display {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 24px;
  margin: 16px 0;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.id-container {
  text-align: center;
}

.id-label {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.id-code {
  font-family: 'Courier New', monospace;
  font-size: 24px;
  font-weight: bold;
  color: white;
  background: rgba(255, 255, 255, 0.1);
  padding: 16px 24px;
  border-radius: 12px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  margin: 12px 0;
  letter-spacing: 2px;
  transition: all 0.3s ease;
}

.id-code.generating {
  animation: pulse 1.5s infinite;
  opacity: 0.7;
}

.id-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 12px;
  margin-top: 8px;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.7;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.02);
  }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .patient-id-display {
    padding: 16px;
    margin: 12px 0;
  }
  
  .id-code {
    font-size: 18px;
    padding: 12px 16px;
    letter-spacing: 1px;
  }
  
  .id-label {
    font-size: 12px;
  }
}
</style> 