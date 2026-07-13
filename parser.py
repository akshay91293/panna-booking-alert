from bs4 import BeautifulSoup

from models import Snapshot


def parse(html: str) -> Snapshot:

    soup = BeautifulSoup(html, "lxml")

    snapshot = Snapshot()

    to_dt = soup.find(id="To_dt")
    snapshot.to_dt = to_dt["value"] if to_dt else None

    park = soup.find("div", id="ParkHeading")
    snapshot.park_name = park.get_text(strip=True) if park else None

    rule_img = soup.find("img", src=lambda s: s and "ForestNewRule" in s)
    snapshot.rule_image = rule_img["src"] if rule_img else None

    single = soup.find(id="SingleSeatlink")
    snapshot.single_seat_banner = (
        single.get_text(" ", strip=True)
        if single else None
    )

    tatkal = soup.find(id="TatkalLink")
    snapshot.tatkal_banner = (
        tatkal.get_text(" ", strip=True)
        if tatkal else None
    )

    notes = soup.select_one(".BlockContent")

    snapshot.important_notes = (
        notes.get_text("\n", strip=True)
        if notes else None
    )

    return snapshot
