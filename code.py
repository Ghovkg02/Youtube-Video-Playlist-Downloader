from pytube import YouTube, Playlist

def get_video_details(yt):
    print("\nDetails for Video\n")
    print("Title of video:   ", yt.title)
    print("Number of views:  ", yt.views)
    print("Length of video:  ", yt.length, "seconds")

def display_stream_options(streams):
    print("\nAll available options for downloads:\n")
    for i, stream in enumerate(streams, start=1):
        print(f"{i}) {stream.resolution} and {stream.mime_type} (itag: {stream.itag})")

def download_video(yt, tag):
    selected_stream = yt.streams.get_by_itag(tag)
    if selected_stream:
        try:
            print("\nDownloading...")
            selected_stream.download()
            print("\nDownload completed!!")
        except Exception as e:
            print(f"An error occurred during download: {e}")
    else:
        print(f"\nSelected stream with itag {tag} not found. Downloading the last available stream...")
        last_available_stream = yt.streams.filter(progressive=True).last()
        if last_available_stream:
            try:
                print("\nDownloading...")
                last_available_stream.download()
                print("\nDownload completed!!")
            except Exception as e:
                print(f"An error occurred during download: {e}")
        else:
            print("\nNo available streams found. Download failed.")


def download_playlist(playlist_url, chosen_tag):
    playlist = Playlist(playlist_url)
    print(f"\nDownloading videos from the playlist: {playlist.title}\n")

    for video_url in playlist.video_urls:
        yt = YouTube(video_url)
        get_video_details(yt)

        progressive_streams = yt.streams.filter(progressive=True).all()
        display_stream_options(progressive_streams)

        if chosen_tag:
            tag = chosen_tag
        else:
            tag = int(input("\nEnter the tag (itag) of your preferred stream to download: "))
            chosen_tag = tag  # Save the chosen tag for subsequent videos

        download_video(yt, tag)

def main():
    chosen_tag = None  # Initialize chosen_tag as None
    while True:
        url = input("Enter the YouTube video or playlist URL: ")
        if "playlist" in url.lower():
            download_playlist(url, chosen_tag)
        else:
            yt = YouTube(url)
            get_video_details(yt)

            progressive_streams = yt.streams.filter(progressive=True).all()
            display_stream_options(progressive_streams)

            tag = int(input("\nEnter the tag (itag) of your preferred stream to download: "))
            download_video(yt, tag)

        again = input("\nWanna download another video or playlist? (Y or N): ").upper()
        if again != "Y":
            break

if __name__ == "__main__":
    main()
