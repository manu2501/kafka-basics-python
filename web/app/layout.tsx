import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Burger App',
  description: 'User and Admin portal',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="container">
          <header className="header">
            <a href="/" className="brand">Burger</a>
            <nav className="nav">
              <a href="/menu">Menu</a>
              <a href="/admin">Admin</a>
            </nav>
          </header>
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}
