import { NextRequest, NextResponse } from 'next/server';
import { jwtVerify } from 'jose';

const encoder = new TextEncoder();
const JWT_SECRET = process.env.JWT_SECRET || 'dev_secret_change_me';

export async function GET(req: NextRequest) {
  try {
    const token = req.cookies.get('session')?.value;
    if (!token) return NextResponse.json({ user: null }, { status: 200 });

    const { payload } = await jwtVerify(token, encoder.encode(JWT_SECRET));
    const user = {
      id: String(payload.sub || ''),
      username: String(payload.username || ''),
      name: String(payload.name || ''),
      role: String(payload.role || ''),
    };
    return NextResponse.json({ user });
  } catch {
    return NextResponse.json({ user: null }, { status: 200 });
  }
}
