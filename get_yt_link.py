from youtube_search import YoutubeSearch


def search(param=""):
    if param != "":
        results = YoutubeSearch(param, max_results=1).to_dict()
        videoinfo = []
        result = results[0]
        for k, v in result.items():
            if k == "id":
                videoinfo.append("https://www.youtube.com/watch?v=" + str(v))
            if k == "duration":
                videoinfo.append(v)
        return (videoinfo)
    else:
        return "Erro! Não foi possível encontrar o vídeo!"


if __name__ == "__main__":
    print(search("K-on"))
