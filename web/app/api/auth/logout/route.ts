import { NextResponse } from 'next/server';

export async function POST() {
  const res = NextResponse.json({ ok: true });
  res.cookies.set({ name: 'session', value: '', maxAge: 0, httpOnly: true, path: '/' });
  return res;
}
