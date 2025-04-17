import subprocess

# 用户输入
text = input("请输入你要说的话（Morgan Freeman 风格）：\n> ")

# 替换智能引号
text = text.replace("’", "'").replace("“", "\"").replace("”", "\"")

# 手动加上引号包裹，防止字符丢失（双重保险）
if not text.startswith('"'):
    text = '"' + text
if not text.endswith('"'):
    text = text + '"'

# 参数
output_dir = "audio_output"
model_dir = "pretrained_models\\Spark-TTS-0.5B"
prompt_text = "This is Morgan Freeman. I'm here to narrate something special for you."
prompt_speech_path = "example\\prompt.wav"

# 命令参数列表
cmd = [
    "python", "-m", "cli.inference",
    "--text", text,
    "--device", "0",
    "--save_dir", output_dir,
    "--model_dir", model_dir,
    "--prompt_text", prompt_text,
    "--prompt_speech_path", prompt_speech_path
]

print("\n🎙 正在合成语音，请稍候...\n")
subprocess.run(cmd, shell=True)
