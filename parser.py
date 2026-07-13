from bs4 import BeautifulSoup


def parse(html: str):

    soup = BeautifulSoup(html, "lxml")

    data = {}

    # Backend season end date
    to_dt = soup.find(id="To_dt")
    data["to_dt"] = to_dt["value"] if to_dt else None

    # Park name
    park = soup.find("div", id="ParkHeading")
    data["park_name"] = park.get_text(strip=True) if park else None

    # Rule image
    rule_img = soup.find("img", src=lambda s: s and "ForestNewRule" in s)
    data["rule_image"] = rule_img["src"] if rule_img else None

    # Single seat banner
    single = soup.find(id="SingleSeatlink")
    data["single_seat_banner"] = (
        single.get_text(" ", strip=True)
        if single else None
    )

    # Tatkal banner
    tatkal = soup.find(id="TatkalLink")
    data["tatkal_banner"] = (
        tatkal.get_text(" ", strip=True)
        if tatkal else None
    )

    # Entire Important Notes block
    notes = soup.select_one(".BlockContent")

    if notes:
        data["important_notes"] = notes.get_text(
            "\n",
            strip=True
        )
    else:
        data["important_notes"] = None

    return data
