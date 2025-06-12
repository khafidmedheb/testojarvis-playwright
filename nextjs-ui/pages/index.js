
import { useState } from 'react';

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');

  async function askJarvis() {
    const res = await fetch('/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    });
    const data = await res.json();
    setResponse(data.reply);
  }

  return (
    <main style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>🧪 TestoJarvis (Playwright Copilot)</h1>
      <textarea
        rows={6}
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        style={{ width: '100%' }}
      />
      <br /><br />
      <button onClick={askJarvis}>Envoyer</button>
      <pre style={{ background: '#eee', padding: '1rem', marginTop: '1rem' }}>
        {response}
      </pre>
    </main>
  );
}
