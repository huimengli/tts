import os;
import re;
import torch;

from ttskit.sdk_api import tts_sdk;
from pydub import AudioSegment;

outputFile = "output.wav";                      #输出文件
output_folder = "tempWav";                      #音频文件暂存位置
speaker = "14";                                 #语言模型
file_path = "女主来现实砍我，你跟我说游戏.txt"  #输入文件

def openWtite(path:str,s:str):
    '''
    打开一个不存在的文件并写内容
    '''
    with open(path,"wb") as f:
        f.write(s);
    return;

def readAdd(folder_path,outputFile):
    '''
    读取文件夹中的所有wav文件并且按照文件名顺序合并
    '''
    # 获取文件夹中所有的wav文件
    files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
    files.sort()  # 按文件名排序

    # 读取并合并文件
    combined = AudioSegment.empty()
    for file in files:
        sound = AudioSegment.from_wav(os.path.join(folder_path, file))
        combined += sound

    # 导出合并后的文件
    combined.export(outputFile, format="wav")

def deleteDir(folder_path):
    '''
    删除文件夹中的所有内容
    '''
    # 检查文件夹是否存在
    if os.path.exists(folder_path):
        # 删除文件夹中的所有内容
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    else:
        print("The folder does not exist.")

def readTxtToWav(file_path, output_folder):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

     # 读取文本文件
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 定义多种句号
    sentence_endings = re.compile(r'[。.！!?？]+')

    # 按照句号或150个字符分割文本
    sentences = []
    while text:
        # 查找最近的句号位置
        match = sentence_endings.search(text[:150])
        if match:
            end = match.end()
        else:
            end = 150

        sentences.append(text[:end].strip())
        text = text[end:]

    # 将每个句子转换成语音
    for i, sentence in enumerate(sentences, start=1):
        wav_data = tts_sdk(sentence,audio=speaker)
        with open(os.path.join(output_folder, f"{i}.wav"), 'wb') as f:
            f.write(wav_data)

if __name__ == "__main__":
    
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"        #设置GPU,如果有CUDA则能加速
    #print(torch.cuda.is_available());

    readTxtToWav(file_path,output_folder);
    readAdd(output_folder,outputFile);
    deleteDir(output_folder);
