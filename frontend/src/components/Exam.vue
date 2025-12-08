<template>
  <div class="speech-input">
    <h2>Frage {{ currentIndex + 1 }}</h2>
    <div v-if="currentQuestion">
      <button @click="speakQuestion">Frage anhören</button>

      <div style="margin-top: 20px">
        <button @click="startListening" :disabled="listening">
          {{ listening ? 'Höre...' : 'Sprich jetzt' }}
        </button>
        <button @click="stopListening" :disabled="!listening">Stopp</button>
      </div>

      <p>Erkannte Antwort: {{ transcript }}</p>

      <button @click="submitAnswer" :disabled="!transcript">Antwort absenden</button>
      <button @click="nextQuestion" :disabled="currentIndex >= questions.length - 1">
        Nächste Frage
      </button>
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
      const feedback = ref('')
      const listening = ref(false)
      let recognition = null

      const currentQuestion = computed(() => questions.value[currentIndex.value])

      /* ----------------------------------------
       TEXT TO SPEECH
    ---------------------------------------- */
      const speakQuestion = () => {
        if (!currentQuestion.value) return

        const utterance = new SpeechSynthesisUtterance(currentQuestion.value.question)
        utterance.lang = 'de-DE'
        utterance.rate = 1
        utterance.pitch = 1
        speechSynthesis.speak(utterance)
      }

      /* ----------------------------------------
       SPEECH TO TEXT
    ---------------------------------------- */
      if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
        recognition = new SpeechRecognition()
        recognition.lang = 'de-DE'
        recognition.interimResults = false

        recognition.onresult = (event) => {
          transcript.value = event.results[0][0].transcript
          listening.value = false
        }

        recognition.onend = () => (listening.value = false)
      } else {
        alert('Speech-to-Text wird von diesem Browser nicht unterstützt.')
      }

      const startListening = () => {
        transcript.value = ''
        listening.value = true
        recognition.start()
      }

      const stopListening = () => {
        recognition.stop()
        listening.value = false
      }

      /* ----------------------------------------
       ANTWORT AN BACKEND SENDEN
    ---------------------------------------- */
      const submitAnswer = async () => {
        const res = await fetch('http://localhost:8000/exam/evaluate_answer', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            unique_exam_id: '1',
            student_answer: transcript.value,
            correct_answer: currentQuestion.value.answer
          })
        })
        const data = await res.json()
        feedback.value = data.feedback

        // Rückfrage oder Folgefrage könnte hier per TTS vorgelesen werden:
        if (data.followup_question) {
          setTimeout(() => {
            const u = new SpeechSynthesisUtterance(data.followup_question)
            u.lang = 'de-DE'
            speechSynthesis.speak(u)
          }, 300)
        }
      }

      const nextQuestion = () => {
        transcript.value = ''
        feedback.value = ''
        if (currentIndex.value < questions.value.length - 1) currentIndex.value++
      }

      /* ----------------------------------------
       FRAGEN LADEN
    ---------------------------------------- */
      onMounted(async () => {
        const res = await fetch('http://localhost:8000/questions/random')
        questions.value = await res.json()
      })

      return {
        questions,
        currentIndex,
        currentQuestion,
        transcript,
        feedback,
        listening,
        startListening,
        stopListening,
        submitAnswer,
        nextQuestion,
        speakQuestion
      }
    }
  }
</script>
