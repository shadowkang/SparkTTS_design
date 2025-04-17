import os
import time
import subprocess
import soundfile as sf
from pydub import AudioSegment
import textwrap

# 基本配置
model_dir = "pretrained_models\\Spark-TTS-0.5B"
prompt_text = "This is Morgan Freeman. I'm here to narrate something special for you."
prompt_speech_path = "example\\prompt.wav"
save_dir = "audio_output"
device = "0"

# 确保输出目录存在
os.makedirs(save_dir, exist_ok=True)

# 读取长文本
print("📜 请输入或粘贴你的旁白内容（建议英文），输入完成后按 Enter，再输入 DONE 并回车：")
lines = []
while True:
    line = input()
    if line.strip().upper() == "DONE":
        break
    lines.append(line)
text = " ".join(lines)

# 分段策略：按句号或每段不超过 350 字拆分
print("\n🧠 正在拆分文本...")
chunks = textwrap.wrap(text, width=350, break_long_words=False, break_on_hyphens=False)
print(f"✂️ 共拆分为 {len(chunks)} 段。")

generated_segments = []

for idx, chunk in enumerate(chunks):
    print(f"\n🎙 正在合成第 {idx+1} 段语音...")
    output_name = f"segment_{idx+1}.wav"
    output_path = os.path.join(save_dir, output_name)

    cmd = [
        "python", "-m", "cli.inference",
        "--text", chunk,
        "--device", device,
        "--save_dir", save_dir,
        "--model_dir", model_dir,
        "--prompt_text", prompt_text,
        "--prompt_speech_path", prompt_speech_path
    ]

    subprocess.run(cmd)
        # 获取最新生成的 wav 文件
    latest_file = max(
        [f for f in os.listdir(save_dir) if f.endswith(".wav")],
        key=lambda x: os.path.getctime(os.path.join(save_dir, x))
    )
    latest_path = os.path.join(save_dir, latest_file)

    # 重命名为统一格式
    output_path = os.path.join(save_dir, f"segment_{idx+1}.wav")
    os.rename(latest_path, output_path)
    generated_segments.append(output_path)

# 音频拼接
print("\n🔊 正在拼接所有音频段...")
final_audio = AudioSegment.empty()
for seg_path in generated_segments:
    seg = AudioSegment.from_wav(seg_path)
    final_audio += seg + AudioSegment.silent(duration=500)  # 每段中间加0.5秒静音

final_output_path = os.path.join(save_dir, "final_shawshank_voiceover.wav")
final_audio.export(final_output_path, format="wav")

print(f"\n✅ 旁白合成完成！已保存为：{final_output_path}")
for path in generated_segments:
    os.remove(path)
print("🧹 已清理中间语音片段。")