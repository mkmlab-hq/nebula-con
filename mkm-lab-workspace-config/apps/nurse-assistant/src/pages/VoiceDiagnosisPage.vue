<template>
  <q-page class="flex flex-center bg-grey-1">
    <div class="column q-gutter-md" style="width: 100%; max-width: 800px; padding: 20px;">
      <!-- 진행 상태 표시 -->
      <q-card flat bordered>
        <q-card-section class="text-center">
          <h5 class="text-h5 text-primary q-my-md">성진 녹음</h5>
          <p class="text-body2 text-grey-6">음성을 명확하게 녹음해주세요</p>
          <q-linear-progress :value="1.0" color="primary" class="q-mt-md" />
          <div class="text-caption text-grey-6 q-mt-xs">4/4 단계</div>
        </q-card-section>
      </q-card>

      <!-- 녹음 영역 -->
      <q-card flat bordered>
        <q-card-section>
          <div class="recording-container">
            <!-- 녹음 상태 표시 -->
            <div class="recording-status">
              <div class="audio-visualizer">
                <div
                  v-for="i in 20"
                  :key="i"
                  class="audio-bar"
                  :class="{ 'active': isRecording && i <= audioLevel }"
                ></div>
              </div>

              <div class="recording-info">
                <div v-if="!isRecording && !recordedAudio" class="ready-to-record">
                  <q-icon name="mic" size="80px" color="grey-5" />
                  <div class="text-h6 text-grey-6 q-mt-md">녹음 준비</div>
                </div>

                <div v-else-if="isRecording" class="recording-active">
                  <q-icon name="mic" size="80px" color="red" class="pulsing" />
                  <div class="text-h6 text-red q-mt-md">녹음 중...</div>
                  <div class="text-h4 text-primary q-mt-sm">{{ formatTime(recordingTime) }}</div>
                </div>

                <div v-else class="recording-complete">
                  <q-icon name="check_circle" size="80px" color="green" />
                  <div class="text-h6 text-green q-mt-md">녹음 완료</div>
                  <div class="text-body2 text-grey-6">{{ formatTime(audioDuration) }}</div>
                </div>
              </div>
            </div>

            <!-- 녹음 제어 버튼 -->
            <div class="recording-controls q-mt-lg">
              <div v-if="!recordedAudio" class="record-buttons">
                <q-btn
                  v-if="!isRecording"
                  round
                  color="red"
                  icon="mic"
                  size="xl"
                  @click="startRecording"
                  class="record-btn"
                />
                <q-btn
                  v-else
                  round
                  color="grey-7"
                  icon="stop"
                  size="xl"
                  @click="stopRecording"
                  class="record-btn"
                />
              </div>

              <div v-else class="playback-controls">
                <q-btn
                  round
                  :color="isPlaying ? 'orange' : 'primary'"
                  :icon="isPlaying ? 'pause' : 'play_arrow'"
                  size="lg"
                  @click="togglePlayback"
                  class="q-mr-md"
                />
                <q-btn
                  flat
                  color="grey-7"
                  icon="refresh"
                  label="다시 녹음"
                  @click="retakeRecording"
                />
              </div>
            </div>

            <!-- 오디오 플레이어 (숨김) -->
            <audio
              ref="audioPlayer"
              @ended="onAudioEnded"
              @timeupdate="onTimeUpdate"
            ></audio>
          </div>
        </q-card-section>
      </q-card>

      <!-- 성진 녹음 가이드 -->
      <q-card flat bordered class="bg-purple-1">
        <q-card-section>
          <div class="text-h6 q-mb-md">
            <q-icon name="record_voice_over" color="purple" class="q-mr-sm" />
            성진 녹음 가이드
          </div>
          <q-list dense>
            <q-item>
              <q-item-section avatar>
                <q-icon name="volume_up" color="purple" />
              </q-item-section>
              <q-item-section>
                <q-item-label>명확한 발음</q-item-label>
                <q-item-label caption>"아" 소리를 5초간 지속해주세요</q-item-label>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section avatar>
                <q-icon name="hearing" color="purple" />
              </q-item-section>
              <q-item-section>
                <q-item-label>조용한 환경</q-item-label>
                <q-item-label caption>주변 소음이 없는 곳에서 녹음</q-item-label>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section avatar>
                <q-icon name="mic_external_on" color="purple" />
              </q-item-section>
              <q-item-section>
                <q-item-label>적절한 거리</q-item-label>
                <q-item-label caption>마이크에서 10-15cm 거리 유지</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>

      <!-- 음성 분석 -->
      <q-card v-if="recordedAudio" flat bordered>
        <q-card-section>
          <div class="text-h6 q-mb-md">음성 분석</div>
          <div class="row q-gutter-md">
            <div class="col">
              <div class="analysis-item">
                <q-icon name="graphic_eq" color="blue" size="sm" />
                <span class="q-ml-sm">음량</span>
                <q-rating
                  v-model="voiceAnalysis.volume"
                  max="5"
                  size="sm"
                  color="blue"
                  class="q-ml-md"
                />
              </div>
            </div>
          </div>
          <div class="row q-gutter-md q-mt-sm">
            <div class="col">
              <div class="analysis-item">
                <q-icon name="tune" color="orange" size="sm" />
                <span class="q-ml-sm">음질</span>
                <q-rating
                  v-model="voiceAnalysis.clarity"
                  max="5"
                  size="sm"
                  color="orange"
                  class="q-ml-md"
                />
              </div>
            </div>
          </div>
          <div class="row q-gutter-md q-mt-sm">
            <div class="col">
              <div class="analysis-item">
                <q-icon name="timer" color="green" size="sm" />
                <span class="q-ml-sm">길이</span>
                <q-rating
                  v-model="voiceAnalysis.duration"
                  max="5"
                  size="sm"
                  color="green"
                  class="q-ml-md"
                />
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- 버튼 영역 -->
      <div class="row q-gutter-md">
        <q-btn
          flat
          color="grey-7"
          icon="arrow_back"
          label="이전"
          class="col"
          @click="goBack"
        />
        <q-btn
          color="primary"
          icon="check"
          label="완료"
          class="col"
          :loading="isLoading"
          @click="completeRecording"
          :disable="!recordedAudio || averageVoiceAnalysis < 3"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePatientStore } from '../stores/patient.js'
