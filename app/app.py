# Add requirements at the top 
import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 
from shinywidgets import render_altair



df = palmerpenguins.load_penguins()

# Add the title to the App
ui.page_opts(title="St. Cyr Penguins Dashboard", fillable=True)

# Add the sidebar filters, in this case add the checkbox group, which allows the user to select, or deselect each species of penguin.
with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    
    # Insert a horizontal line 
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/14dstcyr/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://14dstcyr.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/14dstcyr/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/14dstcyr/pyshiny-penguins-dashboard-express",
        target="_blank",
    )


with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("linux"), theme="bg-gradient-purple-blue"):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("feather"), font="bold", theme="bg-gradient-purple-pink",
                     ):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("feather"), font="bold", theme="bg-gradient-purple-pink"):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Use Altair to replace the scatterplot with an interactive Plotly chart
ui.input_selectize(
    "var", "Select variable",
    choices=["bill_length_mm", "body_mass_g"]
)

@render_altair
def hist():
    import altair as alt
    from palmerpenguins import load_penguins
    df = load_penguins()
    return alt.Chart(df).mark_bar().encode(
        x=alt.X(f"{input.var()}:Q", bin=True),
        y="count()"
    )


with ui.layout_columns():
   
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data", style="color: purple")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
