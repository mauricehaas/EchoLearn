export function speakText(text, lang = 'de-DE') {
  if (!text) return
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = lang
  utterance.rate = 1
  utterance.pitch = 1
  speechSynthesis.speak(utterance)
}
