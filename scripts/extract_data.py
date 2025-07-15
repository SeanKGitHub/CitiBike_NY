import zipfile
from pathlib import Path

source_dir = Path(r"C:\Data\Citibike_NY_2022\2022-citibike-tripdata")
target_dir = Path(r"C:\Data\Citibike_NY_2022\2022-citibike-tripdata\extracted_data")
target_dir.mkdir(exist_ok=True)

for zip_file in source_dir.glob("*.zip"):
    with zipfile.ZipFile(zip_file) as zip_ref:
        zip_stem = zip_file.stem
        for member in zip_ref.namelist():
            if member.endswith('.csv'):
                member_name = Path(member).name
                if member_name.startswith(zip_stem):
                    member_name = member_name[len(zip_stem):].lstrip('_-')
                output_filename = f"{zip_stem}_{member_name}"
                with zip_ref.open(member) as src, open(target_dir / output_filename, "wb") as dst:
                    dst.write(src.read())

print(f"All CSV files extracted to {target_dir}")