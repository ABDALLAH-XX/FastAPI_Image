import React, { useState, useEffect, useRef } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [action, setAction] = useState('gray');
  const [thresholdValue, setThresholdValue] = useState(127); 
  const [resultImage, setResultImage] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const debounceTimeout = useRef(null);

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setFile(e.target.files[0]);
      setResultImage(null); 
    }
  };

  const processImage = async (currentThreshold = thresholdValue) => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('threshold_value', currentThreshold);

    try {
      const response = await fetch(`http://127.0.0.1:8000/process/?action=${action}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error("Erreur lors du traitement");
      
      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      setResultImage(imageUrl);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!file || action !== 'threshold') return;

    if (debounceTimeout.current) clearTimeout(debounceTimeout.current);

    debounceTimeout.current = setTimeout(() => {
      processImage(thresholdValue);
    }, 40); // 40ms pour une excellente réactivité sans saccade

    return () => clearTimeout(debounceTimeout.current);
  }, [thresholdValue]);

  useEffect(() => {
    setResultImage(null);
  }, [action]);

  return (
    <div style={{ padding: '30px', textAlign: 'center', fontFamily: 'Segoe UI, sans-serif', color: '#333' }}>
      
      {/* NOUVEAU TITRE ICI */}
      <h1 style={{ color: '#5845ac', marginBottom: '30px' }}>
        PhotoLab (C++ & FastAPI)
      </h1>

      <div style={{ marginBottom: '30px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '15px' }}>
        <div>
          <input type="file" onChange={handleFileChange} accept="image/*" style={{ padding: '10px' }} />
          
          <select value={action} onChange={(e) => setAction(e.target.value)} style={{ margin: '0 10px', padding: '8px', borderRadius: '4px' }}>
            <option value="gray">Niveaux de gris</option>
            <option value="rotate90">Rotation 90°</option>
            <option value="threshold">Seuil Binaire Dynamique</option>
          </select>

          {action !== 'threshold' && (
            <button onClick={() => processImage()} disabled={loading} style={{ padding: '8px 15px', backgroundColor: '#34495e', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
              {loading ? 'Calcul C++...' : 'Exécuter le traitement'}
            </button>
          )}
        </div>

        {action === 'threshold' && (
          <div style={{ background: '#f8f9fa', padding: '15px', borderRadius: '8px', width: '350px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
            <label style={{ fontWeight: 'bold' }}>Seuil de coupure : {thresholdValue}</label>
            <input 
              type="range" 
              min="0" 
              max="255" 
              value={thresholdValue} 
              onChange={(e) => setThresholdValue(parseInt(e.target.value))}
              style={{ width: '100%', marginTop: '10px', cursor: 'pointer' }}
              disabled={!file}
            />
          </div>
        )}
      </div>

      {/* ZONE DES IMAGES OPTIMISÉE POUR ÉVITER LE TREMBLEMENT */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: '40px', flexWrap: 'wrap', marginTop: '20px' }}>
        
        {/* Boîte fixe pour l'image originale */}
        <div style={{ width: '450px', height: '450px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <h3>Image Originale</h3>
          <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#eaeaea', borderRadius: '8px', overflow: 'hidden' }}>
            {file ? (
              <img src={URL.createObjectURL(file)} alt="Original" style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }} />
            ) : (
              <p style={{ color: '#999' }}>Aucune image sélectionnée</p>
            )}
          </div>
        </div>

        {/* Boîte fixe pour l'image de résultat C++ */}
        <div style={{ width: '450px', height: '450px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <h3>Résultat OpenCV (C++)</h3>
          <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#eaeaea', borderRadius: '8px', overflow: 'hidden', border: resultImage ? '2px solid #2ecc71' : 'none', boxSizing: 'border-box' }}>
            {resultImage ? (
              <img src={resultImage} alt="Result" style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }} />
            ) : (
              <p style={{ color: '#999' }}>{loading ? 'Calcul en cours en RAM...' : 'En attente de traitement'}</p>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;