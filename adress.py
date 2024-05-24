from dadata import Dadata


def city_guess(city_name):
    token = "05f0207076526748631c35236a8871faee450c64"
    dadata = Dadata(token)
    result = dadata.suggest("address", city_name)
    if result:
        result = result[0]
        if all([result['data']['country'], result['data']['region_with_type'],
                result['data']['city_type_full'], result['data']['city']]):
            return [result['data']['country'], result['data']['region_with_type'],
                    result['data']['city'], result['data']['street_with_type'],
                    result['data']['house']]
    return False


def city_cords(city_name):
    token = "05f0207076526748631c35236a8871faee450c64"
    dadata = Dadata(token)
    result = dadata.suggest("address", city_name)
    if result:
        return [result[0]['data']['geo_lat'], result[0]['data']['geo_lon']]