# Sanity check

Bài này ngăn chặn user thực hiện các hành vi mở devtool hay check source code cho nên mình sẽ mở Burp Suite để xem source code của web như thế nào? 

![image](https://hackmd.io/_uploads/SycQVOhSR.png)
Flag có ngay trong source code của bài.
Flag: `vsctf{c0ngratulati0ns_y0u_viewed_the_s0urc3!...welcome_to_vsctf_2024!}`

# Spinner

Bài này tác giả xây dựng giống bài spinner trong giải AngStromCTF mới diễn ra gần đây.

Mục tiêu là xoay đủ 9999 lần quanh chấm đỏ ta sẽ có được flag.
![image](https://hackmd.io/_uploads/B1ZnVdhSC.png)

Đây là cách mà web lấy data và gửi vị trí chuột qua websocket để tính toán số lần quay quanh chấm đỏ. 
![image](https://hackmd.io/_uploads/Hkg54uhr0.png)

```javascript=
const WebSocket = require('ws');

const ws = new WebSocket('wss://spinner.vsc.tf/ws');

ws.on('open', () => {
    console.log('WebSocket connected');

    let intervalId;

    function sendMouseData() {
        const centerX = 500 / 2;
        const centerY = 500 / 2;

        intervalId = setInterval(() => {
            const x = Math.floor(Math.random() * 500); 
            const y = Math.floor(Math.random() * 500);

            const message = {
                x: x,
                y: y,
                centerX: centerX,
                centerY: centerY
            };

            ws.send(JSON.stringify(message));
        }, 1); 
    }

    ws.on('message', (data) => {
        const message = JSON.parse(data);
        console.log('Received message:', message);

        if (message.spins >= 9999) {
            console.log('Flag:', message.message);
            clearInterval(intervalId); 
            ws.close();
        }
    });

    sendMouseData();
});

ws.on('close', () => {
    console.log('WebSocket connection closed');
});

ws.on('error', (error) => {
    console.error('WebSocket error:', error.message);
});
```

Bên trên là đoạn script payload của mình.

Sau khi giải kết thúc thì có 1 player đưa ra đoạn script ngắn hơn và có thể dán vào trong console devtool để chạy.

```javascript=
function spin(r) {
  socket.send(JSON.stringify({centerX: 0, centerY: 0, x: -r, y: -r}))
  socket.send(JSON.stringify({centerX: 0, centerY: 0, x: r, y: -r}))
  socket.send(JSON.stringify({centerX: 0, centerY: 0, x: r, y: r}))
  socket.send(JSON.stringify({centerX: 0, centerY: 0, x: -r, y: r}))
}

let i = 0.001;
setInterval(() => {
  for (let z = 0; z < 1000; z++) spin(++i);
}, 1);
```


# flarenotes

Bài này là 1 chall về XSS bypass DOMPurify. Trong thời gian diễn ra thì mình không giải được. Sau khi giải kết thúc, thì mình có hỏi anh Thắng thì anh ấy đưa cho mình solution như sau: 
> The trick was to insert a newline, because the parser of the web app created a new html for every line. Dompurify is safe but because of this parser difference it was possible to insert XSS. For dompurify my payload is `<IMG class="abc\n{some_payload}">` while website splits the whole thing and inserts 
`<IMG class="abc which the browser converts to <img class="abc">`
And the payload which get inserted on its own.
                                                              
                                                              
Đại khái thì nó sẽ như sau: Do trình dịch của web và DOMPurify khác nhau, khi mình insert newline char vào trong payload thì nó sẽ cắt thành 2 payload khác nhau, từ đó ta sẽ bypass được DOMPurify.

Giả sử mình có payload như sau:
![image](https://hackmd.io/_uploads/HkRbOO3rC.png)

Thì khi đó, web sẽ cắt payload của mình ra và chuyển thành `<img src=x onerror=alert(document.domain)>`, thẻ a thì bị cắt thành `<a href="abcd` và sẽ bị coi là 1 thẻ không hợp lệ và bị cắt đi. `"></a>` cũng như vậy
> Chú ý: Bạn cần đóng thẻ a lại cho đàng hoàng nếu không, payload img kia của chúng ta cũng sẽ bị cắt đi đấy

![image](https://hackmd.io/_uploads/ryJgFu2BC.png)


Giờ steal cookie thôi.

![image](https://hackmd.io/_uploads/BJo3YdhHC.png)
Flag: `vsctf{sh0uldnt_h4v3_us3d_cr1mefl4r3}`
