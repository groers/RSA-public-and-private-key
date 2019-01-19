"""
所有数字以列表形式存放，并且列表第一个元素为符号位，0为正，1为负，如果数字长n位，则列表长度为n+1位
若无特别说明 export_length 均为运算中数字存储最大长度
公钥为两个数字的组合，分别为e 和m
私钥也是两个数字的组合。分别为d 和m（这个m与上面那个m相同）
"""

from random import randrange
import datetime


def bu_wei(a, export_length):
    """
    将带符号数a列表长度扩充为export_length长度，高位补0
    """

    export = [a[0]]
    new_a = a[1:]
    if len(new_a)-1 <= export_length:
        temp_list = [0]*(export_length-len(new_a))
        temp_list.extend(new_a)
        new_a = temp_list
    else:
        print("During bu wei parameter is too long!")
        exit()
    export.extend(new_a)
    return export


def compare(a, b, length):
    """
    先将a，b均扩展至length位再
    比较两个数的大小
    a > b 返回 1
    a = b 返回 0
    a < b 返回 -1
    """

    if zui_gao_wei(a) == 0:
        a[0] = 0
    if zui_gao_wei(b) == 0:
        b[0] = 0
    new_a = bu_wei(a, length)
    new_b = bu_wei(b, length)
    if a[0] != b[0]:
        if a[0] == 1:
            return -1
        else:
            return 1
    elif a[0] == 0:
        for i in range(1, length+1):
            if new_a[i] > new_b[i]:
                return 1
            elif new_a[i] < new_b[i]:
                return -1
        return 0
    else:
        for i in range(1, length+1):
            if new_a[i] > new_b[i]:
                return -1
            elif new_a[i] < new_b[i]:
                return 1
        return 0


def zui_gao_wei(a):
    """
    返回数字a的最高位所在位数
    如 [0, 0, 1, 2, 6, 4] 返回结果为4
    如 [1, 0, 0, 0, 0, 0，1, 0, 0, 7, 0] 返回结果为5 （1为符号位）
    """

    for i in range(1, len(a)):
        if a[i] > 0:
            effect_a = len(a) - i
            return effect_a
    return 0


def strip_zero(a):
    """
    去掉带符号数字前多余的0
    """

    return a[-zui_gao_wei(a)-1:]


def big_plus(a, b, base=10, export_length=64):
    """
    无符号数的加法
    """

    export = [0] * export_length  # 生成长度为export_length的全0列表
    new_a = bu_wei(a, export_length)
    new_b = bu_wei(b, export_length)
    for i in range(-1, -export_length-1, -1):
        export[i] += (new_a[i] + new_b[i])
        if export[i] >= base:
            export[i] -= base
            export[i-1] += 1
    return export


def big_minus(a, b, base=10, export_length=64):
    """
    无符号数的减法
    """

    if compare(a, b, export_length) == -1:
        print("a can not smaller than b!")
        exit()
    export = [0] * export_length  # 生成长度为export_length的全0列表
    new_a = bu_wei(a, export_length)
    new_b = bu_wei(b, export_length)
    for i in range(-1, -export_length-1, -1):
        export[i] += (new_a[i] - new_b[i])
        if export[i] < 0:
            export[i] += base
            export[i-1] -= 1
    return export


def ex_big_plus(a, b, base=10, export_length=64):
    """
    带符号数的加法
    """

    new_a = bu_wei(a, export_length)
    new_b = bu_wei(b, export_length)
    new_a[0] = new_b[0] = 0
    if a[0] == b[0]:
        export = [a[0]]
        export.extend(big_plus(new_a[1:], new_b[1:], base, export_length))
        return export
    elif compare(new_a, new_b, export_length) == 1:
        export = [a[0]]
        export.extend(big_minus(new_a[1:], new_b[1:], base, export_length))
        return export
    elif compare(new_a, new_b, export_length) == -1:
        export = [b[0]]
        export.extend(big_minus(new_b[1:], new_a[1:], base, export_length))
        return export
    else:
        export = [0]*(export_length+1)
        return export


def ex_big_minus(a, b, base=10, export_length=64):
    """
    带符号数的减法
    """

    new_a = bu_wei(a, export_length)
    new_b = bu_wei(b, export_length)
    new_b[0] = abs(new_b[0]-1)
    return ex_big_plus(new_a, new_b, base, export_length)


