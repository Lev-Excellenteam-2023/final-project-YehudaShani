
import openai
import asyncio
import json
import aiohttp
import os
from . import file_writer
from .parser import Parser, get_text_from_slide

# read the API key from the file
root_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(root_dir, "Gpt_API_Key.txt")

with open(file_path, "r") as file:
    openai.api_key = file.read()


def generate_summary(parser: Parser):
    """
    Generate a summary of the presentation.
    :param parser: The parser object that holds the slides.
    :return: a generator that yields the slide number and the summary of the slide.
    """

    messages_to_send = [{"role": "assistant", "content": "Hello, I am your assistant, i will explain these topics."}]
    for number, slide in enumerate(parser):
        text = get_text_from_slide(slide)
        if len(text) == 0:
            continue
        content = " ".join(get_text_from_slide(slide))
        messages_to_send.append({"role": "user", "content": "Summarize and explain these topics: " + content})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_to_send
        )

        chat_response = completion.choices[0].message.content
        messages_to_send.append({"role": "assistant", "content": chat_response})

        yield number, chat_response


async def get_gpt_answer(parser, file_name):
    """
    Get the GPT answer and write it to a file.
    :param parser: The parser object.
    :param file_name: The name of the file to write to.
    :return: None
    """
    generator = generate_summary(parser)
    writer = file_writer.FileWriter(file_name)
    while True:
        try:
            slide_number, text = next(generator)
            print(text)
            print("Writing slide number", slide_number)
            writer.write_to_file(slide_number, text)
            await asyncio.sleep(20)
        except StopIteration:
            writer.close_file()
            break
        except Exception as e:
            print(e)
            break


async def make_api_request(user_message: str):
    """
    Sends a request to the GPT-3.5-turbo model for generating text based on a user message.

    :param user_message: The message from the user to be used as a prompt for text generation.
    :return: A dictionary containing the response from the GPT-3.5-turbo model.
    """
    # Set engine and parameters
    engine = "gpt-3.5-turbo"
    max_tokens = 512

    # Generate text from prompt asynchronously
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            "https://api.openai.com/v1/chat/completions",  # Updated endpoint URL
            headers={
                "Authorization": f"Bearer {openai.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "messages": [{"role": "system", "content": "You explain bullet points of a presentation."},
                             {"role": "user", "content": user_message}],
                "max_tokens": max_tokens,
                "model": engine  # Add the model parameter
            }
        )
        return await response.json()



async def get_gpt_answer2(parser, file_name):
    """
    Get the GPT answer and write it to a file.
    :param parser: The parser object.
    :param file_name: The name of the file to write to.
    :return: None
    """
    writer = file_writer.FileWriter(file_name)
    prompts = []
    for slide_number, slide in enumerate(parser):
        text = get_text_from_slide(slide)
        if len(text) == 0:
            continue
        content = " ".join(get_text_from_slide(slide))
        prompt = "Summarize and explain these topics: " + content
        prompts.append((slide_number, prompt))

    tasks = [make_api_request(prompt) for slide_number, prompt in prompts]
    responses = await asyncio.gather(*tasks)
    for (slide_number, prompt), response in zip(prompts, responses):
        print(response)
        print("Writing slide number", slide_number)
        if len(response["choices"]) == 0:
            writer.write_to_file(slide_number, "No response")
        writer.write_to_file(slide_number, response["choices"][0]["message"]["content"])
    writer.close_file()
