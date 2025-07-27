import os
import requests
from pytube import YouTube
from colorama import Fore, init
import instaloader

init(autoreset=True)
SAVE_PATH = "/storage/emulated/0/Download/termux"

def ensure_dir():
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.CYAN + """
╔════════════════════════════════╗
║   📥 SOCIAL MEDIA DOWNLOADER   ║
╠════════════════════════════════╣
║ 1. YouTube Video/Audio         ║
║ 2. Instagram Reel/Video        ║
║ 3. TikTok Video (No Watermark) ║
╚════════════════════════════════╝
""")

# YOUTUBE
def download_youtube():
    try:
        url = input("🔗 URL YouTube: ")
        if "youtube.com" not in url:
            print(Fore.RED + "❌ Masukkan URL lengkap, bukan versi pendek.")
            return
        yt = YouTube(url)
        print(Fore.YELLOW + f"\n🎬 Judul   : {yt.title}")
        print(Fore.YELLOW + f"📺 Channel : {yt.author}")
        print(Fore.YELLOW + f"👁️ Views   : {yt.views:,}")
        print(Fore.YELLOW + f"📅 Upload  : {yt.publish_date}")
        print(Fore.YELLOW + f"⏱️ Durasi  : {yt.length} detik")

        print(Fore.CYAN + "\n[1] Video\n[2] Audio (MP3)")
        opt = input("Pilih opsi: ")

        if opt == "1":
            yt.streams.get_highest_resolution().download(output_path=SAVE_PATH)
            print(Fore.GREEN + "✅ Video diunduh.")
        elif opt == "2":
            stream = yt.streams.filter(only_audio=True).first()
            out = stream.download(output_path=SAVE_PATH)
            os.rename(out, out.replace(".mp4", ".mp3"))
            print(Fore.GREEN + "✅ Audio diunduh.")
        else:
            print(Fore.RED + "❌ Opsi tidak dikenal.")
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")

# INSTAGRAM
def download_instagram():
    try:
        url = input("🔗 URL Instagram: ")
        if not url.startswith("http"):
            print(Fore.RED + "❌ URL tidak valid.")
            return
        shortcode = url.split("/")[-2]
        loader = instaloader.Instaloader(dirname_pattern=SAVE_PATH)
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        print(Fore.YELLOW + f"\n🎬 Caption  : {post.caption[:100]}...")
        print(Fore.YELLOW + f"❤️ Likes    : {post.likes}")
        print(Fore.YELLOW + f"👁️ Views    : {post.video_view_count or 'N/A'}")
        loader.download_post(post, target="instagram_post")
        print(Fore.GREEN + "✅ Instagram berhasil diunduh.")
    except Exception as e:
        print(Fore.RED + f"❌ Gagal: {e}")

# TIKTOK
def download_tiktok():
    try:
        url = input("🔗 URL TikTok: ")
        if not url.startswith("http"):
            print(Fore.RED + "❌ URL tidak valid.")
            return
        lookup = requests.post("https://api.tikmate.app/api/lookup", data={"url": url}).json()
        if not lookup.get("token"):
            raise Exception("Token gagal diambil")
        video_url = f"https://tikmate.app/download/{lookup['token']}/{lookup['id']}.mp4"
        print(Fore.YELLOW + f"\n🎬 Judul   : {lookup['text']}")
        print(Fore.YELLOW + f"👁️ Views   : {lookup['plays']}")
        print(Fore.YELLOW + f"❤️ Likes   : {lookup['likes']}")
        r = requests.get(video_url)
        file_path = os.path.join(SAVE_PATH, "tiktok_video.mp4")
        with open(file_path, "wb") as f:
            f.write(r.content)
        print(Fore.GREEN + "✅ Video TikTok berhasil diunduh.")
    except Exception as e:
        print(Fore.RED + f"❌ Gagal: {e}")

# MAIN
def main():
    ensure_dir()
    while True:
        clear()
        banner()
        pilihan = input("Pilih (1/2/3) atau 'exit': ")

        if pilihan == "1":
            download_youtube()
        elif pilihan == "2":
            download_instagram()
        elif pilihan == "3":
            download_tiktok()
        elif pilihan.lower() == "exit":
            break
        else:
            print(Fore.RED + "❌ Pilihan tidak tersedia.")

        input("\nTekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()
