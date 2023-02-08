import livepopulartimes


def Populartime(name: str):
    data = livepopulartimes.get_populartimes_by_address(f"{name}", proxy=False)
    print(data)
    return data

Populartime("H-E-B, SouthwestFreeway, SugarLand, TX, USA")