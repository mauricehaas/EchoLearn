<template>
  <div class="table-container">
    <h2>Ergebnisübersicht</h2>

    <!-- Loading -->
    <div v-if="loading">Lade Ergebnisse...</div>

    <!-- Error -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Gesamtübersicht -->
    <div v-if="!loading && !error && results.length > 0" class="summary-card" :class="gradeClass">
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

    <!-- Tabelle -->
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
  import { ref, onMounted, computed } from 'vue'

  const results = ref([])
  const summary = ref({
    total_points: 0,
    max_points: 0,
    percentage: 0,
    grade: ''
  })

  const loading = ref(true)
  const error = ref(null)

  const uniqueExamId = '1'

  const gradeClass = computed(() => {
    const grade = parseFloat(summary.value.grade.replace(',', '.'))
    if (grade <= 2) return 'good'
    if (grade <= 4) return 'medium'
    return 'bad'
  })

  async function loadResults() {
    loading.value = true
    error.value = null

    try {
      // Einzelne Antworten
      const resAnswers = await fetch(
        `http://localhost:8000/exam_evaluation_single_answers/exam/${uniqueExamId}`
      )
      if (!resAnswers.ok) throw new Error(resAnswers.status)
      results.value = await resAnswers.json()

      // Gesamtauswertung
      const resSummary = await fetch(
        `http://localhost:8000/exam_evaluation_single_answers/exam_scores/${uniqueExamId}`
      )
      if (!resSummary.ok) throw new Error(resSummary.status)
      summary.value = await resSummary.json()
    } catch (err) {
      error.value = 'Fehler beim Laden der Ergebnisse'
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

  /* Summary Card jetzt weiß */
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

  /* Note in Tabellen-Lila */
  .grade {
    font-size: 32px;
    font-weight: bold;
    color: #6a1b9a; /* lila wie typische Tabellen/Headers */
  }

  /* Table */
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
