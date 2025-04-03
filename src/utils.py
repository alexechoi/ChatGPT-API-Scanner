"""
This module provides a function to check the validity of an OpenAI API key by making a test request
to a chosen model using the OpenAI client. It captures various exceptions and prints error details.
"""

from anthropic import Anthropic
from openai import APIStatusError, AuthenticationError, OpenAI, RateLimitError
import rich


def check_key(key, model="gpt-4o-mini", provider_type="openai") -> str | None:
    """
    Check if the API key is valid for the specified provider type (OpenAI or Anthropic).
    """
    try:
        rich.print(f"🔍 Validating key for provider: [bold blue]{provider_type}[/bold blue]")

        if provider_type == "openai":
            # OpenAI API key validation
            client = OpenAI(api_key=key)

            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a yeser, you only output lowercase yes.",
                    },
                    {"role": "user", "content": "yes or no? say yes"},
                ],
            )
            result = completion.choices[0].message.content
            rich.print(f"🔑 [bold green]available key[/bold green]: [orange_red1]'{key}'[/orange_red1] ({result})\n")
            return "yes"

        elif provider_type == "anthropic":
            # Anthropic API key validation
            client = Anthropic(api_key=key)

            message = client.messages.create(
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": "You are a yeser, you only output lowercase yes",
                    }
                ],
                model="claude-3-5-sonnet-latest",
            )
            result = message.content
            rich.print(f"🔑 [bold green]available key[/bold green]: [orange_red1]'{key}'[/orange_red1] ({result})\n")
            return "yes"

        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")

    except AuthenticationError as e:
        rich.print(f"[deep_sky_blue1]{e.body['code']} ({e.status_code})[/deep_sky_blue1]: '{key[:10]}...{key[-10:]}'")  # type: ignore
        return e.body["code"]  # type: ignore
    except RateLimitError as e:
        rich.print(f"[deep_sky_blue1]{e.body['code']} ({e.status_code})[/deep_sky_blue1]: '{key[:10]}...{key[-10:]}'")  # type: ignore
        return e.body["code"]  # type: ignore
    except APIStatusError as e:
        rich.print(f"[bold red]{e.body['code']} ({e.status_code})[/bold red]: '{key[:10]}...{key[-10:]}'")  # type: ignore
        return e.body["code"]  # type: ignore
    except Exception as e:  # pylint: disable=broad-except
        rich.print(f"[bold red]{e}[/bold red]: '{key[:10]}...{key[-10:]}'")  # type: ignore
        return "Unknown Error"


if __name__ == "__main__":
    check_key("sk-proj-12345")