def big_multiply(a, b, base=10, export_length=64):
    """
    带符号数的乘法
    """

    export = [0] * export_length  # 生成长度为export_length的全0列表
    new_a = bu_wei(a, export_length)
    new_b = bu_wei(b, export_length)
    effect_a = - zui_gao_wei(new_a)
    effect_b = - zui_gao_wei(new_b)
    if new_a[0] != new_b[0]:
        result = [1]
    else:
        result = [new_a[0]]
    if (effect_a == 0) or (effect_b == 0):
        result = [0]
        result.extend(export)
        return result
    for i in range(-1, effect_a - 1, -1):
        for j in range(-1, effect_b - 1, -1):
            export[i+j+1] += (new_a[i] * new_b[j])
    for i in range(-1, -export_length - 1, -1):
        jin_wei = export[i] // base
        if jin_wei > 0:
            export[i] -= (base * jin_wei)
            export[i-1] += jin_wei
    result.extend(export)
    return result


def big_divide(a, b, base=10, export_length=64):
    """
    带符号数的除法
    返回一个二维列表，下标为0的元素为商，下标为1的元素为余数（余数绝对值为两数绝对值相除的余数，符号与被除数相同）
    """

    export = [0] * export_length  # 生成长度为export_length的全0列表
    new_a = bu_wei(a, export_length)
    new_b = bu_wei(b, export_length)
    if new_a[0] != new_b[0]:
        result = [1]
    else:
        result = [new_a[0]]
    new_a[0] = new_b[0] = 0
    if len(a) < len(b):
        result = [0]
        result.extend(export)
        return [result, new_a]
    while zui_gao_wei(new_a) >= zui_gao_wei(new_b):
        temp_bei = zui_gao_wei(new_a) - zui_gao_wei(new_b)
        while True:
            chen = [0] * (export_length+1)  # 将被除数扩大的倍数
            chen[-temp_bei - 1] = 1
            temp_list = big_multiply(new_b, chen, base, export_length)
            flag = compare(new_a, temp_list, export_length)
            if flag == 1:
                bei_shu = 1
                for j in range(base - 1, 0, -1):
                    if compare(new_a, big_multiply([0, j], temp_list, base, export_length), export_length) >= 0:
                        bei_shu = j
                        break
                new_a = ex_big_minus(new_a, big_multiply([0, bei_shu], temp_list, base, export_length), base, export_length)
                export[-temp_bei - 1] = bei_shu
                break
            elif flag == 0:
                export[-temp_bei - 1] = 1
                result.extend(export)
                return [result, [0] * (export_length + 1)]
            elif flag == -1:
                if temp_bei > 0:
                    temp_bei -= 1
                else:
                    result.extend(export)
                    new_a[0] = a[0]
                    return [result, new_a]
    result.extend(export)
    new_a[0] = a[0]
    return [result, new_a]


def qiu_ni(a, b, base=10, export_length=64):
    """
    求b mod a的逆元，如果a与b最大公约数不为1，则返回0，如果a不大于b则，报错并退出程序
    """

    x2, x1, y2, y1 = [0, 1], [0, 0], [0, 0], [0, 1]
    m, new_a, new_b = bu_wei(a, export_length), bu_wei(a, export_length), bu_wei(b, export_length)
    if compare(new_a, new_b, export_length) != 1:
        print("During qiu ni, a most bigger than b!")
        exit()
    while compare(new_b, bu_wei([0, 0], export_length), export_length) == 1:
        temp_list = big_divide(new_a, new_b, base, export_length)
        q = temp_list[0]
        r = temp_list[1]
        x = ex_big_minus(x2, big_multiply(q, x1, base, export_length), base, export_length)
        y = ex_big_minus(y2, big_multiply(q, y1, base, export_length), base, export_length)
        new_a = new_b[:]
        new_b = r[:]
        x2 = x1[:]
        x1 = x[:]
        y2 = y1[:]
        y1 = y[:]
    d = new_a[:]
    x = x2[:]
    y = y2[:]
    if compare(d, bu_wei([0, 1], export_length), export_length) == 1:
        return 0  # d是最大公约数，d大于1即a与b不互素，输入错误，返回0
    else:
        export = big_divide(y, m, base, export_length)[1]
        if compare(export, [0, 0], export_length) == -1:
            export = ex_big_plus(export, m, base, export_length)
        return export


