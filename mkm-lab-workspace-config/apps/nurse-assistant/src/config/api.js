// API 설정
export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000',
  environment: import.meta.env.VITE_APP_ENV || 'development',
  endpoints: {
    // 4대 진단법 API 엔드포인트
    tongue: '/api/diagnosis/tongue',
    face: '/api/diagnosis/face',
    voice: '/api/diagnosis/voice',
    pulse: '/api/diagnosis/pulse',

    // 환자 정보 API
    patients: '/api/patients',

    // 진단 결과 API
    results: '/api/results'
  }
}

// API 호출 헬퍼 함수
export const apiCall = async (endpoint, options = {}) => {
  const url = `${API_CONFIG.baseURL}${endpoint}`

  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  }

  const response = await fetch(url, { ...defaultOptions, ...options })

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`)
  }

  return response.json()
}

export default API_CONFIG
