<template>
  <q-page class="flex flex-center bg-grey-1">
    <div class="column q-gutter-lg" style="width: 100%; max-width: 600px; padding: 20px;">
      <!-- 완료 상태 표시 -->
      <q-card flat bordered class="bg-green-1">
        <q-card-section class="text-center">
          <q-icon name="check_circle" size="120px" color="green" class="q-mb-md" />
          <h4 class="text-h4 text-green q-my-md">수집 완료!</h4>
          <p class="text-body1 text-grey-7">모든 진단 데이터가 성공적으로 수집되었습니다</p>
          <q-linear-progress :value="1.0" color="green" size="8px" class="q-mt-md" />
          <div class="text-caption text-grey-6 q-mt-xs">4/4 단계 완료</div>
        </q-card-section>
      </q-card>

      <!-- 환자 정보 요약 -->
      <q-card flat bordered>
        <q-card-section>
          <div class="text-h6 q-mb-md">
            <q-icon name="person" class="q-mr-sm" />
            환자 정보
          </div>
          <div class="patient-summary">
            <div class="row q-gutter-md">
              <div class="col">
                <div class="info-item">
                  <span class="label">이름:</span>
                  <span class="value">{{ patientInfo.name || '-' }}</span>
                </div>
              </div>
              <div class="col">
                <div class="info-item">
                  <span class="label">나이:</span>
                  <span class="value">{{ patientInfo.age || '-' }}세</span>
                </div>
              </div>
            </div>
            <div class="row q-gutter-md q-mt-sm">
              <div class="col">
                <div class="info-item">
                  <span class="label">성별:</span>
                  <span class="value">{{ getGenderText(patientInfo.gender) }}</span>
                </div>
              </div>
              <div class="col">
                <div class="info-item">
                  <span class="label">수집 시간:</span>
                  <span class="value">{{ formatDateTime(completionTime) }}</span>
                </div>
              </div>
            </div>
            <div class="q-mt-sm">
              <div class="info-item">
                <span class="label">주소증:</span>
                <span class="value">{{ patientInfo.chiefComplaint || '-' }}</span>
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- 수집된 데이터 요약 -->
      <q-card flat bordered>
        <q-card-section>
          <div class="text-h6 q-mb-md">
            <q-icon name="data_usage" class="q-mr-sm" />
            수집 데이터
          </div>
          <q-list>
            <!-- 설진 -->
            <q-item>
              <q-item-section avatar>
                <q-avatar :color="diagnosisData.tongue.image ? 'green' : 'grey'" text-color="white">
                  <q-icon name="psychology" />
                </q-avatar>
              </q-item-section>
              <q-item-section>
                <q-item-label>설진 (혀 상태)</q-item-label>
                <q-item-label caption>
                  {{ diagnosisData.tongue.image ? '이미지 수집 완료' : '수집되지 않음' }}
                  {{ diagnosisData.tongue.timestamp ? '• ' + formatTime(diagnosisData.tongue.timestamp) : '' }}
                </q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-chip
                  :color="diagnosisData.tongue.image ? 'green' : 'grey'"
                  text-color="white"
                  size="sm"
                >
                  {{ diagnosisData.tongue.image ? '완료' : '미완료' }}
                </q-chip>
              </q-item-section>
            </q-item>

            <!-- 면진 -->
            <q-item>
              <q-item-section avatar>
                <q-avatar :color="diagnosisData.face.image ? 'green' : 'grey'" text-color="white">
                  <q-icon name="face" />
                </q-avatar>
              </q-item-section>
              <q-item-section>
                <q-item-label>면진 (얼굴 상태)</q-item-label>
                <q-item-label caption>
                  {{ diagnosisData.face.image ? '이미지 수집 완료' : '수집되지 않음' }}
                  {{ diagnosisData.face.timestamp ? '• ' + formatTime(diagnosisData.face.timestamp) : '' }}
                </q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-chip
                  :color="diagnosisData.face.image ? 'green' : 'grey'"
                  text-color="white"
                  size="sm"
                >
                  {{ diagnosisData.face.image ? '완료' : '미완료' }}
                </q-chip>
              </q-item-section>
            </q-item>

            <!-- 성진 -->
            <q-item>
              <q-item-section avatar>
                <q-avatar :color="diagnosisData.voice.audio ? 'green' : 'grey'" text-color="white">
                  <q-icon name="record_voice_over" />
                </q-avatar>
              </q-item-section>
              <q-item-section>
                <q-item-label>성진 (음성 상태)</q-item-label>
                <q-item-label caption>
                  {{ diagnosisData.voice.audio ? `음성 수집 완료 (${diagnosisData.voice.duration}초)` : '수집되지 않음' }}
                  {{ diagnosisData.voice.timestamp ? '• ' + formatTime(diagnosisData.voice.timestamp) : '' }}
                </q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-chip
                  :color="diagnosisData.voice.audio ? 'green' : 'grey'"
                  text-color="white"
                  size="sm"
                >
                  {{ diagnosisData.voice.audio ? '완료' : '미완료' }}
                </q-chip>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>

      <!-- 품질 평가 -->
      <q-card flat bordered class="bg-blue-1">
        <q-card-section>
          <div class="text-h6 q-mb-md">
            <q-icon name="assessment" color="blue" class="q-mr-sm" />
            데이터 품질 평가
          </div>
          <div class="quality-summary">
            <div class="overall-quality">
              <div class="text-h5 text-primary">{{ overallQuality.toFixed(1) }}/5.0</div>
              <div class="text-caption text-grey-6">종합 품질 점수</div>
            </div>
            <q-separator vertical class="q-mx-md" />
            <div class="quality-details">
              <div class="quality-item">
                <span>설진:</span>
                <q-rating
                  :model-value="tongueQuality"
                  readonly
                  size="sm"
                  color="orange"
                />
              </div>
              <div class="quality-item">
                <span>면진:</span>
                <q-rating
                  :model-value="faceQuality"
                  readonly
                  size="sm"
                  color="blue"
                />
              </div>
              <div class="quality-item">
                <span>성진:</span>
                <q-rating
                  :model-value="voiceQuality"
                  readonly
                  size="sm"
                  color="purple"
                />
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- 액션 버튼 -->
      <div class="column q-gutter-md">
        <!-- 메인 액션 -->
        <div class="row q-gutter-md">
          <q-btn
            size="lg"
            color="primary"
            icon="cloud_upload"
            label="서버 전송"
            class="col"
            :loading="isUploading"
            @click="uploadData"
          />
          <q-btn
            size="lg"
            color="positive"
            icon="save"
            label="로컬 저장"
            class="col"
            @click="saveLocally"
          />
        </div>

        <!-- 추가 액션 -->
        <div class="row q-gutter-md">
          <q-btn
            flat
            color="orange"
            icon="edit"
            label="수정하기"
            class="col"
            @click="editData"
          />
          <q-btn
            flat
            color="grey-7"
            icon="share"
            label="공유"
            class="col"
            @click="shareData"
          />
        </div>

        <!-- 새 환자 시작 -->
        <q-btn
          size="lg"
          color="secondary"
          icon="person_add"
          label="새 환자 시작"
          class="full-width q-mt-lg"
          @click="startNewPatient"
        />
      </div>

      <!-- 성공 메시지 -->
      <q-card v-if="uploadSuccess" flat class="bg-green-1">
        <q-card-section class="text-center">
          <q-icon name="cloud_done" color="green" class="q-mr-sm" />
          <span class="text-green">데이터가 성공적으로 서버에 전송되었습니다!</span>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePatientStore } from '../stores/patient.js'