def get_public_and_private_key():
    """
    从质数表中选取公钥和私钥并输出到屏幕
    """

    with open("RSA_files//小质数.txt") as file:  # 从小质数表中选取质数作为第一个公钥e
        little_prime_number_list = file.read().split()
    with open("RSA_files//大质数.txt") as file:  # 从大质数表中选取两个不相等的质数p和q来生成私钥d和公钥私钥公共部分m
        big_prime_number_list = file.read().split()
    p_index = randrange(0, len(big_prime_number_list))
    q_index = randrange(0, len(big_prime_number_list))
    while p_index == q_index:
        q_index = randrange(0, len(big_prime_number_list))
    p = [0]
    p.extend([int(i) for i in list(big_prime_number_list[p_index])])
    q = [0]
    q.extend([int(i) for i in list(big_prime_number_list[q_index])])
    num = len(p) + len(q)
    tem_p = ex_big_minus(p, [0, 1], 10, len(p))
    tem_q = ex_big_minus(q, [0, 1], 10, len(q))
    ro = big_multiply(tem_p, tem_q, 10, num)
    e = [0]
    e_index = randrange(0, len(little_prime_number_list))
    e.extend([int(i) for i in little_prime_number_list[e_index]])
    while compare(big_divide(tem_p, e, 10, len(p))[1], [0, 0], len(p)) == 0 or \
            compare(big_divide(tem_q, e, 10, len(q))[1], [0, 0], len(q)) == 0:  # e必须与q - 1和p - 1互素
        e = [0]
        e_index = randrange(0, len(little_prime_number_list))
        e.extend([int(i) for i in little_prime_number_list[e_index]])
    d = qiu_ni(ro, e, 10, num)  # d为e对p*q的欧拉函数的逆元
    m = big_multiply(p, q, 10, num)
    e = strip_zero(e)  # 除去将要输出结果的多余的0
    m = strip_zero(m)
    d = strip_zero(d)
    print("公钥为:")
    print(e)
    print(m)
    print("私钥为:")
    print(d)
    print(m)


def big_to_binary(a, base=10, export_length=64):
    """
    将base进制数转化为2进制数，默认base取10
    :param a: 被转化数字
    :param base: 被转化数字进制
    :param export_length: 被转化数字的最大长度
    :return: 返回二进制数
    """

    new_a = bu_wei(a, export_length)
    if compare(new_a, [0, 0], export_length) == -1:
        print("a can not smaller than 0!")
        exit()
    if compare(new_a, [0, 0], export_length) == 0:
        return [0, 0]
    export = []
    while compare(new_a, [0, 0], export_length) != 0:
        temp_list = big_divide(new_a, [0, 2], base, export_length)
        q = temp_list[0]
        r = temp_list[1]
        export.append(r[-1])
        new_a = q
    export.append(0)
    export.reverse()
    return export


def big_binary_to_else(a, base=10, export_length=64):
    """
    将2进制数转化为base进制数，默认base取10
    :param a: 被转化的二进制数
    :param base: 目标数进制
    :param export_length: 目标数字最大长度
    :return: 返回base进制的数字
    """

    result = [0, 0]
    A = [0, 1]
    new_a = a[:]
    new_a.reverse()
    for i in new_a:
        if i == 1:
            result = ex_big_plus(result, A, base, export_length)
        A = big_multiply(A, [0, 2], base, export_length)
    return result


def big_repeat_mod(a, k, m, base=10, export_length=64):
    """
    基于模重复平方算法，计算并返回a的k次方模m的结果
    """

    export_length *= 2  # 数存储长度变为两倍放置平方计算后越界
    new_a = a[:]
    new_k = k[:]
    new_m = m[:]
    if compare(new_k, [0, 0], export_length) == 0:
        return [0, 1]
    new_k = big_to_binary(new_k, base, export_length)
    new_k.reverse()
    b = [0, 1]
    A = new_a[:]
    if new_k[0] == 1:
        b = big_divide(new_a, new_m, base, export_length)[1]
    for i in new_k[1:]:
        A = big_divide(big_multiply(A, A, base, export_length), new_m, base, export_length)[1]
        if i == 1:
            b = big_divide(big_multiply(b, A, base, export_length), new_m, base, export_length)[1]
    export_length = int(export_length / 2)
    for i in range(export_length):  # 去掉输出结果中多余的0，将输出结果长度变回export_length(不计符号位)
        b.pop(1)
    return b


