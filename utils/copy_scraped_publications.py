import difflib
from bs4 import BeautifulSoup

def read_and_format_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')
    return soup.prettify()

def copy_html_contents(source_file, destination_file, similarity_threshold=0.9):
    try:
        # Read the content from the source HTML file
        with open(source_file, 'r', encoding='utf-8') as source:
            source_content = source.read()

        # Read the content from the destination HTML file
        with open(destination_file, 'r', encoding='utf-8') as destination:
            destination_lines = destination.readlines()

        # Find the line numbers where the <main> tag starts and ends
        main_start_line = None
        main_end_line = None
        for i, line in enumerate(destination_lines):
            if '<main>' in line:
                main_start_line = i
            if '</main>' in line:
                main_end_line = i

        if main_start_line is not None and main_end_line is not None:
            # Extract the content between <main> tags from the destination HTML file
            target_content = "".join(destination_lines[main_start_line +1 : main_end_line])

            target_content = BeautifulSoup(target_content, 'html.parser').prettify()
            source_content = BeautifulSoup(source_content, 'html.parser').prettify()

            # Calculate the similarity between the source and target content
            d = difflib.SequenceMatcher(None, source_content, target_content)
            similarity_ratio = d.ratio()

            # Create a visual diff of the source and target content
            d = difflib.HtmlDiff()
            diff_html = d.make_file(source_content.splitlines(), target_content.splitlines())

            # Save the visual diff to an HTML file
            with open("utils/publications_diff.html", 'w', encoding='utf-8') as diff_file:
                diff_file.write(diff_html)

            if similarity_ratio >= similarity_threshold:
                # Remove the old content between <main> tags
                destination_lines = (
                    destination_lines[:main_start_line + 1]
                    + ['\n']
                    + source_content.split('\n')
                    + ['\n']
                    + destination_lines[main_end_line:]
                )

                # Write the modified content back to the destination HTML file
                with open(destination_file, 'w', encoding='utf-8') as destination:
                    destination.writelines(destination_lines)

                print(f"Contents copied successfully, similarity is {similarity_ratio}. Visual diff saved to content_diff.html.")
            else:
                raise Exception(f"Content similarity is {similarity_ratio}. No copy operation performed. Visual diff saved to utils/content_diff.html.")
        else:
            raise Exception("Destination file does not contain <main> and/or </main> tags.")

    except Exception as e:
        raise Exception("An error occurred:", str(e))

if __name__ == "__main__":
    source_file = "utils/scraped_publications.html"  # Replace with your source HTML file's path
    destination_file = "publications.html"  # Replace with your destination HTML file's path

    copy_html_contents(source_file, destination_file)
