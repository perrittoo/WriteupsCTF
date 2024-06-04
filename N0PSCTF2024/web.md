# Web Cook

## Preview
![image](https://hackmd.io/_uploads/B1L9Qa24R.png)
Web chỉ có chức năng nhập username, mình thử nhập admin nhưng không có gì. Check xem trong BurpSuite xem sao

![image](https://hackmd.io/_uploads/ryhb4ahN0.png)
Ở đây cookie của mình đã chuyển thành 1 serial object. Đây có vẻ là 1 challenge về Deserialization cơ bản. Chuyển `isAdmin` thành 1 và mình có flag.

![image](https://hackmd.io/_uploads/BkkP4p3EA.png)
Flag: `N0PS{y0u_Kn0W_H0w_t0_c00K_n0W}`

# Outsiders

## Preview
![image](https://hackmd.io/_uploads/S1Cc4TnNR.png)

Có vẻ như đây là 1 challenge về headers.
Tiêu đề là `You come from the big outside, I don't trust you.` Mình đã nghĩ đến 2 header là User-Agent và Referer nhưng mà sửa thì không thấy điều gì xảy ra. 

![image](https://hackmd.io/_uploads/rJlVHT2NC.png)

Lúc đó mình chợt nghĩ lại tiêu đề rằng "Bạn đến từ bên ngoài, chúng tôi hông tin bạn." Vậy thì mình bằng cách nào đó để website biết được rằng chúng ta đến từ localhost thì sao? Và mình search 403 bypass trên HackTrick. Trong đó có chứa những header để lừa website rằng mình đến từ localhost. 
![image](https://hackmd.io/_uploads/H1q0BTn4A.png)

Copy hết vào và gửi 1 thể bằng Burp Suite.

![image](https://hackmd.io/_uploads/r1gfIphVR.png)

Yes thành công. Và header đúng là X-Forwarded.
Flag: `N0PS{XF0rw4Rd3D}`

# XSS Lab

Bài XSS này mình đánh giá nó dễ, filter có rất nhiều cách bypass nhưng mà không hiểu tại sao cứ send payload là lại bị error hoặc đã visited nhưng không có request đến webhook. Do con bot nó bị lag hay sao ấy. vv

# Get A Gift

## Preview 
![image](https://hackmd.io/_uploads/HJppLThNR.png)

Bài này bắt mình nhập 1 valid gift code với regex sau `/[A-Z]{4}-[0-9]{4}-.{4,}/g`. Giftcode đúng chính là flag.

Lúc đầu mình nghĩ bruteforce tất cả các gift code theo regex (ngáo hay sao mà đâm đầu vào cái cách đấy), cho nên mình không có detect thêm các vuln. 

Sau khi có được hint từ anh Thắng thì mình mới nhận ra đây là SSTI. 
Mình nhập payload sao cho đúng đoạn regex đầu và thêm payload vào đằng sau
`ABCD-1234-abcdac {{ 7*7 }}`
Nhưng mà sau khi send, thì bị cắt mất dấu ngoặc nhọn, và dấu cách. `ABCD-1234-abcdac{7*7}`

Khi 2 hoặc nhiều dấu ngoặc đứng cách nhau nó sẽ bị filter. Mình đã có thử để 3 dấu ngoặc nhọn luôn nhưng mà vẫn bị filter. 

Hmmm, nếu bị cắt mất các dấu cách, và filter đi các dấu ngoặc nếu nó đứng cạnh nhau. Tại sao lại không để payload như `ABCD-1234-abcdac { { 7*7 } }` này nhỉ? 

Khi dấu cách bị cắt mất, nó sẽ còn lại {{7*7}} và không dấu ngoặc nào bị cắt mất cả. 

Lúc đó payload thực thi thành công, số 49 xuất hiện
![image](https://hackmd.io/_uploads/By3a_TnN0.png)

Detect được SSTI jinja2 
![image](https://hackmd.io/_uploads/S12XtanEC.png)

Do mục tiêu là đọc được valid code, cho nên mình sẽ tìm source code của file.
![image](https://hackmd.io/_uploads/Bk2hF6nNA.png)

Đọc source code để lấy valid giftcode
![image](https://hackmd.io/_uploads/Hkxqo62NR.png)

Flag: `N0PS{SSTI-1337-Templ4Te-inj3cT10N}`

# JoJo Website 1
Bài đó thì là IDOR chỗ update password của admin để chiếm nick của admin luôn.

# JoJo Website 2
https://nolliv22.com/writeups/n0psctf%202024/jojo-website-2

Cụ thể là Download Terms and ... thì sẽ ra được wkhtmltopdf bản 0.12.6 bị dính SSRF. Nhưng mà ở đây thì lại liên quan tới bypass `sed` command trong linux, khi đó sẽ command injection chỗ username. Từ đó, tạo reverse shell. Phase2 sẽ là leo quyền với file sh chạy quyền root với tar command ở folder mà ta có thể ghi. Khi đó chèn lệnh mà mình muốn thực thi vào (target ở đây là lấy được password của root cho nên đọc file shadow) rồi dùng johntheripper để crack password với hint của tác giả là rockyou.txt với best64.rule