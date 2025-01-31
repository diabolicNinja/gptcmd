#!/usr/bin/env python3

import os
import sys
import time
import readline
import openai
from rich.panel import Panel
from rich.console import Console
from rich.markdown import Markdown
from rich import box
from rich.pretty import pprint


HISTORY_FILE = os.path.expanduser("~/.chatgpt_history")
SYSTEM_PROMPT = """
    You are an expert AI assistant that generates **well-formatted programming code** in multiple languages, including **Golang, Python, and Bash**.
    You also expert in Operation Systems, including Linux, Unix, MacOS and Windows.
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

class LLMProvider:
    def get_response(self, user_prompt: str) -> str:
        raise NotImplementedError

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        try:
            self.api_key = api_key
            self.client = openai.Client()
        except openai.OpenAIError:
            print(f"No OPENAI_API_KEY found.\nPlease, set: OPENAI_API_KEY env variable first.")
            sys.exit(1)

    def __repr__(self):
        masked_key = self.api_key[:4] + "..." if self.api_key else "NO_KEY"
        return f"openai: api_key='{masked_key}'"

    def get_response(self, user_prompt: str) -> str:
        openai.api_key = self.api_key

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "system",  "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )
 
        return completion.choices[0].message.content
    
class PerplexityProvider(LLMProvider):
    def __init__(self, api_key: str):
        try:
            self.api_key = api_key
            self.client = openai.Client(api_key=self.api_key, base_url="https://api.perplexity.ai")
        except Exception as e:
            print(f"Error: {e}")
            exit(2)

    def __repr__(self):
        masked_key = self.api_key[:4] + "..." if self.api_key else "NO_KEY"
        return f"perplexity: api_key='{masked_key}'"

    def get_response(self, user_prompt: str) -> str:
        openai.api_key = self.api_key
        try:
            completion = self.client.chat.completions.create(
                model="sonar-pro",
                messages=[
                    {"role": "system",  "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ]
            )
        except openai.AuthenticationError:
            print(f"No PERPLEXITY_API_KEY found.\nPlease, set: PERPLEXITY_API_KEY env variable first.")
            exit(3)
 
        return completion.choices[0].message.content


def main():
    os.system('clear')
    console = Console()
    
    try:
        readline.read_history_file(HISTORY_FILE)
    except FileNotFoundError:
        pass

    providers = {
        "openai": OpenAIProvider(os.getenv("OPENAI_API_KEY")),
        "perplexity": PerplexityProvider(os.getenv("PERPLEXITY_API_KEY"))
    }

    console.print("Available providers:")
    for name, provider_obj in providers.items():
        console.print(f"- {name}")
    provider_choice = input("Choose provider: ").strip()
    provider_instance = providers.get(provider_choice, providers["openai"])
    
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
                start_time = time.time()
                response = provider_instance.get_response(user_input)
                end_time = time.time()
                elapsed_time = end_time - start_time
                seconds = int(elapsed_time)
                milliseconds = int((elapsed_time - seconds) * 1000)
                elapsedtime = f"{seconds}.{milliseconds:03d} seconds"
                console.print(Panel(Markdown(response), subtitle=elapsedtime, box=box.SIMPLE, style="on #000000"))
                
        except EOFError as e:
                console.print(f"[bold red]An error occurred: {e}.[/bold red]")
                break
        except KeyboardInterrupt:
                console.print("Exiting...")
                break
        

if __name__ == "__main__":
    main()
    readline.write_history_file(HISTORY_FILE)
    exit(0)
