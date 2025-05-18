import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = 'http://localhost:8000'; // Your backend URL

const BhojpuriPhysicsTutor = () => {
  const [prompt, setPrompt] = useState(''); // Store the question from the user
  const [jsCode, setJsCode] = useState('');
  const [explanation, setExplanation] = useState('');
  const [isInitialized, setIsInitialized] = useState(false);
  
  const fetchExplanationAndDiagram = async () => {
    try {
      const response = await axios.post(`${BACKEND_URL}/explain`, { prompt });
      const data = response.data;
      setExplanation(data.explanation);

      const diagramResponse = await axios.post(`${BACKEND_URL}/generate_diagram_code`, { prompt });
      const diagramData = diagramResponse.data;
      setJsCode(diagramData.p5js);
      setIsInitialized(true);
    } catch (error) {
      console.error("Error fetching explanation and diagram:", error);
    }
  };

  const handleAsk = () => {
    if (prompt) {
      fetchExplanationAndDiagram();
    }
  };

  return (
    <div>
      <h1>Bhojpuri Physics Tutor (AI-Powered)</h1>
      <p>Ask a physics question and the AI tutor will explain it in Bhojpuri with text, audio, and diagrams.</p>

      <input 
        type="text" 
        placeholder="Ask a physics question..." 
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)} 
      />
      <button onClick={handleAsk}>Ask</button>

      {isInitialized && explanation && (
        <div>
          <h2>Step 1: Explanation</h2>
          <p>{explanation}</p>
        </div>
      )}

      {isInitialized && jsCode && (
        <div>
          <h2>Step 2: Diagram & Animation</h2>
          <div
            id="p5-canvas-container"
            dangerouslySetInnerHTML={{ __html: `<script> 
              function setup() { createCanvas(600, 500); angleMode(DEGREES); }
              function draw() { background(255); let amplitude = 100; let frequency = 5; 
                let x = 300 + amplitude * sin(frameCount * frequency); 
                stroke(0); fill(220); rect(295, 100, 10, 300); 
                line(300, 400, x, 400); circle(x, 400, 30);
                textSize(20); fill(0); text("ऊपर वाली बिंदु", 250, 90); 
                text("डोलन करत वस्तु", x - 60, 430); 
              }
              ${jsCode} 
            </script>` }}
          />
        </div>
      )}
    </div>
  );
};

export default BhojpuriPhysicsTutor;
