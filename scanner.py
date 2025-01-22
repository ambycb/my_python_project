import os
import requests
import logging
import time

def scan_and_convert(folder_path):
    logger = logging.getLogger()
    result_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # if file.endswith('.docx') or file.endswith('.pdf'):
            if file.endswith('.docx'):
                file_path = os.path.join(root, file)
                max_retries = 10  # 最大重试次数
                retries = 0
                while retries < max_retries:
                    try:
                        with open(file_path, 'rb') as f:
                            files = {'file': (file, f)}
                            logger.info(f"正在处理文件: {file_path}")
                            response = requests.post('https://ai.hbisscm.com/ai-backend/ai/document2MdAsync', files=files)
                            result_list.append(response.text)
                            logger.info(f"文件 {file_path} 处理完成，结果: {response.text}")
                        break  # 下载成功，跳出重试循环
                    except Exception as e:
                        retries += 1
                        if retries < max_retries:
                            logger.warning(f"处理文件 {file_path} 时出错，将在10秒后重试，错误信息: {e}")
                            time.sleep(10)  # 等待10秒
                        else:
                            logger.error(f"处理文件 {file_path} 失败，已达到最大重试次数，错误信息: {e}")
    return result_list