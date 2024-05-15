import { Button } from '@/components/base/button';
import { useGraphDataStore } from '@/stores/GraphData';
import React, { useState } from 'react';
import Modal from 'react-modal';
import { Card,CardTitle, CardHeader, CardContent} from '@/components/base/card';
import Lottie from 'lottie-react';
import ChartLoadingGIF from "@/assets/chartloading.json";
import BokehPlot from "@/components/common/BokehPlot";
import SamsungLogo from "@/assets/images/Logo_BLUE.png";

Modal.setAppElement('#root'); // 모달이 바인딩될 HTML 엘리먼트의 ID를 설정합니다.

function CreatePostModal() {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [author, setAuthor] = useState('');
  const [password, setPassword] = useState('');

  const { graphData, isFetching } = useGraphDataStore();

  const openModal = () => {
    setModalIsOpen(true);
    console.log(graphData)
  };

  const closeModal = () => {
    setModalIsOpen(false);
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    // 여기에 제목(title), 내용(content), 닉네임(nickname), 패스워드(password)을 사용하여 게시글 생성 로직을 구현합니다.
  
    // 백엔드로 보낼 데이터 구성
    const postData = {
      title,
      content,
      author,
      password,
      graphData,
    };
  
    // fetch를 사용하여 백엔드에 POST 요청 보내기
    fetch('http://localhost:8000/post/posts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postData),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      closeModal(); // 성공적으로 제출 후 모달 창을 닫습니다.
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };

  return (
    <div>
      <Button onClick={openModal}>공유하기</Button>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="공유하기"
      >
        <h2>글 작성</h2>
        <button onClick={closeModal}>닫기</button>
        <div className="flex flex-col ">
      <Card className="mr-5 min-h-[800px]">
        <CardHeader>
          <CardTitle>Graph Overview</CardTitle>
        </CardHeader>
        <CardContent>
          {isFetching ? (
            <div className="flex flex-col items-center">
              <Lottie animationData={ChartLoadingGIF} style={{ width: 400 }} />
              <p className="text-[42px]">그래프를 조회하고 있습니다.</p>
            </div>
          ) : graphData.length != 0 ? (
            graphData.map((data, index) => (
              <div key={index}>
                <BokehPlot data={data} />
              </div>
            ))
          ) : (
            <div className="flex flex-col items-center my-[100px]">
              <img src={SamsungLogo} width={800} alt="" />
              <p className="text-[40px]">GLOBAL TECHNOLOGY RESEARCH</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
        <form onSubmit={handleSubmit}>
          <div>
            <label>제목</label>
            <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} />
          </div>
          <div>
            <label>내용</label>
            <textarea value={content} onChange={(e) => setContent(e.target.value)} />
          </div>
          <div>
            <label>닉네임</label>
            <textarea value={author} onChange={(e) => setAuthor(e.target.value)} />
          </div>
          <div>
            <label>패스워드</label>
            <textarea value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          <button type="submit">제출</button>
        </form>
      </Modal>
    </div>
  );
}

export default CreatePostModal;
