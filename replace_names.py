import os

target_dir = r"c:\Users\cavit\Desktop\Python ile Yapay Zeka 102"
extensions = {".py", ".md", ".txt", ".json"}

replacements = [
    ("Hamit Mızrak", "Cavit Batu Soylu"),
    ("hamitmizrak", "Cavitbatusoylu"),
    ("Hamit", "Cavit"),
    ("hamit.mizrak", "Cavitbatusoylu"),
    ("hamit", "cavit")
]

for root, dirs, files in os.walk(target_dir):
    if ".git" in root or ".venv" in root or ".idea" in root:
        continue
    for file in files:
        if any(file.endswith(ext) for ext in extensions):
            if file == "replace_names.py":
                continue
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                new_content = content
                for old, new in replacements:
                    new_content = new_content.replace(old, new)
                
                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated {path}")
            except Exception as e:
                print(f"Error processing {path}: {e}")