import { useQuasar } from 'quasar'

const router = useRouter()
const patientStore = usePatientStore()
const $q = useQuasar()

// 컴포넌트 참조
const audioPlayer = ref(null)

// 상태
const isRecording = ref(false)
const recordedAudio = ref(null)
const isPlaying = ref(false)
const isLoading = ref(false)
const recordingTime = ref(0)
const audioDuration = ref(0)
const audioLevel = ref(0)

// 미디어 레코더
let mediaRecorder = null
let audioChunks = []
let recordingInterval = null
let audioContext = null
let analyser = null
let microphone = null

// 음성 분석 데이터
const voiceAnalysis = ref({
  volume: 3,
  clarity: 3,
  duration: 3
})

// 평균 음성 분석 점수
const averageVoiceAnalysis = computed(() => {
  const total = voiceAnalysis.value.volume + voiceAnalysis.value.clarity + voiceAnalysis.value.duration
  return total / 3
})

// 시간 포맷팅
const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

// 마이크 초기화
const initMicrophone = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true
      }
    })

    // 오디오 컨텍스트 설정 (음성 시각화용)
    audioContext = new (window.AudioContext || window.webkitAudioContext)()
    analyser = audioContext.createAnalyser()
    microphone = audioContext.createMediaStreamSource(stream)
    microphone.connect(analyser)

    analyser.fftSize = 256

    // 미디어 레코더 설정
    mediaRecorder = new MediaRecorder(stream)

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data)
      }
    }

    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' })
      const audioUrl = URL.createObjectURL(audioBlob)
      recordedAudio.value = audioUrl

      // 오디오 재생기에 설정
      if (audioPlayer.value) {
        audioPlayer.value.src = audioUrl
      }

      // 음성 분석 수행
      analyzeVoice()

      audioChunks = []
    }

  } catch (error) {
    console.error('마이크 초기화 실패:', error)
    $q.notify({
      type: 'negative',
      message: '마이크에 접근할 수 없습니다. 권한을 확인해주세요.',
      position: 'top'
    })
  }
}

// 오디오 레벨 모니터링
const monitorAudioLevel = () => {
  if (!analyser) return

  const bufferLength = analyser.frequencyBinCount
  const dataArray = new Uint8Array(bufferLength)

  const updateLevel = () => {
    if (!isRecording.value) return

    analyser.getByteFrequencyData(dataArray)

    let sum = 0
    for (let i = 0; i < bufferLength; i++) {
      sum += dataArray[i]
    }
    const average = sum / bufferLength
    audioLevel.value = Math.floor((average / 255) * 20)

    requestAnimationFrame(updateLevel)
  }

  updateLevel()
}

