import create from 'zustand';

const useCommentStore = create(set => ({
  comments: [],
  addComment: (comment) => set(state => ({ comments: [...state.comments, comment] })),
  setComments: (comments) => set({ comments }),
}));

export default useCommentStore;