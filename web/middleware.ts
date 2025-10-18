import { NextRequest, NextResponse } from 'next/server';
import { jwtVerify } from 'jose';

const encoder = new TextEncoder();
const JWT_SECRET = process.env.JWT_SECRET || 'dev_secret_change_me';

export async function middleware(req: NextRequest) {
  const { pathname, search } = req.nextUrl;
  const needsAdmin = pathname === '/admin' || pathname.startsWith('/admin/');

  if (!needsAdmin) return NextResponse.next();

  const token = req.cookies.get('session')?.value;
  const redirectTo = encodeURIComponent(pathname + (search || ''));
  const loginUrl = new URL(`/login?next=${redirectTo}`, req.url);

  if (!token) return NextResponse.redirect(loginUrl);

  try {
    const { payload } = await jwtVerify(token, encoder.encode(JWT_SECRET));
    if (payload.role !== 'admin') {
      return NextResponse.redirect(new URL('/', req.url));
    }
    return NextResponse.next();
  } catch {
    return NextResponse.redirect(loginUrl);
  }
}

export const config = {
  matcher: ['/admin/:path*'],
};
