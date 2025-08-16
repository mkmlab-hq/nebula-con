<template>
  <div class="basic-info-form">
    <div class="form-header">
      <h3>기본 정보 입력</h3>
      <p class="subtitle">개인정보 없이 간단하게 입력해주세요</p>
    </div>
    
    <div class="form-content">
      <!-- 가명 입력 -->
      <div class="form-group">
        <label class="form-label">
          <q-icon name="person" size="sm" />
          가명 또는 초성
        </label>
        <q-input
          v-model="formData.nickname"
          placeholder="예: 김환자, 김ㅊㅊ"
          outlined
          dense
          class="form-input"
          @update:model-value="updateForm"
        >
          <template v-slot:hint>
            실명 대신 가명이나 초성만 입력하세요
          </template>
        </q-input>
      </div>
      
      <!-- 성별 선택 -->
      <div class="form-group">
        <label class="form-label">
          <q-icon name="wc" size="sm" />
          성별
        </label>
        <div class="radio-group">
          <q-radio
            v-model="formData.gender"
            val="male"
            label="남성"
            @update:model-value="updateForm"
          />
          <q-radio
            v-model="formData.gender"
            val="female"
            label="여성"
            @update:model-value="updateForm"
          />
        </div>
      </div>
      
      <!-- 나이대 선택 -->
      <div class="form-group">
        <label class="form-label">
          <q-icon name="cake" size="sm" />
          나이대
        </label>
        <q-select
          v-model="formData.ageGroup"
          :options="ageGroupOptions"
          outlined
          dense
          class="form-input"
          @update:model-value="updateForm"
        />
      </div>
      
      <!-- 주요 증상 키워드 -->
      <div class="form-group">
        <label class="form-label">
          <q-icon name="healing" size="sm" />
          주요 증상 (선택사항)
        </label>
        <div class="symptom-input">
          <q-input
            v-model="newSymptom"
            placeholder="증상 키워드 입력 (예: 요통)"
            outlined
            dense
            class="form-input"
            @keyup.enter="addSymptom"
          >
            <template v-slot:append>
              <q-btn
                icon="add"
                flat
                round
                dense
                @click="addSymptom"
                :disable="!newSymptom.trim()"
              />
            </template>
          </q-input>
        </div>
        
        <!-- 증상 태그들 -->
        <div v-if="formData.mainSymptoms.length > 0" class="symptom-tags">
          <q-chip
            v-for="symptom in formData.mainSymptoms"
            :key="symptom"
            removable
            color="primary"
            text-color="white"
            @remove="removeSymptom(symptom)"
          >
            {{ symptom }}
          </q-chip>
        </div>
        
        <!-- 증상 예시 -->
        <div class="symptom-examples">
          <span class="example-label">자주 사용되는 증상:</span>
          <q-btn
            v-for="example in commonSymptoms"
            :key="example"
            flat
            dense
            size="sm"
            color="primary"
            @click="addSymptom(example)"
            class="example-btn"
          >
            {{ example }}
          </q-btn>
        </div>
      </div>
    </div>
    
    <!-- 완료 상태 표시 -->
    <div v-if="isComplete" class="completion-status">
      <q-icon name="check_circle" color="positive" size="lg" />
      <span>기본 정보 입력 완료</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useQuickScanStore } from '@/stores/quickScan'

const quickScanStore = useQuickScanStore()

// 폼 데이터
const formData = ref({
  nickname: '',
  gender: '',
  ageGroup: '',
  mainSymptoms: []
})

// 새 증상 입력
const newSymptom = ref('')

// 나이대 옵션
const ageGroupOptions = [
  { label: '20대', value: '20s' },
  { label: '30대', value: '30s' },
  { label: '40대', value: '40s' },
  { label: '50대', value: '50s' },
  { label: '60대 이상', value: '60s+' }
]

// 자주 사용되는 증상 예시
const commonSymptoms = [
  '요통', '두통', '소화불량', '피로', '불면',
  '어깨통증', '관절통', '소화불량', '스트레스'
]

// 완료 상태 계산
const isComplete = computed(() => {
  return formData.value.nickname && 
         formData.value.gender && 
         formData.value.ageGroup
})

// 폼 업데이트
const updateForm = () => {
  quickScanStore.updateBasicInfo(formData.value)
}

// 증상 추가
const addSymptom = (symptom = null) => {
  const symptomToAdd = symptom || newSymptom.value.trim()
  
  if (symptomToAdd && !formData.value.mainSymptoms.includes(symptomToAdd)) {
    formData.value.mainSymptoms.push(symptomToAdd)
    quickScanStore.addSymptom(symptomToAdd)
    newSymptom.value = ''
  }
}

// 증상 제거
const removeSymptom = (symptom) => {
  const index = formData.value.mainSymptoms.indexOf(symptom)
  if (index > -1) {
    formData.value.mainSymptoms.splice(index, 1)
    quickScanStore.removeSymptom(symptom)
  }
}

// 스토어에서 초기 데이터 로드
watch(() => quickScanStore.basicInfo, (newInfo) => {
  formData.value = { ...newInfo }
}, { immediate: true })
</script>

<style scoped>
.basic-info-form {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.form-header {
  text-align: center;
  margin-bottom: 24px;
}

.form-header h3 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 20px;
  font-weight: 600;
}

.subtitle {
  margin: 0;
  color: #7f8c8d;
  font-size: 14px;
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: #2c3e50;
  font-size: 14px;
}

.form-input {
  width: 100%;
}

.radio-group {
  display: flex;
  gap: 24px;
  margin-top: 8px;
}

.symptom-input {
  margin-bottom: 12px;
}

.symptom-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.symptom-examples {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.example-label {
  font-size: 12px;
  color: #6c757d;
  margin-right: 8px;
}

.example-btn {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 12px;
}

.completion-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 20px;
  padding: 16px;
  background: #d4edda;
  border-radius: 8px;
  color: #155724;
  font-weight: 500;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .basic-info-form {
    padding: 16px;
  }
  
  .form-header h3 {
    font-size: 18px;
  }
  
  .radio-group {
    flex-direction: column;
    gap: 12px;
  }
  
  .symptom-examples {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style> 