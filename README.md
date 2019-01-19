# RSA-public-and-private-key
you can use the code to get your own public and private key. you can also use them to encrypt your text, and decrypt the encrypted text。
使用函数get_public_and_private_key()可以在屏幕上输出系统随机生成的公钥和私钥将之复制到对应的e，d，m变量进行覆盖即可使用。
使用encrypt函数可以对文本进行加密，输出的密文是字符串形式的2进制数字串。
使用decrypt函数可以对2进制文本进行解密还原文本，解密速度大约是每两个字耗时2.5s。
源代码中自带使用范例。
公钥为两个数字的组合，分别为e 和m
私钥也是两个数字的组合。分别为d 和m（这个m与上面那个m相同）
大质数.txt为公钥和私钥的公共元素m的因子p和q的提供来源
小质数.txt为公钥e的提供来源，私钥d由p和q和e共同进行计算得出

