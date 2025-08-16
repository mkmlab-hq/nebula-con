<template>
  <q-app>
    <!-- 상단 헤더 -->
    <q-header elevated class="bg-primary">
      <q-toolbar>
        <q-btn
          v-if="$route.name !== 'home'"
          flat
          round
          dense
          icon="arrow_back"
          @click="$router.go(-1)"
        />
        <q-toolbar-title class="text-center">
          {{ pageTitle }}
        </q-toolbar-title>
        <q-btn
          flat
          round
          dense
          icon="refresh"
          @click="refreshApp"
        />
      </q-toolbar>
    </q-header>

    <!-- 메인 컨텐츠 -->
    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- 하단 진행 상태 표시 -->
    <q-footer v-if="showProgress" elevated class="bg-white">
      <div class="q-pa-md">
        <q-linear-progress
          :value="progressValue"
          color="primary"
          size="8px"
          class="q-mb-sm"
        />
        <div class="text-center text-caption text-grey-7">
          {{ progressText }}
        </div>
      </div>
    </q-footer>

    <!-- 로딩 오버레이 -->
    <q-ajax-bar
      ref="bar"
      position="top"
      color="accent"
      size="10px"
    />
  </q-app>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { usePatientStore } from './stores/patient.js'

const route = useRoute()
const patientStore = usePatientStore()

// 페이지 제목 계산
const pageTitle = computed(() => {
  const titles = {
    'home': 'MKM 어시스턴트',
    'patient-info': '환자 정보',
    'tongue-diagnosis': '설진 촬영',
    'face-diagnosis': '면진 촬영',
    'voice-diagnosis': '성진 녹음',
    'complete': '수집 완료'
  }
  return titles[route.name] || 'MKM 어시스턴트'
})

// 진행 상태 표시 여부
const showProgress = computed(() => {
  return ['patient-info', 'tongue-diagnosis', 'face-diagnosis', 'voice-diagnosis'].includes(route.name)
})

// 진행률 계산
const progressValue = computed(() => {
  const steps = ['patient-info', 'tongue-diagnosis', 'face-diagnosis', 'voice-diagnosis']
  const currentIndex = steps.indexOf(route.name)
  return currentIndex >= 0 ? (currentIndex + 1) / steps.length : 0
})

// 진행 텍스트
const progressText = computed(() => {
  const steps = ['patient-info', 'tongue-diagnosis', 'face-diagnosis', 'voice-diagnosis']
  const currentIndex = steps.indexOf(route.name)
  return currentIndex >= 0 ? `${currentIndex + 1} / ${steps.length} 단계` : ''
})

// 앱 새로고침
const refreshApp = () => {
  window.location.reload()
}
</script>

<style scoped>
.q-app {
  font-family: 'Noto Sans KR', sans-serif;
}

/* 태블릿 최적화 */
@media (min-width: 768px) {
  .q-toolbar-title {
    font-size: 1.5rem;
    font-weight: 500;
  }
}
</style>
