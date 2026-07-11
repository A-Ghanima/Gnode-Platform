import { useState, useEffect } from 'react'
import ContainerCard from './ContainerCard'

interface Container {
  id: string
  name: string
  status: string
  image: string
  created: string
  group: string
}

interface Metrics {
  cpu_percent: number
  ram_mb: number
  ram_percent: number
}

interface Props {
  token: string
  onLogout: () => void
}

const GROUP_ORDER = ['dashboard', 'infrastructure', 'monitoring', 'apps', 'backend', 'database', 'other']

export default function Dashboard({ token, onLogout }: Props) {
  const [containers, setContainers] = useState<Container[]>([])
  const [metrics, setMetrics] = useState<Record<string, Metrics>>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchContainers = async () => {
    try {
      const res = await fetch('/api/v1/containers/', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (res.status === 401) { onLogout(); return }
      setContainers(await res.json())
    } catch {
      setError('Failed to fetch containers')
    } finally {
      setLoading(false)
    }
  }

  const fetchMetrics = async () => {
    try {
      const res = await fetch('/api/v1/metrics/containers', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (res.ok) setMetrics(await res.json())
    } catch {}
  }

  useEffect(() => {
    fetchContainers()
    fetchMetrics()
    const c = setInterval(fetchContainers, 10000)
    const m = setInterval(fetchMetrics, 30000)
    return () => { clearInterval(c); clearInterval(m) }
  }, [])

  const grouped = GROUP_ORDER.reduce((acc, group) => {
    const items = containers.filter(c => c.group === group)
    if (items.length > 0) acc[group] = items
    return acc
  }, {} as Record<string, Container[]>)

  const running = containers.filter(c => c.status === 'running').length

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold">Gnode Dashboard</h1>
          <p className="text-gray-400 text-sm">{running}/{containers.length} running</p>
        </div>
        <button onClick={onLogout} className="text-gray-400 hover:text-white text-sm transition-colors">
          Logout
        </button>
      </div>

      <div className="p-6 space-y-8">
        {loading && <p className="text-gray-400">Loading containers...</p>}
        {error && <p className="text-red-400">{error}</p>}
        {Object.entries(grouped).map(([group, items]) => (
          <div key={group}>
            <div className="flex items-center gap-3 mb-4">
              <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">{group}</h2>
              <div className="flex-1 h-px bg-gray-800" />
              <span className="text-xs text-gray-600">{items.length}</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {items.map(c => (
                <ContainerCard
                  key={c.id}
                  container={c}
                  token={token}
                  metrics={metrics[c.name] || null}
                  onRefresh={fetchContainers}
                />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
