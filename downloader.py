import os
import yt_dlp
import sys

# Archivo donde se registrarán las descargas para evitar duplicados
ARCHIVO_DESCARGAS = "descargas.txt"

def cargar_descargas():
    """Carga la lista de descargas previas desde el archivo."""
    if os.path.exists(ARCHIVO_DESCARGAS):
        with open(ARCHIVO_DESCARGAS, "r", encoding="utf-8") as file:
            return set(file.read().splitlines())
    return set()

def guardar_descarga(titulo):
    """Guarda el título de una canción descargada en el registro."""
    with open(ARCHIVO_DESCARGAS, "a", encoding="utf-8") as file:
        file.write(titulo + "\n")

def download_audio(url, output_folder="downloads"):
    """Descarga un video o una playlist de YouTube en formato MP3 sin repetir canciones."""
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    descargas_previas = cargar_descargas()  # Cargar descargas anteriores

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'yes_playlist': True,  # Si es una playlist, la descarga completa
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',  # Fuerza la calidad a 320kbps si es posible
        }],
        'progress_hooks': [lambda d: print(f"Descargando: {d['filename']}") if d['status'] == 'downloading' else None],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)  # Obtener la info antes de descargar

        if "entries" in info:  # Si es una playlist
            videos = info["entries"]
        else:  # Si es un solo video
            videos = [info]

        for video in videos:
            if video:
                titulo = video["title"]
                if titulo in descargas_previas:
                    print(f"⏭️ {titulo} ya fue descargado chinchulín. Pasando a la siguiente...")
                else:
                    ydl.download([video["webpage_url"]])
                    guardar_descarga(titulo)  # Guardar en el registro

if __name__ == "__main__":
    # Verifica si se pasó una URL como argumento al ejecutar el script
    if len(sys.argv) < 2:
        print("Por favor, proporciona una URL.")
        sys.exit(1)  # Termina el script si no se proporciona la URL

    url = sys.argv[1]  # Toma la URL proporcionada como primer argumento
    print(f"Descargando desde {url}...")
    download_audio(url)
