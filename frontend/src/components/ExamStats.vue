<template>
  <div class="table-container">
    <h2>Ergebnisübersicht</h2>

    <div v-if="loading">Lade Ergebnisse...</div>
    <div v-if="error" class="error">{{ error }}</div>
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
        <tr v-for="row in results" :key="row.id">
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

    <div v-if="!loading && results.length === 0 && !error">
      Keine Ergebnisse für diese Prüfung gefunden.
    </div>
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
      if (!resAnswers.ok) throw new Error(resAnswers.status)
      results.value = await resAnswers.json()
    } catch (err) {
      error.value =
        'Entweder wurde noch keine Prüfung abgelegt oder es gab einen Fehler beim Laden der Ergebnisse'
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
  }

  .results-table th,
  .results-table td {
    border: 1px solid #ccc;
    padding: 8px;
    text-align: left;
  }

  .error {
    color: red;
    margin: 10px 0;
  }
</style>
