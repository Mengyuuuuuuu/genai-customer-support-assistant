from src.workflow import run_workflow


def main():
    print("GenAI Customer Support Assistant")
    print("---------------------------------")

    while True:
        user_input = input("\nIhre Anfrage (oder 'exit'): ")

        if user_input.lower() == "exit":
            print("Beendet.")
            break

        category, response = run_workflow(user_input)

        print("\nKategorie:", category)
        print("Antwort:")
        print(response)


if __name__ == "__main__":
    main()
