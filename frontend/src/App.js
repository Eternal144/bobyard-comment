import React, { useState, useEffect } from 'react';
import './App.css';
import CommentList from './components/CommentList';
import CommentForm from './components/CommentForm';
import { getComments, createComment, updateComment, deleteComment } from './services/api';

function App() {
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadComments = async () => {
    try {
      setLoading(true);
      const data = await getComments();
      setComments(data);
      setError(null);
    } catch (err) {
      setError('Failed to load comments. Please try again.');
      console.error('Error loading comments:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadComments();
  }, []);

  const handleAddComment = async (text) => {
    try {
      const newComment = await createComment(text);
      setComments([newComment, ...comments]);
      return true;
    } catch (err) {
      console.error('Error adding comment:', err);
      setError('Failed to add comment. Please try again.');
      return false;
    }
  };

  const handleEditComment = async (id, newText) => {
    try {
      const updatedComment = await updateComment(id, newText);
      setComments(comments.map(comment => 
        comment.id === id ? updatedComment : comment
      ));
      return true;
    } catch (err) {
      console.error('Error editing comment:', err);
      setError('Failed to edit comment. Please try again.');
      return false;
    }
  };

  const handleDeleteComment = async (id) => {
    if (window.confirm('Are you sure you want to delete this comment?')) {
      try {
        await deleteComment(id);
        setComments(comments.filter(comment => comment.id !== id));
      } catch (err) {
        console.error('Error deleting comment:', err);
        setError('Failed to delete comment. Please try again.');
      }
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>💬 Comments</h1>
        <p>Share your thoughts</p>
      </header>

      <main className="App-main">
        <div className="container">
          {error && (
            <div className="error-message">
              {error}
              <button onClick={() => setError(null)}>✕</button>
            </div>
          )}

          <CommentForm onSubmit={handleAddComment} />

          {loading ? (
            <div className="loading">Loading comments...</div>
          ) : (
            <CommentList
              comments={comments}
              onEdit={handleEditComment}
              onDelete={handleDeleteComment}
            />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
