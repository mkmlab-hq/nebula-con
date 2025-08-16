import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiCall, API_CONFIG } from '../config/api.js'

export const usePatientStore = defineStore('patient', () => {
  // 상태 (State)
  const patientInfo = ref({
    id: '',
    name: '',
    age: '',
    gender: '',
    symptoms: [],
    chiefComplaint: ''
  })

  const diagnosisData = ref({
    tongue: {
      image: null,
      imageUrl: '',
      quality: null,
      timestamp: null
    },
    face: {
      image: null,
      imageUrl: '',
      quality: null,
      timestamp: null
    },
    voice: {
      audio: null,
      audioUrl: '',
      duration: 0,
      quality: null,
      timestamp: null
    }
  })

  const currentStep = ref(0)
  const isLoading = ref(false)
  const errors = ref({})

  // 계산된 속성 (Getters)
  const isPatientInfoComplete = computed(() => {
    return patientInfo.value.name &&
           patientInfo.value.age &&
           patientInfo.value.gender &&
           patientInfo.value.chiefComplaint
  })

  const completedSteps = computed(() => {
    let count = 0
    if (isPatientInfoComplete.value) count++
    if (diagnosisData.value.tongue.image) count++
    if (diagnosisData.value.face.image) count++
    if (diagnosisData.value.voice.audio) count++
    return count
  })

  const totalSteps = 4

  const progressPercentage = computed(() => {
    return (completedSteps.value / totalSteps) * 100
  })

  const canProceedToNext = computed(() => {
    switch (currentStep.value) {
      case 0: return isPatientInfoComplete.value
      case 1: return diagnosisData.value.tongue.image !== null
      case 2: return diagnosisData.value.face.image !== null
      case 3: return diagnosisData.value.voice.audio !== null
      default: return false
    }
  })

  // 액션 (Actions)
  const updatePatientInfo = (info) => {
    patientInfo.value = { ...patientInfo.value, ...info }
    clearError('patientInfo')
  }

  const updateTongueData = (data) => {
    diagnosisData.value.tongue = {
      ...diagnosisData.value.tongue,
      ...data,
      timestamp: new Date().toISOString()
    }
    clearError('tongue')
  }

  const updateFaceData = (data) => {
    diagnosisData.value.face = {
      ...diagnosisData.value.face,
      ...data,
      timestamp: new Date().toISOString()
    }
    clearError('face')
  }

  const updateVoiceData = (data) => {
    diagnosisData.value.voice = {
      ...diagnosisData.value.voice,
      ...data,
      timestamp: new Date().toISOString()
    }
    clearError('voice')
  }

  const nextStep = () => {
    if (currentStep.value < totalSteps - 1) {
      currentStep.value++
    }
  }

  const prevStep = () => {
    if (currentStep.value > 0) {
      currentStep.value--
    }
  }

  const setError = (field, message) => {
    errors.value[field] = message
  }

  const clearError = (field) => {
    if (errors.value[field]) {
      delete errors.value[field]
    }
  }

  const clearAllErrors = () => {
    errors.value = {}
  }

  const resetAll = () => {
    patientInfo.value = {
      id: '',
      name: '',
      age: '',
      gender: '',
      symptoms: [],
      chiefComplaint: ''
    }

    diagnosisData.value = {
      tongue: { image: null, imageUrl: '', quality: null, timestamp: null },
      face: { image: null, imageUrl: '', quality: null, timestamp: null },
      voice: { audio: null, audioUrl: '', duration: 0, quality: null, timestamp: null }
    }

    currentStep.value = 0
    isLoading.value = false
    clearAllErrors()
  }

  const generatePatientId = () => {
    const timestamp = new Date().toISOString().replace(/[-:]/g, '').split('.')[0]
    const random = Math.random().toString(36).substring(2, 6)
    return `MKM${timestamp}${random}`.toUpperCase()
  }

  // API 연동 준비
  const submitToServer = async () => {
    isLoading.value = true
    clearAllErrors()

    try {
      // 환자 ID 생성
      if (!patientInfo.value.id) {
        patientInfo.value.id = generatePatientId()
      }

      // 서버로 전송할 데이터 구성
      const payload = {
        patient: patientInfo.value,
        diagnosis: {
          tongue: diagnosisData.value.tongue,
          face: diagnosisData.value.face,
          voice: diagnosisData.value.voice
        },
        metadata: {
          collectedAt: new Date().toISOString(),
          deviceInfo: {
            userAgent: navigator.userAgent,
            platform: navigator.platform
          }
        }
      }

      // TODO: 실제 API 호출
      const response = await fetch('/api/patient-data/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })

      if (!response.ok) {
        throw new Error('데이터 전송에 실패했습니다')
      }

      const result = await response.json()
      return result

    } catch (error) {
      setError('submit', error.message)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  return {
    // State
    patientInfo,
    diagnosisData,
    currentStep,
    isLoading,
    errors,

    // Getters
    isPatientInfoComplete,
    completedSteps,
    totalSteps,
    progressPercentage,
    canProceedToNext,

    // Actions
    updatePatientInfo,
    updateTongueData,
    updateFaceData,
    updateVoiceData,
    nextStep,
    prevStep,
    setError,
    clearError,
    clearAllErrors,
    resetAll,
    generatePatientId,
    submitToServer
  }
})
