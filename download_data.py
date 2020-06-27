from urllib.request import urlretrieve


def download_data():
    url_OxCGRT = "https://docs.google.com/uc?export=download&id=1ZkY0PWLCQO_Zdunrrv9L9Tk-pIJvGZo_"
    url_pop = "https://docs.google.com/uc?export=download&id=13B8HqnY063THHbKfN7_Cq3kVgQhp15cT"
    _ = urlretrieve(url_OxCGRT, "OxCGRT_latest.csv")
    _ = urlretrieve(url_pop, "worldPop2020.csv")

