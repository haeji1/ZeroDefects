import {useState} from 'react'
import axios from 'axios'


function UploadedFileSection(){
    const [files, setFiles] = useState([]);

    const handleFilesChange = (e) => {
        setFiles(Array.from(e.target.files));
    }

    const uploadFiles = (e) => {
        e.preventDefault();
        let formData = new FormData();

        files.map((file) => {
            formData.append("files", file);
        });

        console.log(Array.from(formData));
        console.log('첨부파일 보내기 시작');

        // 수정
        axios.post('http://localhost:8000/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
            .then((res) => {
                console.log(res.data);
                console.log('첨부파일 보내기 성공');
                const imageBase64 = res.data.img_data64;
                console.log(imageBase64);
                const imageElement = document.createElement('img');
                imageElement.src = `data:image/png;base64,${imageBase64}`;
                document.body.insertAdjacentElement('beforeend', imageElement); // 이미지를 기존 HTML 아래에 추가
            }).catch((err) => {
                console.error(err);
                console.log('첨부파일 보내기 실패');
            });
    }

    return (
        <>
            <h1>삼성전자 분석기</h1>
            <p>당신의 비밀스런 파일을 첨부하세요</p>
            <p>현재 CSV 파일만 첨부 가능합니다</p>
            <form>
                <input
                    type='file'
                    multiple={true}
                    onChange={handleFilesChange}
                    accept='.csv'
                />
                <button onClick={uploadFiles}>분석!!</button>
            </form>

            <img src="./sample.svg" alt="" />
        </>
    )
}export default UploadedFileSection