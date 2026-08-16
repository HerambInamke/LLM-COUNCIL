import './WelcomePage.css';

export default function WelcomePage({ onNewConversation }) {
  return (
    <div className="welcome-page">
      <div className="hero-section">
        <h1>Welcome to the LLM Council</h1>
        <p className="hero-subtitle">
          A multi-agent deliberation system for high-quality, unbiased answers.
        </p>
      </div>

      <div className="features-grid">
        <div className="feature-card" style={{ animationDelay: '0.1s' }}>
          <div className="feature-icon">1</div>
          <h3>Parallel Generation</h3>
          <p>Three elite models independently evaluate your question and draft initial responses without anchoring on each other.</p>
        </div>

        <div className="feature-card" style={{ animationDelay: '0.2s' }}>
          <div className="feature-icon">2</div>
          <h3>Blind Peer Review</h3>
          <p>The models critique and rank anonymized responses from their peers to eliminate bias and identify the strongest logic.</p>
        </div>

        <div className="feature-card" style={{ animationDelay: '0.3s' }}>
          <div className="feature-icon">3</div>
          <h3>Chairman Synthesis</h3>
          <p>A designated Chairman model reviews the aggregate votes and arguments to synthesize the ultimate final answer.</p>
        </div>
      </div>

      <div className="action-section" style={{ animationDelay: '0.4s' }}>
        <button className="start-btn" onClick={onNewConversation}>
          Start Consulting the Council
        </button>
      </div>
    </div>
  );
}