/**
 * useSpeechRecognition
 *
 * Ein Vue 3 Composable-Hook für die Sprachaufnahme und Transkription.
 * Unterstützt Interim-Ergebnisse und kontinuierliche Erkennung.
 *
 * @param {Object} options                      - Optionen zur Konfiguration
 * @param {Ref<string>} [options.transcriptRef] - Ref für endgültigen Transkripttext
 * @param {Ref<string>} [options.interimRef]    - Ref für Zwischenergebnisse
 * @param {Ref<boolean>} [options.listeningRef] - Ref für den Listening-Status
 * @param {string} [options.lang='de-DE']       - Sprache für die Spracherkennung
 *
 * @returns {Object}                      - Enthält:
 *   - transcript {Ref<string>}           - finaler Transkripttext
 *   - interimTranscript {Ref<string>}    - aktueller Zwischentext
 *   - listening {Ref<boolean>}           - ob gerade aufgenommen wird
 *   - startListening {Function}          - startet die Spracherkennung
 *   - stopListening {Function}           - stoppt die Spracherkennung
 *   - restartListening {Function}        - setzt Transkript und Status zurück
 *
 * @author Maurice Haas
 */

import { ref } from 'vue'

export function useSpeechRecognition({
  transcriptRef,
  interimRef,
  listeningRef,
  lang = 'de-DE'
} = {}) {
  const transcript = transcriptRef || ref('')
  const interimTranscript = interimRef || ref('')
  const listening = listeningRef || ref(false)
  const stopRequested = ref(false)
  let recognition = null

  const initRecognition = () => {
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      alert('Speech-to-Text wird von diesem Browser nicht unterstützt.')
      return
    }
    if (recognition) return
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    recognition = new SpeechRecognition()
    recognition.lang = lang
    recognition.interimResults = true
    recognition.continuous = true

    recognition.onresult = (event) => {
      let finalTranscript = ''
      let interim = ''
      for (let i = event.resultIndex; i < event.results.length; i++) {
        if (event.results[i].isFinal) finalTranscript += event.results[i][0].transcript
        else interim += event.results[i][0].transcript
      }
      transcript.value = (transcript.value + ' ' + finalTranscript).trim()
      interimTranscript.value = interim
    }

    recognition.onend = () => {
      if (listening.value && !stopRequested.value) recognition.start()
      else stopRequested.value = false
    }
  }

  const startListening = () => {
    initRecognition()
    if (!recognition) return
    listening.value = true
    recognition.start()
  }

  const stopListening = () => {
    if (!recognition) return
    stopRequested.value = true
    recognition.stop()
    listening.value = false
  }

  const restartListening = () => {
    transcript.value = ''
    interimTranscript.value = ''
    listening.value = false
  }

  return {
    transcript,
    interimTranscript,
    listening,
    startListening,
    stopListening,
    restartListening
  }
}
