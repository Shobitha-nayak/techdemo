import { NextResponse } from 'next/server';

export async function GET(req) {
  const token = req.cookies.get('token');
  
  if (token === 'your_token_here') {
    return NextResponse.json({ message: 'Authenticated' });
  }

  return NextResponse.json({ message: 'Not authenticated' }, { status: 401 });
}
