def get_info_per_year(year, info):
    if info == "n_municipalities":
        if year == 2022:
            return 7904
        elif year == 2023:
            return 7899
        else:
            raise ValueError("Not availble year")
    elif info == "population":
        if year == 2022:
            return 59019317
        elif year == 2023:
            return 58840177
        else:
            raise ValueError("Not availble year")