import { useQuasar } from 'quasar'

const router = useRouter()
const patientStore = usePatientStore()
const $q = useQuasar()

// 상태
const isUploading = ref(false)
const uploadSuccess = ref(false)
const completionTime = ref(new Date())

// 환자 정보 및 진단 데이터
const patientInfo = computed(() => patientStore.patientInfo)
const diagnosisData = computed(() => patientStore.diagnosisData)

// 품질 점수 계산
const tongueQuality = computed(() => {
  const quality = diagnosisData.value.tongue.quality
  if (!quality) return 0
  return (quality.brightness + quality.clarity + quality.coverage) / 3
})

const faceQuality = computed(() => {
  const analysis = diagnosisData.value.face.analysis
  if (!analysis) return 0
  return (analysis.complexion + analysis.expression + analysis.quality) / 3
})

const voiceQuality = computed(() => {
  const analysis = diagnosisData.value.voice.analysis
  if (!analysis) return 0
  return (analysis.volume + analysis.clarity + analysis.duration) / 3
})

const overallQuality = computed(() => {
  const scores = [tongueQuality.value, faceQuality.value, voiceQuality.value].filter(score => score > 0)
  if (scores.length === 0) return 0
  return scores.reduce((sum, score) => sum + score, 0) / scores.length
})

