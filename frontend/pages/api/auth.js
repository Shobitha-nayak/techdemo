import { NextResponse } from 'next/server';
import { serialize } from 'cookie';

export async function POST(req) {
  const { email, password } = await req.json();

  // Replace with your own authentication logic
  if (email === 'user@example.com' && password === 'password') {
    // Set a cookie or a session for the user
    const cookie = serialize('token', 'your_token_here', { httpOnly: true, path: '/' });
    
    return NextResponse.json({ message: 'Login successful' }, { headers: { 'Set-Cookie': cookie } });
  }

  return NextResponse.json({ message: 'Invalid credentials' }, { status: 401 });
}
