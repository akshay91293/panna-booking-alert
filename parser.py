from bs4 import BeautifulSoup


def get_to_dt(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    field = soup.find(id="To_dt")

    if field is None:
        raise Exception("Could not locate To_dt.")

    return field["value"]
