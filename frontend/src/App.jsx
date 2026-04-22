import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [action, setAction] = useState('gray');
  const [resultImage, setResultImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResultImage(null); // Réinitialiser si on change d'image
  };

  const processImage = async () => {
    if (!file) return alert("Sélectionne une image d'abord !");

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      // On envoie l'action en paramètre d'URL comme défini dans ton FastAPI
      const response = await fetch(`http://127.0.0.1:8000/process/?action=${action}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error("Erreur lors du traitement");

      // Récupérer la réponse sous forme de blob (données binaires de l'image)
      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      setResultImage(imageUrl);
    } catch (error) {
      console.error(error);
      alert("Le serveur n'a pas pu traiter l'image.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', textAlign: 'center', fontFamily: 'sans-serif' }}>
      <h1>FastAPI + C++ Image Processor</h1>

      <div style={{ marginBottom: '20px' }}>
        <input type="file" onChange={handleFileChange} accept="image/*" />
        
        <select value={action} onChange={(e) => setAction(e.target.value)} style={{ margin: '0 10px' }}>
          <option value="gray">Niveaux de gris</option>
          <option value="rotate90">Rotation 90°</option>
        </select>

        <button onClick={processImage} disabled={loading}>
          {loading ? 'Traitement en cours...' : 'Lancer le C++'}
        </button>
      </div>

      <div style={{ display: 'flex', justifyContent: 'center', gap: '20px' }}>
        {file && (
          <div>
            <h3>Original</h3>
            <img src={URL.createObjectURL(file)} alt="Original" style={{ maxWidth: '400px' }} />
          </div>
        )}

        {resultImage && (
          <div>
            <h3>Résultat (via C++)</h3>
            <img src={resultImage} alt="Résultat" style={{ maxWidth: '400px', border: '2px solid green' }} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;