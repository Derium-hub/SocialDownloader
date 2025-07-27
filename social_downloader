import os
import requests
from pytube import YouTube
from colorama import Fore, init

init(autoreset=True)

SAVE_PATH = "/storage/emulated/0/Download/termux"

def clear():
    os.system("clear")

def banner():
    print(Fore.CYAN + """
╔══════════════════════════════════════╗
║     📥 SOCIAL MEDIA DOWNLOADER      ║
╠══════════════════════════════════════╣
║  1. YouTube Video/Audio              ║
║  2. Instagram Video/Reel            ║
║  3. TikTok Video (No Watermark)     ║
╚══════════════════════════════════════╝
""")

# ---------- YOUTUBE ----------
def download_youtube():
    try:
        url = input(Fore.GREEN + "\nMasukkan URL YouTube: ")
        yt = YouTube(url)
        print(Fore.YELLOW + f"\n📌 Judul   : {yt.title}")
        print(Fore.YELLOW + f"📺 Channel : {yt.author}")
        print(Fore.YELLOW + f"👁️ Views   : {yt.views:,}")
        print(Fore.YELLOW + f"📅 Upload  : {yt.publish_date.strftime('%d-%m-%Y')}")
        print(Fore.YELLOW + f"⏱️ Durasi  : {yt.length} detik")

        print(Fore.CYAN + "\n[1] Download Video")
        print("[2] Download Audio (MP3)")
        choice = input(Fore.GREEN + "Pilih opsi (1/2): ")

        if choice == "1":
            yt.streams.get_highest_resolution().download(output_path=SAVE_PATH)
            print(Fore.GREEN + "✅ Video berhasil diunduh.")
        elif choice == "2":
            audio = yt.streams.filter(only_audio=True).first()
            out_file = audio.download(output_path=SAVE_PATH)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            print(Fore.GREEN + "✅ Audio berhasil diunduh.")
        else:
            print(Fore.RED + "❌ Opsi tidak valid.")
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")

# ---------- INSTAGRAM ----------
def download_instagram():
    try:
        url = input(Fore.GREEN + "\nMasukkan URL Instagram Reel/Video: ")
        headers = {'User-Agent': 'Mozilla/5.0'}
        api = f"https://saveig.app/api/ajaxSearch?query={url}"
        res = requests.post(api, headers=headers)
        data = res.json()
        video_url = data['medias'][0]['url']
        filename = os.path.join(SAVE_PATH, "instagram_video.mp4")
        vid = requests.get(video_url)
        with open(filename, "wb") as f:
            f.write(vid.content)
        print(Fore.GREEN + "✅ Video Instagram berhasil diunduh.")
    except Exception as e:
        print(Fore.RED + f"❌ Gagal: {e}")

# ---------- TIKTOK ----------
def download_tiktok():
    try:
        url = input(Fore.GREEN + "\nMasukkan URL TikTok: ")
        api_url = f"https://tikwm.com/api/?url={url}"
        res = requests.get(api_url).json()
        video_url = res['data']['play']
        filename = os.path.join(SAVE_PATH, "tiktok_video.mp4")
        video = requests.get(video_url)
        with open(filename, "wb") as f:
            f.write(video.content)
        print(Fore.GREEN + "✅ Video TikTok berhasil diunduh.")
    except Exception as e:
        print(Fore.RED + f"❌ Gagal: {e}")

# ---------- MAIN ----------
def main():
    while True:
        clear()
        banner()
        choice = input(Fore.GREEN + "\nPilih opsi (1-3) atau ketik 'exit' untuk keluar: ")

        if choice == "1":
            download_youtube()
        elif choice == "2":
            download_instagram()
        elif choice == "3":
            download_tiktok()
        elif choice.lower() == "exit":
            break
        else:
            print(Fore.RED + "❌ Pilihan tidak tersedia.")

        input(Fore.CYAN + "\nTekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()
