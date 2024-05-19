import { create } from 'zustand';



interface CommentStoreState {
  comments: any[];
  addComment: (comment: any) => void;
  setComments: (comments: any[]) => void;
}

const useCommentStore = create<CommentStoreState>(set => ({
  comments: [],
  addComment: (comment: any) => set(state => ({ comments: [...state.comments, comment] })),
  setComments: (comments: any) => set({ comments }),
}));

export default useCommentStore;