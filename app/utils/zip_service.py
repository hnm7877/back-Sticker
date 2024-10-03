import zipfile

def zip_files(files, zip_name):
    with zipfile.ZipFile(zip_name, "w") as zipf:
        for file in files:
            zipf.write(file)
    return zip_name
