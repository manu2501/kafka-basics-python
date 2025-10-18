import bcrypt from 'bcryptjs';

export type User = {
  id: string;
  username: string;
  name: string;
  role: 'admin' | 'user';
  passwordHash: string;
};

// In-memory demo users. Passwords are hashed at runtime for the demo.
const adminHash = bcrypt.hashSync('admin123', 10);
const userHash = bcrypt.hashSync('user123', 10);

export const users: User[] = [
  { id: '1', username: 'admin', name: 'Admin', role: 'admin', passwordHash: adminHash },
  { id: '2', username: 'user', name: 'User', role: 'user', passwordHash: userHash },
];
