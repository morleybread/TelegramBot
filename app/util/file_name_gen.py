#�����ļ� ʹɢ���㷨
import hashlib


def gen_name(str_):

    # ����һ��SHA-1��ϣ����
    sha1 = hashlib.sha1()

    # ���¹�ϣ���������
    sha1.update(str(str_).encode('utf-8'))

    # ��ȡ������SHA-1��ϣֵ
    return  sha1.hexdigest()