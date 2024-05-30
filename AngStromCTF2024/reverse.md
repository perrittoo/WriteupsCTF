#guess_the_flag

![image](https://github.com/perrittoo/Writeups/assets/69895129/55cca493-ec92-47d2-b997-a2a8251a1af8)

Đây là file ELF64, ta chạy thử xem nó như nào

![image](https://github.com/perrittoo/Writeups/assets/69895129/54045e74-01c3-4c2c-aa6b-7be2b7e1a650)

Chương trình yêu cầu ta nhập flag kiểm tra, dùng IDA dịch ngược:

![image](https://github.com/perrittoo/Writeups/assets/69895129/00872a9a-f756-40ae-999c-5fda6dcb9141)

Nếu flag đúng thì in ra correct, flag nhập vào được xor với 1 và so sánh với `secretcode`, ta chỉ cần dùng `secretcode` xor lại với 1 là ra:

![image](https://github.com/perrittoo/Writeups/assets/69895129/ee20d116-d5d7-4f39-9daa-4442a63ed21f)

`ctf{committed_to_the_least_significant_bit}`

#switcher

![image](https://github.com/perrittoo/Writeups/assets/69895129/5976a5ae-366c-426d-a4d5-55565b423d7e)

Check thì thấy là ELF64 và không có gì đặc biệt, chạy thử trên linux xem ra cái gì:

![image](https://github.com/perrittoo/Writeups/assets/69895129/e061f090-7001-45fb-9516-9267fec4df03)

Chương trình check password, đưa vào IDA để dịch ngược:

![image](https://github.com/perrittoo/Writeups/assets/69895129/3043862c-8d2f-457b-ba2f-b709a1c5c32d)

s là input và hàm `sub_5540` để check flag, vào đó xem thì ta thấy có if else liên tục:

![image](https://github.com/perrittoo/Writeups/assets/69895129/bbe06886-7d94-4c90-a12e-753cc60a7154)

Chép mấy số này lại và chuyển từ decimal ra text ta có flag: `jumping_my_way_to_the_flag_one_by_one`