// 녹음 시작
const startRecording = async () => {
  if (!mediaRecorder || mediaRecorder.state === 'recording') return

  try {
    recordingTime.value = 0
    audioChunks = []

    mediaRecorder.start()
    isRecording.value = true

    // 녹음 시간 카운터
    recordingInterval = setInterval(() => {
      recordingTime.value++
    }, 1000)

    // 오디오 레벨 모니터링 시작
    monitorAudioLevel()

    $q.notify({
      type: 'positive',
      message: '녹음을 시작합니다.',
      position: 'top'
    })

  } catch (error) {
    console.error('녹음 시작 실패:', error)
    $q.notify({
      type: 'negative',
      message: '녹음을 시작할 수 없습니다.',
      position: 'top'
    })
  }
}

// 녹음 중지
const stopRecording = () => {
  if (!mediaRecorder || mediaRecorder.state !== 'recording') return

  mediaRecorder.stop()
  isRecording.value = false
  audioLevel.value = 0

  if (recordingInterval) {
    clearInterval(recordingInterval)
  }

  audioDuration.value = recordingTime.value

  $q.notify({
    type: 'positive',
    message: '녹음이 완료되었습니다.',
    position: 'top'
  })
}

// 다시 녹음
const retakeRecording = () => {
  recordedAudio.value = null
  recordingTime.value = 0
  audioDuration.value = 0
  isPlaying.value = false

  voiceAnalysis.value = {
    volume: 3,
    clarity: 3,
    duration: 3
  }

  if (audioPlayer.value) {
    audioPlayer.value.pause()
    audioPlayer.value.currentTime = 0
  }
}

// 재생 토글
const togglePlayback = () => {
  if (!audioPlayer.value || !recordedAudio.value) return

  if (isPlaying.value) {
    audioPlayer.value.pause()
    isPlaying.value = false
  } else {
    audioPlayer.value.play()
    isPlaying.value = true
  }
}

// 오디오 재생 완료
const onAudioEnded = () => {
  isPlaying.value = false
}

// 재생 시간 업데이트
const onTimeUpdate = () => {
  // 필요 시 재생 진행률 표시
}

// 음성 분석
const analyzeVoice = () => {
  // 실제로는 오디오 분석 API 호출
  // 임시로 랜덤 값 생성
  const duration = audioDuration.value

  voiceAnalysis.value = {
    volume: Math.floor(Math.random() * 2) + 3,    // 3-4
    clarity: Math.floor(Math.random() * 2) + 3,   // 3-4
    duration: duration >= 3 && duration <= 10 ? 4 : 3  // 적절한 길이면 4, 아니면 3
  }
}

// 녹음 완료
const completeRecording = async () => {
  if (!recordedAudio.value) return

  isLoading.value = true

  try {
    // 성진 데이터 저장
    await patientStore.updateDiagnosisData('voice', {
      audio: recordedAudio.value,
      duration: audioDuration.value,
      analysis: voiceAnalysis.value,
      timestamp: new Date()
    })

    await patientStore.nextStep()

    $q.notify({
      type: 'positive',
      message: '음성 녹음이 저장되었습니다.',
      position: 'top'
    })

    router.push('/complete')
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: '음성 저장 중 오류가 발생했습니다.',
      position: 'top'
    })
  } finally {
    isLoading.value = false
  }
}

// 이전 단계
const goBack = () => {
  router.push('/face-diagnosis')
}

// 생명주기
onMounted(() => {
  initMicrophone()
})

onUnmounted(() => {
  if (recordingInterval) {
    clearInterval(recordingInterval)
  }
  if (audioContext) {
    audioContext.close()
  }
  if (mediaRecorder && mediaRecorder.stream) {
    mediaRecorder.stream.getTracks().forEach(track => track.stop())
  }
})
</script>

<style scoped>
.recording-container {
  text-align: center;
  padding: 20px;
}

.recording-status {
  margin-bottom: 30px;
}

.audio-visualizer {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  height: 60px;
  margin-bottom: 20px;
  gap: 2px;
}

.audio-bar {
  width: 4px;
  height: 10px;
  background: #e0e0e0;
  border-radius: 2px;
  transition: all 0.1s ease;
}

.audio-bar.active {
  background: #f44336;
  height: 40px;
}

.recording-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.pulsing {
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.recording-controls {
  display: flex;
  justify-content: center;
  align-items: center;
}

.record-btn {
  margin: 0 20px;
}

.playback-controls {
  display: flex;
  align-items: center;
  justify-content: center;
}

.analysis-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}
</style>
