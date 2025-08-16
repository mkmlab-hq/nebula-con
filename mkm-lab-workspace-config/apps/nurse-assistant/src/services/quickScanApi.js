// MKM QuickScan API 서비스
// 비식별화된 검사 데이터를 MKM Assist 대시보드로 안전하게 전송

class QuickScanApiService {
  constructor() {
    // TODO: 실제 API 엔드포인트 설정
    this.baseUrl = process.env.VUE_APP_API_BASE_URL || 'http://localhost:3000/api'
    this.quickScanEndpoint = '/quickscan/transmit'
  }
  
  // === 데이터 전송 메서드 ===
  
  /**
   * 검사 데이터를 MKM Assist 대시보드로 전송
   * @param {Object} transmissionData - 전송할 데이터
   * @returns {Promise<Object>} 전송 결과
   */
  async transmitScanData(transmissionData) {
    try {
      // 1. 데이터 검증
      this.validateTransmissionData(transmissionData)
      
      // 2. 데이터 암호화 (TODO: 실제 암호화 구현)
      const encryptedData = this.encryptData(transmissionData)
      
      // 3. API 전송
      const response = await fetch(`${this.baseUrl}${this.quickScanEndpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-QuickScan-Version': '1.0',
          'X-Device-Type': 'nurse-assistant'
        },
        body: JSON.stringify({
          encryptedData,
          metadata: {
            timestamp: new Date().toISOString(),
            deviceId: this.getDeviceId(),
            appVersion: '1.0.0'
          }
        })
      })
      
      if (!response.ok) {
        throw new Error(`전송 실패: ${response.status} ${response.statusText}`)
      }
      
      const result = await response.json()
      
      // 4. 전송 성공 로그
      console.log('QuickScan 데이터 전송 성공:', {
        patientId: transmissionData.patientId,
        timestamp: new Date().toISOString(),
        result
      })
      
      return {
        success: true,
        message: '검사 데이터가 한의사 대시보드로 성공적으로 전송되었습니다.',
        transmissionId: result.transmissionId,
        timestamp: result.timestamp
      }
      
    } catch (error) {
      console.error('QuickScan 데이터 전송 실패:', error)
      
      return {
        success: false,
        message: '데이터 전송에 실패했습니다. 다시 시도해주세요.',
        error: error.message
      }
    }
  }
  
  // === 데이터 검증 ===
  
  /**
   * 전송 데이터 유효성 검증
   * @param {Object} data - 검증할 데이터
   */
  validateTransmissionData(data) {
    const required = ['patientId', 'sessionStartTime', 'basicInfo', 'testResults']
    
    for (const field of required) {
      if (!data[field]) {
        throw new Error(`필수 필드 누락: ${field}`)
      }
    }
    
    // 비식별 코드 형식 검증
    if (!data.patientId.startsWith('TEMP_')) {
      throw new Error('잘못된 비식별 코드 형식')
    }
    
    // 기본 정보 검증
    if (!data.basicInfo.nickname || !data.basicInfo.gender || !data.basicInfo.ageGroup) {
      throw new Error('기본 정보가 불완전합니다')
    }
    
    // 검사 결과 검증
    const testTypes = ['tongue', 'face', 'voice']
    for (const testType of testTypes) {
      if (!data.testResults[testType] || data.testResults[testType].quality !== 'ok') {
        throw new Error(`${testType} 검사가 완료되지 않았습니다`)
      }
    }
  }
  
  // === 데이터 암호화 (시뮬레이션) ===
  
  /**
   * 데이터 암호화 (실제 구현 시 보안 라이브러리 사용)
   * @param {Object} data - 암호화할 데이터
   * @returns {Object} 암호화된 데이터
   */
  encryptData(data) {
    // TODO: 실제 암호화 구현
    // 현재는 시뮬레이션용 base64 인코딩
    return {
      encrypted: btoa(JSON.stringify(data)),
      algorithm: 'simulation-base64',
      timestamp: new Date().toISOString()
    }
  }
  
  // === 디바이스 정보 ===
  
  /**
   * 디바이스 ID 생성/가져오기
   * @returns {String} 디바이스 ID
   */
  getDeviceId() {
    let deviceId = localStorage.getItem('mkm-quickscan-device-id')
    
    if (!deviceId) {
      deviceId = `DEVICE_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`
      localStorage.setItem('mkm-quickscan-device-id', deviceId)
    }
    
    return deviceId
  }
  
  // === 연결 상태 확인 ===
  
  /**
   * 서버 연결 상태 확인
   * @returns {Promise<Boolean>} 연결 가능 여부
   */
  async checkConnection() {
    try {
      const response = await fetch(`${this.baseUrl}/health`, {
        method: 'GET',
        timeout: 5000
      })
      
      return response.ok
    } catch (error) {
      console.warn('서버 연결 확인 실패:', error)
      return false
    }
  }
  
  // === 오프라인 모드 지원 ===
  
  /**
   * 오프라인 대기열에 데이터 추가
   * @param {Object} data - 저장할 데이터
   */
  addToOfflineQueue(data) {
    try {
      const queue = this.getOfflineQueue()
      queue.push({
        data,
        timestamp: new Date().toISOString(),
        retryCount: 0
      })
      
      localStorage.setItem('mkm-quickscan-offline-queue', JSON.stringify(queue))
      console.log('오프라인 대기열에 추가됨:', data.patientId)
    } catch (error) {
      console.error('오프라인 대기열 저장 실패:', error)
    }
  }
  
  /**
   * 오프라인 대기열 가져오기
   * @returns {Array} 대기열 데이터
   */
  getOfflineQueue() {
    try {
      const queue = localStorage.getItem('mkm-quickscan-offline-queue')
      return queue ? JSON.parse(queue) : []
    } catch (error) {
      console.error('오프라인 대기열 읽기 실패:', error)
      return []
    }
  }
  
  /**
   * 오프라인 대기열 처리
   * @returns {Promise<Number>} 처리된 항목 수
   */
  async processOfflineQueue() {
    const queue = this.getOfflineQueue()
    let processedCount = 0
    
    for (let i = queue.length - 1; i >= 0; i--) {
      const item = queue[i]
      
      try {
        const result = await this.transmitScanData(item.data)
        
        if (result.success) {
          queue.splice(i, 1) // 성공한 항목 제거
          processedCount++
        } else {
          item.retryCount++
          if (item.retryCount >= 3) {
            queue.splice(i, 1) // 3회 실패 시 제거
          }
        }
      } catch (error) {
        item.retryCount++
        if (item.retryCount >= 3) {
          queue.splice(i, 1)
        }
      }
    }
    
    // 업데이트된 대기열 저장
    localStorage.setItem('mkm-quickscan-offline-queue', JSON.stringify(queue))
    
    return processedCount
  }
}

// 싱글톤 인스턴스 생성
const quickScanApi = new QuickScanApiService()

export default quickScanApi 