import React from "react";
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
import { Button } from "@/components/base/button";
import { Input } from "@/components/base/input";

function DeletePostDialog({ setAuthor, setPassword, deletePost }) {
  return (
    <AlertDialog style={{ display: "flex", justifyContent: "flex-start" }}>
      <AlertDialogTrigger asChild>
        <button>delete</button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Post Delete</AlertDialogTitle>
        </AlertDialogHeader>
        <AlertDialogDescription>
          If you want to delete the post, please enter the nickname and
          password you used to enter the comment.
        </AlertDialogDescription>
        <Input
          type="text"
          name="id"
          placeholder="ID"
          onChange={(e) => setAuthor(e.target.value)}
          required
          style={{ marginBottom: "-10px" }}
        />
        <Input
          type="password"
          name="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ marginBottom: "-5px" }}
        />
        <AlertDialogFooter>
          <AlertDialogCancel asChild>
            <Button variant="ghost">Cancel</Button>
          </AlertDialogCancel>
          <AlertDialogAction asChild>
            <Button variant="solid" onClick={deletePost}>
              Delete
            </Button>
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

export default DeletePostDialog;
