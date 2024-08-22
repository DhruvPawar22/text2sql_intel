import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("http://localhost:8000/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const res = await axios.post("http://localhost:8000/query/", {
        question: question,
      });

      setResponse(res.data.data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <h1>SQL Query App</h1>
      <input type="file" onChange={handleFileChange} />
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Enter your question"
      />
      <button onClick={handleSubmit}>Submit</button>
      {response && (
        <div>
          <h2>Results:</h2>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
