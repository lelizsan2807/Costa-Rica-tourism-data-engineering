from pathlib import Path
import logging



# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "turismo.xlsx"

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
LOG_DIR = PROJECT_ROOT / "logs"

DATABASE_FILE = OUTPUT_DIR / "tourism.db"

SHEET_NAME = "C2 Total"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Logging configuration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# Table definitions
# ============================================================

# Define the table schema for the SQLite database
#
# Each table is defined by:
# - name
# - rows containing categories
# - dimension assigned to each row
# Row numbers are based on the Excel worsheet loaded with 
# heade=None, meaning Excel row numbers are 0-indexed in the DataFrame.

TABLE_DEFINITIONS = {

    "fact_demographics": {
        "rows": {
            7: ("overall", "Total"),

            10: ("sex", "Hombre"),
            11: ("sex", "Mujer"),

            14: ("zone", "Urbana"),
            15: ("zone", "Rural"),

            18: ("age_group", "15 a 24 años"),
            19: ("age_group", "25 a 34 años"),
            20: ("age_group", "35 a 44 años"),
            21: ("age_group", "45 a 59 años"),
            22: ("age_group", "60 y más"),
            23: ("age_group", "No especificado"),
        }
    },
      "fact_employment_structure": {
        "rows": {
            35: ("overall", "Total"),

            38: ("employment_position", "Dependiente"),
            39: ("employment_position", "Independiente"),

            42: ("occupation_qualification", "Ocupación calificada alta"),
            43: ("occupation_qualification", "Ocupación calificada media"),
            44: ("occupation_qualification", "Ocupación no calificada"),
            45: ("occupation_qualification", "No especificado"),

            48: ("establishment_size", "De 1 a 3 personas"),
            49: ("establishment_size", "De 4 a 9 personas"),
            50: ("establishment_size", "De 10 a 29 personas"),
            51: ("establishment_size", "De 30 o más personas"),
            52: ("establishment_size", "No especificado"),
        }
    },

    "fact_work_conditions": {
        "rows": {
            64: ("overall", "Total"),

            67: ("hours_worked", "Menos de 15"),
            68: ("hours_worked", "De 15 a 39"),
            69: ("hours_worked", "De 40 a 48"),
            70: ("hours_worked", "Más de 48 horas"),
            71: ("hours_worked", "No especificado"),

            74: ("subemployment", "En condición de subempleo"),
            75: ("subemployment", "No en condición de subempleo"),

            78: ("employment_formality", "Ocupados con empleo formal"),
            79: ("employment_formality", "Ocupados con empleo informal"),

            82: ("work_insurance", "No tiene seguro por trabajo"),
            83: ("work_insurance", "Tiene seguro por trabajo"),
        }
    },

    "fact_income": {
        "rows": {
            95: ("overall", "Total"),

            98: ("income_level", "Menos de un salario mínimo"),
            99: ("income_level", "De uno a menos de dos salarios mínimos"),
            100: ("income_level", "Dos salarios mínimos o más"),
            101: ("income_level", "No recibe ingresos o no especificado"),

            103: ("average_income", "Ingreso mensual promedio"),
        }
    }
}

