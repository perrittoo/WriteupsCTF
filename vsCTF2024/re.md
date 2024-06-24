# Intro

![image](https://github.com/perrittoo/Writeups/assets/69895129/9c1a5f96-7237-4413-acd4-64a6a19eb38c)

Đưa file vào DIE để check, file không có gì đặc biệt:

![image](https://github.com/perrittoo/Writeups/assets/69895129/d3d2aee3-4821-4d01-81d7-05b2e04ddf06)

Thực thi thử thì nó in ra các kí tự lạ và dừng luôn:

![image](https://github.com/perrittoo/Writeups/assets/69895129/3b05d45c-1f08-4ede-97d0-d5770d02be02)

Đưa vào IDA để dịch ngược:

![image](https://github.com/perrittoo/Writeups/assets/69895129/8286b3fa-dcca-4fdf-b819-7afa47d32895)

![image](https://github.com/perrittoo/Writeups/assets/69895129/b52d96b6-2a3c-4fb0-b7ff-994640b94489)

Code in ra các chuỗi 202 rồi xuống dòng nhưng do lệnh sleep nên nó không in ra hết được, ta code lại và bỏ cái sleep đi:

![image](https://github.com/perrittoo/Writeups/assets/69895129/021ecf23-c5a3-4b9c-adeb-9f5286d43305)

Kết quả output và thu nhỏ:

![image](https://github.com/perrittoo/Writeups/assets/69895129/99bd1ae5-4597-4693-829a-0216d2cd5516)

`vsctf{1nTr0_r3v3r51ng!}`
