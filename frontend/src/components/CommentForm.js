import React, { useState } from 'react';
import './CommentForm.css';

const CommentForm = ({ onSubmit }) => {
  const [text, setText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (text.trim() === '') {
      alert('Please enter a comment');
      return;
    }

    setIsSubmitting(true);
    const success = await onSubmit(text);
    setIsSubmitting(false);

    if (success) {
      setText('');
    }
  };

  return (
    <div className="comment-form-container">
      <form onSubmit={handleSubmit} className="comment-form">
        <div className="form-header">
          <span className="admin-badge">👤 Admin</span>
          <h3>Add a comment</h3>
        </div>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Share your thoughts..."
          className="form-textarea"
          rows="4"
          disabled={isSubmitting}
        />
        <button
          type="submit"
          className="btn-submit"
          disabled={isSubmitting || text.trim() === ''}
        >
          {isSubmitting ? 'Posting...' : '💬 Post Comment'}
        </button>
      </form>
    </div>
  );
};

export default CommentForm;
