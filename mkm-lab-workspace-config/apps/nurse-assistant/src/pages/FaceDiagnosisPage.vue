<template>
  <q-page class="flex flex-center bg-grey-1">
    <div class="column q-gutter-md" style="width: 100%; max-width: 800px; padding: 20px;">
      <!-- 진행 상태 표시 -->
      <q-card flat bordered>
        <q-card-section class="text-center">
          <h5 class="text-h5 text-primary q-my-md">면진 촬영</h5>
          <p class="text-body2 text-grey-6">얼굴 전체를 정면에서 촬영해주세요</p>
          <q-linear-progress :value="0.66" color="primary" class="q-mt-md" />
          <div class="text-caption text-grey-6 q-mt-xs">3/4 단계</div>
        </q-card-section>
      </q-card>

      <!-- 카메라 영역 -->
      <q-card flat bordered>
        <q-card-section>
          <div class="camera-container">
            <!-- 카메라 프리뷰 -->
            <div v-if="!capturedImage" class="camera-preview">
              <video
                ref="videoElement"
                :class="{ 'mirrored': isFrontCamera }"
                autoplay
                playsinline
                muted
              ></video>

              <!-- 얼굴 가이드 오버레이 -->
              <div class="camera-overlay">
                <div class="face-guide-frame">
                  <div class="face-outline">
                    <div class="eye-guide left-eye"></div>
                    <div class="eye-guide right-eye"></div>
                    <div class="nose-guide"></div>
                    <div class="mouth-guide"></div>
                  </div>
                  <div class="guide-text">얼굴을 가이드에 맞춰주세요</div>
                </div>
              </div>

              <!-- 카메라 제어 버튼 -->
              <div class="camera-controls">
                <q-btn
                  v-if="hasMultipleCameras"
                  round
                  color="white"
                  text-color="dark"
                  icon="flip_camera_ios"
                  @click="switchCamera"
                  class="q-ma-sm"
                />
                <q-btn
                  round
                  color="primary"
                  icon="camera"
                  size="xl"
                  @click="capturePhoto"
                  :loading="isCapturing"
                  class="capture-btn"
                />
                <q-btn
                  round
                  color="white"
                  text-color="dark"
                  icon="timer"
                  @click="startTimer"
                  class="q-ma-sm"
                />
              </div>

              <!-- 타이머 표시 -->
              <div v-if="timerCount > 0" class="timer-overlay">
                <div class="timer-number">{{ timerCount }}</div>
              </div>
            </div>

            <!-- 촬영된 이미지 -->
            <div v-else class="captured-image-container">
              <img :src="capturedImage" alt="촬영된 얼굴 이미지" class="captured-image" />

              <!-- 이미지 제어 버튼 -->
              <div class="image-controls">
                <q-btn
                  flat
                  color="grey-7"
                  icon="refresh"
                  label="다시 촬영"
                  @click="retakePhoto"
                />
                <q-btn
                  color="positive"
                  icon="check"
                  label="확인"
                  @click="confirmPhoto"
                />
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- 면진 촬영 가이드 -->
      <q-card flat bordered class="bg-green-1">
        <q-card-section>
          <div class="text-h6 q-mb-md">
            <q-icon name="face" color="green" class="q-mr-sm" />
            면진 촬영 가이드
          </div>
          <q-list dense>
            <q-item>
              <q-item-section avatar>
                <q-icon name="visibility" color="green" />
              </q-item-section>
              <q-item-section>
                <q-item-label>정면을 바라보기</q-item-label>
                <q-item-label caption>카메라를 정면으로 바라보고 자연스러운 표정</q-item-label>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section avatar>
                <q-icon name="wb_sunny" color="green" />
              </q-item-section>
              <q-item-section>
                <q-item-label>균등한 조명</q-item-label>
                <q-item-label caption>얼굴에 그림자가 지지 않도록 조명 조절</q-item-label>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section avatar>
                <q-icon name="crop_portrait" color="green" />
              </q-item-section>
              <q-item-section>
                <q-item-label>얼굴 전체 포함</q-item-label>
                <q-item-label caption>이마부터 턱까지 얼굴 전체가 화면에 나오도록</q-item-label>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section avatar>
                <q-icon name="face_retouching_off" color="green" />
              </q-item-section>
              <q-item-section>
                <q-item-label>자연스러운 상태</q-item-label>
                <q-item-label caption>화장이나 마스크 착용 시 제거 후 촬영</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>

      <!-- 얼굴 분석 영역 -->
      <q-card v-if="capturedImage" flat bordered>
        <q-card-section>
          <div class="text-h6 q-mb-md">얼굴 분석 확인</div>
          <div class="row q-gutter-md">
            <div class="col">
              <div class="analysis-item">
                <q-icon name="colorize" color="orange" size="sm" />
                <span class="q-ml-sm">안색</span>
                <q-rating
                  v-model="faceAnalysis.complexion"
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
                <q-icon name="sentiment_neutral" color="blue" size="sm" />
                <span class="q-ml-sm">표정</span>
                <q-rating
                  v-model="faceAnalysis.expression"
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
                <q-icon name="center_focus_strong" color="green" size="sm" />
                <span class="q-ml-sm">촬영 품질</span>
                <q-rating
                  v-model="faceAnalysis.quality"
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
          icon="arrow_forward"
          label="다음"
          class="col"
          :loading="isLoading"
          @click="nextStep"
          :disable="!capturedImage || averageAnalysis < 3"
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
const videoElement = ref(null)

