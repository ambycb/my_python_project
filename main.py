import logging
import os  # 导入 os 模块
from scanner import scan_and_convert
import requests


def main():
    # 配置日志记录
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='w')
    logger = logging.getLogger()

    # 获取用户输入的文件夹路径
    # folder_path = input("请输入要扫描的文件夹路径: ")
    folder_path = "/Users/mayubo/Documents/mayubo/AI项目文件/MD文件"
    logger.info(f"开始扫描文件夹: {folder_path}")

    # 获取用户输入的下载文件夹路径
    # download_folder = input("请输入要保存下载文件的文件夹路径: ")
    download_folder = "/Users/mayubo/Documents/mayubo/AI项目文件/OA知识库转MD文件"
    # 确保下载文件夹存在
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    #开始处理文件
    results = scan_and_convert(folder_path)
    with open('results.txt', 'w') as f:
        for i, result in enumerate(results):
            f.write(f"文件 {i + 1} 的处理结果: {result}\n")
            logger.info(f"文件 {i + 1} 的处理结果: {result}")

            # 下载文件
            try:
                response = requests.get(result)
                response.raise_for_status()  # 检查请求是否成功
                # 从链接中提取文件名
                file_name = result.split('/')[-1]
                file_path = os.path.join(download_folder, file_name)
                with open(file_path, 'wb') as download_file:
                    download_file.write(response.content)
                logger.info(f"文件 {file_name} 下载完成，保存路径: {file_path}")
            except Exception as e:
                logger.error(f"下载文件 {result} 时出错: {e}")



if __name__ == "__main__":
    main()