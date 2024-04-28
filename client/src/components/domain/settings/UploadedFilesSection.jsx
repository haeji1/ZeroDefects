import {useState} from 'react'
import axios from 'axios'
import { Button } from '@/components/base/button';
import { Input } from '@/components/base/input';

function UploadedFileSection(){
    const [files, setFiles] = useState([]);

    const handleFilesChange = (e) => {
        setFiles(Array.from(e.target.files));
    }
    
    const deleteFile = (fileName) => {
        setFiles(files.filter(file => file.name !== fileName));
    };

    const onReset= () => {
        setFiles([]);
    };


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
            <div style={{
        display: 'flex',
        justifyContent: 'center', // 가로 방향으로 중앙 정렬
        alignItems: 'center', // 세로 방향으로 중앙 정렬
        height: '100vh', // 부모 컨테이너의 높이를 화면 높이와 동일하게 설정
        flexDirection: 'column', // 자식 요소들을 세로로 배열
    }}>
            <form style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '10px', width: '60%' }}>
                <Input
                    id="fileInput"
                    type='file'
                    multiple={true}
                    onChange={handleFilesChange}
                    accept='.csv'
                />
                <Button onClick={uploadFiles}>분석!!</Button>
            </form>
            <div>
                {files.map((file, index) => (
                    <div key={index} style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        {file.name}
                        <button onClick={() => deleteFile(file.name)}>삭제</button>
                    </div>
                ))}
            </div>
            <Button onClick={onReset}> 전체 삭제 </Button>
            </div>
        </>
    )
}export default UploadedFileSection