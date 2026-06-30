import json, re, sys, os
import openpyxl

SPREADSHEET_PATH = sys.argv[1] if len(sys.argv) > 1 else "artworks.xlsx"
OUTPUT_PATH = sys.argv[2] if len(sys.argv) > 2 else "artworks.json"
ASSETS_BASE = "assets/artworks"  # web-facing path used inside the JSON/HTML
ASSETS_DIR = os.path.join("..", "assets", "artworks")  # actual folder on disk, relative to where this script is run from
GENERIC_THUMBNAIL = "assets/images/windTrees.jpg"  # used when an artwork has no folder/images at all -- update path if windTrees.jpg lives elsewhere

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif")

# Spreadsheet field (row label) -> JSON key
FIELD_MAP = {
    "Name": "name",
    "Google Drive Folder Link": "driveFolder",
    "Type": "type",
    "Dimensions": "dimensions",
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


def slugify(name, max_length=42):
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    if len(s) > max_length:
        # truncate at the last word boundary within max_length so we don't
        # cut a word in half -- only kicks in if no Short Name was given
        truncated = s[:max_length]
        if "-" in truncated:
            truncated = truncated.rsplit("-", 1)[0]
        s = truncated
    return s


def find_first_image(folder_path):
    """Return the filename of the first image (alphabetically) in folder_path,
    or None if the folder doesn't exist or has no images."""
    if not os.path.isdir(folder_path):
        return None
    candidates = sorted(
        f for f in os.listdir(folder_path)
        if f.lower().endswith(IMAGE_EXTENSIONS)
    )
    return candidates[0] if candidates else None


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

    # Find the "Name" row so we can detect which columns actually contain
    # an artwork, regardless of whether the header label above them is
    # filled in correctly. Relying on the header alone is risky -- a blank
    # header cell (e.g. from an accidental column insert) would otherwise
    # cause a real artwork to be silently dropped.
    name_row = next(
        (row for row in rows[1:] if row[0] and row[0].strip() == "Name"),
        None,
    )
    if name_row is None:
        print("Could not find a 'Name' row in the spreadsheet.")
        return

    short_name_row = next(
        (row for row in rows[1:] if row[0] and row[0].strip() == "Short Name"),
        None,
    )

    # Columns D onward (index 3+) are artwork columns; A-C are FIELD/HINT/Example.
    artwork_col_indices = [
        i for i in range(3, len(header))
        if clean(name_row[i]) is not None
    ]

    artworks = []
    for col_idx in artwork_col_indices:
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

            artwork[json_key] = value

        if not artwork.get("name"):
            continue  # skip empty artwork columns

        # slug first, since file paths are built from it (not the raw,
        # possibly-special-character-laden name). Prefer the Short Name
        # if one was given, otherwise slugify the full name (which will
        # get truncated automatically if it's very long).
        short_name = clean(short_name_row[col_idx]) if short_name_row else None
        slug_source = short_name if short_name else artwork["name"]
        artwork["id"] = slugify(slug_source)

        for field in FILE_FIELDS:
            if artwork.get(field):
                artwork[field] = f"{ASSETS_BASE}/{artwork['id']}/{artwork[field]}"

        # Thumbnail fallback chain:
        # 1. Use the thumbnail filename given in the spreadsheet, if any.
        # 2. Otherwise, look in this artwork's actual asset folder on disk
        #    and use the first image found there (alphabetically).
        # 3. If there's no folder at all (e.g. a text-only piece), fall
        #    back to the generic placeholder image.
        if not artwork.get("thumbnail"):
            folder_path = os.path.join(ASSETS_DIR, artwork["id"])
            first_image = find_first_image(folder_path)
            if first_image:
                artwork["thumbnail"] = f"{ASSETS_BASE}/{artwork['id']}/{first_image}"
            else:
                artwork["thumbnail"] = GENERIC_THUMBNAIL

        artworks.append(artwork)

    # encoding="utf-8" is required here -- without it, Windows will use the
    # system locale encoding (often cp1252) and crash or mangle any non-ASCII
    # characters in titles/descriptions (e.g. "西遊記", curly quotes, em dashes)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(artworks, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(artworks)} artworks to {OUTPUT_PATH}")
    print("\nFolder names to use under assets/artworks/:\n")
    for artwork in artworks:
        print(artwork["id"])


if __name__ == "__main__":
    main()