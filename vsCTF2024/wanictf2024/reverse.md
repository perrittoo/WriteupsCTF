![image](https://github.com/perrittoo/Writeups/assets/69895129/4112f59d-9119-4a49-acd1-5531c289ac78)

![image](https://github.com/perrittoo/Writeups/assets/69895129/8122b438-331e-47d9-97e5-e2aa0fe25cdb)

Để trong notepad để dễ nhìn hơn, đi tìm thì ta có thể hiểu chút và lambda:

![image](https://github.com/perrittoo/Writeups/assets/69895129/baac5a2e-9fcf-4805-9508-4c4d4718e11a)

Nhìn vào thì ta thấy nó biến đổi đầu vào bằng cách +12 rồi -3 và cuối cùng là xor với 123 và thêm dấu _ để ra `16_10_13_x_6t_4_1o_9_1j_7_9_1j_1o_3_6_c_1o_6r`

![image](https://github.com/perrittoo/Writeups/assets/69895129/c2bd9019-d8c8-4a77-8f97-1f4969cb15bd)

Code lại và ra flag: `FLAG{l4_1a_14mbd4}`




![image](https://github.com/perrittoo/Writeups/assets/69895129/94d8b3e8-5955-4b40-a92f-b3eadf403c01)

![image](https://github.com/perrittoo/Writeups/assets/69895129/c7be0f8f-4b99-436c-bcb7-5ba5b5565753)

Nó được dùng `Protector: Obfuscator-LLVM(4.0.1)`, chạy thử xem chương trình có cái gì:

![image](https://github.com/perrittoo/Writeups/assets/69895129/7bc1a58e-8561-4cc4-91c5-0b6d5266d1ea)

Có vẻ nó không chống debug và chỉ in ra ;) thôi, mở IDA dịch ngược:

![image](https://github.com/perrittoo/Writeups/assets/69895129/73179e72-dde1-4699-8149-e92040f2b7ce)

À nhầm, nó có chống debug, sau khi `Check passed`, ta dồn sự chú ý vào hàm `constructFlag()`, mở vô thì nó có quá nhiều tính toán, mà chương trình đã chống debug thì tức là ta phải debug:

![image](https://github.com/perrittoo/Writeups/assets/69895129/062da87f-f32a-434d-ab9d-fd879ea83991)

Nhảy đến hàm `constructFlag()` để kiếm xem có gì, nhìn cái `dest` trong rất khả nghi:

![image](https://github.com/perrittoo/Writeups/assets/69895129/9b4b4c97-4ef5-4035-bdf5-6bffc390f954)

Debug cho chạy qua từng lệnh, khi ta đến dòng 157, check giá trị `dest` và xuống dưới dưới là có flag:

![image](https://github.com/perrittoo/Writeups/assets/69895129/aceac622-126b-4271-8422-e53fd73fa630)

![image](https://github.com/perrittoo/Writeups/assets/69895129/5400b74e-a55f-4991-bccc-fef1d77d45e7)

Flag{How_did_you_get_here_4VKzTLibQnPaBzi4}



















