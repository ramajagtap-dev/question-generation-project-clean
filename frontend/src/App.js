import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [questions, setQuestions] = useState("");
  const [loading, setLoading] = useState(false);
  const [dark, setDark] = useState(false);

  const generate = async () => {
    setLoading(true);
    setQuestions("");

    const res = await fetch("http://127.0.0.1:5000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ context: text }),
    });

    const data = await res.json();
    setQuestions(data.questions);
    setLoading(false);
  };

  const copyText = () => {
    navigator.clipboard.writeText(questions);
    alert("Copied to clipboard!");
  };

  return (
    <div style={dark ? styles.darkBg : styles.lightBg}>
      <div style={styles.card}>

        <div style={styles.header}>
          <h1>🧠 Question Generation Using GPT</h1>

          <button
            onClick={() => setDark(!dark)}
            style={styles.toggle}
          >
            {dark ? "☀️ Light" : "🌙 Dark"}
          </button>
        </div>

        <textarea
          placeholder="Paste paragraph / Wikipedia text..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          style={styles.textarea}
        />

        <button onClick={generate} style={styles.button}>
          Generate Questions 🚀
        </button>

        {loading && <p style={styles.loading}>Generating questions...</p>}

        {questions && (
          <div style={styles.outputBox}>
            <h3>📌 Generated Questions</h3>

            <pre style={styles.output}>
              {questions.split("?").map((q, i) =>
                q.trim() ? `${i + 1}. ${q.trim()}?` : ""
              )}
            </pre>

            <button onClick={copyText} style={styles.copyBtn}>
              📋 Copy
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

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
  loading: {
    marginTop: "10px",
    color: "orange",
  },
  outputBox: {
    marginTop: "20px",
    background: "#f9f9f9",
    padding: "10px",
    borderRadius: "10px",
  },
  output: {
    whiteSpace: "pre-wrap",
    fontSize: "14px",
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
   