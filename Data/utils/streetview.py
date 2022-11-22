import json
import requests as r


def get_streetview(coords, url, key):
    size = "600x600"
    loc = f"{coords[0]},{coords[1]}"
    d = 1000

    sv0_url = f"{url}?size={size}&location={loc}&radius={d}&fov=120&heading=0&source=outdoor&key={key}"
    sv120_url = f"{url}?size={size}&location={loc}&radius={d}&fov=120&heading=120&source=outdoor&key={key}"
    sv240_url = f"{url}?size={size}&location={loc}&radius={d}&fov=120&heading=240&source=outdoor&key={key}"
    metadata_url = f"{url}/metadata?size={size}&location={loc}&radius={d}&key={key}"

    sv0 = r.get(sv0_url, stream=all)
    sv120 = r.get(sv120_url, stream=all)
    sv240 = r.get(sv240_url, stream=all)
    info = r.get(metadata_url)

    return json.loads(info.text), sv0, sv120, sv240
