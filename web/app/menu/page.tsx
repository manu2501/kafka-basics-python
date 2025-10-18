"use client";
import useSWR from 'swr';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8080';

type BurgerMenuItem = {
  id: number;
  name: string;
  description: string;
  price: number;
  size: string;
  is_available: boolean;
};

type OrderItem = { burger_id: number; quantity: number; special_instructions?: string };

async function fetcher(url: string) {
  const res = await fetch(url);
  if(!res.ok) throw new Error('Failed to fetch');
  return res.json();
}

export default function MenuPage() {
  const { data, error, isLoading } = useSWR<BurgerMenuItem[]>(`${API_BASE}/user/menu`, fetcher);

  const submitOrder = async (form: HTMLFormElement) => {
    const formData = new FormData(form);
    const name = String(formData.get('customer_name') || 'Guest');
    const items: OrderItem[] = [];
    for(const [key, value] of formData.entries()){
      if(key.startsWith('qty_')){
        const id = Number(key.replace('qty_', ''));
        const qty = Number(value);
        if(qty>0){
          items.push({ burger_id: id, quantity: qty });
        }
      }
    }
    const resp = await fetch(`${API_BASE}/user/order`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ items, customer_name: name }) });
    const json = await resp.json();
    alert(resp.ok ? `Order Accepted! #${json.order_id}` : `Error: ${json.detail||'Unknown'}`);
  };

  if(isLoading) return <p>Loading...</p>;
  if(error) return <p>Error loading menu</p>;

  return (
    <div>
      <h1>Menu</h1>
      <form action={async (formData) => { 'use server'; }} onSubmit={async (e) => { e.preventDefault(); await submitOrder(e.currentTarget); }}>
        <div className="card">
          <label>
            Your name
            <br />
            <input name="customer_name" placeholder="John" />
          </label>
        </div>
        <div className="grid">
          {data?.map(item => (
            <div className="card" key={item.id}>
              <h3>{item.name}</h3>
              <p>{item.description}</p>
              <p><b>${'{'}item.price.toFixed(2){'}'}</b></p>
              <label>
                Qty: <input min={0} defaultValue={0} type="number" name={`qty_${'{'}item.id{'}'}`} />
              </label>
            </div>
          ))}
        </div>
        <button className="btn" type="submit">Place order</button>
      </form>
    </div>
  );
}
