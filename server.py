import connexion

app = connexion.App(__name__, specification_dir='./')
app.add_api('swagger.yml')
app.run(port=8080)
