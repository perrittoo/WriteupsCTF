# sperm_rev
Đưa file vào DIE ta không thấy gì đặc biệt:

![image](https://github.com/perrittoo/Writeups/assets/69895129/c7318e00-ecfa-401d-8092-21063e500927)

Chạy thử file trên linux xem nó như nào:

![image](https://github.com/perrittoo/Writeups/assets/69895129/c56d596d-be20-4e3d-8cf0-ca26524b924c)

Thấy chương trình bảo string thì ta thử string xem ra flag không:

![image](https://github.com/perrittoo/Writeups/assets/69895129/492526e9-8c0b-4424-aaf6-51030cc2f5f9)

`AKASEC{strings_b35t_t00l_1n_r3v3r5e_eng1n33r1ng}`

# GRIP
Đưa file vào DIE ta không thấy gì đặc biệt:

![image](https://github.com/perrittoo/Writeups/assets/69895129/b8a9340e-6f8e-4b1d-8899-2c064c1de803)

Chạy thử file trên linux thì in ra mỗi `:3` và kết thúc chương trình:

![image](https://github.com/perrittoo/Writeups/assets/69895129/ada023db-d4d7-473e-b480-f6a6e7000999)

Đưa vào IDA để dịch file:

![image](https://github.com/perrittoo/Writeups/assets/69895129/7a4ec602-b18b-474d-8d9d-be3d72c35071)

![image](https://github.com/perrittoo/Writeups/assets/69895129/2a8b3c6f-47bd-422d-8a19-7714fdbacf86)

Đây là hàm main của file, nó tính toán phức tạp và in ra `:3`, 

Vì tiến trình dài và phức tạp khi nó liên tục đưa các giá trị vào v14, ta thử debug:

![image](https://github.com/perrittoo/Writeups/assets/69895129/fe4176a4-6369-481e-bc5c-874049e0964d)

Debug đến dòng `puts(":3");` thì trong cửa số hex hiện ra flag:

`akasec{sh1tty_p4y_p4ck3d_b1n4ry}`




