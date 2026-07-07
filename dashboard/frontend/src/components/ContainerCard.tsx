import { useState } from 'react'

interface Container {
  id: string
  name: string
  status: string
  image: string
  created: string
}

interface Props {
  container: Container
  token: string
  onRefresh: () => void
}

export default function ContainerCard({ container, token, onRefresh }: Props) {
  const [loading, setLoading] = useState(false)

  const action = async (act: string) => {
    setLoading(true)
    try {
      await fetch(`/api/v1/containers/${container.id}/${act}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      })
      onRefresh()
    } finally {
      setLoading(false)
    }
  }

  const isRunning = container.status === 'running'

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-medium text-white">{container.name}</h3>
          <p className="text-gray-500 text-xs mt-1 truncate max-w-48">{container.image}</p>
        </div>
        <span className={`text-xs px-2 py-1 rounded-full font-medium ${
          isRunning
            ? 'bg-green-900 text-green-400'
            : 'bg-red-900 text-red-400'
        }`}>
          {container.status}
        </span>
      </div>

      <div className="flex gap-2 mt-4">
        <button
          onClick={() => action('restart')}
          disabled={loading || !isRunning}
          className="flex-1 bg-gray-800 hover:bg-gray-700 disabled:opacity-40 text-sm py-2 rounded-lg transition-colors"
        >
          Restart
        </button>
        {isRunning ? (
          <button
            onClick={() => action('stop')}
            disabled={loading}
            className="flex-1 bg-red-900 hover:bg-red-800 disabled:opacity-40 text-sm py-2 rounded-lg transition-colors"
          >
            Stop
          </button>
        ) : (
          <button
            onClick={() => action('start')}
            disabled={loading}
            className="flex-1 bg-green-900 hover:bg-green-800 disabled:opacity-40 text-sm py-2 rounded-lg transition-colors"
          >
            Start
          </button>
        )}
      </div>
    </div>
  )
}
