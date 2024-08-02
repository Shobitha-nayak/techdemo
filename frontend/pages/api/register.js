import { NextResponse } from 'next/server';
import { serialize } from 'cookie';

// Dummy database and user store (replace with real database logic)
const users = []; // This is just an example; replace with a real database

export async function POST(req) {
  const { email, password } = await req.json();

  // Simple validation
  if (!email || !password) {
    return NextResponse.json({ message: 'Email and password are required.' }, { status: 400 });
  }

  // Check if user already exists
  const userExists = users.some(user => user.email === email);
  if (userExists) {
    return NextResponse.json({ message: 'User already exists.' }, { status: 400 });
  }

  // Register user (dummy example; replace with actual database logic)
  users.push({ email, password });

  // Set a cookie or a session for the user (dummy example)
  const cookie = serialize('token', 'your_token_here', { httpOnly: true, path: '/' });
  
  return NextResponse.json({ message: 'Registration successful' }, { headers: { 'Set-Cookie': cookie } });
}
