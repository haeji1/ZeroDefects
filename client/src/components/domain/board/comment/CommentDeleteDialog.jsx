import React from 'react';
import { Button } from "@/components/base/button";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/base/alert-dialog";
import { Input } from "@/components/base/input";

function CommentDeleteDialog({ commentId, onDelete }) {
  const [deleteFormData, setDeleteFormData] = React.useState({
    id: "",
    password: "",
  });

  const handleDeleteFormChange = (e) => {
    const { name, value } = e.target;
    setDeleteFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        {/* <Button variant="outline">댓글 삭제</Button> */}
        <button className="text-sm text-gray-500">삭제</button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Comment Delete</AlertDialogTitle>
        </AlertDialogHeader>
        <AlertDialogDescription>
          If you want to delete the comment, please enter the nickname and password you used to enter the comment.
        </AlertDialogDescription>
        <Input
          type="text"
          name="id"
          placeholder="ID"
          value={deleteFormData.id}
          onChange={handleDeleteFormChange}
          required
          style={{ marginBottom: "-10px" }}
        />
        <Input
          type="password"
          name="password"
          placeholder="Password"
          value={deleteFormData.password}
          onChange={handleDeleteFormChange}
          required
          style={{ marginBottom: "-5px" }}
        />
        <AlertDialogFooter>
          <AlertDialogCancel asChild>
            <Button variant="ghost">Cancel</Button>
          </AlertDialogCancel>
          <AlertDialogAction asChild>
            <Button
              variant="solid"
              onClick={() => onDelete(commentId, deleteFormData.id, deleteFormData.password)}
            >
              Delete
            </Button>
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

export default CommentDeleteDialog;
