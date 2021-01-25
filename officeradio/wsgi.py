from .websrv import app as application

def main():
    application.run(port=5001)

if __name__ == "__main__":
    main()
