import argparse
import app

if __name__ == "__main__":
    scrapping_app = app.create_app()
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=5000, help="Porta da API de serviço")
    args = parser.parse_args()
    scrapping_app.run(host="0.0.0.0", port=args.port)
