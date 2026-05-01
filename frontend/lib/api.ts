const API = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export async function register(username:string, password:string){
  const r=await fetch(`${API}/auth/register`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username,password})});
  if(!r.ok) throw new Error(await r.text());
  return r.json();
}
export async function createTask(token:string, payload:any){
  const r=await fetch(`${API}/tasks`,{method:'POST',headers:{'Content-Type':'application/json','Authorization':`Bearer ${token}`},body:JSON.stringify(payload)});
  if(!r.ok) throw new Error(await r.text());
  return r.json();
}
export async function getTask(token:string,id:number){
  const r=await fetch(`${API}/tasks/${id}`,{headers:{'Authorization':`Bearer ${token}`},cache:'no-store'});
  if(!r.ok) throw new Error(await r.text());
  return r.json();
}
