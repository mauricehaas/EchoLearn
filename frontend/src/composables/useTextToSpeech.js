/**
 * speakText
 *
 * Wandelt einen Text in Sprache um und gibt ihn über die Systemausgabe aus.
 *
 * @param {string} text           - Der Text, der gesprochen werden soll
 * @param {string} [lang='de-DE'] - Sprachcode für die Sprachausgabe (z.B. 'de-DE', 'en-US')
 * @returns {void}                - Gibt keinen Wert zurück
 *
 * @author Maurice Haas
 */

export function speakText(text, lang = 'de-DE') {
  if (!text) return
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = lang
  utterance.rate = 1
  utterance.pitch = 1
  speechSynthesis.speak(utterance)
}
