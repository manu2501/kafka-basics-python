"use client";
import useSWR from 'swr';
import { useEffect, useRef, useState } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8080';

type Metrics = { orders_total: number; revenue_total: number };

aSYNC function fetcher(url: string) {
  const res = await fetch(url, { credentials: 'include' });
  if(!res.ok) throw new Error('Failed to fetch');
  return res.json();
}

export default function AdminPage() {
  const { data, error, isLoading } = useSWR<Metrics>(`${API_BASE}/admin/metrics`, fetcher, { refreshInterval: 3000 });
  const [events, setEvents] = useState<any[]>([]);
  const sseRef = useRef<EventSource | null>(null);

  useEffect(() => {
    sseRef.current = new EventSource(`${API_BASE}/admin/events`, { withCredentials: true });
    sseRef.current.onmessage = (evt) => {
      try { setEvents(prev => [JSON.parse(evt.data), ...prev].slice(0, 50)); } catch { /* ignore */ }
    };
    return () => { sseRef.current?.close(); };
  }, []);

  if(isLoading) return <p>Loading...</p>;
  if(error) return <p>Error loading metrics</p>;

  return (
    <div>
      <h1>Admin Dashboard</h1>
      <div className="grid">
        <div className="card">
          <h3>Orders</h3>
          <p>{data?.orders_total ?? 0}</p>
        </div>
        <div className="card">
          <h3>Revenue</h3>
          <p>${'{'}(data?.revenue_total ?? 0).toFixed(2){'}'}</p>
        </div>
      </div>

      <h2>Recent Events</h2>
      <div className="card" style={{maxHeight: 300, overflow: 'auto'}}>
        {events.map((e, idx) => (
          <pre key={idx} style={{margin:0}}>{JSON.stringify(e, null, 2)}</pre>
        ))}
      </div>
    </div>
  );
}
