<template>
  <div class="speech-input">
    <div v-if="currentQuestion && !examFinished">
      <h2>Frage {{ currentIndex + 1 }}</h2>
      <button @click="speakQuestion" :disabled="loading || locked">🔊 Frage anhören</button>

      <div style="margin-top: 20px">
        <button @click="startListening" :disabled="listening || loading || locked">
          {{ listening ? 'Höre...' : '🎤 Sprich jetzt' }}
        </button>
        <button @click="stopListening" :disabled="!listening || loading || locked">⏹️ Stopp</button>
        <button @click="restartListening" :disabled="loading || locked">
          🔄 Antwort verwerfen
        </button>
      </div>

      <div style="margin-top: 10px">
        <p class="interim" v-if="interimTranscript">…{{ interimTranscript }}</p>

        <AnswerBox
          v-model="transcript"
          :loading="loading"
          :locked="locked"
          @submit="submitAnswer"
        />

        <span v-if="loading" class="spinner"></span>
        <p v-if="feedback" style="margin-top: 10px; color: green">{{ feedback }}</p>
      </div>

      <div
        v-if="submitted && followupText"
        style="margin-top: 20px; border-top: 1px solid #ccc; padding-top: 15px"
      >
        <h2>Rückfrage</h2>
        <button @click="speakFollowUp" :disabled="followupLoading || followupLocked">
          🔊 Rückfrage anhören
        </button>

        <div style="margin-top: 20px">
          <button
            @click="startFollowupListening"
            :disabled="followupListening || followupLoading || followupLocked"
          >
            {{ followupListening ? 'Höre...' : '🎤 Sprich jetzt' }}
          </button>
          <button
            @click="stopFollowupListening"
            :disabled="!followupListening || followupLoading || followupLocked"
          >
            ⏹️ Stopp
          </button>
          <button @click="restartFollowupListening" :disabled="followupLoading || followupLocked">
            🔄 Antwort verwerfen
          </button>
        </div>

        <div style="margin-top: 10px">
          <p class="interim" v-if="followupInterimTranscript">…{{ followupInterimTranscript }}</p>

          <AnswerBox
            v-model="followupTranscript"
            :loading="followupLoading"
            :locked="followupLocked"
            @submit="submitFollowUp"
          />

          <span v-if="followupLoading" class="spinner"></span>
          <p v-if="followupFeedback" style="margin-top: 10px; color: green">
            {{ followupFeedback }}
          </p>
        </div>
      </div>

      <QuestionNavigation
        :currentIndex="currentIndex"
        :total="questions.length"
        :submitted="submitted"
        :loading="loading || nextDisabled"
        @next="nextQuestion"
        @finish="finishExam"
      />
    </div>

    <div v-else-if="examFinished" style="margin-top: 20px; font-weight: bold">
      <h2>Prüfung abgeschlossen.</h2>
      <p>Sehen Sie im Statistik-Bereich Ihre Bewertung.</p>
    </div>

    <p v-else>Lade Fragen...</p>
  </div>
</template>

<script>
  import { ref, onMounted, computed } from 'vue'
  import { useSpeechRecognition } from '../composables/useSpeechRecognition'
  import { speakText } from '../composables/useTextToSpeech'
  import AnswerBox from './AnswerBox.vue'
  import QuestionNavigation from './QuestionNavigation.vue'

  export default {
    components: { AnswerBox, QuestionNavigation },
    setup() {
      const questions = ref([])
      const currentIndex = ref(0)
      const feedback = ref('')
      const loading = ref(false)
      const locked = ref(false)
      const submitted = ref(false)
      const examFinished = ref(false)
      const followupText = ref('')
      const followupTranscript = ref('')
      const followupInterimTranscript = ref('')
      const followupFeedback = ref('')
      const followupLoading = ref(false)
      const followupLocked = ref(false)
      const followupListening = ref(false)

      const {
        transcript,
        interimTranscript,
        listening,
        startListening,
        stopListening,
        restartListening
      } = useSpeechRecognition({ lang: 'de-DE' })

      const {
        startListening: startFollowupListening,
        stopListening: stopFollowupListening,
        restartListening: restartFollowupListening
      } = useSpeechRecognition({
        transcriptRef: followupTranscript,
        interimRef: followupInterimTranscript,
        listeningRef: followupListening,
        lang: 'de-DE'
      })

      const currentQuestion = computed(() => questions.value[currentIndex.value])

      const nextDisabled = computed(() => {
        if (!submitted.value) return true

        if (followupText.value && !followupLocked.value) return true

        return false
      })

      const speakQuestion = () => {
        if (!currentQuestion.value || loading.value || locked.value) return
        speakText(currentQuestion.value.question)
      }

      const speakFollowUp = () => {
        if (!followupText.value || followupLoading.value || followupLocked.value) return
        followupLoading.value = true
        try {
          speakText(followupText.value)
        } finally {
          followupLoading.value = false
        }
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
              correct_answer: currentQuestion.value.answer,
              max_points: '5'
            })
          })
          const data = await res.json()
          feedback.value = data.feedback || 'Antwort erfolgreich abgesendet'
          locked.value = true
          submitted.value = true
          if (data.followup_text) followupText.value = data.followup_text
        } catch (err) {
          feedback.value = 'Fehler beim Absenden, bitte erneut versuchen.'
          console.error(err)
        } finally {
          loading.value = false
        }
      }

      const submitFollowUp = async () => {
        if (!followupTranscript.value || followupLoading.value || followupLocked.value) return
        followupLoading.value = true
        followupFeedback.value = ''
        if (followupListening.value) stopFollowupListening()
        try {
          const res = await fetch('http://localhost:8000/exam/evaluate_answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              unique_exam_id: '1',
              question: followupText.value,
              student_answer: followupTranscript.value,
              correct_answer: currentQuestion.value.answer,
              max_points: '5'
            })
          })
          const data = await res.json()
          followupFeedback.value = data.feedback || 'Antwort erfolgreich abgesendet'
          followupLocked.value = true
        } catch (err) {
          followupFeedback.value = 'Fehler beim Absenden, bitte erneut versuchen.'
          console.error(err)
        } finally {
          followupLoading.value = false
        }
      }

      const nextQuestion = () => {
        transcript.value = ''
        feedback.value = ''
        locked.value = false
        submitted.value = false
        followupText.value = ''
        followupTranscript.value = ''
        followupInterimTranscript.value = ''
        followupFeedback.value = ''
        followupLoading.value = false
        followupLocked.value = false
        followupListening.value = false
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
        followupText,
        followupTranscript,
        followupInterimTranscript,
        followupFeedback,
        followupLoading,
        followupLocked,
        followupListening,
        examFinished,
        nextDisabled,
        startListening,
        stopListening,
        restartListening,
        startFollowupListening,
        stopFollowupListening,
        restartFollowupListening,
        speakQuestion,
        speakFollowUp,
        submitAnswer,
        submitFollowUp,
        nextQuestion,
        finishExam
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
  .interim {
    font-style: italic;
    color: gray;
  }
</style>
