<template>
  <q-page class="flex flex-center bg-grey-1">
    <div class="column items-center q-gutter-lg" style="width: 100%; max-width: 600px; padding: 20px;">
      <!-- 로고 및 제목 -->
      <div class="text-center">
        <q-avatar size="120px" class="q-mb-md">
          <q-icon name="medical_services" size="80px" color="primary" />
        </q-avatar>
        <h4 class="text-h4 text-primary q-my-md">MKM Lab</h4>
        <p class="text-h6 text-grey-7">한의학 진단 데이터 수집 시스템</p>
      </div>

      <!-- 메인 버튼 -->
      <q-btn
        unelevated
        size="xl"
        color="primary"
        class="full-width q-py-lg"
        label="새 환자 데이터 수집 시작"
        icon="add_circle"
        @click="startNewPatient"
      />

      <!-- 상태 카드 -->
      <q-card flat bordered class="full-width">
        <q-card-section class="text-center">
          <div class="text-h6 text-primary">시스템 준비 완료</div>
          <div class="text-body2 text-grey-6">4대 진단법 데이터 수집 가능</div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const startNewPatient = () => {
  router.push('/patient-info')
}
</script>

<style scoped>
.q-page {
  min-height: 100vh;
}
</style>
