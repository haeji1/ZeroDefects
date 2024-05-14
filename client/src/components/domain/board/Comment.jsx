import React from 'react';

function Comment({ content, author, date }) {
  return (<><div>{content} {author}{date}</div></>
  );
}

export default Comment;
