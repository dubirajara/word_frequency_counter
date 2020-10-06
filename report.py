def generate_report(result):
    # Template HTML Table Listing Report.
    table_base = f"""<style>
        .i-am-centered {{ margin: auto; max-width: 800px;}}
        table .alto {{background-color:gray;}}
        </style>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
        <br>
        <div class="i-am-centered">
        <div class="row">
        <div class="col-lg-8 col-md-8 col-sm-8 col-xs-8">
        <h2>Shakespeare's Research</h2>
        <hr>
        <table class="table table-hover table-bordered">
        <caption>{len(result)} Relevant words in three Shakespeare's literary masterpieces.</caption>
        <thead><tr><th class="alto" scope="col">Words</th><th class="alto" 
        scope="col">Frecuency</th></tr></thead><tbody>"""

    # Create a HTML Table Listing Report.
    for w, f in result.items():
        table_item = f'<tr><th> {str(w)} </th><th> {str(f)} </td></tr>'
        table_base = table_base + table_item

    report = f'{table_base}</tbody></table></div></div></div></div>'

    with open("word_frequencies_report.html", "w") as file:
        file.write(report)
