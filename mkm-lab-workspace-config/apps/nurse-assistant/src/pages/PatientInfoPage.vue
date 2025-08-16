<template>
  <q-page class="flex flex-center bg-grey-1">
    <div class="column q-gutter-md" style="width: 100%; max-width: 600px; padding: 20px;">
      <!-- 진행 상태 표시 -->
      <q-card flat bordered>
        <q-card-section class="text-center">
          <h5 class="text-h5 text-primary q-my-md">환자 정보 입력</h5>
          <p class="text-body2 text-grey-6">정확한 진단을 위해 기본 정보를 입력해주세요</p>
        </q-card-section>
      </q-card>

      <!-- 환자 정보 입력 폼 -->
      <q-card flat bordered>
        <q-card-section>
          <q-form @submit="onSubmit" class="q-gutter-md">
            <!-- 환자 이름 -->
            <q-input
              v-model="form.name"
              label="환자 이름 *"
              outlined
              :rules="[val => !!val || '이름을 입력해주세요']"
              hint="환자의 실명을 입력해주세요"
              autofocus
            >
              <template v-slot:prepend>
                <q-icon name="person" />
              </template>
            </q-input>

            <!-- 나이 -->
            <q-input
              v-model.number="form.age"
              label="나이 *"
              type="number"
              outlined
              :rules="[
                val => !!val || '나이를 입력해주세요',
                val => val > 0 && val < 150 || '올바른 나이를 입력해주세요'
              ]"
              hint="만 나이를 입력해주세요"
            >
              <template v-slot:prepend>
                <q-icon name="cake" />
              </template>
            </q-input>

            <!-- 성별 -->
            <div class="q-mb-md">
              <q-field
                v-model="form.gender"
                label="성별 *"
                outlined
                :rules="[val => !!val || '성별을 선택해주세요']"
              >
                <template v-slot:control>
                  <q-option-group
                    v-model="form.gender"
                    :options="genderOptions"
                    color="primary"
                    inline
                    class="q-mt-xs"
                  />
                </template>
                <template v-slot:prepend>
                  <q-icon name="wc" />
                </template>
              </q-field>
            </div>

            <!-- 주요 증상 -->
            <q-select
              v-model="form.symptoms"
              :options="symptomOptions"
              label="주요 증상"
              outlined
              multiple
              use-chips
              hint="해당하는 증상을 모두 선택해주세요"
            >
              <template v-slot:prepend>
                <q-icon name="healing" />
              </template>
            </q-select>

            <!-- 주소증 (Chief Complaint) -->
            <q-input
              v-model="form.chiefComplaint"
              label="주소증 *"
              type="textarea"
              outlined
              rows="3"
              :rules="[val => !!val || '주소증을 입력해주세요']"
              hint="환자가 호소하는 주요 증상을 자세히 기록해주세요"
            >
              <template v-slot:prepend>
                <q-icon name="description" />
              </template>
            </q-input>

            <!-- 추가 메모 -->
            <q-input
              v-model="form.additionalNotes"
              label="추가 메모"
              type="textarea"
              outlined
              rows="2"
              hint="기타 특이사항이 있다면 기록해주세요"
            >
              <template v-slot:prepend>
                <q-icon name="note" />
              </template>
            </q-input>
          </q-form>
        </q-card-section>
      </q-card>

      <!-- 버튼 영역 -->
      <div class="row q-gutter-md">
        <q-btn
          flat
          color="grey-7"
          icon="arrow_back"
          label="취소"
          class="col"
          @click="goBack"
        />
        <q-btn
          color="primary"
          icon="arrow_forward"
          label="다음"
          class="col"
          :loading="isLoading"
          @click="onSubmit"
          :disable="!isFormValid"
        />
      </div>

      <!-- 임시 저장 안내 -->
      <q-card flat class="bg-blue-1">
        <q-card-section class="text-center">
          <q-icon name="info" color="blue" class="q-mr-sm" />
          <span class="text-body2">입력하신 정보는 자동으로 임시 저장됩니다</span>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePatientStore } from '../stores/patient.js'
import { useQuasar } from 'quasar'

const router = useRouter()
const patientStore = usePatientStore()
const $q = useQuasar()

// 폼 데이터
const form = ref({
  name: '',
  age: null,
  gender: '',
  symptoms: [],
  chiefComplaint: '',
  additionalNotes: ''
})

const isLoading = ref(false)

// 성별 옵션
const genderOptions = [
  { label: '남성', value: 'male' },
  { label: '여성', value: 'female' }
]

// 증상 옵션
const symptomOptions = [
  '소화불량', '복통', '설사', '변비',
  '두통', '어지러움', '불면증', '피로감',
  '관절통', '요통', '근육통', '어깨 결림',
  '기침', '가래', '목 아픔', '코막힘',
  '가슴 답답함', '두근거림', '손발 저림',
  '식욕부진', '체중감소', '체중증가',
  '스트레스', '우울감', '불안감',
  '기타'
]

// 폼 유효성 검사
const isFormValid = computed(() => {
  return form.value.name &&
         form.value.age &&
         form.value.gender &&
         form.value.chiefComplaint
})

// 자동 저장 기능
const autoSave = () => {
  if (form.value.name || form.value.age || form.value.chiefComplaint) {
    patientStore.updatePatientInfo({
      ...form.value,
      id: Date.now().toString() // 임시 ID
    })
  }
}

// 폼 변경 감지하여 자동 저장
watch(form, autoSave, { deep: true })

// 폼 제출
const onSubmit = async () => {
  if (!isFormValid.value) {
    $q.notify({
      type: 'negative',
      message: '필수 항목을 모두 입력해주세요.',
      position: 'top'
    })
    return
  }

  isLoading.value = true

  try {
    // 환자 정보 저장
    await patientStore.updatePatientInfo({
      ...form.value,
      id: form.value.id || Date.now().toString(),
      timestamp: new Date()
    })

    // 다음 단계로 이동
    await patientStore.nextStep()

    $q.notify({
      type: 'positive',
      message: '환자 정보가 저장되었습니다.',
      position: 'top'
    })

    router.push('/tongue-diagnosis')
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: '정보 저장 중 오류가 발생했습니다.',
      position: 'top'
    })
  } finally {
    isLoading.value = false
  }
}

// 뒤로 가기
const goBack = () => {
  $q.dialog({
    title: '확인',
    message: '입력 중인 정보가 있습니다. 정말 취소하시겠습니까?',
    cancel: true,
    persistent: true
  }).onOk(() => {
    patientStore.resetSession()
    router.push('/')
  })
}

// 컴포넌트 마운트 시 기존 데이터 로드
onMounted(() => {
  const existingData = patientStore.patientInfo
  if (existingData && existingData.name) {
    form.value = { ...existingData }
  }
})
</script>

<style scoped>
.q-page {
  min-height: 100vh;
}
</style>
