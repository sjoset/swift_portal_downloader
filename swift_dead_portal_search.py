import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    from dataclasses import asdict

    import pandas as pd
    import matplotlib.pyplot as plt

    from src.swift_portal_downloader.portal.search.search_by_name import soup_to_comet_db_entries, search_portal_by_target_name

    return asdict, mo, pd, plt, search_portal_by_target_name


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Swift dead portal search:
    """)
    return


@app.cell
def _(mo):
    search_term_widget = mo.ui.text(label="Search term:", value="", placeholder="C/, P/, Comet", kind="text", debounce=True)
    search_term_widget
    return (search_term_widget,)


@app.cell
def _(search_portal_by_target_name, search_term_widget):
    if search_term_widget.value != "":
        search_result_list = search_portal_by_target_name(search_term_widget.value)
    else:
        search_result_list = []
    return (search_result_list,)


@app.cell
def _(asdict, pd, search_result_list):
    search_result_df = pd.DataFrame([asdict(x) for x in search_result_list])
    search_result_df['print_canonical_name'] = search_result_df.canonical_name.str.replace('_', '/')
    return (search_result_df,)


@app.cell
def _(pd, plt, search_result_df):
    def plot_number_of_observations(df: pd.DataFrame):

        fwidth = len(set(df.canonical_name))/2
        f, ax = plt.subplots(1, 1, figsize=(fwidth, 6))

        ax.bar(x=df.print_canonical_name, height=df.number_of_observations)
        ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=90)

        return f

    plot_number_of_observations(df=search_result_df)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