// 상태
const capturedImage = ref(null)
const isCapturing = ref(false)
const isLoading = ref(false)
const isFrontCamera = ref(true) // 면진은 기본적으로 전면 카메라
const hasMultipleCameras = ref(false)
const timerCount = ref(0)

// 카메라 스트림
let mediaStream = null
let currentDeviceId = null
let availableCameras = []
let timerInterval = null

// 얼굴 분석 데이터
const faceAnalysis = ref({
  complexion: 3,
  expression: 3,
  quality: 3
})

// 평균 분석 점수 계산
const averageAnalysis = computed(() => {
  const total = faceAnalysis.value.complexion + faceAnalysis.value.expression + faceAnalysis.value.quality
  return total / 3
})

// 카메라 초기화
const initCamera = async () => {
  try {
    // 사용 가능한 카메라 목록 가져오기
    const devices = await navigator.mediaDevices.enumerateDevices()
    availableCameras = devices.filter(device => device.kind === 'videoinput')
    hasMultipleCameras.value = availableCameras.length > 1

    // 전면 카메라 우선 선택
    const frontCamera = availableCameras.find(camera =>
      camera.label.toLowerCase().includes('front') ||
      camera.label.toLowerCase().includes('user')
    )
    if (frontCamera) {
      currentDeviceId = frontCamera.deviceId
    }

    // 카메라 스트림 시작
    await startCamera()
  } catch (error) {
    console.error('카메라 초기화 실패:', error)
    $q.notify({
      type: 'negative',
      message: '카메라에 접근할 수 없습니다. 권한을 확인해주세요.',
      position: 'top'
    })
  }
}

// 카메라 시작
const startCamera = async () => {
  try {
    const constraints = {
      video: {
        deviceId: currentDeviceId ? { exact: currentDeviceId } : undefined,
        width: { ideal: 1280 },
        height: { ideal: 720 },
        facingMode: isFrontCamera.value ? 'user' : 'environment'
      }
    }

    mediaStream = await navigator.mediaDevices.getUserMedia(constraints)

    if (videoElement.value) {
      videoElement.value.srcObject = mediaStream
    }
  } catch (error) {
    console.error('카메라 시작 실패:', error)
    throw error
  }
}

// 카메라 전환
const switchCamera = async () => {
  if (availableCameras.length < 2) return

  const currentIndex = availableCameras.findIndex(camera => camera.deviceId === currentDeviceId)
  const nextIndex = (currentIndex + 1) % availableCameras.length
  currentDeviceId = availableCameras[nextIndex].deviceId
  isFrontCamera.value = !isFrontCamera.value

  // 기존 스트림 정지
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop())
  }

  // 새 카메라로 시작
  await startCamera()
}

// 타이머 시작
const startTimer = () => {
  if (timerCount.value > 0) return

  timerCount.value = 3
  timerInterval = setInterval(() => {
    timerCount.value--
    if (timerCount.value === 0) {
      clearInterval(timerInterval)
      setTimeout(() => {
        capturePhoto()
      }, 500)
    }
  }, 1000)
}

