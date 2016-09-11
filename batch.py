import extract
import arrange
import publish

if __name__ == "__main__":
    if extract.main():
        arrange.main()
    publish.main()
