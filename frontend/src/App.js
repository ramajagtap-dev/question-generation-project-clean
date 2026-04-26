import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dark, setDark] = useState(false);

  const API_URL = "https://question-generator-q32x.onrender.com/generate";

  const generate = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setQuestions([]);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ context: text }),
      });

      // 🔥 SAFE JSON PARSE
      const data = await res.json().catch(() => null);

      console.log("API RESPONSE:", data);

      if (!data) {
        setQuestions(["Server not responding ❌"]);
        return;
      }

      if (data.questions && Array.isArray(data.questions)) {
        setQuestions(data.questions);
      } 
      else if (data.question) {
        setQuestions([data.question]);
      } 
      else if (data.error) {
        setQuestions(["Backend Error: " + JSON.stringify(data.error)]);
      } 
      else {
        setQuestions(["No questions generated ❌"]);
      }

    } catch (error) {
      console.log("FETCH ERROR:", error);
      setQuestions(["Network Error ❌"]);
    }

    setLoading(false);
  };

  const copyText = () => {
    if (!questions.length) return;
    navigator.clipboard.writeText(questions.join("\n"));
    alert("Copied to clipboard!");
  };

  return (
    <div style={dark ? styles.darkBg : styles.lightBg}>
      <div style={styles.card}>
        
        {/* HEADER */}
        <div style={styles.header}>
          <h1>🧠 AI Question Generator</h1>

          <button onClick={() => setDark(!dark)} style={styles.toggle}>
            {dark ? "☀️ Light" : "🌙 Dark"}
          </button>
        </div>

        {/* INPUT */}
        <textarea
          placeholder="Paste your paragraph here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          style={styles.textarea}
        />

        {/* BUTTON */}
        <button onClick={generate} style={styles.button}>
          {loading ? "Generating..." : "Generate Questions 🚀"}
        </button>

        {/* OUTPUT */}
        {questions.length > 0 && (
          <div style={styles.outputBox}>
            <h3>📌 Generated Questions</h3>

            <ul>
              {questions.map((q, i) => (
                <li key={i} style={styles.output}>
                  {q}
                </li>
              ))}
            </ul>

            <button onClick={copyText} style={styles.copyBtn}>
              📋 Copy All
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

/* 🎨 STYLES */
const styles = {
  lightBg: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#f4f6f8",
    fontFamily: "Arial",
  },
  darkBg: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#121212",
    fontFamily: "Arial",
    color: "white",
  },
  card: {
    width: "650px",
    padding: "25px",
    borderRadius: "15px",
    backgroundColor: "white",
    boxShadow: "0 10px 30px rgba(0,0,0,0.2)",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  toggle: {
    padding: "6px 10px",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
  textarea: {
    width: "100%",
    height: "140px",
    marginTop: "10px",
    padding: "10px",
    borderRadius: "10px",
    border: "1px solid #ccc",
  },
  button: {
    marginTop: "10px",
    padding: "10px 20px",
    backgroundColor: "#4CAF50",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },
  outputBox: {
    marginTop: "20px",
    background: "#f9f9f9",
    padding: "10px",
    borderRadius: "10px",
  },
  output: {
    fontSize: "15px",
    fontWeight: "500",
    color: "#333",
    marginBottom: "5px",
  },
  copyBtn: {
    marginTop: "10px",
    padding: "6px 10px",
    border: "none",
    background: "#007bff",
    color: "white",
    borderRadius: "6px",
    cursor: "pointer",
  },
};

export default App;