import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getComments = async () => {
  try {
    const response = await api.get('/comments/');
    // Handle both paginated and non-paginated responses
    return response.data.results || response.data;
  } catch (error) {
    console.error('Error fetching comments:', error);
    throw error;
  }
};

export const createComment = async (text) => {
  try {
    const response = await api.post('/comments/', {
      text,
      author: 'Admin',
      likes: 0,
      image: '',
    });
    return response.data;
  } catch (error) {
    console.error('Error creating comment:', error);
    throw error;
  }
};

export const updateComment = async (id, text) => {
  try {
    const response = await api.patch(`/comments/${id}/`, {
      text,
    });
    return response.data;
  } catch (error) {
    console.error('Error updating comment:', error);
    throw error;
  }
};

export const deleteComment = async (id) => {
  try {
    await api.delete(`/comments/${id}/`);
  } catch (error) {
    console.error('Error deleting comment:', error);
    throw error;
  }
};

export default api;
