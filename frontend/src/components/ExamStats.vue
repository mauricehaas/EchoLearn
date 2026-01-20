<template>
  <div class="table-container">
    <h2>Ergebnisübersicht</h2>

    <!-- Loading Indicator -->
    <div v-if="loading">Lade Ergebnisse...</div>

    <!-- Error -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Tabelle -->
    <table v-if="results.length > 0" class="results-table">
      <thead>
        <tr>
          <th>Frage</th>
          <th>Ihre Antwort</th>
          <th>Musterlösung</th>
          <th>Bewertung (max. 5)</th>
          <th>Feedback</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in results" :key="row.id">
          <td>{{ row.question }}</td>
          <td>{{ row.student_answer }}</td>
          <td>{{ row.correct_answer }}</td>
          <td>{{ row.rating }}</td>
          <td>{{ row.feedback }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Keine Ergebnisse -->
    <div v-if="!loading && results.length === 0 && !error">
      Keine Ergebnisse für diese Prüfung gefunden.
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'

  const results = ref([])
  const loading = ref(true)
  const error = ref(null)

  // Hier kannst du die Exam-ID dynamisch setzen, z.B. via Props oder Router-Param
  const uniqueExamId = '1'

  async function loadResults() {
    loading.value = true
    error.value = null

    try {
      const res = await fetch(
        `http://localhost:8000/exam_evaluation_single_answers/exam/${uniqueExamId}`
      )
      if (!res.ok) throw new Error('Fehler beim Laden: ' + res.status)

      const data = await res.json()

      // FastAPI gibt direkt eine Liste zurück, also kein data.results
      results.value = Array.isArray(data) ? data : []
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  onMounted(loadResults)
</script>

<style scoped></style>
