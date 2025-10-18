export default function HomePage() {
  return (
    <div>
      <h1>Welcome to Burger</h1>
      <p>Order delicious burgers and track metrics.</p>
      <div style={{display:'flex', gap:12}}>
        <a className="btn" href="/menu">Go to Menu</a>
        <a className="btn" href="/admin">Admin Dashboard</a>
      </div>
    </div>
  );
}
