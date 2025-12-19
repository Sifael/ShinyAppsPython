
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from shiny import App, Inputs, Outputs, Session, render, ui
from pathlib import Path
from data_class import DataSet

# setting up a style
plt.style.use('seaborn-v0_8-darkgrid')

# setting up data objectes
data_obj = DataSet( data_path="programming_languages.csv", 
                    date_column='date')

data_obj.process_data()
languages = data_obj.get_numeric_column_names()


app_ui = ui.page_fluid(
    ui.br(),
    ui.panel_title(title= ui.h4("Programming Languages Popularity by Month (2004-2024)")),
    ui.br(),
    ui.layout_sidebar(
        ui.sidebar(
                ui.input_selectize( id = "languages_select", 
                                    label = "Select Languages",  
                                    choices = languages, 
                                    selected = languages[0],
                                    multiple = True ),
                ui.download_button( id = "download_plot", 
                                    label = "Download Plot")
    ),
    ui.output_plot("plot")
)
)


def server(input: Inputs, output: Outputs, session: Session):
    
    
    def make_plot():
        fig, ax = plt.subplots()
        for language in input.languages_select():
            plt.plot(data_obj.data.Date, data_obj.data[language], label = language)
        

        ax.set_title("Programming Languages Popularity by Month (2004–2024)")
        ax.set_ylabel("Percentage Use Worldwide (%)")
        ax.set_xlabel("Year")
        
        # ticker setup
        ax.xaxis.set_major_locator(mdates.YearLocator(2)) 
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

        ax.xaxis.set_minor_locator(mdates.YearLocator(1))   # minor ticks every year
        ax.tick_params(axis='x', rotation=20)

        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        fig.tight_layout()
        
        return fig

    @render.plot(alt="Programming Languages Popularity Plot")
    def plot(): 
        return make_plot()

    @render.download(filename="programming_languages_popularity.png")
    def download_plot():
        fig = make_plot()
        path = Path("programming_languages_popularity.png")
        fig.savefig(path, dpi = 300, bbox_inches="tight")
        plt.close(fig)
        return path


app = App(app_ui, server)