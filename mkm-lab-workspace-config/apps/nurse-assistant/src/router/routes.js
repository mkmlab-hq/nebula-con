export default [
  {
    path: '/',
    name: 'home',
    component: () => import('../pages/HomePage.vue')
  },
  // MKM QuickScan 라우트
  {
    path: '/quickscan',
    name: 'quickscan',
    redirect: '/quickscan/start'
  },
  {
    path: '/quickscan/start',
    name: 'quickscan-start',
    component: () => import('../pages/QuickScanStart.vue')
  },
  {
    path: '/quickscan/test',
    name: 'quickscan-test',
    component: () => import('../pages/QuickScanTest.vue')
  },
  {
    path: '/quickscan/result',
    name: 'quickscan-result',
    component: () => import('../pages/QuickScanResult.vue')
  },
  // 기존 라우트들
  {
    path: '/patient-info',
    name: 'patient-info',
    component: () => import('../pages/PatientInfoPage.vue')
  },
  {
    path: '/tongue-diagnosis',
    name: 'tongue-diagnosis',
    component: () => import('../pages/TongueDiagnosisPage.vue')
  },
  {
    path: '/face-diagnosis',
    name: 'face-diagnosis',
    component: () => import('../pages/FaceDiagnosisPage.vue')
  },
  {
    path: '/voice-diagnosis',
    name: 'voice-diagnosis',
    component: () => import('../pages/VoiceDiagnosisPage.vue')
  },
  {
    path: '/complete',
    name: 'complete',
    component: () => import('../pages/CompletePage.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]
