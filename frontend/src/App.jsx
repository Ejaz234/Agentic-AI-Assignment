import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
      return;
    }

    // Add user message
    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        content: trimmedQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    const API_URL =
      import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: trimmedQuestion,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response from server");
      }

      const data = await response.json();

      // Add assistant response
      setMessages((prev) => [
        ...prev,
        {
          type: "assistant",
          content: data.answer,
          score: data.score,
          context: data.retrieved_context || [],
        },
      ]);
    } catch (error) {
      console.error("Chat error:", error);

      setMessages((prev) => [
        ...prev,
        {
          type: "assistant",
          content:
            "Unable to connect to the backend. Please make sure FastAPI is running.",
          score: null,
          context: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      askQuestion();
    }
  };

  return (
    <div className="app">

      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div>
            <h1>Agentic AI Assistant</h1>
            <p>Ask questions from the Agentic AI eBook</p>
          </div>
        </div>
      </header>

      {/* Chat */}
      <main className="chat-container">

        {/* Welcome screen */}
        {messages.length === 0 && (
          <div className="welcome">
            <h2>Ask anything about Agentic AI</h2>

            <p>
              Get answers grounded strictly in the Agentic AI eBook.
            </p>
          </div>
        )}

        {/* Messages */}
        {messages.map((message, index) => (
          <div
            className={`message ${message.type}`}
            key={index}
          >
            <div className="message-label">
              {message.type === "user" ? "You" : "Assistant"}
            </div>

            <div className="message-box">
              <p>{message.content}</p>

              {/* Assistant metadata */}
              {message.type === "assistant" &&
                message.score !== null && (
                  <div className="metadata">

                    {/* Similarity Score */}
                    <div className="score">
                      <span>Similarity Score</span>

                      <strong>
                        {message.score.toFixed(2)}
                      </strong>
                    </div>

                    {/* Sources */}
                    {message.context.length > 0 && (
                      <div className="sources">
                        <h3>Retrieved Sources</h3>

                        <div className="source-list">
                          {message.context.map(
                            (item, sourceIndex) => (
                              <div
                                className="source"
                                key={sourceIndex}
                              >
                                <span>
                                  Page {item.page}
                                </span>

                                <span>
                                  Score{" "}
                                  {item.score.toFixed(2)}
                                </span>
                              </div>
                            )
                          )}
                        </div>
                      </div>
                    )}

                  </div>
                )}
            </div>
          </div>
        ))}

        {/* Loading */}
        {loading && (
          <div className="message assistant">
            <div className="message-label">
              Assistant
            </div>

            <div className="message-box loading-box">
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>

              <span>
                Searching the knowledge base...
              </span>
            </div>
          </div>
        )}

      </main>

      {/* Input */}
      <div className="input-area">
        <div className="input-wrapper">

          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="Ask something about the eBook..."
            rows="1"
            disabled={loading}
          />

          <button
            className="send-button"
            onClick={askQuestion}
            disabled={
              loading || !question.trim()
            }
          >
            {loading ? "..." : "Send"}
          </button>

        </div>

        <p className="footer-text">
          LangGraph · Pinecone · Groq
        </p>
      </div>

    </div>
  );
}

export default App;
