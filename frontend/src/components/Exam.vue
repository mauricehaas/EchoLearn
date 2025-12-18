<template>
  <div class="speech-input">
    <div v-if="currentQuestion && !examFinished">
      <h2>Frage {{ currentIndex + 1 }}</h2>
      <button @click="speakQuestion" :disabled="loading || locked">Frage anhören</button>

      <div style="margin-top: 20px">
        <button @click="startListening" :disabled="listening || loading || locked">
          {{ listening ? 'Höre...' : 'Sprich jetzt' }}
        </button>
        <button @click="stopListening" :disabled="!listening || loading || locked">Stopp</button>
        <button @click="restartListening" :disabled="loading || locked">Neu aufnehmen</button>
      </div>

      <div style="margin-top: 10px">
        <p>
          Erkannte Antwort: {{ transcript }}
          <span v-if="interimTranscript">…{{ interimTranscript }}</span>
        </p>

        <button @click="submitAnswer" :disabled="!transcript || loading || locked">
          {{ loading ? 'Wird geprüft…' : 'Antwort absenden' }}
        </button>
        <span v-if="loading" class="spinner"></span>
        <p v-if="feedback" style="margin-top: 10px; color: green">{{ feedback }}</p>
      </div>

      <div style="margin-top: 20px" v-if="currentIndex == 1">
        <hr />
        <button @click="speakQuestion" :disabled="loading || locked">Rückfrage anhören</button>

        <div style="margin-top: 20px">
          <button @click="startListening" :disabled="listening || loading || locked">
            {{ listening ? 'Höre...' : 'Sprich jetzt' }}
          </button>
          <button @click="stopListening" :disabled="!listening || loading || locked">Stopp</button>
          <button @click="restartListening" :disabled="loading || locked">Neu aufnehmen</button>
        </div>

        <div style="margin-top: 10px">
          <p>
            Erkannte Antwort: {{ transcript }}
            <span v-if="interimTranscript">…{{ interimTranscript }}</span>
          </p>

          <button @click="submitAnswer" :disabled="!transcript || loading || locked">
            {{ loading ? 'Wird geprüft…' : 'Antwort absenden' }}
          </button>
          <span v-if="loading" class="spinner"></span>
          <p v-if="feedback" style="margin-top: 10px; color: green">{{ feedback }}</p>
        </div>
      </div>

      <div style="margin-top: 10px">
        <!-- Wenn letzte Frage und abgeschickt, Abschließen-Button anzeigen -->
        <button v-if="currentIndex >= questions.length - 1 && submitted" @click="finishExam">
          Abschließen
        </button>

        <!-- Ansonsten nächste Frage -->
        <button
          v-else
          @click="nextQuestion"
          :disabled="currentIndex >= questions.length - 1 || !submitted || loading"
        >
          Nächste Frage
        </button>
      </div>
    </div>

    <!-- Abschlussanzeige -->
    <div v-else-if="examFinished" style="margin-top: 20px; font-weight: bold">
      <h2>Prüfung abgeschlossen.</h2>
      <p>Sehen Sie im Statistik-Bereich Ihre Bewertung.</p>
    </div>

    <p v-else>Lade Fragen...</p>
  </div>
</template>

<script>
  import { ref, onMounted, computed } from 'vue'

  export default {
    setup() {
      const questions = ref([])
      const currentIndex = ref(0)
      const transcript = ref('')
      const interimTranscript = ref('')
      const feedback = ref('')
      const listening = ref(false)
      const loading = ref(false)
      const locked = ref(false)
      const submitted = ref(false)
      const stopRequested = ref(false)
      const examFinished = ref(false) // neu: Prüfung abgeschlossen
      let recognition = null

      const currentQuestion = computed(() => questions.value[currentIndex.value])

      const speakQuestion = () => {
        if (!currentQuestion.value || loading.value || locked.value) return
        const utterance = new SpeechSynthesisUtterance(currentQuestion.value.question)
        utterance.lang = 'de-DE'
        utterance.rate = 1
        utterance.pitch = 1
        speechSynthesis.speak(utterance)
      }

      if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
        recognition = new SpeechRecognition()
        recognition.lang = 'de-DE'
        recognition.interimResults = true
        recognition.continuous = true

        recognition.onresult = (event) => {
          let finalTranscript = ''
          let interim = ''

          for (let i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) finalTranscript += event.results[i][0].transcript
            else interim += event.results[i][0].transcript
          }

          transcript.value += finalTranscript
          interimTranscript.value = interim
        }

        recognition.onend = () => {
          if (listening.value && !locked.value && !stopRequested.value) {
            recognition.start()
          } else stopRequested.value = false
        }
      } else {
        alert('Speech-to-Text wird von diesem Browser nicht unterstützt.')
      }

      const startListening = () => {
        if (loading.value || locked.value) return
        listening.value = true
        recognition.start()
      }

      const stopListening = () => {
        if (!listening.value) return
        stopRequested.value = true
        recognition.stop()
        listening.value = false
      }

      const restartListening = () => {
        transcript.value = ''
        interimTranscript.value = ''
        listening.value = false
      }

      const submitAnswer = async () => {
        if (!transcript.value || loading.value || locked.value) return

        loading.value = true
        feedback.value = ''
        if (listening.value) stopListening()

        try {
          const res = await fetch('http://localhost:8000/exam/evaluate_answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              unique_exam_id: '1',
              question: currentQuestion.value.question,
              student_answer: transcript.value,
              correct_answer: currentQuestion.value.answer
            })
          })
          const data = await res.json()
          feedback.value = data.feedback || 'Antwort erfolgreich abgesendet.'

          locked.value = true
          submitted.value = true

          if (data.followup_question) {
            const u = new SpeechSynthesisUtterance(data.followup_question)
            u.lang = 'de-DE'
            speechSynthesis.speak(u)
          }
        } catch (err) {
          feedback.value = 'Fehler beim Absenden, bitte erneut versuchen.'
          console.error(err)
        } finally {
          loading.value = false
        }
      }

      const nextQuestion = () => {
        transcript.value = ''
        interimTranscript.value = ''
        feedback.value = ''
        locked.value = false
        submitted.value = false
        if (currentIndex.value < questions.value.length - 1) currentIndex.value++
      }

      const finishExam = () => {
        examFinished.value = true
      }

      onMounted(async () => {
        const res = await fetch('http://localhost:8000/questions/random')
        questions.value = await res.json()
      })

      return {
        questions,
        currentIndex,
        currentQuestion,
        transcript,
        interimTranscript,
        feedback,
        listening,
        loading,
        locked,
        submitted,
        examFinished,
        startListening,
        stopListening,
        restartListening,
        submitAnswer,
        nextQuestion,
        finishExam,
        speakQuestion
      }
    }
  }
</script>

<style scoped>
  button:disabled {
    background-color: #ddd;
    color: #888;
    cursor: not-allowed;
  }

  .spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid #ccc;
    border-top-color: #333;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-left: 10px;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>
