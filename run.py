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
        title = yt.title.strip()
        author = yt.author
        views = yt.views

        print(Fore.YELLOW + f"\n📝 Caption : {title[:100]}{'...' if len(title) > 100 else ''}")
        print(Fore.YELLOW + f"👤 Author  : {author}")
        print(Fore.YELLOW + f"❤️ Likes   : Tidak tersedia")  # Pytube tidak support likes
        print(Fore.YELLOW + f"👁️ Views   : {views:,}")

        print(Fore.CYAN + "\n[1] Video\n[2] Audio (MP3)")
        opt = input("Pilih opsi: ")

        if opt == "1":
            yt.streams.get_highest_resolution().download(output_path=SAVE_PATH)
            print(Fore.GREEN + "✅ YouTube berhasil diunduh.")
        elif opt == "2":
            stream = yt.streams.filter(only_audio=True).first()
            out = stream.download(output_path=SAVE_PATH)
            os.rename(out, out.replace(".mp4", ".mp3"))
            print(Fore.GREEN + "✅ YouTube audio berhasil diunduh.")
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
        loader = instaloader.Instaloader(dirname_pattern=SAVE_PATH, download_comments=False, save_metadata=False)
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        caption = post.caption or "Tidak ada caption"
        author = post.owner_username
        likes = post.likes
        views = post.video_view_count or "Tidak tersedia"

        print(Fore.YELLOW + f"\n📝 Caption : {caption[:100]}{'...' if len(caption) > 100 else ''}")
        print(Fore.YELLOW + f"👤 Author  : {author}")
        print(Fore.YELLOW + f"❤️ Likes   : {likes}")
        print(Fore.YELLOW + f"👁️ Views   : {views}")

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

        if 'token' not in lookup:
            raise Exception("❌ Gagal ambil data dari TikTok.")

        caption = lookup.get("text", "Tidak ada caption").strip()
        author = lookup.get("author_name", "Tidak diketahui")
        likes = lookup.get("likes", 0)
        views = lookup.get("plays", 0)

        print(Fore.YELLOW + f"\n📝 Caption : {caption[:100]}{'...' if len(caption) > 100 else ''}")
        print(Fore.YELLOW + f"👤 Author  : {author}")
        print(Fore.YELLOW + f"❤️ Likes   : {likes}")
        print(Fore.YELLOW + f"👁️ Views   : {views}")

        video_url = f"https://tikmate.app/download/{lookup['token']}/{lookup['id']}.mp4"
        r = requests.get(video_url)
        file_path = os.path.join(SAVE_PATH, "tiktok_video.mp4")
        with open(file_path, "wb") as f:
            f.write(r.content)

        print(Fore.GREEN + "✅ TikTok berhasil diunduh.")
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
