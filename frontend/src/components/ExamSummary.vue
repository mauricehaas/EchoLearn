<template>
  <div v-if="!loading && summary" class="summary-card" :class="gradeClass">
    <h3>Gesamtergebnis</h3>
    <div class="summary-grid">
      <div>
        <strong>Punkte</strong>
        <p>{{ summary.total_points }} / {{ summary.max_points }}</p>
      </div>
      <div>
        <strong>Prozent</strong>
        <p>{{ summary.percentage }} %</p>
      </div>
      <div>
        <strong>Note</strong>
        <p class="grade">{{ summary.grade }}</p>
      </div>
    </div>
  </div>

  <div v-else-if="loading">Lade Gesamtergebnis...</div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue'

  const props = defineProps({
    examId: {
      type: String,
      required: true
    }
  })

  const summary = ref(null)
  const loading = ref(true)

  const gradeClass = computed(() => {
    if (!summary.value) return ''
    const g = parseFloat(summary.value.grade.replace(',', '.'))
    if (g <= 2) return 'good'
    if (g <= 4) return 'medium'
    return 'bad'
  })

  onMounted(async () => {
    const res = await fetch(
      `http://localhost:8000/exam_evaluation_single_answers/exam_scores/${props.examId}`
    )
    summary.value = await res.json()
    loading.value = false
  })
</script>

<style scoped>
  .summary-card {
    margin: 20px 0;
    padding: 20px;
    border-radius: 12px;
    background: white;
    border: 1px solid #ccc;
    font-size: 18px;
  }

  /* Grid */
  .summary-grid {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
  }

  .summary-grid div {
    text-align: center;
    flex: 1;
  }

  /* Note */
  .grade {
    font-size: 32px;
    font-weight: bold;
    color: #6a1b9a;
  }
</style>