// 유틸리티 함수
const getGenderText = (gender) => {
  const texts = {
    'male': '남성',
    'female': '여성'
  }
  return texts[gender] || '-'
}

const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  return new Date(timestamp).toLocaleTimeString('ko-KR', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 서버 전송
const uploadData = async () => {
  isUploading.value = true
  uploadSuccess.value = false

  try {
    // TODO: 실제 서버 API 호출
    await new Promise(resolve => setTimeout(resolve, 2000)) // 시뮬레이션

    uploadSuccess.value = true

    $q.notify({
      type: 'positive',
      message: '데이터가 성공적으로 서버에 전송되었습니다.',
      position: 'top'
    })

    // 세션 완료 처리
    await patientStore.completeSession()

  } catch (error) {
    console.error('데이터 업로드 실패:', error)
    $q.notify({
      type: 'negative',
      message: '서버 전송 중 오류가 발생했습니다.',
      position: 'top'
    })
  } finally {
    isUploading.value = false
  }
}

// 로컬 저장
const saveLocally = async () => {
  try {
    // TODO: 로컬 스토리지 또는 IndexedDB에 저장
    const data = {
      patientInfo: patientInfo.value,
      diagnosisData: diagnosisData.value,
      completionTime: completionTime.value
    }

    localStorage.setItem(`patient_${patientInfo.value.id}`, JSON.stringify(data))

    $q.notify({
      type: 'positive',
      message: '데이터가 로컬에 저장되었습니다.',
      position: 'top'
    })
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: '로컬 저장 중 오류가 발생했습니다.',
      position: 'top'
    })
  }
}

// 데이터 수정
const editData = () => {
  $q.dialog({
    title: '데이터 수정',
    message: '어떤 단계를 수정하시겠습니까?',
    options: {
      type: 'radio',
      model: 'patient-info',
      items: [
        { label: '환자 정보', value: 'patient-info' },
        { label: '설진 촬영', value: 'tongue-diagnosis' },
        { label: '면진 촬영', value: 'face-diagnosis' },
        { label: '성진 녹음', value: 'voice-diagnosis' }
      ]
    },
    cancel: true,
    persistent: true
  }).onOk(data => {
    router.push(`/${data}`)
  })
}

// 데이터 공유
const shareData = () => {
  if (navigator.share) {
    navigator.share({
      title: 'MKM Lab 진단 데이터',
      text: `${patientInfo.value.name} 환자의 진단 데이터`,
      url: window.location.href
    })
  } else {
    $q.notify({
      message: '공유 기능이 지원되지 않는 브라우저입니다.',
      position: 'top'
    })
  }
}

// 새 환자 시작
const startNewPatient = () => {
  $q.dialog({
    title: '새 환자',
    message: '현재 세션을 종료하고 새 환자를 시작하시겠습니까?',
    cancel: true,
    persistent: true
  }).onOk(async () => {
    await patientStore.resetSession()
    router.push('/')
  })
}

// 생명주기
onMounted(() => {
  // 완료 시간 설정
  completionTime.value = new Date()
})
</script>

<style scoped>
.patient-summary {
  padding: 16px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 8px;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 4px;
}

.info-item .label {
  font-weight: 500;
  color: #666;
  margin-right: 8px;
  min-width: 60px;
}

.info-item .value {
  color: #333;
}

.quality-summary {
  display: flex;
  align-items: center;
  padding: 16px;
  background: rgba(25, 118, 210, 0.05);
  border-radius: 8px;
}

.overall-quality {
  text-align: center;
}

.quality-details {
  flex: 1;
}

.quality-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.quality-item span {
  font-weight: 500;
  color: #666;
  min-width: 40px;
}

.full-width {
  width: 100%;
}
</style>
