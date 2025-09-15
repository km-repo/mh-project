import { useState } from 'react'
import axios from 'axios';

import './App.css'

function App(){
  const [q, setQ] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:4000'}/search`, { query: q, k: 6 });
      setResults(res.data.results || []);
    } catch (err) {
      console.error(err);
      alert('Search failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h1>Mental Health — Response Finder</h1>
      <p style={{color: '#666'}}>Tool for professionals. Not a clinical decision maker.</p>
      <form onSubmit={submit}>
        <textarea value={q} onChange={(e)=>setQ(e.target.value)} rows={4} style={{width: '100%'}} placeholder="Paste patient query or notes..." />
        <button type="submit" disabled={!q || loading} style={{marginTop: 8}}>{loading ? 'Searching...' : 'Search'}</button>
      </form>
      <div style={{marginTop: 20}}>
        {results.map((r, idx) => (
          <div key={idx} style={{padding: 12, border: '1px solid #eee', marginBottom: 10, borderRadius: 6}}>
            <div style={{fontSize: 12, color: '#888'}}>score: {r.score.toFixed(3)}</div>
            <div><strong>Response:</strong><div>{r.response}</div></div>
            <div style={{marginTop:6, fontSize:12, color:'#555'}}><em>Context:</em> {r.context}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App
