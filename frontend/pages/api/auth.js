
import { NextResponse } from 'next/server';

export async function POST(req) {
  const { email, password } = await req.json();

  const res = await fetch('http://localhost:5006/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();

  if (res.ok) {
    const token = data.token;
    return NextResponse.json({ message: 'Login successful' }, { headers: { 'Set-Cookie': `token=${token}; HttpOnly; Path=/` } });
  }

  return NextResponse.json({ message: data.message }, { status: res.status });
}
