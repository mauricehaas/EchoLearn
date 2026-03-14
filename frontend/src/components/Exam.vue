<template>
  <div class="speech-input">
    <div v-if="currentQuestion && !examFinished">
      <h2>Frage {{ currentIndex + 1 }}</h2>
      <button @click="speakQuestion" :disabled="loading || locked">🔊 Frage anhören</button>
      <button @click="rephraseQuestion" :disabled="loading || locked">
        🔊 Frage umformulieren
      </button>

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

        <p v-if="feedback" style="margin-top: 10px; color: green">{{ feedback }}</p>
      </div>

      <!-- Rückfrage -->
      <div
        v-if="submitted && followupText"
        style="margin-top: 20px; border-top: 1px solid #ccc; padding-top: 15px"
      >
        <h2>{{ followupType === 'DEEPEN' ? 'Vertiefungsfrage' : 'Rückfrage' }}</h2>
        <button @click="speakFollowUp" :disabled="followupLoading || followupLocked">
          🔊 {{ followupType === 'DEEPEN' ? 'Vertiefungsfrage anhören' : 'Rückfrage anhören' }}
        </button>
        <button @click="rephraseFollowUpQuestion" :disabled="followupLoading || followupLocked">
          🔊 Frage umformulieren
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
        :examId="'1'"
        @next="nextQuestion"
        @finish="handleExamFinished"
      />
    </div>

    <div v-else-if="examFinished" style="margin-top: 20px; font-weight: bold">
      <h2>Prüfung abgeschlossen.</h2>
      <ExamSummary examId="1" />
      <p v-if="finishMessage">{{ finishMessage }}</p>
      <p>
        Sehen Sie im <router-link to="/statistik">Statistik-Bereich</router-link> Ihre Bewertung und
        weitere Details.
      </p>
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
  import ExamSummary from './ExamSummary.vue'

  export default {
    components: { AnswerBox, QuestionNavigation, ExamSummary },
    setup() {
      const questions = ref([])
      const currentIndex = ref(0)
      const feedback = ref('')
      const loading = ref(false)
      const locked = ref(false)
      const submitted = ref(false)
      const examFinished = ref(false)
      const finishMessage = ref('')

      const followupText = ref('')
      const followupType = ref('BASE')
      const followupTranscript = ref('')
      const followupInterimTranscript = ref('')
      const followupFeedback = ref('')
      const followupLoading = ref(false)
      const followupLocked = ref(false)
      const followupListening = ref(false)
      const lastAnswerId = ref(null)
      const nextAnswer = ref('')

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

      const submit = async ({
        examId = '1',
        questionTextRef,
        answerRef,
        feedbackRef,
        lockedRef,
        listeningRef,
        loadingRef,
        correctAnswer = '',
        maxPoints = '5',
        evaluateOnly = false,
        parentId = null,
        typeOverride = null
      }) => {
        if (!answerRef.value || loadingRef.value || lockedRef.value) return
        loadingRef.value = true
        feedbackRef.value = ''
        if (listeningRef.value) stopListening()

        try {
          const body = {
            unique_exam_id: examId,
            question:
              typeof questionTextRef.value === 'string'
                ? questionTextRef.value
                : questionTextRef.value.question,
            student_answer: answerRef.value,
            correct_answer: correctAnswer,
            max_points: maxPoints,
            evaluate_only: evaluateOnly,
            question_type: typeOverride || 'BASE'
          }

          if (parentId !== null) body.parent_id = parentId

          const res = await fetch('http://localhost:8000/exam/evaluate_answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
          })

          const data = await res.json()

          feedbackRef.value = 'Antwort erfolgreich abgesendet'
          lockedRef.value = true

          if (!evaluateOnly && data.answer_id) lastAnswerId.value = data.answer_id

          if (!evaluateOnly && data.followup_text) {
            followupText.value = data.followup_text
            followupType.value = data.next_action || 'BASE'
            followupTranscript.value = ''
            followupInterimTranscript.value = ''
            followupFeedback.value = ''
            followupLoading.value = false
            followupLocked.value = false
            followupListening.value = false

            if (data.next_action == 'DEEPEN') {
              nextAnswer.value = data.next_answer
            }
          }

          if (!evaluateOnly) submitted.value = true
        } catch (err) {
          feedbackRef.value = 'Fehler beim Absenden, bitte erneut versuchen.'
          console.error(err)
        } finally {
          loadingRef.value = false
        }
      }

      const submitAnswerOrFollowUp = (isFollowUp = false) => {
        let answerRef = transcript
        let feedbackRef = feedback
        let lockedRef = locked
        let listeningRef = listening
        let loadingRef = loading
        let questionTextRef = currentQuestion
        let evaluateOnly = false
        let parentId = 0
        let maxPoints = currentQuestion.value?.max_points
        let typeOverride = 'BASE'
        let correctAnswer = currentQuestion.value?.answer || ''

        if (isFollowUp) {
          typeOverride = followupType.value
          answerRef = followupTranscript
          feedbackRef = followupFeedback
          lockedRef = followupLocked
          listeningRef = followupListening
          loadingRef = followupLoading
          questionTextRef = followupText
          evaluateOnly = true
          parentId = lastAnswerId.value

          if (typeOverride === 'CLARIFY') {
            answerRef = { value: transcript.value + ' ' + followupTranscript.value }
            questionTextRef = currentQuestion
          }

          if (typeOverride === 'DEEPEN') {
            correctAnswer = nextAnswer.value
            maxPoints = 5
          }
        }

        submit({
          examId: '1',
          questionTextRef,
          answerRef,
          feedbackRef,
          lockedRef,
          listeningRef,
          loadingRef,
          correctAnswer,
          maxPoints,
          evaluateOnly,
          parentId,
          typeOverride
        })
      }

      const submitAnswer = () => submitAnswerOrFollowUp(false)
      const submitFollowUp = () => submitAnswerOrFollowUp(true)

      const speak = async (textRef, loadingRef, lockedRef) => {
        if (!textRef.value || loadingRef.value || lockedRef.value) return
        loadingRef.value = true
        try {
          const textToSpeak =
            typeof textRef.value === 'string' ? textRef.value : textRef.value.question
          await speakText(textToSpeak)
        } finally {
          loadingRef.value = false
        }
      }

      const speakQuestion = () => speak(currentQuestion, loading, locked)
      const speakFollowUp = () => speak(followupText, followupLoading, followupLocked)

      const rephraseAndSpeak = async (textRef, lockedRef) => {
        if (!textRef.value || lockedRef.value) return

        try {
          const originalText =
            typeof textRef.value === 'string' ? textRef.value : textRef.value.question

          const res = await fetch('http://localhost:8000/exam/rephrase_question', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: originalText })
          })

          if (!res.ok) {
            throw new Error(`Server error ${res.status}`)
          }

          const data = await res.json()

          await speakText(data.answer_llm)
        } catch (err) {
          console.error('Rephrase fehlgeschlagen, nutze Originaltext:', err)

          await speakText(
            typeof textRef.value === 'string' ? textRef.value : textRef.value.question
          )
        }
      }

      const rephraseQuestion = () => rephraseAndSpeak(currentQuestion, locked)
      const rephraseFollowUpQuestion = () => rephraseAndSpeak(followupText, followupLocked)

      const resetFollowUp = () => {
        followupText.value = ''
        followupType.value = 'BASE'
        followupTranscript.value = ''
        followupInterimTranscript.value = ''
        followupFeedback.value = ''
        followupLoading.value = false
        followupLocked.value = false
        followupListening.value = false
      }

      const nextQuestion = () => {
        transcript.value = ''
        feedback.value = ''
        locked.value = false
        submitted.value = false
        lastAnswerId.value = null
        resetFollowUp()
        if (currentIndex.value < questions.value.length - 1) currentIndex.value++
      }

      const handleExamFinished = (message) => {
        finishMessage.value = message
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
        followupType,
        followupTranscript,
        followupInterimTranscript,
        followupFeedback,
        followupLoading,
        followupLocked,
        followupListening,
        lastAnswerId,
        examFinished,
        nextDisabled,
        finishMessage,
        startListening,
        stopListening,
        restartListening,
        startFollowupListening,
        stopFollowupListening,
        restartFollowupListening,
        speakQuestion,
        rephraseQuestion,
        rephraseFollowUpQuestion,
        speakFollowUp,
        submitAnswer,
        submitFollowUp,
        nextQuestion,
        handleExamFinished
      }
    }
  }
</script>

<style scoped>
  .interim {
    font-style: italic;
    color: gray;
  }
</style>
