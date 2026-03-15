/**
 * submitToEndpoint
 *
 * Sendet die Antwort eines Studierenden an das Backend zur Bewertung.
 *
 * @param {string} examId             - Eindeutige ID der Prüfung
 * @param {string} question           - Text der Prüfungsfrage
 * @param {string} studentAnswer      - Antwort des Studierenden
 * @param {string|null} correctAnswer - Optional: korrekte Antwort zur Referenz
 * @param {number} maxPoints          - Maximal erreichbare Punkte für die Frage
 *
 * @returns {Promise<Object>}         - JSON-Antwort vom Backend mit Bewertung und Feedback
 *
 * @author Maurice Haas
 */

export async function submitToEndpoint({
  examId,
  question,
  studentAnswer,
  correctAnswer = null,
  maxPoints = 5
}) {
  try {
    const res = await fetch('http://localhost:8000/exam/evaluate_answer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        unique_exam_id: examId,
        question,
        student_answer: studentAnswer,
        correct_answer: correctAnswer,
        max_points: maxPoints
      })
    })
    return await res.json()
  } catch (err) {
    console.error(err)
    return { feedback: 'Fehler beim Absenden, bitte erneut versuchen.' }
  }
}
