import gradio as gr  # Import the Gradio library for building the web UI.
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from a .env file.
from research_manager import ResearchManager  # Import the ResearchManager class, which orchestrates the research process.

load_dotenv(override=True)  # Load environment variables from a .env file.
                            # 'override=True' ensures that variables in the .env file
                            # will overwrite existing system environment variables if there's a conflict.
# Define the custom Seafoam theme
class Seafoam(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.emerald,
        secondary_hue: colors.Color | str = colors.blue,
        neutral_hue: colors.Color | str = colors.blue,
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_md,
        text_size: sizes.Size | str = sizes.text_lg,
        font: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("Quicksand"),
            "ui-sans-serif",
            "sans-serif",
        ),
        font_mono: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("IBM Plex Mono"),
            "ui-monospace",
            "monospace",
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        super().set(
            body_background_fill="repeating-linear-gradient(45deg, *primary_200, *primary_200 10px, *primary_50 10px, *primary_50 20px)",
            body_background_fill_dark="repeating-linear-gradient(45deg, *primary_800, *primary_800 10px, *primary_900 10px, *primary_900 20px)",
            button_primary_background_fill="linear-gradient(90deg, *primary_300, *secondary_400)",
            button_primary_background_fill_hover="linear-gradient(90deg, *primary_200, *secondary_300)",
            button_primary_text_color="white",
            button_primary_background_fill_dark="linear-gradient(90deg, *primary_600, *secondary_800)",
            slider_color="*secondary_300",
            slider_color_dark="*secondary_600",
            block_title_text_weight="600",
            block_border_width="3px",
            block_shadow="*shadow_drop_lg",
            button_primary_shadow="*shadow_drop_lg",
            button_large_padding="32px",
        )

# Instantiate the Seafoam theme
seafoam = Seafoam()
async def run(query: str):
    """
    Asynchronously runs the research process using the ResearchManager.
    This is an asynchronous generator function that yields chunks of output
    as they become available from the ResearchManager's run method.
    """
    # Create an instance of ResearchManager and call its 'run' method with the user's query.
    # The 'async for' loop iterates over the chunks yielded by ResearchManager.run().
    async for chunk in ResearchManager().run(query):
        yield chunk  # Yield each chunk received from the research process to the Gradio output.

# Define the Gradio UI using gr.Blocks for a more customizable layout.
# The theme is set to 'Default' with a 'slate' primary hue.
with gr.Blocks(theme=gr.themes.Default(primary_hue="slate")) as ui:
    # Add a Markdown component for the main title of the application.
    gr.Markdown("# Minh's Crypto Research Agent")
    
    # Create a Textbox component for users to input their research query.
    # It has a label "What topic would you like to research?".
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    
    # Create a Button component to trigger the research process.
    # 'variant="primary"' gives it a distinct primary button style.
    run_button = gr.Button("Run", variant="primary")
    
    # Create a Markdown component to display the research report.
    # It has a label "Report".
    report = gr.Markdown(label="Report")
    
    # This line seems to be a personal note or a placeholder for tracking origin.
    print("forked from ed@edonner.com")
    
    # Configure the 'Run' button's click event.
    # When clicked, it calls the 'run' function with the input from 'query_textbox'
    # and displays the output in the 'report' Markdown component.
    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    
    # Configure the 'submit' event for the query_textbox.
    # This allows users to press Enter (or similar) in the textbox to trigger the research,
    # providing an alternative to clicking the button. It calls the same 'run' function.
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

# Launch the Gradio user interface.
# 'inbrowser=True' attempts to open the application in the default web browser automatically.
ui.launch(inbrowser=True)
