import json, re, sys
import openpyxl

SPREADSHEET_PATH = sys.argv[1] if len(sys.argv) > 1 else "artworks.xlsx"
OUTPUT_PATH = sys.argv[2] if len(sys.argv) > 2 else "artworks.json"
ASSETS_BASE = "assets/artworks"  # change this if your folder structure changes

# Spreadsheet field (row label) -> JSON key
FIELD_MAP = {
    "Name": "name",
    "Google Drive Folder Link": "driveFolder",
    "Type": "type",
    "Date": "date",
    "Description": "description",
    "Location": "location",
    "Publisher": "publisher",
    "External URL": "externalUrl",
    "Thumbnail Image": "thumbnail",
    "Video Link": "videoLink",
    "Sound Link": "soundLink",
    "Document Link": "documentLink",
    "Tags": "tags",
    "Archive": "archive",
    "Notes": "notes",
}

# Fields treated as comma-separated lists -> JSON arrays
LIST_FIELDS = {"type", "tags"}

# Fields that are filenames needing to become full relative paths
FILE_FIELDS = {"thumbnail", "documentLink"}


def slugify(name):
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def clean(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value if value else None
    return value


def main():
    wb = openpyxl.load_workbook(SPREADSHEET_PATH, data_only=True)
    ws = wb["Artworks"]

    rows = list(ws.iter_rows(values_only=True))
    header = rows[0]
    num_artwork_cols = len(header) - 1  # minus the FIELD column

    artworks = []
    for col_idx in range(1, num_artwork_cols + 1):
        artwork = {}
        for row in rows[1:]:
            field_label = row[0]
            if field_label is None:
                continue
            json_key = FIELD_MAP.get(field_label.strip())
            if json_key is None:
                continue
            value = clean(row[col_idx])

            if value is not None and hasattr(value, "strftime"):
                value = value.strftime("%Y-%m-%d")

            if value is not None and json_key in LIST_FIELDS:
                value = [v.strip() for v in value.split(",") if v.strip()]

            if value is not None and json_key in FILE_FIELDS:
                artwork_name = clean(row[1]) if json_key != "name" else value
                # use this column's Name (filled in below) for the path

            artwork[json_key] = value

        if not artwork.get("name"):
            continue  # skip empty artwork columns

        # now resolve file paths using this artwork's own name
        for field in FILE_FIELDS:
            if artwork.get(field):
                artwork[field] = f"{ASSETS_BASE}/{artwork['name']}/{artwork[field]}"

        artwork["id"] = slugify(artwork["name"])
        artworks.append(artwork)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(artworks, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(artworks)} artworks to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()