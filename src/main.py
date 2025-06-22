import os
import shutil

def copy_recursive(source_dir, dest_dir):
    items = os.listdir(source_dir)
    for item in items:
        source_path = os.path.join(source_dir, item)
        destination_path = os.path.join(dest_dir, item)
        print(f"Found: {source_path}")

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copying: {source_path} -> {destination_path}")
        else:
            os.mkdir(destination_path)
            print(f"Created directory: {destination_path}")
            copy_recursive(source_path, destination_path)


def copy_static_to_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")

    copy_recursive("static", "public")

    
        


def main():
    copy_static_to_public()

if __name__ == "__main__":
    main()