import gradio as gr

def parse_input(text):
    if not text.strip():
        raise ValueError("Input cannot be empty.")

    songs = []
    lines = text.strip().split("\n")

    for line in lines:
        parts = line.split(",")

        if len(parts) != 4:
            raise ValueError("Each line must have 4 values: title, artist, genre, duration.")

        title = parts[0].strip()
        artist = parts[1].strip()
        genre = parts[2].strip()
        duration_str = parts[3].strip()

        if not title or not artist or not genre or not duration_str:
            raise ValueError("All fields must be filled (title, artist, genre, duration).")

        try:
            duration = int(duration_str)
        except ValueError:
            raise ValueError("Duration must be a number.")

        song = {
            "title": title,
            "artist": artist,
            "genre": genre,
            "duration": duration
        }

        songs.append(song)

    return songs


def merge(leftSorted, rightSorted, key, steps):
    merged = []
    i = 0
    j = 0

    while i < len(leftSorted) and j < len(rightSorted):

        if isinstance(leftSorted[i][key], str):
            leftValue = leftSorted[i][key].lower()
            rightValue = rightSorted[j][key].lower()
        else:
            leftValue = leftSorted[i][key]
            rightValue = rightSorted[j][key]

        steps.append(
            f"Compare {leftSorted[i]['title']} ({leftSorted[i][key]}) with {rightSorted[j]['title']} ({rightSorted[j][key]})"
        )

        if leftValue <= rightValue:
            merged.append(leftSorted[i])
            steps.append(f"Take {leftSorted[i]['title']}")
            i += 1
        else:
            merged.append(rightSorted[j])
            steps.append(f"Take {rightSorted[j]['title']}")
            j += 1

    while i < len(leftSorted):
        merged.append(leftSorted[i])
        steps.append(f"Add remaining from left: {leftSorted[i]['title']}")
        i += 1

    while j < len(rightSorted):
        merged.append(rightSorted[j])
        steps.append(f"Add remaining from right: {rightSorted[j]['title']}")
        j += 1

    steps.append(f"Merged result: {[song['title'] for song in merged]}")
    return merged


def merge_sort(songs, key, steps):
    if len(songs) <= 1:
        return songs

    mid = len(songs) // 2
    leftHalf = songs[:mid]
    rightHalf = songs[mid:]

    steps.append(
        f"Split into left: {[song['title'] for song in leftHalf]} and right: {[song['title'] for song in rightHalf]}"
    )

    leftSorted = merge_sort(leftHalf, key, steps)
    rightSorted = merge_sort(rightHalf, key, steps)

    return merge(leftSorted, rightSorted, key, steps)


def format_steps(steps):
    return "\n".join([f"Step {i+1}: {step}" for i, step in enumerate(steps)])


def run_sort(input_text, sort_key):
    try:
        songs = parse_input(input_text)
        steps = []

        sorted_songs = merge_sort(songs, sort_key, steps)

        steps_output = format_steps(steps)

        results_output = "\n".join(
            [f"{song['title']} - {song['artist']} ({song[sort_key]})" for song in sorted_songs]
        )

        return steps_output, results_output

    except Exception as e:
        return f"Error: {str(e)}", ""


# Example input
example_text = """Blinding Lights, The Weeknd, Pop, 200
Cardigan, Taylor Swift, Indie, 240
Levitating, Dua Lipa, Pop, 203
SICKO MODE, Travis Scott, Rap, 312
Bohemian Rhapsody, Queen, Rock, 354"""


with gr.Blocks() as demo:
    gr.Markdown("# Merge Sort Playlist Organizer")

    gr.Markdown(
        "Enter one song per line in this format:\n"
        "title, artist, genre, duration\n\n"
        "Then choose how to sort and click the button."
    )

    input_box = gr.Textbox(
        label="Playlist Input",
        lines=10,
        value=example_text
    )

    sort_dropdown = gr.Dropdown(
        choices=["genre", "duration"],
        value="genre",
        label="Sort By"
    )

    run_button = gr.Button("Run Merge Sort")

    steps_box = gr.Textbox(label="Step-by-Step Simulation", lines=15)
    results_box = gr.Textbox(label="Final Sorted Playlist", lines=10)

    run_button.click(
        fn=run_sort,
        inputs=[input_box, sort_dropdown],
        outputs=[steps_box, results_box]
    )


demo.launch()