def string_to_code(string):
    """
    将一个字符串中每个字符转换为Ascll码，再变为2进制，统一16位，不足补0。并将这些数字按照字符串顺序连接起来，首位补0作为符号位
    如字符串长度为n，则最终的到的数字长度为16*n+1.返回这个数字
    """

    code = [0]
    for i in string:
        temp_list = [int(j) for j in list(bin(ord(i))[2:])]
        head = [0]*(16 - len(temp_list))
        head.extend(temp_list)
        code.extend(head)
    return code


def code_to_string(code):
    """
    将code数字解析回它对应的字符串，并返回
    """

    if zui_gao_wei(code) == 0:
        return ""
    new_code = code[1:]  # 去掉符号位
    aid_str = ""
    for i in range(0, len(new_code), 16):
        temp_code = [0]
        temp_code.extend(new_code[i:i+16])
        temp_code = big_binary_to_else(temp_code, 10, 64)
        temp_str = ""
        for j in range(-zui_gao_wei(temp_code), 0, 1):
            temp_str += str(temp_code[j])
        if temp_str != "":
            temp_str = chr(int(temp_str))
            aid_str += temp_str
    return aid_str


def encrypt(en_text, e, m, encrypt_length=2):
    """
    en_text :字符串形式的原文
    e: 列表形式的第一个公钥
    m: 列表形式的第二个公钥
    encrypt_length: 单位加密字符串长度
    输出为二进制字符串
    """

    # p*q的结果，即m，这个数字越大单位加密字符串的长度，即encrypt_length就能越长，保密性就越好，最长加密长度为（len（m(2进制形式)）-1）//16
    new_e = big_to_binary(e, 10, 64)
    new_m = big_to_binary(m, 10, 64)
    # ↑最后一个参数为十进制的e或者m最大位数
    en_text_list = []
    i = 0
    for i in range(0, len(en_text) - encrypt_length, encrypt_length):  # 将源字符串流分为encrypt_length个一组，置于列表中
        en_text_list.append(en_text[i:i+encrypt_length])
    i += encrypt_length
    en_text_list.append(en_text[i:])  # 将末尾不足encrypt_length个部分，也附加在列表中
    for i in range(len(en_text_list)):
        en_text_list[i] = big_repeat_mod(string_to_code(en_text_list[i]), new_e, new_m, 2, len(new_m))
        # 将列表中的字符串变为二进制代码。再进行加密，加密后存储长度为转化为二进制后m的长度+1
    export = ""
    for i in en_text_list:
        for j in i:
            export += str(j)
    return export


def decrypt(number_stream, d, m, decrypt_length=2):
    """
    number_stream: 二进制字符串
    d: 列表形式的第一个私钥
    m: 列表形式的第二个私钥
    decrypt_length: 单位加密字符串长度
    解密速度大约每两个字花费2.5s
    输出字符串形式的原文
    """

    new_d = big_to_binary(d, 10, 64)
    new_m = big_to_binary(m, 10, 64)
    # ↑最后一个参数为十进制的d或者m最大位数
    de_text = []
    for i in range(0, len(number_stream), len(new_m)+1):  # 将数字流切割成长转化为二进制后m的长度+2的字符流，作为解密单位
        temp_list = list(number_stream[i:i + len(new_m) + 1])
        for j in range(len(temp_list)):
            temp_list[j] = int(temp_list[j])
        de_text.append(temp_list)
    for i in range(len(de_text)):
        de_text[i] = big_repeat_mod(de_text[i], new_d, new_m, 2, len(new_m))[-16*decrypt_length-1:]
        # 将密文还原为二进制原文，并保留有用部分，即只保留末尾16*decrypt_length+1位（算上符号位）
    decrypted_str = ""
    for i in de_text:
        decrypted_str += code_to_string(i)  # 将二进制原文还原为字符串，并返回
    return decrypted_str


e = [0, 3, 7, 9, 7]
m = [0, 1, 0, 1, 3, 0, 6, 5, 1, 9, 7, 4, 5, 9, 7, 1]
d = [0, 4, 6, 1, 3, 0, 8, 7, 6, 4, 3, 8, 1, 4, 1]

# get_public_and_private_key()
start_time = datetime.datetime.now()
print("开始时间: "+str(start_time))
# with open("RSA_files//text3.txt", "r") as file:
#     source_text = file.read()
source_text = "君埋泉下泥销骨，@我寄人间雪满头！09）（】"
encrypted_text = encrypt(source_text, e, m)
print(decrypt(encrypted_text, d, m))
end_time = datetime.datetime.now()
print("结束时间: "+str(end_time))
print("花费时间: "+str(end_time - start_time))
