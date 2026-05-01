"use client";
import { useState } from "react";
import { register, createTask, getTask } from "../lib/api";

export default function Page(){
  const [token,setToken]=useState(""); const [topic,setTopic]=useState("AI副业");
  const [taskId,setTaskId]=useState<number|undefined>(); const [result,setResult]=useState<any>(null);

  return <main style={{maxWidth:900,margin:'30px auto',fontFamily:'sans-serif'}}>
    <h1>内容生产控制台</h1>
    <button onClick={async()=>{const d=await register('demo','demo1234'); setToken(d.access_token);}}>一键注册Demo</button>
    <p>Token: {token? token.slice(0,20)+"...":"未登录"}</p>
    <input value={topic} onChange={e=>setTopic(e.target.value)} />
    <button onClick={async()=>{const d=await createTask(token,{topic,platform:'xiaohongshu',count:5,use_evaluator:true}); setTaskId(d.id);}}>创建任务</button>
    <button onClick={async()=>{if(taskId){const d=await getTask(token,taskId); setResult(d);}}}>刷新结果</button>
    <pre>{JSON.stringify(result,null,2)}</pre>
  </main>
}
