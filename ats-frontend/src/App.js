import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/upload/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            setMessage(`Matched Keywords: ${response.data.matched_keywords.join(",")}`);
        } catch (error) {
            setMessage("Error uploading file");
        }
    };

    return (
        <div className="App">
            <h1>ATS Checker</h1>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} />
                <button type="submit">Upload</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
}

export default App;