import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [images, setImages] = useState([]);
  const [file, setFile] = useState(null);
  // Nouvel état pour l'image traitée
  const [processedImageUrl, setProcessedImageUrl] = useState(null);

  const API_URL = "http://127.0.0.1:8000";

  // 1. Charger les images au démarrage
  useEffect(() => {
    fetchImages();
  }, []);

  const fetchImages = async () => {
    try {
      const response = await axios.get(`${API_URL}/images/`);
      // Comme ton API renvoie un dictionnaire {id: {data}}, on le convertit en liste
      setImages(Object.values(response.data));
    } catch (error) {
      console.error("Erreur lors du chargement :", error);
    }
  };

  // 2. Gérer l'Upload
  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post(`${API_URL}/images/`, formData);
      setFile(null);
      fetchImages(); // Rafraîchir la galerie
    } catch (error) {
      alert("Erreur lors de l'upload");
    }
  };

  // 3. Gérer la Suppression
  const deleteImage = async (id) => {
    try {
      await axios.delete(`${API_URL}/images/${id}`);
      fetchImages();
    } catch (error) {
      alert("Erreur suppression");
    }
  };

  const processImage = async (id, action) => {
    try {
      const response = await axios.get(`${API_URL}/images/${id}/process/${action}`);
      // On récupère l'URL renvoyée par FastAPI et on l'affiche
      setProcessedImageUrl(response.data.url_processed);
    } catch (error) {
      alert("Le traitement a échoué. Vérifie tes dossiers 'uploads' et 'processed'.");
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif', maxWidth: '1000px', margin: 'auto' }}>
      <h1>📸 PhotoLab Vision</h1>
      
      {/* 1. Zone d'Upload */}
      <div style={{ marginBottom: '20px', padding: '15px', border: '2px dashed #3498db', borderRadius: '8px' }}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Uploader</button>
      </div>

      <div style={{ display: 'flex', gap: '40px' }}>
        {/* 2. Galerie de gauche (Source) */}
        <div style={{ flex: 1 }}>
          <h3>Images Sources</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: '15px' }}>
            {images.map((img) => (
              <div key={img.id} style={{ border: '1px solid #ccc', padding: '10px', borderRadius: '5px' }}>
                <img src={img.url} alt="source" style={{ width: '100%', borderRadius: '3px' }} />
                <div style={{ marginTop: '10px', display: 'flex', gap: '5px' }}>
                  <button onClick={() => processImage(img.id, 'grayscale')} title="Noir et blanc">🔘</button>
                  <button onClick={() => processImage(img.id, 'rotate')} title="Rotation 90°">🔄</button>
                  <button onClick={() => deleteImage(img.id)} style={{color: 'red'}}>🗑️</button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 3. Zone de Résultat (Droite) */}
        <div style={{ flex: 1, borderLeft: '1px solid #eee', paddingLeft: '20px' }}>
          <h3>Résultat du Traitement</h3>
          {processedImageUrl ? (
            <div>
              <img 
                src={`${processedImageUrl}?t=${new Date().getTime()}`} // Le "?t=" force le navigateur à rafraîchir l'image
                alt="Résultat" 
                style={{ width: '100%', border: '4px solid #2ecc71', borderRadius: '8px' }} 
              />
              <p>✅ Traitement terminé !</p>
              <button onClick={() => setProcessedImageUrl(null)}>Effacer l'aperçu</button>
            </div>
          ) : (
            <p style={{ color: '#888' }}>Cliquez sur un bouton de traitement pour voir le résultat ici.</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default App