"use client"
import { useState, useEffect } from 'react'

export default function Home() {
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetch('/api/solve')
            .then(res => res.json())
            .then(data => { setData(data); setLoading(false) })
    }, [])

    if (loading) return <div className="p-8">Loading solution...</div>

    return (
        <main className="p-8 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-4">Show HN: We built open OpenRouter that turns usage into a better model</h1>
            <p className="text-gray-600 mb-8">Hi HN, we built an open source model gateway. It&#x27;s a single place to manage our own self hosted, frontier, and open source models in one place.<p>It’s is rust native, built for concurrency, and i</p>
            <div className="bg-gray-50 p-6 rounded-lg">
                <h2 className="text-xl font-semibold mb-2">AI-Generated Solution</h2>
                <pre className="bg-white p-4 rounded overflow-auto text-sm">
                    {JSON.stringify(data, null, 2)}
                </pre>
            </div>
        </main>
    )
}