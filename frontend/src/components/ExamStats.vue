<template>
  <div class="table-container">
    <h2>Ergebnisübersicht</h2>

    <div v-if="loading">Lade Ergebnisse...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="results.length === 0">Noch keine Prüfung abgelegt.</div>
    <div v-else><ExamSummary examId="1" /></div>

    <table v-if="results.length > 0" class="results-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Frage</th>
          <th>Ihre Antwort</th>
          <th>Musterlösung</th>
          <th>Parent</th>
          <th>Typ</th>
          <th>Punkte</th>
          <th>Max. Punkte</th>
          <th>Feedback</th>
        </tr>
      </thead>
      <tbody>
        <tr
          :class="{ clarify: row.question_type === 'CLARIFY' }"
          v-for="row in results"
          :key="row.id"
        >
          <td>{{ row.id }}</td>
          <td>{{ row.question }}</td>
          <td>{{ row.student_answer }}</td>
          <td>{{ row.correct_answer }}</td>
          <td>{{ row.parent_id }}</td>
          <td>{{ row.question_type }}</td>
          <td>{{ row.rating }}</td>
          <td>{{ row.max_points }}</td>
          <td>{{ row.feedback }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import ExamSummary from './ExamSummary.vue'

  const results = ref([])
  const loading = ref(true)
  const error = ref(null)

  const uniqueExamId = '1'

  async function loadResults() {
    loading.value = true
    error.value = null

    try {
      const resAnswers = await fetch(
        `http://localhost:8000/exam_evaluation_single_answers/exam/${uniqueExamId}`
      )
      if (resAnswers.status === 404) {
        results.value = []
        return
      }
      if (!resAnswers.ok) throw new Error(resAnswers.status)
      results.value = await resAnswers.json()
    } catch (err) {
      error.value = 'Es gab einen Fehler beim Laden der Ergebnisse'
    } finally {
      loading.value = false
    }
  }

  onMounted(loadResults)
</script>

<style scoped>
  .table-container {
    padding: 20px;
  }

  .results-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;

    th,
    td {
      border: 1px solid #ccc;
      padding: 8px;
      text-align: left;
    }

    tr {
      &:has(+ tr.clarify) {
        color: lightgrey;
      }
    }
  }

  .error {
    color: red;
    margin: 10px 0;
  }
</style>
