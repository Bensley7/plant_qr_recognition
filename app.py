from flask import Flask, render_template, request
import os
import pandas as pd
import ast
from pathlib import Path


app = Flask(__name__, static_folder="static", template_folder="templates")

plant_db = pd.read_csv("data/fiche_technique_v10.csv")

def postprocess(code):
    if "_andalous" in code:
        return code.split("_andalous")[0], "Andalous"
    elif "_ens" in code:
        return code.split("_ens")[0], "ENS"
    elif "_amerique" in code:
        return code.split("_ens")[0], "Amerique Latine"
    else:
        return None, None

def get_institution(name):
    if "ENS" in name:
        return "ENS"
    elif "Amerique Latine" in name:
        return "Amerique Latine"
    elif "Andalous" in name:
        return "Andalous"
    else:
        return None

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/fiche/<code>")
def fiche(code):
    code, institution = postprocess(code)
    espece_db = plant_db[plant_db["Nom scientifique"] == code].copy()
    espece_db["Institution"] = espece_db.apply(lambda x: get_institution(x), axis = 1)
    plant = espece_db[espece_db["Institution"] == institution].iloc[0].to_dict()
    species_root_disk = Path(os.path.join('static', 'images', 'plantes', plant['Unnamed: 0']))
    species_root_relative_path = species_root_disk.relative_to("static")
    species_image_files = [
        str(species_root_relative_path / f)
        for f in os.listdir(species_root_disk)
        if os.path.isfile(species_root_disk / f)
    ]
    plant["image"] = species_image_files
    map_img_path = os.path.join( 'images', 'maps', plant['Unnamed: 0']+ ".png" )
    plant["map"] = map_img_path
    if "intérêts" in plant and isinstance(plant["intérêts"], str):
        try:
            plant["intérêts"] = ast.literal_eval(plant["intérêts"])
        except:
            pass
    return render_template("fiche.html", plant=plant, code=code)

if __name__ == "__main__":
    app.run(debug=False)
