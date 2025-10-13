import React, { useState } from 'react';
import './CommentItem.css';

const CommentItem = ({ comment, onEdit, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(comment.text);
  const [isSaving, setIsSaving] = useState(false);

  const handleSave = async () => {
    if (editText.trim() === '') {
      alert('Comment cannot be empty');
      return;
    }

    setIsSaving(true);
    const success = await onEdit(comment.id, editText);
    setIsSaving(false);

    if (success) {
      setIsEditing(false);
    }
  };

  const handleCancel = () => {
    setEditText(comment.text);
    setIsEditing(false);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);

    if (diffInSeconds < 60) return 'Just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;

    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div className="comment-item">
      <div className="comment-header">
        <div className="comment-author-info">
          {comment.image ? (
            <img
              src={comment.image}
              alt={comment.author}
              className="comment-avatar"
            />
          ) : (
            <div className="comment-avatar comment-avatar-default">
              {comment.author}
            </div>
          )}
          <div>
            <span className="comment-author">{comment.author}</span>
            <span className="comment-date">{formatDate(comment.date)}</span>
          </div>
        </div>
        <div className="comment-likes">
          <span className="like-icon">👍</span>
          <span className="like-count">{comment.likes}</span>
        </div>
      </div>

      <div className="comment-body">
        {isEditing ? (
          <div className="comment-edit">
            <textarea
              value={editText}
              onChange={(e) => setEditText(e.target.value)}
              className="comment-textarea"
              rows="3"
              disabled={isSaving}
            />
            <div className="comment-edit-actions">
              <button
                onClick={handleSave}
                className="btn btn-save"
                disabled={isSaving}
              >
                {isSaving ? 'Saving...' : 'Save'}
              </button>
              <button
                onClick={handleCancel}
                className="btn btn-cancel"
                disabled={isSaving}
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <>
            <p className="comment-text">{comment.text}</p>
            <div className="comment-actions">
              <button
                onClick={() => setIsEditing(true)}
                className="btn-action"
              >
                ✏️ Edit
              </button>
              <button
                onClick={() => onDelete(comment.id)}
                className="btn-action btn-delete"
              >
                🗑️ Delete
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default CommentItem;
