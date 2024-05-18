import { Button } from "@/components/base/button";
import { useGraphDataStore } from "@/stores/GraphData";
import React, { useState } from "react";
import Modal from "react-modal";
import {
  Card,
  CardTitle,
  CardHeader,
  CardContent,
} from "@/components/base/card";
import Lottie from "lottie-react";
import ChartLoadingGIF from "@/assets/chartloading.json";
import BokehPlot from "@/components/common/BokehPlot";
import SamsungLogo from "@/assets/images/Logo_BLUE.png";
import { Input } from "@/components/base/input";
import { FaRegEye, FaRegEyeSlash } from "react-icons/fa";

Modal.setAppElement("#root"); // 모달이 바인딩될 HTML 엘리먼트의 ID를 설정합니다.

function CreatePostModal() {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [author, setAuthor] = useState("");
  const [password, setPassword] = useState("");
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const [passwordError, setPasswordError] = useState("");
  const [authorError, setAuthorError] = useState("");

  const { graphData, isFetching } = useGraphDataStore();
  const togglePasswordVisibility = (event) => {
    setIsPasswordVisible(!isPasswordVisible);
    event.stopPropagation(); // 이벤트 버블링 중지
  };
  const openModal = () => {
    setModalIsOpen(true);
    console.log(graphData);
  };

  const validatePassword = (password) => {
    const regex = /^[A-Za-z\d!@#$%^&*()_+]{1,8}$/; // 수정된 정규식
    return regex.test(password);
  };

  const validateNickname = (author) => {
    const regex = /^.{1,8}$/; // 모든 문자를 허용하고 글자수가 1자 이상 8자 이하인지 검사
    return regex.test(author);
  };

  const handlePasswordChange = (e) => {
    const newPassword = e.target.value;
    setPassword(newPassword);

    if (!validatePassword(newPassword)) {
      setPasswordError(
        "비밀번호는 8자 이하이며 알파벳, 숫자만 포함해야 합니다."
      ); // 에러 메시지 수정
    } else {
      setPasswordError("");
    }
  };

  const handleAuthorChange = (e) => {
    const newAuthor = e.target.value;
    setAuthor(newAuthor);

    if (!validateNickname(newAuthor)) {
      setAuthorError("닉네임은 8자리 이하여야 합니다."); // 에러 메시지 수정
    } else {
      setAuthorError("");
    }
  };

  const closeModal = () => {
    setModalIsOpen(false);
    setTitle(""); // 제목 초기화
    setContent(""); // 내용 초기화
    setAuthor(""); // 작성자 초기화
    setPassword(""); // 비밀번호 초기화
    setIsPasswordVisible(false); // 비밀번호 가시성 초기화
    setPasswordError(""); // 비밀번호 에러 메시지 초기화
    setAuthorError("");
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    // 여기에 제목(title), 내용(content), 닉네임(nickname), 패스워드(password)을 사용하여 게시글 생성 로직을 구현합니다.
    // 모든 필드가 채워져 있는지 확인
    if (!title || !content || !author || !password) {
      alert("제목, 내용, 이름, 비밀번호를 모두 입력해주세요.");
      return; // 함수를 여기서 종료시켜, 더 이상 진행하지 않도록 합니다.
    }
    // 비밀번호 유효성 검사 추가
    if (!validatePassword(password)) {
      alert("비밀번호가 유효하지 않습니다.");
      return; // 비밀번호가 유효하지 않으면 함수 실행 종료
    }
    if(!validateNickname(author)){
      alert("닉네임이 유효하지 않습니다.");
      return;
    }
    // 백엔드로 보낼 데이터 구성
    const postData = {
      title,
      content,
      author,
      password,
      graphData,
    };

    // fetch를 사용하여 백엔드에 POST 요청 보내기
    fetch("http://localhost:8000/post/posts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(postData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        closeModal(); // 성공적으로 제출 후 모달 창을 닫습니다.
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div>
      <Button onClick={openModal}>공유하기</Button>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="공유하기"
        style={{
          overlay: {
            zIndex: 1000, // 이 값을 조정하여 다른 요소들보다 상위에 위치하도록 할 수 있습니다.
          },
        }}
      >
        <div className="flex justify-between items-center p-4 bg-blue-500 text-white">
          <h2 className="scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight first:mt-0">
            Share Graph
          </h2>
          <button onClick={closeModal} className="text-4xl font-semibold">
            ×
          </button>
        </div>
        <div style={{ marginLeft: "10%", marginRight: "10%" }}>
          <div style={{ padding: "20px" }}></div>
          <Card>
            <CardHeader>
              <CardTitle>Graph Overview</CardTitle>
            </CardHeader>
            <CardContent>
              {isFetching ? (
                <div className="flex flex-col items-center">
                  <Lottie
                    animationData={ChartLoadingGIF}
                    style={{ width: 400 }}
                  />
                  <p className="text-[42px]">그래프를 조회하고 있습니다.</p>
                </div>
              ) : graphData.length != 0 ? (
                graphData.map((data, index) => (
                  <div key={index}>
                    <div style={{ width: "100%" }}>
                      <BokehPlot data={data} />
                    </div>
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
          <div style={{ padding: "5px" }}></div>
          <div>
            <form onSubmit={handleSubmit}>
              <div>
                <h4 className="scroll-m-20 text-xl font-semibold tracking-tight">
                  Title
                </h4>
                <div style={{ padding: "3px" }}></div>
                <Input
                  placeholder="Input Title..."
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                />
              </div>
              <div>
                <div style={{ padding: "5px" }}></div>
                <h4 className="scroll-m-20 text-xl font-semibold tracking-tight">
                  Content
                </h4>
                <textarea
                  placeholder="Input Content..."
                  className="flex w-full rounded-md border border-input bg-transparent text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 min-h-[400px] flex-1 p-4 md:min-h-[700px] lg:min-h-[200px]"
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                />
              </div>
              <div style={{ padding: "10px" }}></div>

              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <div style={{ flex: 1, marginRight: "20px" }}>
                  <div className="text-l font-semibold">Nickname</div>
                  <div style={{ padding: "3px" }}></div>
                  <div className="flex items-center">
                    <Input
                      placeholder="Input Nickname..."
                      className="flex-1 px-3 py-2 border rounded-md"
                      value={author}
                      onChange={handleAuthorChange}
                    />
                  </div>
                  {authorError && (
                    <p style={{ color: "red" }}>{authorError}</p>
                  )}
                </div>
                <div style={{ flex: 1 }}>
                  <div className="text-l font-semibold">Password</div>
                  <div style={{ padding: "3px" }}></div>
                  <div className="flex items-center">
                    <Input
                      type={isPasswordVisible ? "text" : "password"}
                      className="flex-1 h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus-visible:outline-none"
                      value={password}
                      onChange={handlePasswordChange}
                      placeholder="Input Password..."
                    />
                    <button
                      type="button"
                      onClick={togglePasswordVisibility}
                      className="ml-2"
                    >
                      {isPasswordVisible ? <FaRegEyeSlash /> : <FaRegEye />}
                    </button>
                  </div>
                  {passwordError && (
                    <p style={{ color: "red" }}>{passwordError}</p>
                  )}
                </div>
              </div>
              <div style={{ padding: "5px" }}></div>
              <Button type="submit">Submit</Button>
            </form>
          </div>
        </div>
      </Modal>
    </div>
  );
}

export default CreatePostModal;
