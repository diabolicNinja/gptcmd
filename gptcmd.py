#!/usr/bin/env python3

import os
import sys
import time
import readline
from openai import OpenAI
from openai import OpenAIError
from rich.panel import Panel
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt


history_file = os.path.expanduser("~/.chatgpt_history")


def main():
    console = Console()
    try:
        client = OpenAI()
    except OpenAIError:
         console.print("no OpenAI key set!\nPlease: export OPENAI_API_KEY='my_key'")
         sys.exit(1)
    
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass

    os.system('clear')
    
    while True:
        try:
            sys.stdout.write("\033[999B")
            console.rule()
            user_input = input(" Ask me anything: ")

            if user_input.lower() == "":
                continue
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            if user_input.lower() == "quit":
                print("Goodbye!")
                break
            if user_input.lower() == "clear":
                os.system('clear')
                continue

            with console.status("[bold green]Processing...") as status:
                try:
                    start_time = time.time()
                    completion = client.chat.completions.create(
                        model="gpt-4o-mini",
                        store=True,
                        messages=[
                            {
                            "role": "system",
                            "content": """
                            You are an expert AI assistant that generates **well-formatted programming code** in multiple languages, including **Golang, Python, and Bash**.  
                            All responses must be **formatted using Markdown** for syntax highlighting and readability.

                            ### **🔹 Code Formatting Rules:**
                            - **Syntax Highlighting:** Every code block starts with triple backticks (```) followed by the language name (e.g., `python`, `go`, `bash`).
                            - **Ensure the code block ends with triple backticks (` ``` `).**
                            - **Clear Formatting:** Proper indentation and spacing for clean code structure.
                            - **Structured Comments:** Add concise, inline comments to explain key logic.
                            - **Execution Instructions:** If the user is likely to run the code, provide setup or execution steps.
                            - **Error Handling:** Include exception handling and validation when applicable.

                            ### **🔹 Markdown Styling Guidelines:**
                            - **Headings (`# H1`, `## H2`)** → Use for structuring responses.
                            - **Bold text (`**text**`)** → Highlight key points.
                            - **Italic text (`*text*`)** → Emphasize important concepts.
                            - **Bullet Points & Lists** → Organize information clearly.
                            - **Blockquotes (`> text`)** → Provide special notes or warnings.
                            - **Code Blocks (` ```python `, ` ```bash `, ` ```go ` )** → Format properly for readability.

                            ### **🔹 Example Response:**
                            ```markdown
                            ## Example Code
                            **Note:** This is a properly formatted code snippet.

                            ```go
                            package main

                            import "fmt"

                            func main() {
                                fmt.Println("Hello, World!") // Prints output
                            }
                            ```
                            ```
                
                            - Keep responses **concise and structured**.
                            - **Avoid unnecessary explanations**—focus on **direct, well-formatted answers**.
                            - Ensure Markdown **renders correctly in dark-mode themes**.
                            """
                            },
                            {"role": "user", "content": user_input}
                        ]
                    )

                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    seconds = int(elapsed_time)
                    milliseconds = int((elapsed_time - seconds) * 1000)
                    elapsedtime = f"{seconds}.{milliseconds:03d} seconds"

                    response = completion.choices[0].message.content
                    console.print(Panel(Markdown(response), subtitle=elapsedtime, style="on #000000"))
                except Exception as e:
                    console.print(f"[bold red]An error occurred: {e}.[/bold red]")
        except EOFError as e:
                console.print(f"[bold red]An error occurred: {e}.[/bold red]")
                break
        except KeyboardInterrupt:
                console.print("Exiting...")
                break
        
if __name__ == "__main__":
    main()
    readline.write_history_file(history_file)
    exit(0)
