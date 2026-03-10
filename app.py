# -----------------------------------------------------------
# RUN DASH APPLICATION
# -----------------------------------------------------------

# Render and other cloud platforms require this configuration
server = app.server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)
