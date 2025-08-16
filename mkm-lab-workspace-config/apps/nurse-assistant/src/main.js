import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import { Quasar, Notify, Dialog, Loading } from 'quasar'

// Quasar CSS 및 아이콘 import
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/material-icons-outlined/material-icons-outlined.css'
import 'quasar/dist/quasar.css'

import App from './App.vue'
import routes from './router/routes.js'

// PWA 설정
import { registerSW } from 'virtual:pwa-register'

const updateSW = registerSW({
  onNeedRefresh() {
    // 업데이트 가능할 때 알림
    Notify.create({
      message: '새 버전이 사용 가능합니다. 새로고침하시겠습니까?',
      color: 'primary',
      actions: [
        {
          label: '새로고침',
          color: 'white',
          handler: () => {
            updateSW(true)
          }
        }
      ],
      timeout: 0
    })
  },
  onOfflineReady() {
    Notify.create({
      message: '오프라인에서도 사용 가능합니다',
      color: 'positive'
    })
  }
})

// 라우터 설정
const router = createRouter({
  history: createWebHistory(),
  routes
})

// Pinia 스토어
const pinia = createPinia()

const app = createApp(App)

app.use(Quasar, {
  plugins: {
    Notify,
    Dialog,
    Loading
  },
  config: {
    notify: {
      position: 'top',
      timeout: 3000
    }
  }
})

app.use(pinia)
app.use(router)

// 디버깅: Vue 앱 마운트 확인
console.log('Vue 앱 마운트 시작...')
document.getElementById('vue-status').textContent = 'Vue 앱 마운트 시도 중...'

try {
  app.mount('#app')
  console.log('Vue 앱 마운트 성공!')
  setTimeout(() => {
    const statusEl = document.getElementById('vue-status')
    if (statusEl) {
      statusEl.textContent = 'Vue 앱 마운트 성공! 🎉'
      statusEl.style.background = '#d4edda'
      statusEl.style.color = '#155724'
    }
  }, 100)
} catch (error) {
  console.error('Vue 앱 마운트 실패:', error)
  document.getElementById('vue-status').textContent = `Vue 앱 마운트 실패: ${error.message}`
  document.getElementById('vue-status').style.background = '#f8d7da'
  document.getElementById('vue-status').style.color = '#721c24'
}
