'use client'

import { useState } from 'react'
import axios from 'axios'

interface AiResponse {
  question: string
  reponse: string
  type: 'sarcastique' | 'normale'
  est_bete: boolean
  confiance_normale: number
  confiance_bete: number
}

export default function Home() {
  const [question, setQuestion] = useState('')
  const [response, setResponse] = useState<AiResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim()) return

    setLoading(true)
    setError('')
    setResponse(null)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'
      const res = await axios.post<AiResponse>(`${apiUrl}/api/ai/ask`, {
        question: question.trim(),
      })
      setResponse(res.data)
    } catch (err) {
      setError('Erreur lors de la communication avec l\'IA')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            🤖 IA Sarcastique
          </h1>
          <p className="text-xl text-gray-600">
            Détecteur de questions bêtes avec réponses sarcastiques
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Entraînée pour reconnaître les questions basiques et répondre avec ironie 😏
          </p>
        </div>

        {/* Form */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="question" className="block text-lg font-semibold text-gray-700 mb-3">
                Pose ta question :
              </label>
              <textarea
                id="question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ex: C'est quoi une variable ? ou Comment implémenter un algorithme de consensus Raft ?"
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 text-gray-800 text-lg resize-none"
                rows={4}
                disabled={loading}
              />
            </div>

            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold py-4 px-6 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed text-lg shadow-lg"
            >
              {loading ? '🤔 Analyse en cours...' : '🚀 Analyser la question'}
            </button>
          </form>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg mb-8">
            <p className="font-bold">Erreur</p>
            <p>{error}</p>
          </div>
        )}

        {/* Response */}
        {response && (
          <div className="space-y-6">
            {/* Question posée */}
            <div className="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-lg">
              <p className="text-sm text-blue-600 font-semibold mb-2">Question posée :</p>
              <p className="text-gray-800 text-lg">{response.question}</p>
            </div>

            {/* Réponse de l'IA */}
            <div
              className={`border-l-4 p-6 rounded-lg ${
                response.est_bete
                  ? 'bg-red-50 border-red-500'
                  : 'bg-green-50 border-green-500'
              }`}
            >
              <div className="flex items-center justify-between mb-4">
                <p
                  className={`text-sm font-bold ${
                    response.est_bete ? 'text-red-600' : 'text-green-600'
                  }`}
                >
                  {response.est_bete ? '😤 Question bête détectée !' : '✅ Question normale'}
                </p>
                <span
                  className={`px-4 py-1 rounded-full text-sm font-semibold ${
                    response.est_bete
                      ? 'bg-red-200 text-red-800'
                      : 'bg-green-200 text-green-800'
                  }`}
                >
                  {response.type}
                </span>
              </div>
              <p className="text-gray-800 text-lg font-medium">{response.reponse}</p>
            </div>

            {/* Statistiques */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-bold text-gray-700 mb-4">📊 Analyse de confiance :</h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-600">Question normale</span>
                    <span className="font-bold text-green-600">
                      {(response.confiance_normale * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-green-500 h-3 rounded-full transition-all"
                      style={{ width: `${response.confiance_normale * 100}%` }}
                    />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-600">Question bête</span>
                    <span className="font-bold text-red-600">
                      {(response.confiance_bete * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-red-500 h-3 rounded-full transition-all"
                      style={{ width: `${response.confiance_bete * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="mt-12 text-center text-gray-500 text-sm">
          <p>Modèle : DistilBERT multilingual • Précision : 98.92%</p>
          <p className="mt-2">Entraîné sur 464 questions (244 bêtes + 220 normales)</p>
        </div>
      </div>
    </main>
  )
}
