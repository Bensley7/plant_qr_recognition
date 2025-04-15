from flask import Flask, render_template, request
import os
import pandas as pd
import ast
from pathlib import Path


app = Flask(__name__, static_folder="static", template_folder="templates")

plant_db = pd.read_csv("data/fiche_technique_v6.csv")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/fiche/<code>")
def fiche(code):
    plant = plant_db[plant_db["Nom scientifique"] == code].iloc[0].to_dict()
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
