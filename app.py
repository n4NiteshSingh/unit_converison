from flask import Flask, render_template, request, jsonify,redirect

app = Flask(__name__)

# Conversion constants
C = 299792458  # Speed of light in m/s
H = 4.135667696e-15  # Planck's constant in eV·s
EV_TO_NM = 1239.84198300923944  # Conversion factor for eV to nm


def convert_from_nm(value_nm, target_unit):
    """Convert a value in nanometers to the target unit."""
    try:
        if target_unit == "nm":
            return value_nm
        elif target_unit == "µm":
            return value_nm * 1e-3
        elif target_unit == "eV":
            return EV_TO_NM / value_nm
        elif target_unit == "meV":
            return (EV_TO_NM / value_nm) * 1e3
        elif target_unit == "THz":
            return C / (value_nm * 1e-9) / 1e12
        elif target_unit == "fs":
            return value_nm * 3.3356409519815204 * 1e-3
        elif target_unit == "ps":
            return value_nm * 3.3356409519815204 * 1e-6
        elif target_unit == "cm⁻¹":
            return 1e7 / value_nm
        else:
            return None
    except ZeroDivisionError:
        return 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/unit_conversion.html")
@app.route("/unit_conversion")
def uc():
    return render_template("unit_conversion.html")

@app.route("/about.html")
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/convert", methods=["POST"])
def convert():
    input_unit = request.json.get("input_unit")
    input_value = float(request.json.get("input_value"))

    # Convert the input value to nanometers (nm)
    if input_unit == "nm":
        value_in_nm = input_value
    elif input_unit == "µm":
        value_in_nm = input_value * 1e3
    elif input_unit == "eV":
        value_in_nm = EV_TO_NM / input_value
    elif input_unit == "meV":
        value_in_nm = EV_TO_NM / (input_value * 1e-3)
    elif input_unit == "THz":
        value_in_nm = C / (input_value * 1e12) * 1e9
    elif input_unit == "fs":
        value_in_nm = input_value * 3.3356409519815204
    elif input_unit == "ps":
        value_in_nm = input_value * 3.3356409519815204 * 1e3
    elif input_unit == "cm⁻¹":
        value_in_nm = 1e7 / input_value
    else:
        return jsonify({"error": "Invalid input unit"}), 400

    # Convert to all other units
    results = {}
    for unit in ["nm", "µm", "eV", "meV", "THz", "fs", "ps", "cm⁻¹"]:
        results[unit] = convert_from_nm(value_in_nm, unit)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)