import { NextResponse } from 'next/server';

export async function GET(req) {
  const token = req.cookies.get('token');

  const res = await fetch('http://localhost:5006/api/check-auth', {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` }
  });

  const data = await res.json();

  if (res.ok) {
    return NextResponse.json({ message: 'Authenticated', user: data.user });
  }

  return NextResponse.json({ message: data.message }, { status: res.status });
}
