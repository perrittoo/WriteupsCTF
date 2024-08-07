# Save the city
Description: The RAW Has Got An Input That ISIS Has Planted a Bomb Somewhere In The Pune! Fortunetly, RAW Has Infiltratrated The Internet Activity of One Suspect And They Found This Link. You Have To Find The Location ASAP!

Khi deploy instance của chall này thì mình nhận được 1 shell
![image](https://hackmd.io/_uploads/ryKKwKmaT.png)
Mình đã cố nhập thử 1 thứ gì đó nhưng mà không có kết quả gì đáng chú ý.
![image](https://hackmd.io/_uploads/rJn3PF7TT.png)
Nhưng mà mình chú ý tới `SSH-2.0-libssh_0.8.1`. Khi search trên web thì đây là CVE-2018-10993 với tên là libSSH authentication bypass expolit 
https://gist.github.com/mgeeky/a7271536b1d815acfb8060fd8b65bd5d

Tải code exploit về và chạy thành công, mình đã RCE vào được server
![image](https://hackmd.io/_uploads/S1zcOY7pa.png)

Flag ở file location.txt
![image](https://hackmd.io/_uploads/HJeTutQpT.png)
Flag: `VishwaCTF{elrow-club-pune}`

# Trip To Us
Description: IIT kharakpur is organizing a US Industrial Visit. The cost of the registration is $1000. But as always there is an opportunity for intelligent minds. Find the hidden login and Get the flag to get yourself a free US trip ticket.

![image](https://hackmd.io/_uploads/SJTAYYXTp.png)

Khi nhìn thấy user welcome page của bài này, mình đã nghĩ tới tác giả giấu một số đường dẫn quan trọng đi. Vì vậy mình đã dùng gobuster để scan.
![image](https://hackmd.io/_uploads/HJt2gwETT.png)
Mình check thì chỉ thấy có endpoint `/db` là có thứ có ích. Mình được 2 file sql
![image](https://hackmd.io/_uploads/SybzZPN66.png)

Sau khi mở file users.sql ra thì mình thấy có 1 credential được cung cấp. Giờ chỉ cần đi tìm form login nữa thôi.
![image](https://hackmd.io/_uploads/BJzP-DEpa.png)

Check 1 vòng source code thì mình thấy hint tại `Error.php` khi ấn vào nút `Click Here`

![image](https://hackmd.io/_uploads/ryrF9YQp6.png)


Sau khi thay đổi User Agent trên Burp Suite, mình được redirect đến endpoint `/auth-iit-user.php`

Mình được 1 form login như sau
![image](https://hackmd.io/_uploads/rkevjF7Ta.png)

Trong source code
![image](https://hackmd.io/_uploads/S1rKoKQp6.png)

Đăng nhập và capture the flag
![image](https://hackmd.io/_uploads/HyUMfv466.png)
Flag: `VishwaCTF{y0u_g0t_th3_7r1p_t0_u5}`

P/S: Có 1 cách thay đổi header rất dễ ngay tại browser mà không cần dùng Burp Suite đó là [Requestly](https://app.requestly.io/)

# They are coming
Description: Aesthetic Looking army of 128 Robots with AGI Capabilities are coming to destroy our locality!

Check 1 vòng source code thì mình thấy 1 file js. Nghi ngờ nó không phải là 1 library opensource cho nên mình có nhìn sơ qua source của nó và thấy 1 điều đặc biệt
![image](https://hackmd.io/_uploads/Hk8GXw46p.png)
Có vẻ như Flag đã bị mã hóa với thuật toán nào đó

Cùng với chủ đề của bài này là robots, mình mở file `/robots.txt` ra thấy có hint tiếp theo
```
# https://www.robotstxt.org/robotstxt.html
User-agent: *
Disallow: /admin
L3NlY3JldC1sb2NhdGlvbg==
Decryption key: th1s_1s_n0t_t5e_f1a9
```

Decode đoạn base64 kia mình được `/secret-location`. Check endpoint `/admin` mình không thấy có điều gì đặc biệt. Đến với `/secret-location`, mình lấy được hint tiếp theo `128 cbc test`
![image](https://hackmd.io/_uploads/rke7Nw4a6.png)

Search thử thì mình thấy có 1 loại mã hóa khớp với các hint trong bài này đó là [AES 128 cbc](https://www.devglan.com/online-tools/aes-encryption-decryption). Đưa flag vào tool decrypt, và key chính là `Decryption key` trong file `robots.txt` mà mình đã đọc. Khi chạy thử thì mình nhận được thông báo 
![image](https://hackmd.io/_uploads/SyHrHPNTp.png)

Thử xóa decryption key sao cho đúng 16 kí tự và mình thành công ngay lần đầu tiên. Key là `th1s_1s_n0t_t5e_`
Flag: `VishwaCTF{g0_Su88m1t_1t_Qu14kl7}`

# Medicare Pharma
Description: Greetings form MediCare Pharma!!!!
We have started a very new pharmacy where we have various surgical equipments (more to be added soon).
But recently some hackers took control of our server and changed a hell lot of things (probably wiped out everything). Luckily we have few of the accounts and we need more consumers on board. For security reasons, we have disabled SignUp, only authorised persons are allowed to login.
Have a look at our pharmacy and hope we grow again soon.

![image](https://hackmd.io/_uploads/SkBZvv4ap.png)

Với UI như vậy cùng với description thì chall này sẽ hướng đến lỗ hổng SQLi. Đầu tiên mình đã nghĩ bài này là bypass authentication. Khi mình nhập 1 username và password hợp lệ thì ta sẽ thấy câu query sau hiện lên
`SELECT * FROM users WHERE username='perryto' and pass='perryto'`

Mình mở Burp Suite lên và bắt được file js validate input mà mình nhập vào 
```javascript=
function createAccount() {
  alert("Access Forbidden");
}

function submitForm() {
    var username = document.getElementById("uname").value;
    var password = document.getElementById("pass").value;
    var xhr = new XMLHttpRequest();
  
    xhr.onreadystatechange = function () {
      console.log('ReadyState:', xhr.readyState);
      if (xhr.readyState == XMLHttpRequest.DONE) {
        console.log('Status:', xhr.status);
        if (xhr.status == 200) {
          alert(xhr.responseText);
        } else {
          alert("Error : " + xhr.status);
        }
      }
    };
    
    xhr.open("POST", "login.php", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    
    var data = "username=" + encodeURIComponent(username) + "&password=" + encodeURIComponent(password);
    
    xhr.send(data);
  }
```

Ở đây input được mã hóa bởi hàm encodeURIComponent trước khi được gửi đi. Nói một chút về hàm này thì nó sẽ mã hóa các ký tự đặc biệt, ngoại trừ: `-_.!~*'()`. Mình thử nhập payload để bypass login như `perryto' OR 1=1--` nhưng mà câu query sai khiến response về là 502. Thay dấu comment thành `#`, payload đúng nhưng mà mình vẫn không bypass được login và nhận lại `Incorrect Username or Password`. 

Bằng 1 cách thần kì nào đó, tay mình nhập payload `perryto' UNION SELECT username,pass FROM users;#` và một số credentials hiện ra. Hơi rùa tí...
```
Username : medicare ,Password : 5trongp455!
Username : janice ,Password : 5trongp455@
Username : rootuser ,Password : 5trongp455%
Username : pharmaowner ,Password : 5trongp455$
```

Mình thử tất cả các credential và không có cái nào khác biệt cả.
![image](https://hackmd.io/_uploads/SkrBawNpa.png)

Đầu tiên mình đã nghĩ, mình sẽ tiếp tục SQLi tại thanh search để hiện ra các sản phẩm bị ẩn nhưng không có kết quả khả quan. 
Vào check source code thì mình thấy có đoạn code nghi ngờ
![image](https://hackmd.io/_uploads/SJORpPNaT.png)

Mình mua 1 sản phẩm Needle and Syringe và 1 file được tải về ngay lập tức 
```php=
<?php
header('Content-Type: application/json');

if ($_SERVER["REQUEST_METHOD"] == "POST") 
{
    $enteredInput = $_POST['search_param'];
    
    if (strlen($enteredInput) == 0)
    {
        echo json_encode(['result' => "Search bar cannot be empty"]);
    }

    else
    {
        $result = shell_exec($enteredInput);

        if ($result == null)
        {
            echo json_encode(['result' => ($enteredInput . " not found in store")]);
        }

        else
        {
            echo json_encode(['result' => $result]);
        }
    }

} 

else 
{
    http_response_code(404);
    echo json_encode(['error' => 'Access Forbidden']);
}
?>
```

Nó lấy input từ thanh search và chuyển ngay vào hàm shell_exec thì đây là command injection chứ còn gì nữa.
Thử và thành công
![image](https://hackmd.io/_uploads/BkYuCwV6T.png)

Tìm vị trí của flag và đọc nó thôi
![image](https://hackmd.io/_uploads/B1ej0DET6.png)
![image](https://hackmd.io/_uploads/Hker2ADVpp.png)

May mà không phải leo quyền nữa :)) 
Flag: `VishwaCTF{d1g1t4l_p41n_di5p4tch3d_th4nk5_f0r_sh0pp1ng_with_M3diC4re_Ph4rm4}`

# H34D3RS
```
GET / HTTP/2
Host: ch421057157746.ch.eng.run
Sec-Ch-Ua: "Chromium";v="121", "Not A(Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 10
User-Agent: lorbrowser
Date: 2044
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Priority: u=0, i
Referer: https://vishwactf.com/
Downlink: 999999999
```