// 사진 촬영
const capturePhoto = async () => {
  if (!videoElement.value || isCapturing.value) return

  isCapturing.value = true

  try {
    const canvas = document.createElement('canvas')
    const context = canvas.getContext('2d')

    canvas.width = videoElement.value.videoWidth
    canvas.height = videoElement.value.videoHeight

    // 전면 카메라인 경우 좌우 반전
    if (isFrontCamera.value) {
      context.scale(-1, 1)
      context.translate(-canvas.width, 0)
    }

    context.drawImage(videoElement.value, 0, 0)

    capturedImage.value = canvas.toDataURL('image/jpeg', 0.9)

    // 자동 얼굴 분석 (임시로 랜덤 값)
    faceAnalysis.value = {
      complexion: Math.floor(Math.random() * 2) + 3,  // 3-4
      expression: Math.floor(Math.random() * 2) + 3,  // 3-4
      quality: Math.floor(Math.random() * 2) + 3      // 3-4
    }

  } catch (error) {
    console.error('사진 촬영 실패:', error)
    $q.notify({
      type: 'negative',
      message: '사진 촬영에 실패했습니다.',
      position: 'top'
    })
  } finally {
    isCapturing.value = false
  }
}

// 다시 촬영
const retakePhoto = () => {
  capturedImage.value = null
  faceAnalysis.value = {
    complexion: 3,
    expression: 3,
    quality: 3
  }
}

// 사진 확인
const confirmPhoto = () => {
  if (averageAnalysis.value < 3) {
    $q.dialog({
      title: '품질 확인',
      message: '이미지 품질이 낮습니다. 다시 촬영하시겠습니까?',
      cancel: true,
      persistent: true
    }).onOk(() => {
      retakePhoto()
    })
    return
  }

  nextStep()
}

// 다음 단계
const nextStep = async () => {
  if (!capturedImage.value) return

  isLoading.value = true

  try {
    // 면진 데이터 저장
    await patientStore.updateDiagnosisData('face', {
      image: capturedImage.value,
      analysis: faceAnalysis.value,
      timestamp: new Date()
    })

    await patientStore.nextStep()

    $q.notify({
      type: 'positive',
      message: '면진 이미지가 저장되었습니다.',
      position: 'top'
    })

    router.push('/voice-diagnosis')
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: '이미지 저장 중 오류가 발생했습니다.',
      position: 'top'
    })
  } finally {
    isLoading.value = false
  }
}

// 이전 단계
const goBack = () => {
  router.push('/tongue-diagnosis')
}

// 생명주기
onMounted(() => {
  initCamera()
})

onUnmounted(() => {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop())
  }
  if (timerInterval) {
    clearInterval(timerInterval)
  }
})
</script>

<style scoped>
.camera-container {
  position: relative;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.camera-preview {
  position: relative;
  width: 100%;
  height: 400px;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
}

.camera-preview video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mirrored {
  transform: scaleX(-1);
}

.camera-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.face-guide-frame {
  width: 70%;
  height: 80%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.face-outline {
  width: 200px;
  height: 250px;
  border: 3px dashed rgba(255, 255, 255, 0.8);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  position: relative;
  margin-bottom: 20px;
}

.eye-guide {
  position: absolute;
  width: 15px;
  height: 10px;
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  top: 30%;
}

.left-eye {
  left: 25%;
}

.right-eye {
  right: 25%;
}

.nose-guide {
  position: absolute;
  width: 8px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 4px;
  top: 45%;
  left: 50%;
  transform: translateX(-50%);
}

.mouth-guide {
  position: absolute;
  width: 30px;
  height: 8px;
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 10px;
  bottom: 25%;
  left: 50%;
  transform: translateX(-50%);
}

.guide-text {
  color: white;
  background: rgba(0, 0, 0, 0.7);
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  text-align: center;
}

.camera-controls {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.capture-btn {
  margin: 0 20px;
}

.timer-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
}

.timer-number {
  font-size: 120px;
  font-weight: bold;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.captured-image-container {
  text-align: center;
}

.captured-image {
  width: 100%;
  max-width: 400px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.image-controls {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.analysis-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}
</style>
