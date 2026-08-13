import typer
from rich import print
from epifair.config import load_yaml
app=typer.Typer(no_args_is_help=True)
@app.command()
def show_config(path: str="configs/experiment.yaml"):
    print(load_yaml(path))
if __name__=="__main__": app()
