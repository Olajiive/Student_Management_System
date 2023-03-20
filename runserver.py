from Api import create_app
from Api.config.config import config_dict

app=create_app(config=config_dict["prodconfig"])

if __name__ == "__main__":
    app.run()