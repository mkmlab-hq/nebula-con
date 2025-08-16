<template>
  <div style="padding: 40px; text-align: center; background: white; min-height: 100vh;">
    <h1 style="color: #1976d2; margin-bottom: 20px;">🏥 MKM Lab</h1>
    <h2 style="color: #666; margin-bottom: 30px;">한의학 진단 데이터 수집 시스템</h2>

    <div style="display: flex; flex-direction: column; gap: 20px; max-width: 400px; margin: 0 auto;">
      <!-- MKM QuickScan 버튼 -->
      <button
        @click="startQuickScan"
        style="
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          padding: 24px 40px;
          font-size: 18px;
          border-radius: 16px;
          cursor: pointer;
          box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
          font-weight: 600;
          transition: all 0.3s ease;
        "
        onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 12px 40px rgba(102, 126, 234, 0.4)'"
        onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(102, 126, 234, 0.3)'"
      >
        🚀 MKM QuickScan 시작
        <div style="font-size: 14px; margin-top: 8px; opacity: 0.9;">
          빠른 검사 (3-5분)
        </div>
      </button>

      <!-- 기존 시스템 버튼 -->
      <button
        @click="startNewPatient"
        style="
          background: #1976d2;
          color: white;
          border: none;
          padding: 20px 40px;
          font-size: 16px;
          border-radius: 12px;
          cursor: pointer;
          font-weight: 500;
          transition: all 0.3s ease;
        "
        onmouseover="this.style.transform='translateY(-1px)'"
        onmouseout="this.style.transform='translateY(0)'"
      >
        ✨ 기존 시스템 사용
        <div style="font-size: 12px; margin-top: 4px; opacity: 0.9;">
          상세 진단
        </div>
      </button>
    </div>

    <div style="margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 12px; max-width: 500px; margin-left: auto; margin-right: auto;">
      <h3 style="color: #2c3e50; margin-bottom: 16px;">시스템 선택 가이드</h3>
      <div style="text-align: left; color: #6c757d; line-height: 1.6;">
        <div style="margin-bottom: 12px;">
          <strong>🚀 MKM QuickScan:</strong> 간호조무사용 빠른 검사 시스템<br>
          • 비식별화된 환자 정보<br>
          • 3대 검사 자동화 (설진/면진/음성)<br>
          • 즉시 한의사 대시보드 전송
        </div>
        <div>
          <strong>✨ 기존 시스템:</strong> 상세한 진단 데이터 수집<br>
          • 완전한 환자 정보 입력<br>
          • 4대 진단법 상세 분석<br>
          • 종합 진단 리포트 생성
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const startQuickScan = () => {
  router.push('/quickscan/start')
}

const startNewPatient = () => {
  router.push('/patient-info')
}
</script>

<style scoped>
.q-page {
  min-height: 100vh;
}
</style>
