# -*- coding: utf-8 -*-
"""1colab_browser.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SX7cV6sjPXD37X--paPo7Iv_vRc47uWu
"""

from google.colab import drive
drive.mount('/content/drive', force_remount=True)

#!git clone https://github.com/Q110722/umpiyamPF.git
!git clone -b main https://github.com/Q110722/umpiyamPF.git
#!git clone https://github.com/MaPM-git/MapleDpm.git

!git config --global user.email "mushbisu@gmail.com"
!git config --global user.name "Q110722"
#!git remote add origin https://github.com/Q110722/umpiyamPF.git
#!git remote -v
#!git status
#!git remote set-url origin https://github.com/Q110722/umpiyamPF

!cd /content/umpiyamPF/
!git init
!git remote set-url origin https://github.com/Q110722/umpiyamPF

# Commented out IPython magic to ensure Python compatibility.
# %cd umpiyamPF

#!git init
!git remote set-url origin https://Q110722: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@github.com/Q110722/umpiyamPF
#!git remote set-url origin https://<username>@github.com/Q110722/umpiyamPF.git
!git add .
!git commit -m "diff_dark 가독성 및 기반작업시작"
!git push origin main

!git add "ㅇ".ipynb
!git commit -m "ㅇ"
!git push origin main

!git checkout ipynb_and_revision_html

##### 변환기
!pip install nbformat

import nbformat as nbf

py_file = '/content/umpiyamPF/레거시/calculate_DPM_6th4_restraint.py'
ipynb_file = '/content/umpiyamPF/레거시/calculate_DPM_6th4_restraint.ipynb'

with open(py_file, 'r') as f:
    code = f.read()

nb = nbf.v4.new_notebook()
nb['cells'] = [nbf.v4.new_code_cell(code)]

with open(ipynb_file, 'w') as f:
    nbf.write(nb, f)

##### to py
!pip install nbconvert

import nbformat
from nbconvert import PythonExporter

ipynb_file = '/content/calculate_DPM_6th4_new.ipynb'
py_file = '/content/calculate_DPM_6th4_new.py'

with open(ipynb_file, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

exporter = PythonExporter()
code, _ = exporter.from_notebook_node(nb)

with open(py_file, 'w', encoding='utf-8') as f:
    f.write(code)

##### 비교기
import difflib
import os

file1 = '/content/MapleDpm/src/main/java/org/mapledpmlab/type/dealcyclesolo/PathFinderDealCycle.java'
file2 = '/content/MapleDpm/src/main/java/org/mapledpmlab/type/dealcyclesolo/PathFinderContinuousDealCycle.java'

# 파일 읽기
with open(file1) as f1, open(file2) as f2:
    lines1 = f1.readlines()
    lines2 = f2.readlines()

# diff
differ = difflib.HtmlDiff(tabsize=4, wrapcolumn=80)
diff_html = differ.make_file(lines1, lines2, fromdesc=file1, todesc=file2)

# 파일명
base1 = os.path.splitext(os.path.basename(file1))[0]
base2 = os.path.splitext(os.path.basename(file2))[0]

# 공통 prefix 찾기
common_prefix = os.path.commonprefix([base1, base2])
unique1 = base1[len(common_prefix):]
unique2 = base2[len(common_prefix):]

output_filename = f'{base1}_vs_{unique2}_diff_dark.html'

style = """
<style>
    body {
        background-color: #0a0a0a;
        color: #ffffff;
        font-family: 'Courier New', monospace;
        font-size: 14px;
    }
    table.diff {
        width: 100%;
        border-collapse: collapse;
    }
     .diff_header {
        background-color: #000000 !important;
        color: #ffffff;
        font-size: 20px;
        text-align: center !important; /*헤더번호*/
    }
    .diff_next {
        background-color: #111111;
        text-align: center;
    }
    .diff_add {
        background-color: #144212 !important;  /* 진초록 */
        color: #ffffff;
    }
    .diff_chg {
        background-color: #6b3e1d !important;  /* 오렌지브라운 */
        color: #ffffff;
    }
    .diff_sub {
        background-color: #5b1d1d !important;  /* 밤색 */
        color: #ffffff;
    }
    td, th {
        border: 1px solid #666;
        padding: 2px;
        white-space: pre-wrap;      /* 줄바꿈 허용 */
        overflow-wrap: break-word; /* normal = 오버플로됨 */
        word-break: normal;     /* break-word = 단어 중간 줄바꿈 */
        max-width: 500px;           /* 너비조정 */
        vertical-align: top;
    }
</style>
"""

diff_html_with_style = style + diff_html

# 저장
output_dir = os.path.dirname(file1)
output_path = os.path.join(output_dir, output_filename)
with open(output_path, 'w') as f:
    f.write(diff_html_with_style)

print(f"HTML diff saved as: {output_filename}")

import sys
import numpy as np
import matplotlib.pyplot as plt
from set_stat import set_directory, cal_stat, print_stat
from calculate_DPM_6th4_log_rev_34 import cal_DPM_6th4_log_rev_34

from calculate_log import cal_log
from calculate_log2 import cal_log2
from calculate_log_assault_fix2 import cal_log_assault_fix2
from calculate_log_assault_fix3 import cal_log_assault_fix3
from calculate_log_assault_fix4 import cal_log_assault_fix4
import os


#sys.path.append('/content/umpiyamPF')
sys.path.append('/content/umpiyamPF/test')
!python umpiyamPF/main.py

print("현재 디렉토리:", os.getcwd())

import requests
from bs4 import BeautifulSoup
from difflib import HtmlDiff

# 함수: 본문 추출 (GM 소리 올림 << 이전의 내용만 추출)
def extract_text_from_maple_notice(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 본문이 포함될 수 있는 클래스들
    candidate_classes = ['notice_wrap', 'contents_wrap']

    for class_name in candidate_classes:
        content_div = soup.find('div', class_=class_name)
        if content_div:
            text = content_div.get_text(separator='\n', strip=True)

            # 'GM 소리 올림 <<' 이전까지의 텍스트만 추출
            split_text = text.split('GM소리 올림', 1)
            return split_text[0] + 'GM소리 올림'  # 'GM소리 올림' 이전까지의 내용만 반환

    return "❌ 본문을 찾을 수 없습니다."

# 두 개의 URL
url2 = 'https://maplestory.nexon.com/news/update/769'
url1 = 'https://maplestory.nexon.com/testworld/news/all/94'

# 텍스트 추출
text1 = extract_text_from_maple_notice(url1).splitlines()
text2 = extract_text_from_maple_notice(url2).splitlines()

# HTML 비교 시각화
differ = HtmlDiff()
diff_html = differ.make_file(text1, text2, fromdesc='테섭', todesc='본섭 공지')

style = """
<style>
    body {
        font-size: 12px;
    }
    .diff_header {
        font-size: 32px;
    }
    .diff_add {
        font-size: 18px;
    }
    .diff_chg {
        font-size: 18px;
    }
    .diff_sub {
        font-size: 18px
    }
    .diff_content {
        font-size: 18px;
    }
    pre, td {
        font-size: 18px;  /*pre 태그 테이블 데이터*/
    }
</style>
"""

diff_html_with_style = style + diff_html

# 파일로 저장
output_path = "/content/maple_notice_diff.html"  # /mnt/data 대신 /content 경로 사용
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(diff_html_with_style)

output_path

from google.colab import files
files.download('maple_notice_diff.html')

