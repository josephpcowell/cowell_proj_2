def directors_list(directors):
    if "," in directors:
        return [name.strip() for name in directors.split(",")]
    else:
        return [directors]


def remove_paren(directors):
    dir_list = []
    for director in directors:
        if "(" in director:
            dir_clean = director.split("(")[0].strip()
            dir_list.append(dir_clean)
        else:
            dir_list.append(director)
    return dir_list


def dir_rating_column(dir_list):
    for director in dir_list:
        rating = ""
        if mean_dir_rating.loc[director]["rating bins"] > rating:
            rating = mean_dir_rating.loc[director]["rating bins"]
        return rating
