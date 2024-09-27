import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        print(result)

# 调用检测函数
detect_encoding('candidates.csv')
