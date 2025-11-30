<template>
  <div class="speech-input">
    <h2>Frage beantworten</h2>

    <div v-if="currentQuestion">
      <p>{{ currentQuestion.question }}</p>

      <button @click="startListening" :disabled="listening">
        {{ listening ? 'Höre...' : 'Sprich jetzt' }}
      </button>
      <button @click="stopListening" :disabled="!listening">Stopp</button>

      <p>Erkannter Text: {{ transcript }}</p>

      <button @click="submitAnswer" :disabled="!transcript">Antwort prüfen</button>
      <p v-if="feedback">Feedback: {{ feedback }}</p>

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

      // Speech-to-Text
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

      const submitAnswer = async () => {
        const res = await fetch('http://localhost:8000/learn/check', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            question_id: currentQuestion.value.id,
            answer: transcript.value
          })
        })
        const data = await res.json()
        feedback.value = data.feedback
      }

      const nextQuestion = () => {
        transcript.value = ''
        feedback.value = ''
        if (currentIndex.value < questions.value.length - 1) currentIndex.value++
      }

      // Fragen vom Backend laden
      onMounted(async () => {
        const res = await fetch('http://localhost:8000/questions/')
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
        nextQuestion
      }
    }
  }
</script>
