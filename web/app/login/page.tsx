"use client";
import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();
  const params = useSearchParams();
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState<string | null>(null);

  const next = params.get('next') || '/';

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (res.ok) {
      router.push(next);
      router.refresh();
    } else {
      const data = await res.json().catch(() => ({}));
      setError(data.error || 'Login failed');
    }
  };

  return (
    <div>
      <h1>Sign in</h1>
      <form onSubmit={onSubmit} className="card" style={{maxWidth:420}}>
        <label>Username<br/>
          <input value={username} onChange={e=>setUsername(e.target.value)} placeholder="admin or user" />
        </label>
        <br/>
        <label>Password<br/>
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        </label>
        <br/>
        <button className="btn" type="submit">Sign in</button>
        {error && <p style={{color:'crimson'}}>{error}</p>}
      </form>
      <p>Demo credentials: admin/admin123 or user/user123</p>
    </div>
  );
}
