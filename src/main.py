import os
import shutil
from markdown_blocks import markdown_to_html_node
from htmlnode import LeafNode

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

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header here")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()  
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)

    output_content = template_content.replace("{{ Title }}", title)
    output_content = output_content.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(output_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    print(f"Contents of {dir_path_content}: {contents}")
    for content in contents:
        print(f"Processing item: {content}")
        item_path = os.path.join(dir_path_content, content) 

        if os.path.isfile(item_path) and content.endswith(".md"):
            new_html_filename = content[0:-3] + ".html"
            dest_path = os.path.join(dest_dir_path, new_html_filename) 

            with open(item_path, "r", encoding="utf-8") as markdown_file:
                markdown_content = markdown_file.read()

            with open(template_path, "r", encoding="utf-8") as template_file:
                template_content = template_file.read()

            html_node = markdown_to_html_node(markdown_content)
            html_content = html_node.to_html()

            page_title = "Default Title"
            lines = markdown_content.splitlines()
            for line in lines:
                if line.startswith("# "):
                    page_title = line[2:].strip()
                    break

            html_with_content = template_content.replace("{{ Content }}", html_content)
            final_html = html_with_content.replace("{{ Title }}", page_title)

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(final_html)

        elif os.path.isdir(item_path): 
            new_dest_dir_path = os.path.join(dest_dir_path, content)
            generate_pages_recursive(item_path, template_path, new_dest_dir_path)

        

def main():
    copy_static_to_public()
    generate_pages_recursive(
        "content",
        "template.html",
        "public",
    )

if __name__ == "__main__":
    main()