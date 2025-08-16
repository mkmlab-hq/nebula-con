import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useQuickScanStore = defineStore('quickScan', () => {
  // === 비식별 환자 ID 관리 ===
  const patientId = ref('')
  const sessionStartTime = ref(null)
  
  // === 기본 정보 (비식별화) ===
  const basicInfo = ref({
    nickname: '', // 가명 또는 초성 (예: '김환자', '김ㅊㅊ')
    gender: '', // 'male' | 'female'
    ageGroup: '', // '20s' | '30s' | '40s' | '50s' | '60s+'
    mainSymptoms: [] // 주요 증상 키워드 배열 (예: ['요통', '두통'])
  })
  
  // === 3대 검사 결과 ===
  const testResults = ref({
    tongue: {
      image: null,
      quality: 'pending', // 'pending' | 'ok' | 'retry'
      aiData: null
    },
    face: {
      image: null,
      quality: 'pending',
      aiData: null
    },
    voice: {
      audio: null,
      quality: 'pending',
      aiData: null
    }
  })
  
  // === 검사 진행 상태 ===
  const currentStep = ref('start') // 'start' | 'test' | 'result'
  const isTransmitting = ref(false)
  const transmissionComplete = ref(false)
  
  // === Computed Properties ===
  const isBasicInfoComplete = computed(() => {
    return basicInfo.value.nickname && basicInfo.value.gender && basicInfo.value.ageGroup
  })
  
  const isAllTestsComplete = computed(() => {
    return testResults.value.tongue.quality === 'ok' &&
           testResults.value.face.quality === 'ok' &&
           testResults.value.voice.quality === 'ok'
  })
  
  const canProceedToTest = computed(() => {
    return patientId.value && isBasicInfoComplete.value
  })
  
  const canTransmit = computed(() => {
    return isAllTestsComplete.value && !isTransmitting.value
  })
  
  // === Actions ===
  
  // 비식별 환자 ID 생성
  const generatePatientId = () => {
    const now = new Date()
    const dateStr = now.getFullYear().toString() +
                   (now.getMonth() + 1).toString().padStart(2, '0') +
                   now.getDate().toString().padStart(2, '0')
    const timeStr = now.getHours().toString().padStart(2, '0') +
                   now.getMinutes().toString().padStart(2, '0') +
                   now.getSeconds().toString().padStart(2, '0')
    const randomStr = Math.random().toString(36).substring(2, 8).toUpperCase()
    
    patientId.value = `TEMP_${dateStr}_${timeStr}_${randomStr}`
    sessionStartTime.value = now
  }
  
  // 새 환자 시작 (세션 초기화)
  const startNewPatient = () => {
    generatePatientId()
    basicInfo.value = {
      nickname: '',
      gender: '',
      ageGroup: '',
      mainSymptoms: []
    }
    testResults.value = {
      tongue: { image: null, quality: 'pending', aiData: null },
      face: { image: null, quality: 'pending', aiData: null },
      voice: { audio: null, quality: 'pending', aiData: null }
    }
    currentStep.value = 'start'
    isTransmitting.value = false
    transmissionComplete.value = false
  }
  
  // 기본 정보 업데이트
  const updateBasicInfo = (info) => {
    basicInfo.value = { ...basicInfo.value, ...info }
  }
  
  // 증상 키워드 추가/제거
  const addSymptom = (symptom) => {
    if (!basicInfo.value.mainSymptoms.includes(symptom)) {
      basicInfo.value.mainSymptoms.push(symptom)
    }
  }
  
  const removeSymptom = (symptom) => {
    const index = basicInfo.value.mainSymptoms.indexOf(symptom)
    if (index > -1) {
      basicInfo.value.mainSymptoms.splice(index, 1)
    }
  }
  
  // 검사 결과 업데이트
  const updateTestResult = (testType, data) => {
    testResults.value[testType] = { ...testResults.value[testType], ...data }
  }
  
  // 검사 품질 설정
  const setTestQuality = (testType, quality) => {
    testResults.value[testType].quality = quality
  }
  
  // 단계 이동
  const goToStep = (step) => {
    currentStep.value = step
  }
  
  // 데이터 전송 시작
  const startTransmission = async () => {
    isTransmitting.value = true
    transmissionComplete.value = false
    
    try {
      // TODO: 실제 API 호출 구현
      const transmissionData = {
        patientId: patientId.value,
        sessionStartTime: sessionStartTime.value,
        basicInfo: basicInfo.value,
        testResults: testResults.value
      }
      
      console.log('전송 데이터:', transmissionData)
      
      // 시뮬레이션: 2초 후 전송 완료
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      transmissionComplete.value = true
      isTransmitting.value = false
      
      // 전송 완료 후 로컬 데이터 즉시 폐기
      setTimeout(() => {
        clearSessionData()
      }, 3000) // 3초 후 폐기
      
    } catch (error) {
      console.error('전송 실패:', error)
      isTransmitting.value = false
    }
  }
  
  // 세션 데이터 완전 폐기
  const clearSessionData = () => {
    patientId.value = ''
    sessionStartTime.value = null
    basicInfo.value = {
      nickname: '',
      gender: '',
      ageGroup: '',
      mainSymptoms: []
    }
    testResults.value = {
      tongue: { image: null, quality: 'pending', aiData: null },
      face: { image: null, quality: 'pending', aiData: null },
      voice: { audio: null, quality: 'pending', aiData: null }
    }
    currentStep.value = 'start'
    isTransmitting.value = false
    transmissionComplete.value = false
  }
  
  return {
    // State
    patientId,
    sessionStartTime,
    basicInfo,
    testResults,
    currentStep,
    isTransmitting,
    transmissionComplete,
    
    // Computed
    isBasicInfoComplete,
    isAllTestsComplete,
    canProceedToTest,
    canTransmit,
    
    // Actions
    generatePatientId,
    startNewPatient,
    updateBasicInfo,
    addSymptom,
    removeSymptom,
    updateTestResult,
    setTestQuality,
    goToStep,
    startTransmission,
    clearSessionData
  }
}) 