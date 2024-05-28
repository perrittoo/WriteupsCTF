kcehC ytinaS
![image](https://github.com/perrittoo/Writeups/assets/151734752/464a97bf-eac0-419a-bba3-ccee82ec79d2)
để ý ở đây thì có lẽ nội dung của câu này đã bị decode 
![image](https://github.com/perrittoo/Writeups/assets/151734752/9525d390-b711-46c2-aaf5-f1df339df1ec)
em có dùng cipher identifier để decode và biết được đây là loại mã hóa Writing in Reverse > esreveR
![image](https://github.com/perrittoo/Writeups/assets/151734752/5e6be60d-9e31-40f7-a664-fc02722d6173)
![image](https://github.com/perrittoo/Writeups/assets/151734752/df0107f3-ce4f-46ba-99b4-26959229d60b)
và kết quả decode ra chính là : "Join our Discord for the flag (it's the channel topic in #misc)"
kiểm tra kênh mics thì em thấy được đoạn text sau 
![image](https://github.com/perrittoo/Writeups/assets/151734752/e611f949-4058-49f3-81e2-8f9b5e4844a0)
tiếp tục decode text trên bằng mã hóa Writing in Reverse > esreveR thì em nhận được flag 
![image](https://github.com/perrittoo/Writeups/assets/151734752/51600ea0-0138-49b0-aa57-5ad45f5ab1b4)
flag : actf{how_did_you_decode_my_secret_message}

Putnam
![image](https://github.com/perrittoo/Writeups/assets/151734752/11ee04bb-ebb2-40df-9bf4-1423e03fb7df)
![image](https://github.com/perrittoo/Writeups/assets/151734752/e8fcc147-23c8-4e78-a1ab-4f8d824b9936)
câu này khi netcat vô port bài cho thì em nhập vào kết quả phép toán đề cho và nhận được flag
flag : actf{just_a_tad_easier_than_the_actual_putnam}

Trip
![image](https://github.com/perrittoo/Writeups/assets/151734752/50eccb4c-c3c1-4fc3-b79b-037429720e7d)
![image](https://github.com/perrittoo/Writeups/assets/151734752/fd060d37-c4f2-49f9-bce2-4f9f0e087e37)
dựa vào exiftool thì em tìm được GPS position của bức ảnh 
![image](https://github.com/perrittoo/Writeups/assets/151734752/e09602f0-97c0-40d1-9a19-9e000d297755)
và tìm kiếm trên gg map thì em tìm được tên đường đó chính là Chincoteague Road
![image](https://github.com/perrittoo/Writeups/assets/151734752/99511a24-2a33-4c1a-bdf2-43a93b58622d)
và flag : actf{chincoteague}

Aw man
![mann](https://github.com/perrittoo/Writeups/assets/151734752/c138d512-9391-49e1-9c6d-8787646b8a57)
![image](https://github.com/perrittoo/Writeups/assets/151734752/17647573-b0b1-4ede-8e71-b56b79a8feb8)
sau khi dùng stegano decode online và nhận được một đoạn text trên
em sử dụng cipher-identifier để decode và phát hiện ra đoạn text trên được mã hóa bằng base58
sau khi decode thì em nhận được flag
![image](https://github.com/perrittoo/Writeups/assets/151734752/8cbbb6a4-7f17-4553-afbd-bf7105d128d2)
flag : actf{crazy?_i_was_crazy_once}

do you wanna build a snowman
![image](https://github.com/perrittoo/Writeups/assets/151734752/78a6c2a1-1546-48b1-9500-d4dad9b2f4c1)
mở file nên thì em thấy file này bị lỗi k mở được
![image](https://github.com/perrittoo/Writeups/assets/151734752/44d78edd-931a-4749-860d-60be7f25558a)
em dùng exiftool để kiểm tra thì thấy thông báo là file format error
em kiểm tra hex của file trên HxD
![image](https://github.com/perrittoo/Writeups/assets/151734752/73afb933-42c0-4abb-8132-c7dd332c5af2)
nhìn qua thì hex header của file này cũng đúng với format của một file jpg.
check lại hex header của file jpg trên file signature thì chúng ta có thể thấy được hex FD ở đầu đã bị sai , và em sửa lại thành FF theo đúng format
![image](https://github.com/perrittoo/Writeups/assets/151734752/26e88df9-38d6-4b34-b758-c6b0c1af57ce)
và sau khi sửa lại thì ta có được flag trong ảnh 
![snowman](https://github.com/perrittoo/Writeups/assets/151734752/180db03c-8813-462c-82e7-71ae2443216d)
flag : actf{built_the_snowman}
