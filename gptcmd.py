#!/usr/bin/env python3

import os
from openai import OpenAI
from rich.panel import Panel
from rich.console import Console
from rich.markdown import Markdown


def main():
    client = OpenAI()
    console = Console()

    os.system('clear')
    
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        if user_input.lower() == "clear":
            os.system('clear')
            continue

        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                store=True,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant. "
                            "Format all responses using Markdown. "
                            "Ensure the content is visually optimized for a black window background (`#000000`). "
                            "Use colors that provide high contrast and are easy to read on a black background. "
                
                            "### Formatting Guidelines:\n"
                            "- **Headings (`# H1`, `## H2`)** → Use **bold cyan** (`#00FFFF`) for visibility.\n"
                            "- **Bold text (`**text**`)** → Use **light yellow** (`#FFD700`) for emphasis.\n"
                            "- **Italic text (`*text*`)** → Use **light magenta** (`#FF69B4`).\n"
                            "- **Code Blocks (` ```python `, ` ```bash ` )** → Use a **grey background** (`#9c9c9c`) and white text.\n"
                            "- **Bullet Points & Lists** → Use a **light green** (`#00FF00`) for readability.\n"
                            "- **Links (`[text](url)`)** → Display as **light blue** (`#87CEEB`).\n"
                            "- **Error or Warnings** → Highlight in **red** (`#FF5555`) for alerts.\n"
                            "- **Quotes (`> text`)** → Use **italic cyan** (`#5FD3F3`) for distinction.\n"
                            "- **Keep responses concise and well-structured.**\n"
                
                            "### Example Formatting:\n"
                            "```markdown\n"
                            "## **Example Response**\n\n"
                            "**Important Notes:**\n"
                            "- This text is **bold** in yellow.\n"
                            "- This is *italicized* in light magenta.\n"
                            "- Code example:\n"
                            "```python\n"
                            "print(\"Hello, World!\")  # Light grey background\n"
                            "```\n"
                            "- > This is a blockquote in italic cyan.\n"
                            "- ✅ **Use light green checkmarks for success messages.**\n"
                            "- ⚠️ **Use red for errors and warnings.**\n"
                            "```\n"
                
                            "Ensure all responses are **optimized for readability** against a **dark background (`#000000`)** while maintaining Markdown formatting."
                        ),
                    },
                    {"role": "user", "content": user_input}
                ]
            )

            response = completion.choices[0].message.content
            console.print(Panel(Markdown(response), style="on #000000"))
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

