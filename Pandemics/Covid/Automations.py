def kagg():
    import kaggle
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files('sudalairajkumar/covid19-in-india', path=r'downloaded data\covid19', unzip=True)


def who_country():
    import requests
    import os

    path = r'downloaded data\covid19\WHO-COVID-19-global-data.csv'

    if os.path.exists(path=path):
        os.remove(path)
        print("removed")

    who_url = 'https://covid19.who.int/WHO-COVID-19-global-data.csv'

    req = requests.get(who_url, stream=True)

    with open(path, 'w', encoding='utf-8') as file:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                file.write(str(chunk, 'utf-8'))

    print('downloaded')


