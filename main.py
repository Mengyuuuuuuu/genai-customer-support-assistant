from src.workflow import run_workflow


def main():
    print("GenAI Customer Support Assistant")
    print("---------------------------------")

    user_input = input("Ihre Anfrage: ")

    category, response = run_workflow(user_input)

    print("\nKategorie:", category)
    print("Antwort:")
    print(response)


if __name__ == "__main__":
    main()
