<template>
  <q-page class="flex flex-center bg-grey-1">
    <div class="column q-gutter-md" style="width: 100%; max-width: 800px; padding: 20px;">
      <!-- 진행 상태 표시 -->
      <q-card flat bordered>
        <q-card-section class="text-center">
          <h5 class="text-h5 text-primary q-my-md">설진 촬영</h5>
          <p class="text-body2 text-grey-6">혀 상태를 정확히 촬영해주세요</p>
          <q-linear-progress :value="0.33" color="primary" class="q-mt-md" />
          <div class="text-caption text-grey-6 q-mt-xs">2/4 단계</div>
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

              <!-- 가이드 오버레이 -->
              <div class="camera-overlay">
                <div class="guide-frame">
                  <div class="guide-text">혀를 이 영역에 맞춰 촬영해주세요</div>
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
                  icon="flash_on"
                  @click="toggleFlash"
                  class="q-ma-sm"
                  :color="flashEnabled ? 'orange' : 'white'"
                />
              </div>
            </div>

            <!-- 촬영된 이미지 -->
            <div v-else class="captured-image-container">
              <img :src="capturedImage" alt="촬영된 혀 이미지" class="captured-image" />

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

      <!-- 촬영 가이드 -->
      <q-card flat bordered class="bg-blue-1">
        <q-card-section>
          <div class="text-h6 q-mb-md">
            <q-icon name="lightbulb" color="orange" class="q-mr-sm" />
            촬영 가이드
          </div>
          <q-list dense>
            <q-item>
              <q-item-section avatar>
                <q-icon name="brightness_6" color="blue" />
              </q-item-section>
              <q-item-section>
                <q-item-label>충분한 조명 확보</q-item-label>
                <q-item-label caption>자연광이나 밝은 LED 조명 사용</q-item-label>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section avatar>
                <q-icon name="center_focus_strong" color="blue" />
              </q-item-section>
              <q-item-section>
                <q-item-label>혀 전체가 화면에 나오도록</q-item-label>
                <q-item-label caption>혀를 최대한 내밀어 촬영</q-item-label>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section avatar>
                <q-icon name="camera_alt" color="blue" />
              </q-item-section>
              <q-item-section>
                <q-item-label>카메라를 안정적으로 고정</q-item-label>
                <q-item-label caption>흔들림 없이 선명하게 촬영</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>

      <!-- 품질 확인 -->
      <q-card v-if="capturedImage" flat bordered>
        <q-card-section>
          <div class="text-h6 q-mb-md">이미지 품질 확인</div>
          <div class="row q-gutter-md">
            <q-rating
              v-model="imageQuality.brightness"
              max="5"
              size="sm"
              color="orange"
              icon="wb_sunny"
            />
            <span class="text-body2">밝기</span>
          </div>
          <div class="row q-gutter-md q-mt-sm">
            <q-rating
              v-model="imageQuality.clarity"
              max="5"
              size="sm"
              color="blue"
              icon="visibility"
            />
            <span class="text-body2">선명도</span>
          </div>
          <div class="row q-gutter-md q-mt-sm">
            <q-rating
              v-model="imageQuality.coverage"
              max="5"
              size="sm"
              color="green"
              icon="crop_free"
            />
            <span class="text-body2">촬영 범위</span>
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
          :disable="!capturedImage || averageQuality < 3"
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
const isFrontCamera = ref(false)
const hasMultipleCameras = ref(false)
const flashEnabled = ref(false)

// 카메라 스트림
let mediaStream = null
let currentDeviceId = null
let availableCameras = []

// 이미지 품질 평가
const imageQuality = ref({
  brightness: 3,
  clarity: 3,
  coverage: 3
})

// 평균 품질 계산
const averageQuality = computed(() => {
  const total = imageQuality.value.brightness + imageQuality.value.clarity + imageQuality.value.coverage
  return total / 3
})

// 카메라 초기화
const initCamera = async () => {
  try {
    // 사용 가능한 카메라 목록 가져오기
    const devices = await navigator.mediaDevices.enumerateDevices()
    availableCameras = devices.filter(device => device.kind === 'videoinput')
    hasMultipleCameras.value = availableCameras.length > 1

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
        width: { ideal: 1920 },
        height: { ideal: 1080 },
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

// 플래시 토글
const toggleFlash = async () => {
  if (!mediaStream) return

  try {
    const track = mediaStream.getVideoTracks()[0]
    const capabilities = track.getCapabilities()

    if (capabilities.torch) {
      flashEnabled.value = !flashEnabled.value
      await track.applyConstraints({
        advanced: [{ torch: flashEnabled.value }]
      })
    } else {
      $q.notify({
        message: '이 카메라는 플래시를 지원하지 않습니다.',
        position: 'top'
      })
    }
  } catch (error) {
    console.error('플래시 제어 실패:', error)
  }
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

    // 자동 품질 분석 (임시로 랜덤 값)
    imageQuality.value = {
      brightness: Math.floor(Math.random() * 2) + 3, // 3-4
      clarity: Math.floor(Math.random() * 2) + 3,    // 3-4
      coverage: Math.floor(Math.random() * 2) + 3    // 3-4
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
  imageQuality.value = {
    brightness: 3,
    clarity: 3,
    coverage: 3
  }
}

// 사진 확인
const confirmPhoto = () => {
  if (averageQuality.value < 3) {
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
    // 설진 데이터 저장
    await patientStore.updateDiagnosisData('tongue', {
      image: capturedImage.value,
      quality: imageQuality.value,
      timestamp: new Date()
    })

    await patientStore.nextStep()

    $q.notify({
      type: 'positive',
      message: '설진 이미지가 저장되었습니다.',
      position: 'top'
    })

    router.push('/face-diagnosis')
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
  router.push('/patient-info')
}

// 생명주기
onMounted(() => {
  initCamera()
})

onUnmounted(() => {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop())
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

.guide-frame {
  width: 80%;
  height: 60%;
  border: 3px dashed rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
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
</style>
